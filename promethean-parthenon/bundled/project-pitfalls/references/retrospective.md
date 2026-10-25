# Retrospective — turning a project's history into lessons

Use when asked "what went wrong", "what did we learn", or for the lessons chapter of a
report. The method matters more than the prose: a retrospective built from commit titles
and memory repeats the project's blind spots.

---

## Sources, in order

| # | Source | How | What it gives |
| --- | --- | --- | --- |
| 1 | Git history | `git log --reverse --format='%h %ad %s%n%b' --date=short` | The timeline, and in the **bodies** the causes. Titles alone hide them. |
| 2 | Decision and progress docs | Grep for "problem", "risk", "blocked", "decided", and the local language equivalents | Risks that were open, decisions and their dates |
| 3 | Plans with findings lists | Read sections named findings, gaps, open decisions | Problems found before they became bugs |
| 4 | PR descriptions | `gh pr list --state all`, then read bodies | What was claimed tested versus not |
| 5 | Past agent sessions | Search transcripts by keyword; export the few that matter and read them in full | What the user reported, what was measured, what was fixed |

Read oldest-first. Causes come before effects, and a fix makes sense only after its
problem.

**Label coverage.** Say which sources were read in full and which were sampled from
snippets. A retrospective that does not say what it skipped reads as complete.

---

## Sorting what you find

Put each item in one of four buckets:

| Bucket | Question |
| --- | --- |
| **Problem** | What went wrong, observably? (a number, an error, a date) |
| **Cause** | Why — the mechanism, not "we were careless" |
| **Fix** | What changed, and where (commit, file, migration) |
| **Lesson** | The check that would have caught it earlier, stated as an action |

Then group by **when it could have been caught** — before design, day zero, during build,
handoff — not by topic. Grouping by phase tells the next project when to look.

A lesson is a **check**, not a principle. "Be careful with CI" changes nothing. "Open the
latest run of each required job and break one gate on a throwaway branch" gets done.

---

## Lessons file template

Write the result to a file in the repository (for example
`docs/.../lessons-learned.md`), not only to chat — chat is not state.

```markdown
# Lessons learned — <project>

> Created: <date> · Sources: <list, with "read in full" / "sampled">
> Caveat: <what was inferred and not re-verified>

## 1. Before design
### 1.x <short title>
- Problem: <observable>
- Cause: <mechanism>
- Fix: <what changed, where>
- Lesson: <the check, as an action>

## 2. During the lifecycle (setup · build · test · CI/CD · security · team)
...

## 3. What worked and is worth reusing
1. <practice> — <where it paid off>

## 4. Checklist for the next project
- [ ] <check>

## 5. Not covered / not verified
- <source not read, claim not re-checked, open decision>
```

---

## Before you hand it over

- Every number traces to a source you can name.
- Claims marked "fixed" were re-checked, or are labelled as taken from the record.
- Open items are listed, with who owns them.
- Anything new that this skill's checkpoints did not list is a candidate to add to them.
