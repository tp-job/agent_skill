---
name: promethean-parthenon
description: >-
  The operating doctrine for getting high-performance output out of an AI coding agent,
  and the router across the four skills that produce it: brief it properly
  (agentic-engineering), build it under gates and on-disk state
  (long-horizon-engineering-workflow), decide and critique like leadership
  (senior-leadership-advisor), and record what actually shipped (github-report).
  Trigger when: starting any non-trivial piece of work with an agent and unsure where to
  begin, an agent produced code that runs but is wrong or off-target, output quality is
  degrading over a long session, you are about to say "just build it" on something
  substantial, or you ask "how do I get better results from Claude / the agent", "which
  skill should I use for this", "why does the agent keep drifting". Thai triggers:
  "ใช้ AI agent ยังไงให้ได้งานดี", "agent ทำงานหลุดประเด็น", "ควรใช้ skill ไหน",
  "งานที่ได้ไม่ตรงที่สั่ง". Not itself a builder or a reviewer — it decides which pillar
  carries the work and hands off; go straight to a pillar when you already know which one.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: Promethean Parthenon doctrine — four-pillar synthesis of the agentic-engineering, long-horizon-engineering-workflow, senior-leadership-advisor, and github-report skills (compiled 2026)
---

# Promethean Parthenon

**Promethean** — foresight. The thinking happens before the fire, not after the building burns.
**Parthenon** — four pillars carrying one roof. Remove any pillar and the load does not redistribute; the roof comes down.

## The problem this solves

An AI agent's output quality is not mostly a function of the model. It is a function of four things you control, and every one of them fails silently.

- Ask vaguely → you get **plausible code built against invented requirements**. It runs. It is wrong.
- Build without gates → you get **drift**: features declared done that were never verified, context lost between sessions, the ledger no longer matching reality.
- Never apply judgment → you get **the average answer** to a question that needed a call, with trade-offs unnamed.
- Keep no record → you get **work that happened but cannot be shown**, and the same decision re-argued next month.

None of these announce themselves. All four produce output that *looks* like success. That is the whole reason this skill exists: the failures are silent, so the defenses have to be structural.

---

## The four pillars

| Pillar | Skill | Carries | Fails as |
| --- | --- | --- | --- |
| **Foresight** | [agentic-engineering](bundled/agentic-engineering/SKILL.md) | the brief — what, for whom, under what limits, proven how | right thing, invented rules |
| **Structure** | [long-horizon-engineering-workflow](bundled/long-horizon-engineering-workflow/SKILL.md) | gates, the ledger, on-disk state, verification | drift, declared victory, lost context |
| **Judgment** | [senior-leadership-advisor](bundled/senior-leadership-advisor/SKILL.md) | the call, the trade-off, the pre-mortem | competent execution of a bad decision |
| **Record** | [github-report](bundled/github-report/SKILL.md) | what shipped, in writing, from real data | invisible work, re-argued decisions |

Depth on what each pillar holds and how it cracks: [pillars](references/pillars.md).

---

## The load path

Work moves through the pillars in order. Each hands the next a written artifact — that handoff *is* the structure.

```
        ┌───────────── the roof: output you can trust ─────────────┐
        │                                                          │
   FORESIGHT  ────►   STRUCTURE   ────►   JUDGMENT   ────►   RECORD
   the brief        build-spec.md        the call         the report
                    feature-list.json
                    progress.md

   brief ──────► gates ──────► verified commits ──────► written record
     │              │                  │                      │
     └── what does "done" mean?        └── is it actually done?
                    └── is this still the right thing to build?
```

**Judgment is not a stage — it is a pillar you step into and out of.** It carries load at the gates (is this the right design?), on any feature that has failed twice, and whenever the brief and reality disagree. Everywhere else it is dead weight; a decision framework applied to a routine iteration is ceremony.

---

## Routing

Full decision table with tie-breakers: [routing](references/routing.md). The short version:

| What you have | Start at | Why not elsewhere |
| --- | --- | --- |
| One sentence, real work behind it | **Foresight** | Nothing downstream can be right if the target is wrong |
| A written brief, multi-session build | **Structure** | The brief exists; now it needs gates and state |
| A written brief, one small change | Just build it | Gates on a one-liner are ceremony |
| A choice between two approaches | **Judgment** | This is a decision, not a construction |
| Work is finished, needs writing up | **Record** | — |
| Agent output runs but is wrong | **Foresight** | The brief was the defect, not the code |
| Agent lost the thread mid-build | **Structure** | Missing harness state, not missing skill |
| A specific bug with a repro | None of these | Use [debug-master](bundled/debug-master/SKILL.md) |

**Default when genuinely unsure: Foresight.** It is the cheapest pillar to run and the most expensive to skip — ten minutes of briefing against a rebuild you will mistake for a bug fix.

---

## The five levers

What actually moves agent output quality, ranked by effect. Detail and the measurements behind the ranking: [output-quality](references/output-quality.md).

1. **Specificity of the target.** The single largest lever, by a wide margin. A rule with a number in it beats a paragraph of adjectives. "Secure" is not a requirement; "an attacker with the email address cannot confirm the account exists" is.
2. **Verification you actually ran.** A test that has never failed has proven nothing. Implementation errors get caught by verification; verification errors get caught by nothing.
3. **State that outlives the conversation.** Anything living only in the transcript is not state. Compaction keeps the gist and drops the fact — and the fact is what you needed.
4. **Effort placed at decisions, not iterations.** Deep thinking at the gates, at decomposition, and on anything that failed twice. Routine loop iterations were decided upstream; thinking hard there is spend with no return.
5. **Scope held still.** A growing feature list is discovery working. A drifting acceptance criterion is the build going wrong. Know which one you are looking at.

---

## Diagnosing bad output

Symptom → cause → pillar. Expanded, with the tells for each: [failure-modes](references/failure-modes.md).

| What you are seeing | The actual cause | Go to |
| --- | --- | --- |
| Code runs, solves the wrong problem | Q1/Q2 were never answered | Foresight |
| Rules you never agreed to (expiry, limits, defaults) | Q3 was answered with adjectives | Foresight |
| "Done" that isn't | No proof list written before the build | Foresight, then Structure |
| Session two contradicts session one | No on-disk state | Structure |
| Same bug fixed three times | Decomposition was wrong, not the fix | Structure — re-run decomposition |
| Fourth copy of an existing utility | Pattern recognition skipped | Structure — Stage 2 |
| Shape mismatch at every integration | Data mapping skipped | Structure — Stage 2 |
| Confident answer, unnamed trade-offs | No judgment pass | Judgment |
| "What did we ship?" cannot be answered | No record, or no commit conventions | Record |

**The meta-tell:** an agent that never pushes back on an ambiguous ask is not being efficient. It is guessing quietly, and you will find out later.

---

## Operating rules

- **Foresight is never skipped, only sized.** A one-line ask for a one-line change needs one line of brief. It does not need zero.
- **Never claim a pass you did not observe.** "Implemented" ≠ "verified." This is the rule that everything else is built to protect.
- **One artifact per handoff.** A pillar handing off without its artifact is where the work leaks — and the next seat is usually a future session with no memory.
- **Announce a skipped gate in one sentence, then comply.** Name the gate and the specific risk. If the user says go anyway, go — and do not re-raise it. A *new* risk later is fair; re-litigating the same one is not.
- **Stop after three failed attempts at the same thing.** Re-read the brief and the design. A fourth attempt will not find what three missed.
- **The record is written from real data**, not from memory of what you think you did.

---

## When not to use this

- **You already know which pillar you need.** Go straight there. This skill is a router, and routing a decision you have already made is pure overhead.
- **Trivial, fully-specified work** — a typo, a version bump, a named bug with a repro. Four pillars over a one-line change is architecture as theater.
- **Exploration and spikes.** A fixed brief works against you when the goal is to learn what is possible. Set a time or scope limit instead, then brief the real build.
- **Non-engineering requests.** These pillars are for constructing software. A pure research, writing, or analysis task has different failure modes.

---

## One-paragraph version

Brief it before you build it, build it behind gates that write state to disk, apply real judgment at the decisions and nowhere else, and write down what actually shipped. The four failures this prevents — invented requirements, silent drift, average answers, invisible work — all produce output that looks like success, which is exactly why you need structure rather than attention.

---

## Bundled skills

Every skill this file links to travels with it — as copies under `bundled/` at the library root, or as sibling folders when this skill is itself sitting inside another skill's bundle. Either way no link points outside the copied tree, so dropping this folder into a project brings the whole cluster with it and nothing dangles.

These are copies, not forks. Refresh them from the skill library rather than editing them in place; the only thing that differs from the originals is the depth of their relative links.
