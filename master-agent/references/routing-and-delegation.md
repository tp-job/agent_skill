# Routing and delegation

Which capability does the job, and who runs it.

---

## 1. Routing order

Take the first match.

| Priority | Route to | Because |
| --- | --- | --- |
| 1 | A skill whose trigger matches the job | it carries tested instructions for exactly this |
| 2 | A dedicated tool (built-in or MCP) for the operation | schemas, permissions and safety checks come with it |
| 3 | A generic tool (shell, web fetch) | flexible, but you own the correctness |
| 4 | A subagent | only when isolation or parallelism is worth a cold start |
| 5 | Ask the human | when the job needs a capability that is absent or unauthorised |

**BAD:** using a shell `grep` loop over a ClickUp export when a ClickUp server with a bulk-filter operation is connected.
**BETTER:** list the server's operations, run the bulk one once.

**Bulk rule:** when a job touches many objects, look for a single bulk operation before calling a single-object tool in a loop.

---

## 2. Delegation — inline or subagent?

Default is **inline**. A subagent starts with none of your context and re-derives it.

| Spawn a subagent when | Stay inline when |
| --- | --- |
| The user asked for one | You already hold the context the task needs |
| Work is independent and can run in parallel (e.g. five unrelated searches) | Steps depend on each other's results |
| A broad read-only sweep where you need only the conclusion | You need the file contents themselves |
| Isolation matters — a risky change in a separate worktree | The change is small and reviewable in place |

A delegation brief must stand alone: the goal, the files, the constraints, what to return. The subagent never saw this conversation.

---

## 3. Model and effort

Reach for effort before reaching for a different model.

| Work | Effort | Model |
| --- | --- | --- |
| Routine loop iterations, mechanical edits | low | the session default, or a small fast model for subagent sweeps |
| Decomposition, design gates, anything failed twice | high / max | the most capable available |
| Broad read-only search | low–medium | a small fast model |
| Irreversible decisions | max | the most capable available, plus a human gate |

Check the current model identifiers in the client or the provider's docs rather than quoting from memory — they change.

---

## 4. Multi-agent patterns

| Pattern | Use when | Watch for |
| --- | --- | --- |
| **Orchestrator–workers** | one planner, many independent sub-tasks | workers duplicating reads; brief each one narrowly |
| **Pipeline** | stage N's output is stage N+1's input | a bad early stage poisons every later one — gate between stages |
| **Reviewer** | a second seat checks the first's work | the reviewer needs the target, not just the diff |
| **Parallel fan-out, single merge** | many searches, one answer | merge conflicts in shared files — give workers disjoint scopes |

**When not to go multi-agent:** under ~5 independent sub-tasks, or when every step needs the previous one's result. The coordination costs more than it saves.
