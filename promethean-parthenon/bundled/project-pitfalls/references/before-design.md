# A · Before design

## Contents

- A1 · Root problem written down, and every feature traced to it
- A2 · Schema scope matches the written objective
- A3 · Every calculation rule signed off with a worked example
- A4 · Undefined states have a definition
- A5 · Baseline of the current process measured
- A6 · Roles and permissions decided from the matrix, not from intuition
- A7 · Data shapes that are expensive to change later are decided now
- A8 · Diagrams have one source and one official file each
- A9 · Threat model numbers are not presented as protection
- A10 · Decisions recorded as questions with owners
- Exit for checkpoint A

Run when a proposal or a first schema exists and no feature code has been written.
Everything here is cheap now and costs a rebuild later.

Each item: **check** — **prove it** — *what happened when it was skipped*.

---

## A1 · Root problem written down, and every feature traced to it

- **Check:** the problem statement names who is hurt and when. Causes are traced to a
  root (fishbone by category, then "why" five times per branch), and a table maps
  **root → feature that fixes it**.
- **Prove it:** every planned feature appears in the right-hand column of that table.
  A feature with no root is scope you are choosing to carry — say so.
- *Skipped:* features get justified by "it would be nice", and the evaluation chapter has
  nothing to measure against.

## A2 · Schema scope matches the written objective

- **Check:** list every boundary the schema enforces — tenant, organisation, curriculum,
  campus — and find each one in the objective. A boundary the objective does not mention
  is unrequested complexity.
- **Prove it:** a two-column table, *schema boundary* vs *sentence in the objective*,
  with no empty right-hand cells.
- *Skipped:* a multi-institution schema (`Institution`, `Membership`, `Curriculum`) was
  designed for a single-faculty system. Every query would have needed a tenant filter.
  Found during design, it still cost an inserted task, about one sprint, and a revision
  of every document. Found mid-build, it would have touched every query and every screen.

## A3 · Every calculation rule signed off with a worked example

- **Check:** for each number the system computes (score, weight, grade, risk flag),
  write the formula, one worked example with real-looking data, and the edge cases
  (no score yet, excused, zero weight, withdrawn).
- **Prove it:** the domain owner signed a hand-computed sheet. Those sheets become the
  expected values of the first unit tests.
- *Skipped:* "weight" could be read two ways; on the same data the two readings differed
  by about 20 points — enough to flip pass/fail for a whole class. Tests for the
  calculation could not be written because nobody knew which answer was right.
- **When the team cannot decide:** take the comparison table (both formulas, same data,
  the difference) to whoever owns the rule. A question without numbers gets deferred.

## A4 · Undefined states have a definition

- **Check:** for every status the UI will show, decide what it means when data is
  missing. "At risk" for a student with no scores at all? "0" versus "not yet assessed"?
- **Prove it:** each state has one sentence in the requirements and one row in the
  schema (a nullable column or an explicit status), not a convention in someone's head.
- *Skipped:* the core feature — flagging at-risk students early — could not be specified
  because at the start of term every student has no scores.

## A5 · Baseline of the current process measured

- **Check:** time the current manual process (spreadsheet, paper) for a real task
  before the new system exists.
- **Prove it:** a number per participant, recorded with the date.
- *Skipped:* the claim "the system reduces workload" has nothing to compare against, and
  the baseline cannot be collected after the old process is gone.

## A6 · Roles and permissions decided from the matrix, not from intuition

- **Check:** write the permission matrix (capability × role). For any proposal to merge
  or drop a role, count which capabilities change hands.
- **Prove it:** a test reads the matrix from its single source (prototype, config) and
  fails when the server's copy drifts.
- *Example of the count paying off:* merging three course roles into one would have moved
  9 of 18 capabilities — freezing grades, overriding grades, deleting students, inviting
  others — to a teaching assistant invited yesterday. A two-role middle ground kept most
  of the simplification. The team had already made and reversed that merge once; the
  matrix made the reason visible.
- **Also decide early:** what the administrator may do inside data they do not own.
  Three documents said three different things until it was settled in writing.

## A7 · Data shapes that are expensive to change later are decided now

- **Check:** grouping questions — one course with several sections, or one record per
  section? shared outcomes across sections? — answered before tables exist.
- **Prove it:** the unique key of each core table is written next to the sentence that
  justifies it.
- *Example:* one section = one course row (`unique(code, semester, year, section)`) is
  simple, but combining sections into one report later needs a new parent table and a
  migration of every child. Ask the domain owner before building.

## A8 · Diagrams have one source and one official file each

- **Check:** for each diagram type (use case, ER, DFD, flowchart, threat model) there is
  exactly one official file, and generated ones are produced by a script from a single
  source (prototype, SQL, schema).
- **Prove it:** a checker regenerates and compares by **content**, not bytes, and fails
  on numbering that disagrees between files.
- *Skipped:* use-case numbers meant different things in two files (11 mismatches, one
  duplicate, 13 unnumbered); a UML said "delete account" while the schema forbade it;
  two ER PDFs of the same version disagreed; a diagram saved from a stale editor tab
  overwrote the generated one.

## A9 · Threat model numbers are not presented as protection

- **Check:** a modelling tool lists threats with default status. Until each is assessed,
  the count is a to-do list.
- **Prove it:** a mapping table, threat category → code measure → test that checks it.
- *Skipped risk:* 695 threats all "Not Started / High" read like coverage in a slide.

## A10 · Decisions recorded as questions with owners

- **Check:** open questions are written as numbered items (`D-1`, `OI-10`) with the
  default you will use if nobody answers, and what each one blocks.
- **Prove it:** the progress report lists open questions above finished work.
- *Why:* a narrative of what got done hides the question that is blocking next week.

---

## Exit for checkpoint A

Scope table has no orphan boundaries · calculation rules signed with sheets · undefined
states defined · baseline recorded · permission matrix in one place · one official file
per diagram. Anything still open is reported as **blocking** with its default.
