# D · Handoff and team

Run when sharing a branch, writing a PR, onboarding a teammate, or working across many
AI-agent sessions.

Each item: **check** — **prove it** — *what happened when it was skipped*.

---

## D1 · One concern per commit, named for what changed

- **Check:** the subject says what changed (`fix(db): pass the grade to RAISE in
  migration 0004`), the body says why.
- **Prove it:** `git log --oneline` reads like a changelog.
- *Seen:* nine commits titled "Refactor code structure for improved readability and
  maintainability" — one of them overwrote a generated diagram, and nobody could tell
  which from the title.

## D2 · Work in progress does not pile up

- **Check:** uncommitted changes span one feature at a time.
- *Seen:* about 40 modified files across several features at once — impossible to review
  or revert one of them.

## D3 · The PR says what was not tested

- **Check:** a "not verified" list (Docker build not run, DB tests skipped locally,
  diagram not opened in its editor).
- *Why:* an honest list beats ticking every box; reviewers know where to look.

## D4 · Separate checkouts for unrelated work

- **Check:** unrelated work (CI hardening while a feature branch has uncommitted changes)
  goes in its own worktree.
- *Why:* nothing in the feature checkout gets touched or swept into the wrong commit.

## D5 · Teammate onboarding has a "do not run" list

- **Check:** the guide covers clone → setup → env values (shared privately, never in
  chat or git) → run → health check, **and** the commands that are destructive on a
  shared database (`db:seed`, `migrate dev`).
- **Prove it:** a teammate follows it start to finish without asking.
- **Common problems to list with fixes:** runtime too old; port in use; ORM engine file
  locked on Windows; sign-in provider rejects the origin (`origin_mismatch` — add the
  dev origin to the OAuth client's allowed JavaScript origins).

## D6 · Work for teammates goes through issues

- **Check:** a feature handed to someone else is an issue with scope and acceptance, not
  a chat message.

## D7 · Irreversible operations are the human's to press

- **Check:** deleting a hosted project, merging to main, authorising a connector,
  creating a superuser — the agent prepares and reports; the human acts.
- **Prove it:** the old resource is kept until the new one is verified working (keep the
  old database until the new region has migrated, seeded and been measured).

## D8 · Long agent work is split by phase

- **Check:** one session per phase or concern; state that must survive goes to a file
  (plan, ledger, lessons), not only the transcript.
- *Seen:* a session ran until its context had to be summarised and hit a usage limit
  mid-feature; switching models mid-task several times made results harder to compare.

## D9 · Reports to the agent include what you saw

- **Check:** "it did nothing" plus the exact message, a screenshot, or the console
  output — not "here is what I saw:" with nothing after it.
- *Why:* without it the agent can only check what it can observe itself, which for a
  third-party sign-in iframe is nothing.

---

## Exit for checkpoint D

History readable · no cross-feature pile of uncommitted work · PR lists what was not
verified · a teammate can run the project from the guide · irreversible steps handed to
a human · lessons recorded (see retrospective).
