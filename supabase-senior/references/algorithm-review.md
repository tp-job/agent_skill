# Algorithm Reviewer

Reviewing query-heavy code for N+1s, missing indexes, and pagination, plus the Prisma singleton rule.

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
