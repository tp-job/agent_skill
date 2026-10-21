# Test design techniques

Derive cases from the requirement, not from the code. Cases read off the code test that the code does what it does.

| Technique | Use when | Finds |
| --- | --- | --- |
| [Equivalence partitioning](#equivalence-partitioning) | an input has ranges or categories | one representative per class instead of hundreds of redundant cases |
| [Boundary value analysis](#boundary-value-analysis) | a rule has a limit | off-by-one, `<` vs `<=` |
| [Decision table](#decision-table) | several conditions combine into one outcome | missing rule combinations — the classic edge case |
| [State transition](#state-transition) | an entity has a lifecycle | illegal transitions, actions in the wrong state |

Use them together: partition first, take boundaries of each partition, tabulate the combinations, and map states for anything with a status field.

---

## Equivalence partitioning

Split each input into classes the system should treat the same; test one value per class, valid and invalid.

Requirement: *quantity is 1–99.*

| Class | Example | Expected |
| --- | --- | --- |
| below range | 0 | rejected |
| in range | 50 | accepted |
| above range | 100 | rejected |
| not a number | `"abc"` | rejected |
| missing | `null` | rejected |

## Boundary value analysis

Bugs cluster at limits. For each boundary take the value on it and one each side.

For 1–99: **0, 1, 2, 98, 99, 100**.

BAD — testing 5, 50 and 500. All three pass with `qty > 0 && qty < 100` *and* with `qty >= 0 && qty <= 100`; the bug in the second survives.
BETTER — 0 and 100 split the two implementations immediately.

## Decision table

List conditions as rows, every combination as a column, and the expected action. Each column becomes at least one test.

Requirement: *refund allowed within 30 days; members get 60; items marked final-sale never refund.*

| Rule | R1 | R2 | R3 | R4 | R5 |
| --- | --- | --- | --- | --- | --- |
| Final sale | Y | N | N | N | N |
| Member | – | N | N | Y | Y |
| Days since purchase | – | ≤ 30 | > 30 | ≤ 60 | > 60 |
| **Refund** | **No** | **Yes** | **No** | **Yes** | **No** |

`–` means "does not matter". Then add the boundaries of each numeric condition: days 30, 31, 60, 61.

Rules:
- Full combinations are 2ⁿ; collapse with `–` only where the requirement says the condition is irrelevant, and write why.
- A column the requirement does not answer is a **question for the human**, not a guess. Record it as a gap.
- A fuzz crash or production bug that reveals a missing combination becomes a new column.

## State transition

For anything with a status, draw states and allowed events, then test every allowed transition once and the most dangerous illegal ones.

```
Draft ──submit──► Pending ──approve──► Paid ──refund──► Refunded
                    │
                    └──reject──► Rejected
```

| From | Event | Expected |
| --- | --- | --- |
| Draft | submit | Pending |
| Pending | approve | Paid |
| Paid | refund | Refunded |
| Refunded | refund | **rejected** — no double refund |
| Draft | approve | **rejected** — skips review |
| Rejected | approve | **rejected** |

The illegal rows are where money and permissions leak.

---

## When not to apply

- A pure pass-through with no rules: one happy path and one error path are enough.
- Rules that change weekly in a prototype: table the stable core only.
- Generated code (ORM clients, protobuf stubs): test the generator's input, not its output.
