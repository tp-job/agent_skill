# Delegation & Model Placement — where to spend effort

One principle governs this whole file:

> **Spend depth where a wrong answer is expensive to reverse. Spend throughput where it isn't.**

A wrong architecture costs the whole build. A wrong loop iteration costs one `git revert`. A **wrong verification costs everything downstream that trusted it** — which is why the cheapest-looking step in the loop is not the one to economize on.

Who occupies which seat is in [role-placement](./role-placement.md). This file is about how much to spend on each.

---

## The thinking pass

Seven points, run as one silent pass before committing to an answer:

1. **Think thoroughly** — every angle, not just the first plausible one
2. **Cover all bases** — operational reality after the happy path
3. **Consider all use cases** — everyone who touches this, not just the primary persona
4. **Think holistically** — does optimizing this piece break something at the system level?
5. **Edge cases** — empty states, zero values, concurrent writes, adversarial input
6. **First principles** — is this right because it's genuinely best, or just conventional?
7. **Pre-mortem** — if this fails in six months, what's the most believable reason?

Full treatment: [thinking-framework](../bundled/senior-leadership-advisor/references/thinking-framework.md).

### Where to spend it

Running all seven every loop iteration is waste — most iterations are a well-specified sub-task whose decisions were made upstream.

| Where | Which points | Why there |
| --- | --- | --- |
| Stage 1–2, in full | All seven | These decisions get multiplied by every later iteration |
| Decomposition | Edge cases, all use cases | Verification steps are born here; a missed edge case here is **never tested** |
| Verification of a security or data-loss feature | Edge cases, pre-mortem | A false pass here is the expensive kind |
| Stage 6 | Pre-mortem, holistic | Irreversibility |
| Routine loop iteration | None by default | Decisions already made; throughput is the point |
| A feature that failed twice | Full pass, especially first principles | Two failures means the problem isn't effort — re-examine the requirement |

**Pre-mortem is the highest-yield point for long horizons specifically.** "If this build is a mess in six months, what's the most believable reason?" almost always names a process gap the harness can close *now* — an untested integration boundary, a spec drifting from the code, a feature nobody can verify.

---

## Model placement

Assumption, stated so you can override it: **Claude Fable 5 is the base model for the loop.** It carries implementation and search across many iterations, where throughput matters more than depth on any one.

But the loop is not uniform, and splitting it by stakes matters more than the base choice:

| Work | Tier | Because |
| --- | --- | --- |
| Stage 1–2: requirements, architecture, decomposition | **Opus** | One-shot decisions whose cost compounds across every later iteration |
| Loop: implementation, search, status reports, bookkeeping | **Fable 5** | High iteration count, well-specified steps, decisions made upstream |
| **Loop: verification and the ledger write** | **Opus** | A false pass propagates silently and corrupts every decision built on it. This is the single error the whole workflow exists to prevent — do not economize here |
| Debugging something the loop has failed twice | **Opus** | Two failures means the problem isn't throughput |
| Stage 6: rollback and blast-radius reasoning | **Opus** | Irreversibility |

The asymmetry is the point: implementing a feature wrong is caught by verification; **verifying wrong is caught by nothing.** Cheap implementation with expensive verification is strictly better than the reverse, even though the reverse looks like the natural place to save.

---

## Delegating to sub-agents

Separate context is a stronger seat separation than a stated hat, because a fresh agent genuinely cannot inherit your blind spot.

| Situation | Delegate to | Why it helps |
| --- | --- | --- |
| Verifying a feature you just built | QA agent, given only `build-spec.md` + the feature's `steps` | Cannot rationalize an implementation it never saw |
| Locating code across an unfamiliar tree | explore/search agent | Keeps grep noise out of the main context |
| Reviewing a large diff before commit | review agent | Fresh eyes, and the diff doesn't cost you context |
| A self-contained, well-specified sub-task | worker agent | Parallelism without shared-state risk |

**Do not delegate:** requirements elicitation (the user is talking to you), design decisions (they need whole-build context), the commit itself, or anything where two agents would write the same files.

### The handoff contract applies harder to sub-agents

A sub-agent starts cold. Give it the goal, the acceptance criteria **verbatim**, the file paths, the definition of done, and what to report back. Never "continue what I was doing" — it cannot.

### Delegation safety

- Every delegated task gets an explicit **file allowlist**.
- Never run two delegated tasks whose allowlists intersect — a corrupted tree from concurrent writes is one neither agent can diagnose.
- **Commit before delegating anything that writes**, so the pre-delegation state is recoverable.

### Read the report as evidence, not verdict

A sub-agent reporting "all tests pass" without naming which tests has told you nothing. That is the same false pass the QA seat exists to catch, arriving from outside — and it is *more* dangerous than your own, because it wears the authority of an independent check.

Require the same shape you'd require of yourself: which steps ran, what was observed, what failed and what was done about it.
