# Defect loop

Every failed gate enters the same loop. It has a fixed exit, so it cannot spin.

```
gate fails ─► record ─► failing test first ─► fix ─► rerun from Unit ─► gate
                                                          │
                                         round > N on the same defect ─► escalate
```

## 1. Record

| Field | Example |
| --- | --- |
| ID | D-07 |
| Level found | System (API fuzz) |
| Input | `POST /orders` body `{"qty": -2147483648}` |
| Expected | 422 with validation error |
| Actual | 500, integer overflow in `total()` |
| Severity | High |
| Round | 1 |

## Severity

| Severity | Meaning | Blocks exit |
| --- | --- | --- |
| Critical | data loss, security breach, money wrong, service down | yes |
| High | main path broken, no workaround | yes |
| Medium | secondary path broken, or main path with a workaround | per plan (default ≤ 3, owned and dated) |
| Low | cosmetic, wording | no |

## 2. Failing test first

Pin the defect at the **lowest level that can show it**. The overflow above is found by system fuzz but reproduced as a unit test on `total()`, which runs in milliseconds.

The test must fail before the fix. If it passes on broken code, it is not testing the defect.

## 3. Fix at the root

BAD — catch the 500 at the controller and return 422. The overflow still corrupts totals reached by other paths.
BETTER — validate `qty` at the boundary *and* make `total()` use a type that cannot overflow; the unit test covers both.

## 4. Rerun from Unit, count the round

Rerun the whole ladder from Unit, not only the level that failed — the fix can break something lower down.

## Cap and escalation

Default **N = 3** rounds on the same defect. A fourth attempt rarely finds what three missed; the problem is usually in the design or the requirement.

At the cap, stop and send:

> **Blocked on D-07 after 3 rounds.** Tried: (1) …, (2) …, (3) …. Known true: … . Suspected cause: the requirement does not say what a negative quantity means. Need from you: one decision — reject, or treat as a return? Default if no answer: reject with 422.

Then write the report with D-07 at the top. Escalation ends the loop; it does not skip the report.

## Flaky tests

A test that passes and fails on the same code is a defect, logged at Medium or higher. Quarantine it with an owner and a date, find the cause (shared state, time, ordering, network), fix it. Never add retries until it goes green.
