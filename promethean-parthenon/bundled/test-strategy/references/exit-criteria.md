# Exit criteria

Exit criteria decide when testing stops. Write them in step 1, before any test runs, with a number in each line. A criterion without a number is an opinion, and an agent will resolve opinions in its own favour.

## Template

| Criterion | Default | Raise it when | Lower it when |
| --- | --- | --- | --- |
| Open defects, Critical/High | 0 | — | never |
| Open defects, Medium | ≤ 3, each with an owner and a date | money, auth, data integrity | internal tool, one user |
| Line coverage on changed code | ≥ 80% | core library, parser | UI glue, generated code |
| Branch coverage on changed code | ≥ 70% | rule-heavy logic | thin adapters |
| Mutation score on changed modules | ≥ 60% | money, permissions | prototype heading to production later |
| Decision-table rows with a test | 100% | — | never; a row without a test is an untested rule |
| Fuzz run without a new crash | 10 min per target (CI), 1 h before release | parsers, decoders, public APIs | targets with no untrusted input |
| Acceptance criteria verified | 100%, each with evidence | — | never |
| p95 latency of the key endpoint | team target, written as a number | user-facing hot path | batch jobs |
| Flaky tests | 0 unquarantined | — | never |

Choose values per project and write them in the plan. The defaults are starting points, not standards.

## BAD vs BETTER

BAD:
> Testing is complete when the system is stable and well covered.

BETTER:
> Exit when: 0 open Critical/High; ≥ 80% line and ≥ 70% branch coverage on files changed in this branch; mutation score ≥ 60% on `billing/`; every row of the refund decision table has a passing test; `parse_invoice` fuzzed 1 h with no new crash; AC-1…AC-6 each verified with evidence.

## Reading coverage honestly

| Number | Tells you | Does not tell you |
| --- | --- | --- |
| Line coverage | which lines ran at least once | whether any assertion checked them |
| Branch coverage | which decisions took both sides | whether the boundary values were the right ones |
| Mutation score | whether tests fail when the code is wrong | whether the requirement itself is right |

Mutation tools by stack: Stryker (JS/TS, C#), mutmut or cosmic-ray (Python), PIT (Java/JVM), cargo-mutants (Rust), go-mutesting (Go). Run them on changed modules only; whole-repo mutation runs are slow.

## When criteria cannot be met

Do not quietly lower the bar. Put the unmet criterion at the top of the report, say what was measured, and let the human decide to ship, wait, or change the criterion. Write the decision down with its reason.
