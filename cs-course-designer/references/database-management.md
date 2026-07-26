# Database Management — Topic Map

Reference for [cs-course-designer](../SKILL.md), Step 1. Covers ER modeling, the relational model, normalization, transactions, indexing, and a NoSQL overview.

For query-language content, use [sql](sql.md) — the two overlap deliberately, and when a course covers both, teach each concept once, where it is first needed.

The sequencing below is one defensible order. If the request is anchored to a textbook (Elmasri & Navathe, Silberschatz, Connolly & Begg) or an institution's syllabus, follow that instead.

---

## Topic coverage

| Unit | Topics | Depends on |
| --- | --- | --- |
| 1. Why databases | Files vs. DBMS; redundancy, inconsistency, concurrent access, integrity; the three-schema architecture; data independence | — |
| 2. The relational model | Relations, tuples, attributes, domains; the definition of a key; primary/candidate/foreign/composite keys; entity and referential integrity; NULL semantics | 1 |
| 3. Conceptual modeling (ER) | Entities, attributes (simple/composite/derived/multivalued), relationships; cardinality (1:1, 1:N, M:N); participation (total/partial); weak entities; identifying relationships; EER: specialization/generalization | 2 |
| 4. Logical design | ER → relational mapping rules; resolving M:N with a junction table; representing weak entities; surrogate vs. natural keys | 3 |
| 5. Functional dependencies | FDs; closure; determinant; full vs. partial vs. transitive dependency | 4 |
| 6. Normalization | Anomalies (insert/update/delete); 1NF, 2NF, 3NF, BCNF; 4NF/5NF (awareness); lossless decomposition; deliberate denormalization | 5 |
| 7. Relational algebra | σ, π, ⋈, ∪, −, ×, ρ; as the semantic foundation under SQL | 2 |
| 8. DDL & constraints | `CREATE TABLE`, data types, `PRIMARY KEY`, `FOREIGN KEY` with referential actions, `NOT NULL`, `UNIQUE`, `CHECK` | 4 |
| 9. Transactions | ACID; transaction states; commit/rollback/savepoints | 8 |
| 10. Concurrency | Lost update, dirty read, non-repeatable read, phantom read; isolation levels; locking; deadlock | 9 |
| 11. Recovery | Write-ahead logging; checkpoints; backup/restore strategies | 9 |
| 12. Indexing & storage | Pages and rows; B-tree indexes; clustered vs. non-clustered; composite index column order; covering indexes; hash indexes; the write cost of an index | 8 |
| 13. Query processing | Logical → physical plans; reading an execution plan; scan vs. seek; join algorithms (nested loop, hash, merge); the role of statistics | 12, 7 |
| 14. Views, procedures, triggers | Views and updatability; materialized views; stored procedures; triggers and their maintenance cost | 8 |
| 15. Security & integrity | Privileges, roles, `GRANT`/`REVOKE`; least privilege; injection as a design issue; auditing | 8 |
| 16. NoSQL overview | Key-value, document, column-family, graph; CAP and its common misreading; BASE vs. ACID; when relational is still right | 6, 10 |
| 17. Warehousing (optional) | OLTP vs. OLAP; star and snowflake schemas; fact and dimension tables; deliberate denormalization | 6 |

---

## One reasonable sequencing

**14-week course:** 1–2 (wk 1) → 3 (wk 2–3) → 4 (wk 4) → *checkpoint: model a domain end to end* → SQL basics (wk 5–6, see [sql](sql.md)) → 5–6 (wk 7–8) → *checkpoint: normalize a flawed schema* → 8 + 7 (wk 9) → 9–10 (wk 10–11) → 12–13 (wk 12) → 15–16 (wk 13) → project (wk 14)

**Hard dependency edges:**

```
relational model → keys → ER mapping → normalization
functional dependencies → normalization   (skipping FDs makes normalization rote)
transactions → concurrency → isolation levels
schema + DDL → indexing → query plans
```

**Sequencing decisions worth making explicitly:**

- **SQL early or late.** Early gives students something tangible and makes modeling feel purposeful; late keeps the conceptual thread clean. Early is generally better for engagement, provided the relational model came first.
- **Relational algebra before or after SQL.** Before makes SQL's semantics (especially joins and NULLs) make sense; after risks it feeling like pointless formalism. Some courses skip it — say so rather than omitting silently.
- **Normalization before or after students have written queries.** After is more effective: they have felt the anomalies.

---

## Common misconceptions

### Keys and the relational model
- **A primary key is the ID column.** Not seeing that a key is a *uniqueness constraint*, and that a natural composite key can be perfectly valid.
- **Every table needs a surrogate `id`.** Reflexively adding one to junction tables that already have a natural composite key.
- **A foreign key must reference a primary key.** It must reference a unique constraint; usually but not necessarily the PK.
- **NULL means zero, or empty string, or "no."** NULL is *unknown*, and the three-valued logic that follows is the source of nearly every surprising query result. This misconception must be broken early or it contaminates all query work.
- **`NULL = NULL` is true.** It is unknown. Persistent even among students who can recite the definition.

### ER modeling
- **Attributes modeled as entities, or entities as attributes.** No stable rule is internalized for which is which.
- **M:N relationships drawn but not resolved** when mapping to tables.
- **Cardinality read backwards.** Notation direction (crow's foot, Chen, UML) is confusing and inconsistent across tools — pick one notation and stay in it.
- **Relationships confused with foreign keys.** Treating the diagram as a picture of tables rather than of the domain.
- **Weak entities given surrogate keys**, erasing the identifying relationship that made them weak.

### Normalization
- **Normalization is about removing duplicate rows.** It is about removing *dependency* anomalies. This misreading makes 2NF/3NF incomprehensible.
- **Higher normal form is always better.** No sense of when denormalization is the right engineering call.
- **2NF violations exist in tables with a single-column key.** Partial dependency requires a composite key — students apply the rule mechanically without checking.
- **Confusing transitive dependency with any indirect relationship.**
- **Normalizing by intuition** rather than from the functional dependencies. Produces right answers on textbook examples and wrong ones on anything unfamiliar — which is exactly why assessment should require the FDs to be stated.

### Transactions and concurrency
- **ACID is one property**, or Durability means backups.
- **Isolation levels are performance settings** with no correctness consequence — no connection made between the level and which specific anomaly it permits.
- **Higher isolation is always better.** No awareness of the throughput cost or deadlock risk.
- **A transaction is a single statement.** Missing that the point is multi-statement atomicity.
- **Deadlock is a bug in the database.**

### Indexing and performance
- **More indexes = faster database.** No accounting for write amplification and storage.
- **An index on every column in the `WHERE` clause** rather than one well-ordered composite index.
- **Composite index column order doesn't matter.** It determines which queries the index can serve at all.
- **Indexes speed up all queries**, including those returning most of the table — where a scan is genuinely cheaper.
- **The plan is read top to bottom** in execution order. It is generally read inside-out.
- **A function applied to an indexed column still uses the index.** `WHERE YEAR(order_date) = 2026` typically defeats it — one of the highest-value single facts in the course.

### NoSQL
- **NoSQL means no schema.** It means schema-on-read; the schema still exists, in application code.
- **CAP means "pick two."** It is about behavior during a partition. The common misstatement is the most-repeated error in the topic.
- **NoSQL is newer, therefore better.** No sense of the workloads each model actually suits.
- **Joins are impossible in document databases**, rather than deliberately avoided by denormalizing.

---

## Where formative checks pay most

- After **ER → relational mapping**, before normalization — have them map an M:N relationship.
- After **functional dependencies**, before normal forms — have them list FDs for a small table.
- After **NULL semantics** — a three-valued-logic prediction item.
- After **isolation levels** — name which anomaly each level permits.

---

## Related

- [sql](sql.md) — query language detail
- [clo-writing](clo-writing.md) · [assessment-design](assessment-design.md)
