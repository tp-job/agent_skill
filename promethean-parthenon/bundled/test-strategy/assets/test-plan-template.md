# Test plan — <feature or branch>

**Track:** Full | Light | Regression only   ·   **Date:** <YYYY-MM-DD>   ·   **Loop cap N:** 3

## Scope
- In: <components, endpoints, screens>
- Out: <what is deliberately not tested, and why>

## Requirement source
<link or path to the written requirement and its acceptance criteria — AC-1…AC-n>

## Top risks
| Risk | Impact | Where it is tested |
| --- | --- | --- |
| <e.g. double refund> | money lost | decision table R4/R5, state transition Paid→refund |

## Exit criteria
| Criterion | Target |
| --- | --- |
| Open Critical/High | 0 |
| Line / branch coverage on changed code | 80% / 70% |
| Mutation score on <module> | 60% |
| Decision-table rows with a test | 100% |
| Fuzz without new crash | <target>: <time> |
| Acceptance criteria verified | 100% |
| p95 latency <endpoint> | <ms> |

## Design
- Partitions and boundaries: <inputs>
- Decision tables: <rules>
- State machines: <entities with a status>
- Fuzz targets: <unit functions>, <API schema>

## Levels
| Level | Tools | Environment | Owner |
| --- | --- | --- | --- |
| Unit | | local + CI | |
| Integration | | containers in CI | |
| System | | disposable env | |
| Acceptance | AI agent + <human> | staging | |

## Open questions
- <combinations the requirement does not answer — each with a default if nobody answers>
