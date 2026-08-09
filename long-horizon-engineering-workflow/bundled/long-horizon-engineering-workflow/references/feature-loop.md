# The Feature Loop — sub-tasks and the inner cycle

The six gates run **once per build**. This loop runs **once per feature**, dozens of times, and it is where a long build is actually made or lost.

```
     ┌──────────────────────────────────────────────────────────┐
     │                                                          │
     ▼                                                          │
  AFFECTED ──► SELECT ──► IMPLEMENT ──► VERIFY ──► LEDGER ──► COMMIT
   TESTS      (one, by    (smallest    (the        (passes:   (scoped
   (scoped     priority)   change)      feature's   true)      paths)
    to what                             own steps,               │
    you touch)                          e2e)                     │
                                                                 │
                                          ┌──────────────────────┘
                                          ▼
                                   back to AFFECTED TESTS
                                   (full suite at session start
                                    and before the Stage 3 gate)
```

Never skip a box. The loop's value is entirely in its being unbroken — a loop with an optional step is a suggestion.

---

## Regression: full at the edges, scoped in the middle

The full suite runs **twice**: at session bootstrap, and once more before Stage 3 closes. In between, run only the tests touching what you changed.

This is not a weakening. A full suite on every iteration costs quadratic time — forty features against a ten-minute suite is over six hours of re-running tests that nothing touched, which is how the loop stops being run at all. The guarantee is preserved at the edges, where a regression can actually escape.

| When | Scope |
| --- | --- |
| Session bootstrap | Full suite. Never build on a red tree. |
| Each loop iteration | Tests covering the files you touched, plus anything declaring `depends_on` this feature |
| Before Stage 3 closes | Full suite again, plus the cross-feature checks in Stage 4 |
| Anything red, ever | Stop. Fix before new work. |

If something breaks, mark the affected feature `"passes": false` immediately — the ledger must match reality even when reality is embarrassing — fix it, and note it in `progress.md`.

**A feature does not stay `true` because it was once `true`.** Passing is a claim about the current tree.

---

## What a good sub-task looks like

A feature in [feature-list.json](../assets/feature-list.template.json) is a **sub-task with its own acceptance test built in.**

```json
{
  "id": "F014",
  "category": "functional",
  "priority": "high",
  "description": "User can reset password via emailed one-time link",
  "steps": [
    "Request reset for a registered email → 200, email queued",
    "Request reset for an unregistered email → 200, no email, no enumeration leak",
    "Follow a valid link → password form renders",
    "Follow an expired link (>30 min) → clear error, no form",
    "Reuse a consumed link → rejected"
  ],
  "depends_on": ["F008"],
  "passes": false,
  "notes": ""
}
```

| Rule | Why |
| --- | --- |
| One feature = one commit = one working state | If it can't be committed working, it's two features |
| 3–7 verification steps | Fewer means under-specified; more means it's really several features |
| Steps are observable, not internal | "Returns 401" not "calls the auth middleware" — you must be able to *run* the step |
| At least one failure case | A feature verified only on the happy path is verified nowhere |
| Declare `depends_on` | A feature whose dependency is failing **is not selectable** |

### Priority rubric

Assign by consequence, not by enthusiasm:

| | Meaning |
| --- | --- |
| `critical` | Nothing else works without it — bootstrap, auth, the data layer |
| `high` | On the primary user journey; the build is not shippable without it |
| `medium` | Expected, but a workaround exists |
| `low` | Polish. Cut it without renegotiating scope |

### Categories

`core` (scaffolding, environment) · `functional` (behavior a user invokes) · `ui` (screens and states) · `style` (visual polish) · `integration` (crossing a boundary — service, third party, another feature) · `performance` (a stated numeric target) · `security` (a trust boundary; see invariant 9)

---

## How much to specify up front

Write the **critical path in full** — roughly the first 10–15 features, complete with verification steps. **Stub the rest**: description, category, priority, and `"steps": []`.

You cannot write honest verification steps for feature 47 before feature 3 exists; pretending otherwise produces steps that get quietly loosened later, which is the exact failure invariant 1 exists to stop. But an unwritten feature is a forgotten feature, so the scope still gets listed.

**A feature with no steps cannot be marked passing.** That single rule makes the stub self-correcting: specification happens at the moment you actually know enough, and it happens before the work rather than after.

What Stage 1–2 fix is the **acceptance criteria**, not the implementation plan. Criteria should be stable; the feature list is expected to grow. Growth is discovery working; a drifting acceptance criterion is the build going wrong.

---

## Selection order

1. Anything **red** — a failing regression outranks all new work, always.
2. `critical` → `high` → `medium` → `low`.
3. Within a priority: unblocked before blocked, and prefer features building on already-passing ones.
4. Announce the pick in one line: *"Now working on F014: password reset via emailed link."*

Never carry two features in flight. Parallel half-features are how a tree reaches a state no one can commit and no one can revert.

**One exception — the small-feature batch.** Up to three features may share a commit when all of them are the same category, each is under ~10 lines, and **each is verified individually against its own steps**. Five copy strings do not deserve five commits. Verification never batches; only the bookkeeping does. List every ID in the commit message.

---

## Verification: the part that gets faked

The most common failure of a long-running agent is declaring victory. Guardrails:

- Verify **end to end, through the real interface** — the interface your consumer actually touches:

  | Kind of thing | The real interface |
  | --- | --- |
  | Web UI | A browser. Click, type, screenshot, check the console |
  | API | An actual HTTP call. Status, body shape, error paths |
  | CLI | Run the command. Check stdout and the exit code |
  | Library | The public API, imported from a separate test package — not internal calls |
  | Data pipeline | The output artifact, produced from a real input |
  | Compiler / codegen | Compile *and run* the emitted output |

- A `curl` succeeding is not a UI working. A unit test passing is not a feature working.
- Never script around the interface you are supposed to be testing.
- Mark `passes: true` only when **every** step passed. Not most.

BAD: *"Implemented password reset. The endpoint returns 200, so F014 passes."*

BETTER: *"F014: ran all 5 steps. Step 4 (expired link) returned 500 instead of a clean error — fixed, re-ran, now 410 with a message. All 5 pass. Screenshot of the expired-link state attached."*

---

## Commit discipline

Commit **immediately** after verification passes, before anything else starts. Stage the paths you changed — not `-A`, which sweeps whatever else is sitting in the tree.

```bash
git add src/auth/reset.ts src/auth/reset.test.ts
git commit -m "feat(F014): password reset via emailed one-time link

- Implemented: token issue, 30-min expiry, single-use consumption
- Tested: all 5 verification steps incl. expired + reused link
- Notes: reuses the token store from F008"
```

Confirm it landed: `git status` clean, `git log --oneline -1` shows it. **A feature without a commit does not exist** — it is an uncommitted diff the next context window will not know about and may destroy.

---

## When a feature is blocked

Don't grind. After **three distinct approaches** to the same blocker:

1. Write the blocker into `notes` — specifically, not "hard".
2. Add it to `progress.md`.
3. If the blocker is itself a bug, file it as a new feature and set the original's `depends_on`.
4. Move to the next unblocked feature.

After **three completed implement→verify cycles** on the same feature, stop and return to the user. Re-read the requirement and the design first; if both are sound, the problem is genuinely hard and wants a fresh session, not a fourth attempt with exhausted context.
