# Eval results — v0.1.0

> **How these were graded:** by the author of the skill, reading it fresh against each
> case in `evals.json`. This is the weakest form of test (skill-creator, Step 2). No
> subagent runs yet. Re-run with one fresh agent per case before treating these as passes.

| # | Case | Result | Sentence that owns it |
| --- | --- | --- | --- |
| 1 | New project, proposal + schema | pass (self-graded) | SKILL.md top-ten #1, #2 · before-design A2, A3, A5 |
| 2 | Every page slow on Fastify + Prisma + Supabase | pass (self-graded) | Rules "Measure before you theorise" · during-build C1–C4 · day-zero B8, B11 |
| 3 | "CI is green", about to merge | pass (self-graded) | top-ten #4, #5 · day-zero B3, B4 |
| 4 | Write up what went wrong | pass (self-graded) | retrospective — sources table, "Label coverage", template |
| 5 | Typo in README | pass (self-graded) | description negative scope · "When not to use this" |

## Not yet tested

- Triggering: whether the description fires on the Thai phrases and does not fire on
  adjacent asks (a test plan, a single bug). Write 10–15 should / should-not queries.
- Overlap with an engineering hub's brief and build skills, if this is later filed as a
  spoke instead of a standalone folder.
