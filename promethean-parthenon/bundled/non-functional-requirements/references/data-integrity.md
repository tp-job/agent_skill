# Category 10 — Data integrity and accuracy

## Contents

- Floating point is not decimal
- Rounding: pick one rule and test its edges
- Null versus zero
- NFR catalogue
- Oracle: what "correct" is compared against

---

## Floating point is not decimal

JavaScript `number`, Python `float`, Java `double` and PostgreSQL `double precision` are all IEEE 754 binary64. They cannot represent most decimal fractions exactly: `0.1 + 0.2 === 0.30000000000000004`.

So "full precision, no rounding until display" still carries a tiny representation error. Write the accuracy NFR with a tolerance, and do the comparison after rounding to the displayed precision.

| Need | Use |
| --- | --- |
| Scores, percentages, averages that are displayed to 2 dp | binary64 with a tolerance (≤ 1×10⁻⁹) and one controlled rounding at display |
| Money, or sums that must match a ledger exactly | integer minor units (cents, satang), or a decimal type (`NUMERIC` in PostgreSQL, `Decimal` in Python, a decimal library in JS) |

## Rounding: pick one rule and test its edges

Name the rounding rule in the requirement, because different readers assume different ones.

| Rule | 2.345 → 2 dp | 2.355 → 2 dp | Typical use |
| --- | --- | --- | --- |
| Half up (away from zero) | 2.35 | 2.36 | school grading, most hand calculation |
| Half even (banker's) | 2.34 | 2.36 | finance, IEEE default |

`Number.prototype.toFixed` and `Math.round(x * 100) / 100` operate on the binary value, so they **do not** implement either rule reliably:

```js
(1.005).toFixed(2)  // "1.00"  — 1.005 is stored as 1.00499999999999989...
(2.675).toFixed(2)  // "2.67"
(0.125).toFixed(2)  // "0.13"  — exact in binary, so this one rounds as expected
```

To round half up correctly, use a decimal library. That is the only option guaranteed for every input. The shortcuts `Math.round((x + Number.EPSILON) * 100) / 100` and `Number(Math.round(Number(x + 'e2')) + 'e-2')` both give 1.01, 2.68 and 0.13 for the values above, but they are heuristics. Whichever you choose, **pin it with tests on the edge values 1.005, 2.675 and 0.125.** Python's `round()` is half-even, and `Decimal.quantize(..., ROUND_HALF_UP)` is half-up.

## Null versus zero

A missing score and a score of 0 mean different things. Pick a rule for each aggregate, write it down, and test it.

| Case | Must define |
| --- | --- |
| All inputs missing | result is null (shown as "—"), not 0 |
| Some inputs missing | excluded from the denominator, or counted as 0? Write it down. |
| All inputs 0 | result 0 |
| Weight of a missing item | redistributed, or kept? |

Enforce the distinction at the type level (TypeScript `strict` with `number | null`), and also in the database (nullable column, no `DEFAULT 0`).

## NFR catalogue

| ID | Statement | Must | Method |
| --- | --- | --- | --- |
| DI-01 | Results match the oracle | \|computed − oracle\| ≤ 1×10⁻⁹ before rounding; 100% equal after rounding to display precision; ≥ 30 cases | Test |
| DI-02 | Null and zero distinguished | the four cases above produce their defined results | Test |
| DI-03 | Rounding rule | named rule; edge values 1.005, 2.675, 0.125 give the rule's answer | Test |
| DI-04 | One calculation source | all business calculations live in one server-side module; the client only displays results | Inspection |
| DI-05 | Coverage of the calculation module | statement and branch coverage ≥ 90% | Analysis (`--coverage`) |
| DI-06 | Database constraints | invalid rows (score > max, orphan foreign key, duplicate key) rejected even when inserted directly with SQL | Test |
| DI-07 | No hard delete of referenced data | delete becomes deactivate; historical reports still resolve | Test |
| DI-08 | Change history | each edit to a protected value writes one audit row with old value, new value, actor and time | Test |

## Oracle: what "correct" is compared against

A test compares against an **oracle**, and the oracle has to be independent of the code under test.

| Oracle | Strength |
| --- | --- |
| Hand calculation, recorded in a spreadsheet with formulas visible | independent; easy for examiners to audit |
| Worked examples from the official regulation or curriculum document | authoritative |
| A second implementation (e.g. a Python script) | catches logic slips, but not misreadings of the rule that both implementations share |

Store the oracle cases as fixture data, such as `fixtures/accuracy-cases.csv`, so that the tests and the thesis appendix cite the same cases.
