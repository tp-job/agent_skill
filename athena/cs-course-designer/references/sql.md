# SQL — Topic Map

Reference for [cs-course-designer](../SKILL.md), Step 1. Covers querying, joins, subqueries, window functions, and query performance.

**Always state the engine and version.** SQL behavior diverges more than students expect: `LIMIT` vs. `TOP` vs. `FETCH FIRST`, NULL sort order, window-function support, string concatenation, date arithmetic, and identifier quoting all differ. Default to current mainstream **PostgreSQL** unless the request names another engine, and say so up front.

For modeling, normalization, transactions, and indexing theory, see [database-management](database-management.md).

---

## Topic coverage

| Unit | Topics | Depends on |
| --- | --- | --- |
| 1. Foundations | Relations and result sets; `SELECT`/`FROM`; column aliases; literals and data types; **logical processing order** | — |
| 2. Filtering | `WHERE`; comparison and logical operators; `BETWEEN`, `IN`, `LIKE`; `IS NULL`; three-valued logic | 1 |
| 3. Sorting & limiting | `ORDER BY`, multi-column, `ASC`/`DESC`; NULL ordering; `LIMIT`/`OFFSET` (engine-specific) | 2 |
| 4. Distinct & expressions | `DISTINCT`; computed columns; `CASE`; `COALESCE`/`NULLIF`; string, numeric, date functions | 2 |
| 5. Aggregation | `COUNT`/`SUM`/`AVG`/`MIN`/`MAX`; `GROUP BY`; `HAVING` vs. `WHERE`; how aggregates treat NULL | 4 |
| 6. Joins | Inner join; left/right/full outer; self join; cross join; join vs. filter conditions; multi-table joins | 2 |
| 7. Set operations | `UNION` vs. `UNION ALL`; `INTERSECT`; `EXCEPT`; column compatibility rules | 6 |
| 8. Subqueries | Scalar, row, table subqueries; `IN`/`EXISTS`/`ANY`/`ALL`; correlated subqueries; subquery in `FROM` | 6 |
| 9. CTEs | `WITH`; readability and reuse; multiple CTEs; recursive CTEs (hierarchies) | 8 |
| 10. Window functions | `OVER`, `PARTITION BY`, `ORDER BY`; `ROW_NUMBER`/`RANK`/`DENSE_RANK`; `LAG`/`LEAD`; running totals; frame clauses; window vs. `GROUP BY` | 5, 9 |
| 11. Data modification | `INSERT` (values, from select); `UPDATE` with join/subquery; `DELETE`; `UPSERT`; the transaction wrapper | 6 |
| 12. DDL | `CREATE`/`ALTER`/`DROP TABLE`; constraints; indexes; views | 11 |
| 13. Query performance | Reading an execution plan; scan vs. seek; sargability; index usage; join algorithms; common rewrites | 12, 10 |
| 14. Correctness & safety | Parameterized queries vs. injection; the `UPDATE` without `WHERE`; testing on a transaction you roll back | 11 |

---

## One reasonable sequencing

**8-week SQL unit:** 1–2 (wk 1) → 3–4 (wk 2) → 5 (wk 3) → *checkpoint: aggregation with filtering* → 6 (wk 4–5) → 7–8 (wk 6) → 9–10 (wk 7) → 11–13 (wk 8)

**Compressed 3-day workshop:** 1–5 (day 1) → 6, 8 (day 2) → 9–10, 13 (day 3). Drop set operations, DDL, and recursive CTEs; say what was cut.

**Hard dependency edges:**

```
SELECT → WHERE → ORDER BY
WHERE → aggregation → HAVING     (HAVING before GROUP BY is incoherent)
inner join → outer join → NULL semantics in outer joins
aggregation + joins → subqueries → CTEs → window functions
schema/indexes → execution plans
```

**Teach logical processing order in week 1.** `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY` is the single most clarifying idea in the whole subject: it explains why you cannot use a `SELECT` alias in `WHERE`, why `HAVING` exists at all, and why `ORDER BY` *can* use aliases. Teaching it late means re-teaching everything that preceded it.

---

## Common misconceptions

### NULL — the largest single source of wrong answers
- **`WHERE col = NULL` finds NULLs.** It matches nothing. Requires `IS NULL`.
- **`NOT IN` with a NULL in the subquery returns rows.** It returns nothing, silently. Brutal, invisible, and extremely common — worth an entire formative check.
- **`COUNT(col)` and `COUNT(*)` are the same.** `COUNT(col)` skips NULLs.
- **`AVG` divides by the row count.** It divides by the non-NULL count.
- **Concatenating or arithmetic with NULL yields the other operand.** It yields NULL.
- **NULLs sort predictably.** Order differs by engine; Postgres puts them last ascending, others first.

### Joins
- **A `WHERE` filter on the right table of a `LEFT JOIN` silently makes it an inner join.** The single most common join defect in real code. The filter must move into the `ON` clause.
- **The join produces one row per left row.** Not seeing that a one-to-many join multiplies rows — and then that aggregates over the multiplied rows are wrong.
- **`LEFT`/`RIGHT` refer to physical table position** rather than which side is preserved.
- **A missing join condition is an error.** It is a cross join, which runs, returns a plausible-looking huge result, and is wrong.
- **Joining on the wrong cardinality then using `DISTINCT` to "fix" duplicates** — masking a modeling error with a symptom patch.
- **Confusing `JOIN` with `UNION`** — combining columns vs. combining rows.

### Aggregation and grouping
- **Selecting a non-aggregated, non-grouped column.** Rejected by strict engines, silently arbitrary in some MySQL configurations — which is precisely why the engine must be stated.
- **`HAVING` and `WHERE` are interchangeable.** No grasp that `WHERE` filters rows before grouping and `HAVING` filters groups after. Costs correctness *and* performance.
- **`GROUP BY` sorts the result.** It may appear to; it is not guaranteed without `ORDER BY`.
- **`COUNT(*)` after a `LEFT JOIN` counts matched rows.** It counts result rows, including the unmatched left rows — `COUNT(right.id)` is usually what was meant.

### Subqueries and CTEs
- **A correlated subquery runs once.** Not seeing it executes per outer row, and why that matters for cost.
- **`IN` and `EXISTS` are always interchangeable.** They differ with NULLs (see above) and often in plan.
- **A CTE is always materialized** (or never). Depends on the engine and version; do not teach a performance rule that isn't true on the student's engine.
- **Recursive CTEs without a terminating condition.**

### Window functions
- **`GROUP BY` and window functions are alternatives.** They are not: `GROUP BY` collapses rows, a window function preserves them. This distinction *is* the topic.
- **`RANK` and `ROW_NUMBER` are the same.** They differ exactly on ties, and `DENSE_RANK` differs again.
- **A window function can go in `WHERE`.** It cannot — it is computed after `WHERE`. Requires a CTE or subquery wrapper. Follows directly from logical processing order, which is why that must be taught first.
- **Omitting the frame clause when `ORDER BY` is present** and being surprised by the default `RANGE` frame in running totals.

### Performance
- **`SELECT *` is fine.** No sense of the I/O and covering-index consequences.
- **A function on an indexed column keeps the index.** `WHERE YEAR(d) = 2026` typically defeats it; `WHERE d >= '2026-01-01' AND d < '2027-01-01'` does not.
- **Leading wildcard `LIKE '%foo'` uses an index.** It cannot.
- **Query order in the text determines execution order.** The optimizer reorders; that is its job.
- **Adding an index always helps.** No accounting for write cost.
- **`OR` across different columns performs like `AND`.** It frequently forces a scan.

### Modification
- **Testing an `UPDATE`/`DELETE` by running it.** Teach the habit: write it as a `SELECT` with the same `WHERE` first, then run it inside a transaction you can roll back.
- **String-concatenated queries are fine "because it's internal."** Injection belongs in the SQL unit, not deferred to a security course.

---

## Where formative checks pay most

- After **NULL semantics** — predict the result of `NOT IN` with a NULL present.
- After **outer joins** — a filter-in-`WHERE`-vs.-`ON` prediction item.
- After **`GROUP BY`/`HAVING`** — which clause filters what, and why.
- After **window functions** — same query with `GROUP BY` vs. `OVER`, explain the difference in row count.

Every item needs the schema, sample data, and the engine stated.

---

## Related

- [database-management](database-management.md) — modeling, normalization, transactions, indexing theory
- [clo-writing](clo-writing.md) · [assessment-design](assessment-design.md)
