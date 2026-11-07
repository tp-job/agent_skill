---
type: llm
---

PASS if the reply tells the user to measure before changing anything (for example a no-database endpoint timed against a database endpoint, or per-query timing), names round trips rather than payload size as the likely cost, and points at at least two of: region distance, transaction-pooler round trips, read queries batched in $transaction, the one-request-per-student N+1. It orders fixes by measured effect.
FAIL if it jumps straight to indexes, caching or query rewrites with no measurement step.
