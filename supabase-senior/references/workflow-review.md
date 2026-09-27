# Workflow & Logic Checker

Reviewing a multi-step Supabase + Prisma workflow for ordering, transaction, and auth-boundary bugs, with the output format.

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
