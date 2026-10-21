---
name: test-strategy
description: >-
  Plans, designs and runs software testing end to end as one gated loop: plan with written exit
  criteria, design cases (equivalence partitioning, boundary values, decision tables, state
  transitions), then test level by level — unit (white box), integration (grey box), system (black
  box, with API fuzzing, performance and security), acceptance (black box, human plus AI role-play)
  — with fuzzing at unit and API level, a defect loop that turns every failing input into a
  permanent regression test, a hard cap on retries, and a fixed report table. Use when asked to
  write a test plan, decide what or how to test, design test cases, find edge cases, add fuzz
  testing, set exit criteria, or report test results. Trigger for: "write a test plan", "how should
  I test this", "design test cases", "find edge cases", "decision table", "fuzz this", "unit vs
  integration test", "acceptance test", "test report", "are we done testing", "วางแผนเทส",
  "ออกแบบ test case", "ทดสอบระบบ", "หา edge case", "ทำ fuzz testing", "สรุปผลเทส". Not for
  fixing one known bug with a repro (a debugging skill owns that), a security audit, or a
  one-line change where a single regression test is the whole job.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: >-
    ISTQB test levels and design techniques, property-based and coverage-guided fuzzing practice,
    and the owner's hand-drawn test flow, redesigned with gates and a bounded defect loop
    (compiled 2026)
---

# test-strategy

> Plan → Design → Unit → Integration → System → Acceptance → Report. A gate after every level, one defect loop with a cap, and every failure becomes a test that runs forever.

## The flow

```
 Start
   │
 1 PLAN ── scope · risk · exit criteria (written, with numbers)
   │
 2 DESIGN ── EP · boundary values · decision table · state transition
   │
 3 UNIT ──────── white box (+ grey)    + function-level fuzz ──► ◇ gate ─┐
   │ pass                                                                │
 4 INTEGRATION ─ grey box (+ white/black)                       ──► ◇ gate ─┤
   │ pass                                                                │ fail
 5 SYSTEM ────── black box (+ grey)    + API fuzz · perf · security ─► ◇ gate ─┤
   │ pass                                                                │
 6 ACCEPTANCE ── black box · human + AI role-play             ──► ◇ exit? ─┤
   │ all exit criteria met                                               ▼
 7 REPORT ◄──────────── escalate ◄── yes ── ◇ loop > N? ◄── DEFECT → fix → REGRESSION
   │                                              │ no
  End                                             └──► rerun from UNIT
```

Read it as three rules:

1. **Levels run in order, each behind a gate.** Integration on top of failing units tests nothing but the failure you already have.
2. **A failure never restarts the whole flow.** It goes through the defect loop and reruns from Unit — the cheapest level, which now carries the new regression test.
3. **The loop has a ceiling.** After N rounds (default 3) on the same failure, stop and escalate to a human. The report is written either way.

---

## Size the flow before running it

The full seven steps are for work where a missed bug is expensive. Pick the track first and say which one in one line.

| Work | Track | Steps |
| --- | --- | --- |
| New feature, medium or larger; money, auth, user data; a public API | **Full** | 1 → 7 |
| A parser, decoder, or anything that eats untrusted input | **Full**, fuzz mandatory | 1 → 7 |
| Change inside one module, existing suite green | **Light** | 2 (only the changed rules) → 3 → 4 → 7 |
| One bug fix | **Regression only** | write the failing test first, fix, run the suite |
| Spike or throwaway prototype | **None** | say so; set a date to write tests if it survives |

---

## Step by step

| Step | Do | Output | Depth |
| --- | --- | --- | --- |
| **1 Plan** | Write scope, top risks, and exit criteria with numbers. If no written requirement exists, write the target first — a test plan built on invented requirements proves the invention. | a filled [test plan](assets/test-plan-template.md) | [exit-criteria](references/exit-criteria.md) |
| **2 Design** | Derive cases from the requirement, not from the code. Partition, take boundaries, tabulate rule combinations, map states. | case list, decision table | [test-design-techniques](references/test-design-techniques.md) |
| **3 Unit** | White box per function; add grey-box seams for collaborators. Fuzz pure functions that parse or transform input. | unit suite, fuzz harness | [test-levels](references/test-levels.md) · [fuzzing](references/fuzzing.md) |
| **4 Integration** | Real database, real queue, real filesystem in a container; mock only what you do not own. | integration suite | [test-levels](references/test-levels.md) |
| **5 System** | Black box against the running app: end-to-end paths, API fuzz from the schema, a load baseline, a security pass. | e2e suite, API fuzz run, perf numbers | [test-levels](references/test-levels.md) · [fuzzing](references/fuzzing.md) |
| **6 Acceptance** | Each acceptance criterion checked by an agent playing the user; a human judges what needs taste or values. | criterion-by-criterion verdict | [ai-acceptance-testing](references/ai-acceptance-testing.md) |
| **7 Report** | Fill the fixed table from real runs, blocking items first. | report | [report-template](references/report-template.md) |

---

## The defect loop

Every gate failure goes through the same four steps. Detail, severities and the escalation message: [defect-loop](references/defect-loop.md).

1. **Record** — level, input, expected, actual, severity.
2. **Reproduce as a test first** — the failing input becomes a unit test (or a fuzz corpus entry, or a new decision-table row) *before* the fix. A fix without a failing test first proves nothing.
3. **Fix** at the root, not at the symptom.
4. **Rerun from Unit.** Count the round. Round N+1 on the same failure → stop and escalate.

BAD — fix, rerun the one level that failed, move on. The fuzz crash fixed on Tuesday comes back on Friday because nothing pins it.
BETTER — crash input saved to the corpus and copied into a named unit test; every later run replays it.

---

## Box types by level

| Level | Primary | Supporting | Catches |
| --- | --- | --- | --- |
| Unit | White box | Grey box | wrong logic in one function, missed branch, bad boundary |
| Integration | Grey box | White + black box | contract mismatch, wrong query, transaction and serialisation bugs |
| System | Black box | Grey box | broken user path, config, performance, security at the edge |
| Acceptance | Black box | Human + AI | built the wrong thing; a criterion nobody checked |

The higher the level, the less the test knows about the code — and the closer it is to what the user sees.

---

## Operating rules

- **Exit criteria are written before the first test runs.** Written after, they describe whatever passed.
- **Never report a pass you did not observe.** Paste the command and its summary line; "should pass" is not a result.
- **A test that has never failed has not proven anything.** Break the code once (or run mutation testing) and watch the test go red.
- **Coverage is a floor, not a verdict.** 100% line coverage with weak assertions catches nothing; mutation score says whether assertions bite.
- **Fuzz has a time box and a stop rule.** Stop when no new crash or new coverage appears for the boxed time, not "when it feels done".
- **Mock what you do not own, integrate what you do.** A mocked database proves the mock.
- **Flaky is a bug.** Quarantine it with an owner and a date; never retry until green.
- **Stop at the cap.** Three rounds on the same failure means the design or the plan is wrong, not the fourth attempt.

## When not to use this

- **One known bug with a reproduction** — fix it with a regression test; this flow is for deciding *what* to test.
- **A security audit** — the system step runs a security pass, but a threat-model review is its own job.
- **Exploration** — a fixed plan fights learning. Time-box the spike, then plan tests for what survives.
