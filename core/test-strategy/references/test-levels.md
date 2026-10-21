# Test levels

Run levels in order. Each one has a gate: all tests at that level green, and no new Critical/High defect, before the next starts.

| Level | Box | Scope | Speed target | Gate |
| --- | --- | --- | --- | --- |
| Unit | White (+ grey) | one function or class, collaborators faked | whole suite < 1 min | green, coverage on changed code meets the plan |
| Integration | Grey (+ white/black) | your code plus real infrastructure you own | < 5 min | green against real DB/queue in a container |
| System | Black (+ grey) | the deployed app, end to end | < 15 min | key paths green, API fuzz clean for its time box, perf within target |
| Acceptance | Black + human/AI | the requirement as the user states it | — | every acceptance criterion has evidence |

## Unit — white box

Test logic with knowledge of the code: every branch, every boundary from the design step.

- One behaviour per test; the name states it: `rejects_quantity_above_99`.
- Arrange · Act · Assert, with the assert checking the value, not just "no exception".
- Fake collaborators at the seam (grey box): a repository interface, a clock, a random source.

BAD — `expect(calc(5)).toBeDefined()` passes for every wrong answer.
BETTER — `expect(calc(5)).toBe(25)`.

## Integration — grey box

Test that parts fit: SQL against a real database, messages through a real broker, files on a real disk. You know the contracts (grey); you do not assert on internals.

- Run real dependencies in containers (Testcontainers, or `docker compose` in CI).
- Mock only what you do not own — a third-party payment API, an email provider — and pin the mock to a recorded contract.
- Each test owns its data: transaction rollback or a fresh schema. Shared fixtures make order-dependent tests.

## System — black box

Test the running app through its public surface only.

- End-to-end user paths (Playwright for web; HTTP client for APIs).
- API fuzzing from the OpenAPI/GraphQL schema — see the fuzzing reference.
- A load baseline on the hottest endpoint (k6, Locust, or autocannon): record p50/p95 and error rate, compare with the plan.
- A security pass: auth on every route, IDOR (user A reading user B's record), input validation at the edge.

## Acceptance — black box, human and AI

Test the requirement, not the implementation. Each acceptance criterion gets a verdict and evidence. How the AI side works and what stays with the human: [ai-acceptance-testing](ai-acceptance-testing.md).

## Tools by stack (versions as of 2026)

| Stack | Unit | Integration | System / e2e | Property / fuzz |
| --- | --- | --- | --- | --- |
| TypeScript / Node 20+ | Vitest 3, Jest 29 | Vitest + Testcontainers, Supertest | Playwright 1.5x | fast-check 4 |
| Python 3.11+ | pytest 8 | pytest + Testcontainers | Playwright, httpx | Hypothesis, Atheris |
| Java 21 / Kotlin | JUnit 5 | Testcontainers, Spring Boot Test | REST Assured, Playwright | jqwik, Jazzer |
| Go 1.22+ | `testing` | Testcontainers-go | `net/http/httptest`, Playwright | native `go test -fuzz` |
| Rust | `cargo test` | Testcontainers-rs | reqwest | proptest, cargo-fuzz |

Prefer what the repository already uses. Adding a second test runner to fit this table is worse than using the one there.

## Ordering exceptions

- A **legacy system with no unit tests**: start at System to pin current behaviour (characterisation tests), then add units as you change code.
- A **pure library**: there is no System level; Acceptance is the public API examples in the docs, run as tests.
