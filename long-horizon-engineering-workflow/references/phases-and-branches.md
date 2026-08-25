# Phases & Branches — the planning unit between the build and the feature

The gates run **once per build**. The feature loop runs **once per feature**, dozens of times.
Nothing ran in between, and on any build past about a dozen features that missing middle shows up
as the same three symptoms: a flat ledger nobody can read progress off, a branch that has been
open so long it no longer merges cleanly, and a report that cannot say what shipped *when*.

A **phase** is that middle unit. One rule governs it:

> **One phase, one branch.** Exactly one — not zero, not several.
> Every branch below that level is optional and must carry a stated reason.

---

## Phase or sprint — same unit, different cut

Both are a bounded run of the feature loop that ends in something demonstrable. They differ only
in which edge is fixed, and the difference decides what happens when the two disagree.

| | **Phase** | **Sprint** |
| --- | --- | --- |
| Fixed edge | Scope — the phase ends when its features pass | Time — the sprint ends on the date |
| Merges when | The work is done | The date arrives, done or not |
| Overrun shows up as | A late merge | Carry-over |
| Failure mode | A phase that quietly grows until its branch cannot merge | A sprint that merges half-features to hit the date |

**The branch rule is identical for both.** What differs is the close-out: a sprint that reaches its
date with features unfinished merges what verifiably passes and carries the rest forward as
ledger rows — it does **not** hold the branch open, and it does **not** mark unfinished work
`true` to close the sprint cleanly. That second one is the ledger fudge invariant 2 exists to
prevent, arriving dressed as a scheduling decision.

Use whichever cut matches how the work is actually being asked for. If nobody has fixed a date,
you have phases, and calling them sprints adds ceremony without adding a constraint.

---

## How to cut a phase

Decompose at Stage 2 into phases first, then features within them. Cutting features first and
grouping them afterward produces phases that share nothing but their position in a list.

A phase boundary is well-placed when all four hold:

- [ ] **It ends in something demonstrable** — a person can be shown the result and say yes or no. A phase whose output is "the data layer exists" cannot be demonstrated, and cannot be UAT'd either.
- [ ] **Its features share a premise.** Group by the assumption they rest on, so that when a premise expires (see [design-and-architecture](./design-and-architecture.md)) the blast radius is one phase, not the whole ledger.
- [ ] **It merges before it drifts.** If the branch cannot plausibly merge within a session or two, it is not a phase — it is a build, and it needs cutting again.
- [ ] **It is revertable as a unit.** "Undo the billing phase" should be one merge to undo, not an archaeology exercise.

**The demonstrability test is the one that actually does work.** It rejects the phase cut everyone
reaches for first — by layer. Schema → API → UI is three phases none of which can be shown to
anyone until all three land, which means the first two are unverifiable and the third inherits
every mistake in them.

| BAD — cut by layer | BETTER — cut by demonstrable slice |
| --- | --- |
| `phase/1-database`, `phase/2-api`, `phase/3-ui` | `phase/1-signup`, `phase/2-billing`, `phase/3-admin-reports` |
| Nothing is demonstrable until phase 3 | Each merge is something a user can be walked through |
| One premise change touches all three | A premise change usually touches one |

---

## The 1:1 rule, and why it is the branch

```
main ──●────────────────●──────────────────●─────────────►
        \              /  \                /
         ●──●──●──●──●     ●──●──●──●──●──●
         phase/1-signup    phase/2-billing
         (one commit          (one commit
          per feature)         per feature)
```

One branch per phase, merged at the phase's close. The branch is what makes the phase a **unit**
rather than a label:

- **It bounds the blast radius.** The phase's cost of being wrong is one merge to revert. A phase built directly on `main` has no such handle, and "revert the phase" becomes "find and revert eleven commits, in order, hoping none of them touched anything else."
- **It gives the phase a real close-out.** The merge is a moment where something has to be true. Without it the phase ends by assertion, which is the same failure as a feature marked done without verification, one level up.
- **It makes the record derivable.** One phase is one merged range against `main` — which is exactly the query a sprint report already runs. Phases that exist only in someone's head cannot be reported on from real data.

**Zero branches is the more common violation, and the more expensive one.** Building the whole
thing on `main` costs nothing on day one and costs everything the first time a phase has to come
back out.

Name it for the thing, not the date: `phase/2-billing-core`, not `phase/aug-week-3`. The dates are
in the git history already; the name is the only place the *scope* is recorded.

---

## Below the 1:1: branching by rationale

The rule fixes one level and deliberately leaves the rest open — sub-branching depends on the
work, so it is decided per case. The obligation the rule imposes is not a count; it is that
**every branch below the phase level names why it exists**, in `progress.md`, at the moment it is
cut. A branch whose reason is not written down is a branch the next session will find and be
unable to classify.

Legitimate rationales, and what each is actually buying:

| Cut a branch below the phase when | Because it buys | Note it as |
| --- | --- | --- |
| A feature is large or risky enough to want reverting independently of its phase | A second, smaller undo handle inside the phase | `feat/F0XX-<slug>` |
| You are mid-feature at a session or context boundary | Somewhere to put partial work that is neither committed to the phase nor lost — invariant 3 | `wip/F0XX` |
| The approach is genuinely unknown and you are finding out | Permission to throw the work away, which is the whole point of a spike | `spike/<question>`, time-boxed |
| Production is broken and the phase is not shippable yet | A path to `main` that does not drag half a phase with it | `hotfix/<slug>`, cut from `main`, **never** from the phase branch |

And the anti-patterns, which are mostly the same rule over-applied:

| Anti-pattern | Why it costs |
| --- | --- |
| A branch per feature, by default | The commit already carries one reason to revert. A branch adds a merge and a name for no extra handle |
| A branch that outlives its phase | It now belongs to no phase, so nothing merges it and nothing reverts it |
| Two phases sharing one branch | The phases were never units; you have one long phase with two names |
| A phase branch cut from another phase branch | Phase 2 cannot merge until phase 1 does, and a revert of 1 silently takes 2 |
| A branch cut with no reason written | The next session cannot tell a spike from abandoned work from the current front |

**The default below the phase level is no branch at all.** Commit into the phase branch, one
concern per commit. Reach lower only when one of the four rows above is genuinely true — and if
you cannot say which, that is the answer.

---

## Where phases live on disk

A phase plan in the transcript is not a plan — it is the same context-amnesia failure the harness
exists to prevent. Phases go in the ledger, at the same time as the features.

In `feature-list.json`, a `phases` array alongside `features`, and a `phase` field on every
feature:

```json
{
  "phases": [
    {
      "id": "P1",
      "name": "signup",
      "branch": "phase/1-signup",
      "demonstrable": "A new user can register, confirm by email, and sign in",
      "premise": "Email is the only identifier; no SSO in this build",
      "status": "merged",
      "merged_at": "<commit sha of the merge>"
    },
    {
      "id": "P2",
      "name": "billing",
      "branch": "phase/2-billing",
      "demonstrable": "A signed-in user can add a card and be charged once",
      "premise": "One plan, one currency",
      "status": "in_progress",
      "merged_at": null
    }
  ],
  "features": [
    { "id": "F014", "phase": "P1", "...": "..." }
  ]
}
```

`status` takes `planned` · `in_progress` · `merged` · `abandoned`. **`abandoned` is a real
value and must be recorded, not deleted** — a phase that was planned and dropped is a decision,
and under invariant 1 decisions are superseded in place, never erased. Its `premise` field is
usually where the reason already is.

In `build-spec.md`, the phase plan is written at Stage 2 as part of the design, with each phase's
demonstrable outcome stated before any of its features are specified.

**A feature with no `phase` is the tell that the plan was skipped.** Add the phase, not a
null field.

---

## The merge is a gate in miniature

A phase closes the way the build closes, scaled down. Before merging:

- [ ] Every feature in the phase is `true` or explicitly `blocked` with `recheck_when` — no `false`, and no `true` that was never observed
- [ ] The full suite runs green on the phase branch, not just the scoped tests
- [ ] The phase's **demonstrable** outcome has actually been demonstrated end to end, through the interface a consumer touches
- [ ] `progress.md` records what was learned, and any premise that expired during the phase
- [ ] Every sub-branch is merged, abandoned in writing, or carried forward as a named ledger row

Then merge, and **record the merge commit in the phase row.** That sha is what makes the phase
revertable and what a report is later built from.

**Do not open the next phase branch before this one merges.** Cutting phase 3 off an unmerged
phase 2 recreates the dependency the phase structure exists to remove — and it is how a "phase"
plan quietly turns back into one long branch with milestones drawn on it.

---

## When not to use phases

- **A build with fewer than about ten features.** One branch, the feature loop, done. Phases over a small build are the layer of ceremony this file is otherwise arguing against.
- **A single-session build.** The unit exists to survive session boundaries and to bound reverts. Neither pressure exists inside one sitting.
- **Exploration.** A spike has no demonstrable outcome by design — that is what makes it a spike. Time-box it on its own branch and write the phase plan afterwards, once you know what is being built.
- **A repo whose trunk workflow forbids long-lived branches.** Some teams merge to `main` many times a day on purpose. Honour the house mechanics — read them from the repo, per Stage 2 — and keep the phase as a planning and ledger unit without the branch. Record that you did, and why; the 1:1 is a strong default, not a rule that outranks how the repo actually works.
