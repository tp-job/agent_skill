# Report template

The report is written from real runs — paste commands and their summary lines — never from memory. Blocking items go first.

## Layout

```markdown
# Test report — <feature or branch> — <YYYY-MM-DD>

## Blocking
- <unmet exit criterion or escalated defect, and the one decision needed>

## Result: PASS | FAIL | BLOCKED   ·   Track: Full | Light   ·   Loops: <n>

## By level
| Level | Technique | Cases | Pass | Fail | Coverage | Defects (C/H/M/L) | Loops | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Unit | white box, property | 142 | 142 | 0 | 86% line / 74% branch | 0/1/0/0 | 2 | ✅ |
| Integration | grey box | 31 | 31 | 0 | — | 0/0/1/0 | 1 | ✅ |
| System | black box, API fuzz 10 min, k6 | 18 | 17 | 1 | — | 0/0/1/0 | 1 | ⚠️ |
| Acceptance | AI role-play + human | 6 AC | 5 | 0 | — | 0/0/0/1 | 0 | ⚠️ 1 cannot verify |

## Exit criteria
| Criterion | Target | Measured | Met |
| --- | --- | --- | --- |

## Defects
| ID | Level | Severity | Summary | Status | Regression test |
| --- | --- | --- | --- | --- | --- |

## Fuzz
| Target | Tool | Time | Executions | Crashes (new) | Corpus size |
| --- | --- | --- | --- | --- | --- |

## Evidence
<commands run and their summary lines>
```

## Metrics worth tracking across reports

| Metric | Formula | Healthy direction |
| --- | --- | --- |
| Defect escape rate | bugs found after release ÷ all bugs | down — the one that matters most |
| Mutation score | killed mutants ÷ total mutants | up |
| Defects by level | count per level | most at Unit/Integration |
| Loops per run | rounds before exit | low; hitting the cap often means weak design or plan |
| Time per run | wall clock of the ladder | stable; growth means the suite needs pruning |
| Fuzz yield | new crashes per hour | falls to zero, then fuzz less often |

Compare against the previous report for the same component. A single report says where you are; two say which way you are moving.
