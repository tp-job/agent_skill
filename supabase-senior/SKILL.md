---
name: supabase-senior
description: >
  Senior-level Supabase architecture and engineering skill. Activate whenever the user mentions Supabase, Prisma ORM, database schema design, RLS (Row Level Security), Supabase migrations, connection pooling, Supabase Auth, Edge Functions, Realtime, Storage, or any combination of Supabase + Prisma workflows. Also trigger for database algorithm review, long workflow logic checks, architecture advice, migration planning (Postgres → Supabase), and query optimization. This skill acts as a Senior Lead across Prompt Engineering, Context Engineering, Agent Design, and AI Workflow Architecture in the Supabase + Prisma ecosystem. Use it proactively — if the user is building anything backend with PostgreSQL and TypeScript/Node.js, this skill likely applies.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.2.0"
  source: Supabase + Prisma 7 documentation (compiled 2026, checked against Prisma 7.10)
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

### Prisma 7 (current stable) — canonical dual-URL setup

**Check the version first:** `npx prisma --version`. Prisma 7 moved the URLs out of the schema; a v6 project needs the legacy block below.

```prisma
// prisma/schema.prisma — no url/directUrl here in v7 (deprecated)
datasource db {
  provider = "postgresql"
}

generator client {
  provider = "prisma-client"          // v7: replaces "prisma-client-js"
  output   = "../src/generated/prisma" // v7: required
}
```

```ts
// prisma.config.ts — the CLI (migrate, db pull, studio) uses the DIRECT connection
import 'dotenv/config'                 // v7: .env is no longer auto-loaded
import { defineConfig, env } from 'prisma/config'

export default defineConfig({
  schema: 'prisma/schema.prisma',
  migrations: { path: 'prisma/migrations' },
  datasource: { url: env('DIRECT_URL') },
})
```

```ts
// runtime — Prisma Client uses the POOLED connection through a driver adapter
import { PrismaPg } from '@prisma/adapter-pg'
import { PrismaClient } from '../src/generated/prisma/client'

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL })
export const prisma = new PrismaClient({ adapter })
```

```env
# .env
# Runtime: transaction pooler (serverless-safe)
DATABASE_URL="postgresql://postgres.[ref]:[pw]@aws-0-[region].pooler.supabase.com:6543/postgres?pgbouncer=true"

# CLI / migrations: session pooler or direct connection (bypasses transaction pooling)
DIRECT_URL="postgresql://postgres.[ref]:[pw]@aws-0-[region].pooler.supabase.com:5432/postgres"
```

**Mapping rule:** runtime → `DATABASE_URL` (6543, pooled) via adapter; CLI → `DIRECT_URL` (5432) via `prisma.config.ts`. Swap them and migrations hang on the transaction pooler.

<details><summary>Legacy — Prisma 6 and earlier</summary>

```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")       // Transaction pooler — runtime queries
  directUrl = env("DIRECT_URL")         // Direct — migrations only
}

generator client {
  provider = "prisma-client-js"
}
```

Do not advise this block on a v7 project; do not advise the v7 layout on a v6 project without the upgrade (`prisma.config.ts`, adapter, generator output).
</details>

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

### Recommended Strategy

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

Moving an existing Postgres database onto Supabase: checklist, the three paths, pg_dump/pg_restore, and the post-migration steps. Full procedure: [migration-playbook](references/migration-playbook.md).

Covers: Pre-Migration Checklist · Three Migration Paths · pg_dump / pg_restore (canonical) · Post-Migration (always required).

---

## 5. WORKFLOW & LOGIC CHECKER

Reviewing a multi-step Supabase + Prisma workflow for ordering, transaction, and auth-boundary bugs, with the output format. Full procedure: [workflow-review](references/workflow-review.md).

Covers: Workflow Review Protocol · Workflow Output Format.

---

## 6. ALGORITHM REVIEWER

Reviewing query-heavy code for N+1s, missing indexes, and pagination, plus the Prisma singleton rule. Full procedure: [algorithm-review](references/algorithm-review.md).

Covers: Algorithm Review Protocol · Prisma Singleton Pattern (always enforce).

---

## 7. AGENT DESIGN — SUPABASE-BACKED AI AGENTS

Auth boundaries for agents, the Edge Function agent pattern, and multi-step agent workflows with Prisma. Full procedure: [agent-design](references/agent-design.md).

Covers: Agent Auth Architecture · Edge Function Agent Pattern · Multi-Step Agent Workflow with Prisma.

---

## 8. SUPABASE REALTIME + PRISMA COEXISTENCE

Running Realtime subscriptions alongside Prisma writes without fighting over the schema. Full procedure: [realtime-prisma](references/realtime-prisma.md).


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
|Prisma + Supabase official guide|[Prisma Supabase Docs](https://www.prisma.io/docs/orm/overview/databases/supabase)|
|Upgrading a project to Prisma 7|[Upgrade to Prisma 7](https://www.prisma.io/docs/orm/more/upgrade-guides/upgrading-versions/upgrading-to-prisma-7)|
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
