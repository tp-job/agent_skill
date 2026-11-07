---
name: project-pitfalls
description: >-
  Checks a software project against failure modes that happened on a real build, at four
  checkpoints: before design (scope, unsigned business rules, permissions, data boundaries), day
  zero (clean-clone setup, one runtime version, CI that provably fails, database region, secrets),
  during build (measure round trips before tuning, central access gate, isolated tests, generated
  docs) and handoff (one-concern commits, honest PRs, onboarding, lessons mined from git history).
  Each item says how to prove it and what broke when skipped. Trigger for: "project kickoff
  checklist", "what should we check before we start", "set up the repo properly", "is our CI
  trustworthy", "why is every request slow", "pre-merge check", "write the lessons learned",
  "retrospective", "ก่อนเริ่ม dev ต้องเช็คอะไร", "สรุปบทเรียน", "ทำไมเว็บช้าทุกหน้า". Not for one
  known bug or slow query, a security audit, a test plan, running the build phase by phase, or a
  shipped-work report.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Lessons learned from the CMAS course-outcome tracking app, Jul-Oct 2026 (compiled 2026)
---

# Project Pitfalls

A checklist of the ways a real project went wrong, organised by **when** you can still
catch each one cheaply. Every item is something that happened — not a best practice
copied from a blog — and each carries the proof that it is fixed.

The failures share one property: **each produced output that looked like success.** A
green CI that had not run for three weeks. A schema that compiled but served the wrong
scope. A page that worked, slowly, because of four hidden round trips per query. You
will not notice them by paying attention; you notice them by running the check.

---

## Workflow

```
1. Locate the stage   →  2. Run that checkpoint   →  3. Mark each item with evidence
        ↓                                                      ↓
6. Record new lessons ←  5. Fix in order of effect  ←  4. Report blocking items first
```

1. **Locate the stage.** Pick the checkpoint from the table below. A project mid-build
   with no day-zero work done runs both — day zero first, because its gaps poison every
   later measurement.
2. **Run the checkpoint.** Open its reference file and go through it item by item.
   Skip an item only when it cannot apply (no database, no CI) and say so.
3. **Mark each item** `pass` · `fail` · `n/a` · `unchecked`, with the evidence:
   a command and its output, a `file:line`, a measured number. An item without evidence
   is `unchecked`, never `pass`.
4. **Report blocking items first** — anything that invalidates later work (wrong scope,
   CI not actually running, unsigned calculation rules) goes above the summary.
5. **Fix in order of measured effect**, re-measuring after each change. One change per
   measurement, so the improvement can be attributed.
6. **Record what was new.** A failure this checklist did not list goes into the
   project's lessons file using the template in
   [retrospective](references/retrospective.md), and is worth adding here.

## Checkpoints

| Stage | Run when | Reference |
| --- | --- | --- |
| **A · Before design** | Proposal or first schema exists; no feature code yet | [before-design](references/before-design.md) |
| **B · Day zero** | Repo is being set up, or a teammate cannot run it from a clean clone | [day-zero](references/day-zero.md) |
| **C · During build** | At each phase close, before merging to main, or when something is slow, flaky or out of sync | [during-build](references/during-build.md) |
| **D · Handoff and retro** | Sharing a branch with a teammate, writing the PR, or writing up lessons | [handoff-and-team](references/handoff-and-team.md) · [retrospective](references/retrospective.md) |

The evidence behind every item — numbers, dates, what it cost — is in
[case-cmas](references/case-cmas.md). Read it when a teammate asks "does this really
happen?" or when you need a worked example for a report.

The workflow as a draw.io flowchart: [workflow.drawio](assets/workflow.drawio). It is
generated — edit [build_workflow_drawio.py](scripts/build_workflow_drawio.py), then run
`python scripts/build_workflow_drawio.py assets/workflow.drawio preview.svg`. The script
refuses to write when boxes overlap, leave the page, or an arrow points at nothing.

---

## The ten checks that caught the most

If there is time for only ten, run these. Each line is the check, then what it caught.

| # | Check | Caught |
| --- | --- | --- |
| 1 | Compare every table and boundary in the schema with the written objective | A multi-institution schema for a one-faculty system — one sprint lost, every document revised |
| 2 | Get each calculation rule signed off with a worked example before coding it | Two readings of "weight" 20 points apart, enough to flip pass/fail for a whole class |
| 3 | Clone fresh, run the one setup command, start the app | A seed script pointing at a missing file, a README naming the wrong framework |
| 4 | Open the latest run of every required CI job, then break one gate on a throwaway branch | CI failing at install for three weeks while everyone read "green" |
| 5 | Same runtime major in `.nvmrc`, `engines`, CI and every Dockerfile | The cause of check 4 |
| 6 | Time a no-database endpoint against a database endpoint; log per-query time | 250 ms per round trip to a far region; 4 round trips per query through a transaction pooler |
| 7 | Every route declares its access rule, and the server refuses to boot if one does not | A route that forgot its permission check becomes a boot error instead of an open endpoint |
| 8 | Run the database tests twice in a row, and with the real rate limit | Parallel test files deleting each other's users; a 429 instead of the 404 under test |
| 9 | Regenerate every generated diagram and compare by content | An old diagram saved over the generated one from a stale editor tab |
| 10 | Read git history oldest-first, including commit bodies, before writing a retrospective | Nine commits titled "Refactor code structure for improved readability" hiding what changed |

---

## Rules

- **Measure before you theorise.** A number from a no-database endpoint vs a database
  endpoint splits "slow server" from "slow database" in one request. Three theories
  without it only multiply.
- **Prove each gate can fail.** A check that has never been seen failing has proven
  nothing. Break it on purpose, watch it go red, restore it.
- **Generated files are edited at their generator.** If a file comes from a script,
  change the script or its source and regenerate — a hand edit is lost on the next run
  and may already have overwritten newer output.
- **Irreversible actions stay with the human.** Deleting a database project, rotating a
  secret, authorising a connector, merging to main: report what is ready, let them press it.
- **Label what you did not verify.** "Fixed" and "fixed and re-measured" are different
  claims. Say which one you are making.

## When not to use this

- **A trivial, fully-specified edit** — a typo, a version bump. No checklist applies.
- **One known bug with a reproduction** — debug it directly. The same goes for one slow
  query or endpoint you can point at; this skill owns slowness only when *every* page is
  slow, because that is a setup problem (region, pooler, round trips), not a code bug.
- **A full security audit or a test plan** — those need their own method; this skill only
  carries the security and testing failures that actually occurred, not complete coverage.
- **Running the build** — phases, branches and a feature ledger belong to a gated build
  workflow. This skill audits the project at a checkpoint; it does not drive the work.
- **A report of what shipped** — a sprint or feature report is built from commits and PRs.
  A retrospective here asks what went wrong and why, not what was done.
- **Exploration or a spike** — set a time box instead; run checkpoint A when the spike
  turns into a project.

The items are drawn from one stack (React, Fastify, Prisma, PostgreSQL on Supabase, npm
workspaces, GitHub Actions, Windows dev machines). The failure patterns transfer; the
exact commands and settings are marked with the stack they apply to — adapt them, do not
copy them blind.
