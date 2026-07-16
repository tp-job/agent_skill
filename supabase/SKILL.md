---
name: supabase-senior
description: >
  Senior-level Supabase architecture and engineering skill. Activate whenever the user mentions Supabase, Prisma ORM, database schema design, RLS (Row Level Security), Supabase migrations, connection pooling, Supabase Auth, Edge Functions, Realtime, Storage, or any combination of Supabase + Prisma workflows. Also trigger for database algorithm review, long workflow logic checks, architecture advice, migration planning (Postgres → Supabase), and query optimization. This skill acts as a Senior Lead across Prompt Engineering, Context Engineering, Agent Design, and AI Workflow Architecture in the Supabase + Prisma ecosystem. Use it proactively — if the user is building anything backend with PostgreSQL and TypeScript/Node.js, this skill likely applies.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Supabase + Prisma documentation (compiled 2026)
---

# Supabase Senior — Architecture & Engineering Lead

You are acting as a **Senior Lead** across four disciplines simultaneously:

- **Prompt Engineering** — crafting precise instructions for AI-assisted DB workflows
- **Context Engineering** — managing schema context, RLS context, migration state
- **Agent Design** — designing Supabase-backed agentic systems with proper auth boundaries
- **AI Workflow Architecture** — long multi-step pipelines that touch Supabase + Prisma

Always think in layers: **Data → Auth → Access Control → API → Client**.  
Always think in duals: **Prisma owns the schema shape. Supabase owns the runtime security.**

---

## 1. CONNECTION REFERENCE CARD

This is the single most common source of broken Supabase + Prisma setups. Internalize this.

### Three Supabase connection strings (know them all)

|Type|Port|Use for|Format|
|---|---|---|---|
|**Direct**|5432|Prisma migrations, CLI, `prisma db push`|`postgresql://postgres:pw@db.[ref].supabase.co:5432/postgres`|
|**Transaction Pooler**|6543|Runtime queries (serverless, Vercel, edge)|`postgresql://postgres.[ref]:pw@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true`|
|**Session Pooler**|5432|Runtime queries (long-lived servers)|`postgresql://postgres.[ref]:pw@aws-0-[region].pooler.supabase.com:5432/postgres`|

### `schema.prisma` — canonical dual-URL setup

```prisma
// schema.prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")       // Transaction pooler — runtime queries
  directUrl = env("DIRECT_URL")         // Direct — migrations only
}

generator client {
  provider = "prisma-client-js"
}
```

```env
# .env
# Runtime: transaction pooler (serverless-safe)
DATABASE_URL="postgresql://postgres.[ref]:[pw]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true"

# Migrations: direct connection (bypasses pooler)
DIRECT_URL="postgresql://postgres.[ref]:[pw]@aws-0-[region].pooler.supabase.com:5432/postgres"
```

> ⚠️ **Prisma v7+ note**: In Prisma 7.2+, `url`/`directUrl` may move to `prisma.config.ts`. Always check the installed Prisma version before advising the migration pattern.

```ts
// prisma.config.ts (Prisma v7+)
import 'dotenv/config'
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: { path: 'prisma/migrations' },
  datasource: { url: env('DIRECT_URL') }, // CLI uses direct
})
```

---

## 2. RLS (ROW LEVEL SECURITY) — ARCHITECTURE RULES

RLS is Supabase's primary security primitive. Prisma is unaware of RLS at the schema level —  
this creates a **dual ownership split**: Prisma controls shape, Supabase controls access.

### The Three-Role Mental Model

```
anon        → unauthenticated browser users    → governed by RLS
authenticated → logged-in users               → governed by RLS  
service_role  → backend / admin / Edge Funcs  → BYPASSES all RLS
```

### Enable RLS on every public table (non-negotiable)

```sql
-- Always enable on table creation
ALTER TABLE "your_table" ENABLE ROW LEVEL SECURITY;

-- Baseline: deny all until explicit allow
-- (tables with RLS + zero policies = no access to anyone)
```

### Standard Policy Patterns

```sql
-- Pattern 1: User owns their rows
CREATE POLICY "user_select_own"
  ON profiles FOR SELECT
  USING (auth.uid() = user_id);

-- Pattern 2: Authenticated users can read all
CREATE POLICY "authed_read_all"
  ON public_posts FOR SELECT
  TO authenticated
  USING (true);

-- Pattern 3: Insert with user-id enforcement
CREATE POLICY "user_insert_own"
  ON notes FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- Pattern 4: Soft-delete visibility
CREATE POLICY "hide_deleted"
  ON items FOR SELECT
  USING (deleted_at IS NULL AND auth.uid() = owner_id);
```

### Prisma + RLS: The Injection Pattern

Prisma Client connects as `postgres` (superuser) by default → bypasses RLS.  
To enforce RLS through Prisma, set the role per-transaction:

```ts
// Enforce RLS in Prisma by impersonating the authenticated role
async function withRLS(userId: string, fn: (tx: PrismaClient) => Promise<void>) {
  await prisma.$transaction(async (tx) => {
    // Set the Supabase auth context so RLS policies fire
    await tx.$executeRaw`SELECT set_config('request.jwt.claims', ${JSON.stringify({ sub: userId })}, true)`
    await tx.$executeRaw`SET LOCAL ROLE authenticated`
    await fn(tx)
  })
}
```

> **Rule of thumb**: If you're doing admin/backend operations (cron jobs, migrations,  
> server-side data seeding), use `service_role`. If you're proxying user actions,  
> use the anon/authenticated role with RLS ON.

### Anti-Patterns to catch and fix

|Anti-Pattern|Risk|Fix|
|---|---|---|
|`NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY`|Full DB exposed to browser|Move to server-only env var|
|SSR client initialized with `service_role`|Session cookie overrides admin key|Use a separate `adminClient` instance|
|Table created in dashboard, RLS never enabled|All data readable by any `anon`|`ALTER TABLE x ENABLE ROW LEVEL SECURITY`|
|UUID type mismatch in RLS policy|Silent bypass via type coercion|Cast explicitly: `(auth.uid()::text = user_id::text)`|
|Prisma `queryRaw` bypassing RLS unintentionally|Data leak in complex queries|Audit all `$queryRaw`/`$executeRaw` for role context|

---

## 3. SCHEMA DESIGN — PRISMA ↔ SUPABASE RULES

### The Dual-Source-of-Truth Problem

Supabase has its own migration system (`supabase/migrations/`).  
Prisma has its own migration system (`prisma/migrations/`).  
**Never run both on the same project without a clear boundary.**

### Recommended Strategy (2025)

**Option A — Prisma owns schema, Supabase owns runtime features**

- Prisma handles: table structure, indexes, relations, enums
- Supabase handles: RLS policies, auth triggers, storage, functions
- Add RLS as raw SQL appended to Prisma migration files

**Option B — Supabase CLI owns everything (for teams using Supabase heavily)**

- Use `supabase db diff` + `supabase migration new`
- Use Prisma only as a query client (`prisma db pull` to sync types)
- Never run `prisma migrate` — only `prisma generate`

> **Advise Option A for TypeScript-first teams. Option B for infra/DevOps-heavy teams.**

### Auth users → public schema bridge

Prisma cannot introspect `auth.users` (Supabase internal schema). Mirror it:

```prisma
// schema.prisma
model Profile {
  id        String   @id @db.Uuid          // mirrors auth.users.id
  email     String   @unique
  name      String?
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  @@map("profiles")
}
```

```sql
-- Migration SQL appended after Prisma generates it
-- Trigger to auto-create profile on signup
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO public.profiles (id, email)
  VALUES (NEW.id, NEW.email);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();
```

---

## 4. MIGRATION PLAYBOOK — POSTGRES → SUPABASE

### Pre-Migration Checklist

```sql
-- Run on SOURCE database before anything
SELECT pg_size_pretty(pg_database_size(current_database())) AS db_size;
SELECT version();
SELECT extname FROM pg_extension ORDER BY extname;
SELECT count(*) FROM pg_stat_activity;
-- Compare extensions against Supabase's available list
SELECT name FROM pg_available_extensions ORDER BY name; -- (run on Supabase target)
```

### Three Migration Paths

|Method|Downtime|Complexity|Best For|
|---|---|---|---|
|**Google Colab notebook**|~hours|Low|< 10 GB, guided|
|**pg_dump / pg_restore**|Maintenance window|Medium|Any size|
|**Logical Replication**|Near-zero|High|Postgres 10+, large prod DBs|

### pg_dump / pg_restore (canonical)

```bash
# Step 1: Dump (always use --no-owner --no-privileges for Supabase)
pg_dump \
  --host=<source_host> --port=5432 \
  --username=<user> --dbname=<db> \
  --jobs=4 --format=directory \
  --no-owner --no-privileges --no-subscriptions \
  --verbose --file=./db_dump 2>&1 | tee dump.log

# Step 2: Restore to Supabase (use session pooler port 5432)
export SUPABASE_URL="postgresql://postgres.[ref]:[pw]@aws-0-[region].pooler.supabase.com:5432/postgres"
pg_restore \
  --host=... --port=5432 \
  --username=postgres --dbname=postgres \
  --jobs=4 --format=directory \
  --no-owner --no-privileges \
  --verbose ./db_dump 2>&1 | tee restore.log
```

### Post-Migration (always required)

```sql
-- 1. Re-enable RLS on all tables (not migrated by pg_dump)
SELECT 'ALTER TABLE "' || tablename || '" ENABLE ROW LEVEL SECURITY;'
FROM pg_tables WHERE schemaname = 'public';

-- 2. Recreate roles / grants (not migrated)
-- 3. Re-create auth triggers
-- 4. Verify extensions installed on Supabase target
-- 5. Test RLS policies with anon key (not service_role)
```

---

## 5. WORKFLOW & LOGIC CHECKER

When asked to **check**, **review**, or **validate** a workflow, use this structured analysis:

### Workflow Review Protocol

```
STEP 1 — MAP THE FLOW
  Draw out each step: trigger → action → state change → output
  Identify: What data moves? Which role executes each step?

STEP 2 — AUTH BOUNDARY CHECK
  At each step: Is this anon / authenticated / service_role?
  Does the role match the RLS policy on the affected table?

STEP 3 — CONNECTION CHECK
  Is this a migration step? → Must use DIRECT_URL
  Is this a runtime query? → Should use pooled DATABASE_URL
  Is this an Edge Function? → Deno runtime, use supabase-js not Prisma directly

STEP 4 — TRANSACTION SAFETY
  Are there multi-step writes? → Wrap in Prisma $transaction or Postgres transaction
  Can a partial failure corrupt state? → Add compensating rollback

STEP 5 — IDEMPOTENCY CHECK
  Can this workflow run twice safely?
  If not: add idempotency key, deduplication logic, or upsert instead of insert

STEP 6 — SCALE AUDIT
  Does this query have N+1 patterns? (multiple queries inside a loop)
  Are indexes present for all WHERE / JOIN / ORDER BY columns?
  Does this workflow hold a connection open longer than needed?
```

### Workflow Output Format

When reviewing a workflow, always output:

```
## Workflow: [name]
### Flow Map
  [step-by-step with roles annotated]

### ✅ Correct
  [what is right about it]

### ⚠️ Warnings
  [non-critical issues]

### 🔴 Critical Issues
  [security, data integrity, or correctness problems]

### 🔧 Recommended Fix
  [code or SQL with explanation]
```

---

## 6. ALGORITHM REVIEWER

When asked to **review**, **check**, or **summarize** an algorithm or query:

### Algorithm Review Protocol

```
STEP 1 — COMPLEXITY ANALYSIS
  Time: O(?) for the core loop / query
  Space: O(?) for in-memory structures
  DB: How many round-trips? Can they be batched?

STEP 2 — CORRECTNESS CHECK
  Edge cases: empty input, null values, concurrent writes
  Boundary conditions: first/last item, zero rows, max rows

STEP 3 — SUPABASE-SPECIFIC CHECKS
  Does this rely on auth.uid() inside a non-auth context?
  Does this aggregate across RLS-filtered rows correctly?
  Does this use Realtime subscriptions in a way that leaks data?

STEP 4 — PRISMA-SPECIFIC CHECKS
  Are relations loaded with select/include (avoid over-fetching)?
  Are findMany queries paginated (cursor or offset)?
  Are raw queries ($queryRaw) sanitized against SQL injection?
  Does Prisma Client get instantiated once (singleton) or per-request (memory leak)?

STEP 5 — SUMMARIZE
  One-paragraph plain English summary of what the algorithm does
  One-line complexity verdict
  Top 3 improvement recommendations ranked by impact
```

### Prisma Singleton Pattern (always enforce)

```ts
// lib/prisma.ts — singleton for Next.js / serverless
import { PrismaClient } from '@prisma/client'

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient }

export const prisma =
  globalForPrisma.prisma ??
  new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
  })

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma
```

---

## 7. AGENT DESIGN — SUPABASE-BACKED AI AGENTS

### Agent Auth Architecture

```
Agent Layer
    │
    ├── User-context agents  → use anon key + JWT forwarding → RLS enforced
    │                           (chatbots, copilots acting on behalf of a user)
    │
    └── System agents        → use service_role            → RLS bypassed
                                (data processing, cron, background jobs)
```

### Edge Function Agent Pattern

```ts
// supabase/functions/agent-handler/index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

Deno.serve(async (req) => {
  // 1. Verify user JWT (anon client respects RLS)
  const userClient = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  )
  const { data: { user }, error } = await userClient.auth.getUser()
  if (error || !user) return new Response('Unauthorized', { status: 401 })

  // 2. Use service_role for privileged operations AFTER auth check
  const adminClient = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  )

  // 3. Scope all admin operations explicitly to user
  const { data } = await adminClient
    .from('agent_logs')
    .insert({ user_id: user.id, action: 'run', timestamp: new Date() })

  return new Response(JSON.stringify({ ok: true }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### Multi-Step Agent Workflow with Prisma

```ts
// Long workflow with transaction safety
async function runAgentWorkflow(userId: string, payload: AgentPayload) {
  return await prisma.$transaction(async (tx) => {
    // Step 1: Reserve the job (atomic)
    const job = await tx.agentJob.update({
      where: { id: payload.jobId, status: 'pending' },
      data: { status: 'running', startedAt: new Date() },
    })

    try {
      // Step 2: Execute agent steps
      const result = await executeSteps(job.steps)

      // Step 3: Commit result
      await tx.agentJob.update({
        where: { id: job.id },
        data: { status: 'completed', result, completedAt: new Date() },
      })

      return result
    } catch (err) {
      // Step 4: Rollback on failure — transaction auto-rolls back
      // but log the error for observability
      await tx.agentJob.update({
        where: { id: job.id },
        data: { status: 'failed', error: String(err) },
      })
      throw err
    }
  })
}
```

---

## 8. SUPABASE REALTIME + PRISMA COEXISTENCE

Realtime subscriptions use the anon key + RLS. Prisma mutations trigger those events.  
This is safe — Prisma writes hit Postgres, Supabase Realtime listens to the WAL.

```ts
// Client: subscribe with user-scoped filter
const channel = supabase
  .channel('user-updates')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'notifications',
      filter: `user_id=eq.${userId}`,  // Always filter by user — never subscribe to whole table
    },
    (payload) => handleUpdate(payload)
  )
  .subscribe()
```

> **RLS on Realtime**: As of 2024+, Supabase enforces RLS on Realtime subscriptions.  
> Ensure the `authenticated` role has SELECT policy on any table being subscribed to.

---

## 9. ADVISOR MODE — SENIOR RECOMMENDATIONS

When the user asks for advice, architecture review, or "what's the best way to...", apply:

### Decision Matrix

|Question|Answer|
|---|---|
|"Should I use Prisma or Supabase client for queries?"|Prisma for type-safe complex queries; supabase-js for real-time, auth, storage|
|"Who owns migrations?"|Prisma for schema shape; append RLS SQL manually or via Supabase CLI for policies|
|"How do I handle multi-tenancy?"|RLS with `org_id` column + `auth.jwt() ->> 'org_id'` claim in policies|
|"Prisma in Edge Functions?"|Avoid — use Prisma Accelerate or switch to supabase-js / Kysely for edge|
|"How do I avoid N+1 in Prisma?"|Use `include` with pagination, or raw SQL for complex aggregations|
|"When to use `$executeRaw`?"|Only for DDL or Supabase-specific SQL; never for user input without parameterization|
|"Connection pool exhaustion?"|Switch to Transaction Pooler (port 6543); reduce `connection_limit`; use PgBouncer params|

### Red Flags — Always Call Out

```
🔴 service_role key in any client-side code or NEXT_PUBLIC_ variable
🔴 Tables without RLS in production
🔴 `prisma migrate` run against pooled connection (port 6543)
🔴 PrismaClient instantiated inside a request handler (new client per request)
🔴 $queryRaw with string interpolation (SQL injection risk)
🔴 Realtime subscription on a full table without row filter
🔴 auth.users joined directly in Prisma schema (use profiles mirror instead)
🔴 Missing @@index on foreign keys and frequently filtered columns
```

---

## 10. REFERENCES

For deeper dives, load the relevant reference file:

|Topic|Reference|
|---|---|
|Postgres → Supabase migration (full steps)|[Supabase Migrate Docs](https://supabase.com/docs/guides/platform/migrating-to-supabase/postgres)|
|Prisma + Supabase official guide|[Prisma Supabase Docs](https://www.prisma.io/docs/orm/v6/overview/databases/supabase)|
|Prisma Postgres (managed)|[Prisma Postgres Overview](https://www.prisma.io/docs/postgres)|
|Prisma + Supabase connection pooling via Accelerate|[Prisma Accelerate + Supabase](https://www.prisma.io/docs/guides/supabase-accelerate)|
|Supabase RLS docs|[RLS Guide](https://supabase.com/docs/guides/database/postgres/row-level-security)|
|Supabase Edge Functions|[Edge Functions Docs](https://supabase.com/docs/guides/functions)|

---

## QUICK COMMAND REFERENCE

```bash
# Prisma workflow with Supabase
npx prisma generate                  # Regenerate client after schema change
npx prisma migrate dev               # Dev migration (uses DIRECT_URL)
npx prisma migrate deploy            # Prod migration (uses DIRECT_URL)
npx prisma db pull                   # Introspect existing Supabase DB → update schema.prisma
npx prisma db push                   # Push schema without migration history (prototyping only)
npx prisma studio                    # Browse data locally

# Supabase CLI workflow
supabase init                        # Initialize supabase project
supabase start                       # Start local Supabase stack (Docker)
supabase db diff                     # Diff local schema vs remote
supabase migration new <name>        # Create new migration file
supabase db push                     # Push migrations to remote
supabase gen types typescript        # Generate TypeScript types from DB schema

# Combined: Prisma schema → Supabase types
npx prisma migrate dev               # Apply schema via Prisma
supabase gen types typescript \
  --project-id <ref> > types/supabase.ts  # Generate Supabase client types
```