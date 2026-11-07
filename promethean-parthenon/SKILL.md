---
name: promethean-parthenon
description: >-
  Engineering hub; load it before answering any engineering question in scope, even one that looks
  answerable directly; specialists carry checks a direct answer skips. Opens one at once for: a bug,
  error, stack trace, slow query or "something is wrong" (debug-master); security, auth, API keys,
  OWASP (owasp-top-10-2025); theme, dark mode, contrast, layout (ui-checker); test plans, edge
  cases, fuzzing (test-strategy); where a file goes (project-file-structure); kickoff, repo or CI
  setup, pre-merge checks, every page slow, lessons learned (project-pitfalls); writing a skill
  (skill-creator). Runs its own doctrine for trade-offs, requirements, briefs, multi-session builds,
  messy problems. Trigger for: "why is this not working", "I'm stuck", "help me think this through",
  "is this secure", "plan this build", "แก้บัค", "วางแผนเทส", "ก่อนเริ่ม dev ต้องเช็คอะไร",
  "ทำไมเว็บช้าทุกหน้า". Not for trivial fully-specified edits or domain work another skill owns (3D,
  CSS, deploys, design craft, MCP ops).
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "3.8.2"
  source: >-
    Promethean Parthenon doctrine — Role · Task · Format synthesis of the
    senior-leadership-advisor, requirement-gathering, agentic-engineering,
    long-horizon-engineering-workflow, and github-report skills, plus a problem-framing,
    source-synthesis and human-judgment foundation (compiled 2026)
---

# Promethean Parthenon

**Promethean**: foresight, so the thinking happens before the fire. **Parthenon**: pillars carrying one roof; remove one and the roof comes down.

## Fast path — read this first

This skill is the **only** entry point to the twelve skills under `bundled/`; none of them loads on its own. When the request already names its specialist, skip everything below and open it:

| The request is… | Open now |
| --- | --- |
| A bug, error, stack trace, crash, one slow query or endpoint, or "something is wrong" | [debug-master](bundled/debug-master/SKILL.md) |
| Security review, auth, OAuth2, API keys, secrets, "is this secure" | [owasp-top-10-2025](bundled/owasp-top-10-2025/SKILL.md) |
| Theme, dark mode, contrast, layout, "review my UI" | [ui-checker](bundled/ui-checker/SKILL.md) |
| A test plan, test cases, edge cases, fuzzing, exit criteria, a test report | [test-strategy](bundled/test-strategy/SKILL.md) |
| Where a file goes, what to name it | [project-file-structure](bundled/project-file-structure/SKILL.md) |
| Project kickoff, repo or CI setup, "is our CI trustworthy", pre-merge check, every page slow, lessons learned | [project-pitfalls](bundled/project-pitfalls/SKILL.md) |
| Write, fix, or evaluate a skill | [skill-creator](bundled/skill-creator/SKILL.md) |
| A report of shipped work from commits/PRs | [github-report](bundled/github-report/SKILL.md) |

Everything else (an unclear ask, a build, a decision, output that keeps coming back wrong) reads on.

---

## The three pillars

Agent output fails silently in three ways, and each looks like success. **Role · Task · Format** gives each failure an owner.

| Pillar | Answers | Skill | Fails as |
| --- | --- | --- | --- |
| **Role** | Who is answering, and to what standard? | [senior-leadership-advisor](bundled/senior-leadership-advisor/SKILL.md) | the average answer; competent execution of a bad decision |
| **Task** | What is being done, against what target, proven how? | [requirement-gathering](bundled/requirement-gathering/SKILL.md) · [agentic-engineering](bundled/agentic-engineering/SKILL.md) · [long-horizon-engineering-workflow](bundled/long-horizon-engineering-workflow/SKILL.md) | invented rules, then silent drift |
| **Format** | What shape does the output take, and what survives? | [github-report](bundled/github-report/SKILL.md) | invisible work, re-argued decisions |

Work moves Role → Task → Format, and each pillar hands the next a written artifact. **Role is not a stage**: step into it at the gates, on a feature that has failed twice, and when target and reality disagree. Anywhere else it is ceremony. Depth: [pillars](references/pillars.md).

## The foundation: thinking before the pillars

Process built on a wrong frame or an unweighed source is well-executed error.

| Discipline | Use when | Hands to | Depth |
| --- | --- | --- | --- |
| **Frame**: find the real problem | The ask is a symptom, a wish or a mess; or three attempts have failed | Task | [problem-solving](references/problem-solving.md) |
| **Synthesize**: many sources, one position | Sources or experts disagree and a call hangs on them | Role | [synthesis](references/synthesis.md) |
| **Consult**: what only the human knows | The answer turns on values, history, stakes or taste | Every gate | [human-judgment](references/human-judgment.md) |

- **Measure before you theorize.** One number splits the hypothesis space. Label anything unmeasured *inferred*.
- **Summary is not synthesis.** End in a position, its premise, and what would change it.
- **Ask about values, never about checkable facts**, and attach the default you will take if nobody answers.

Skip the foundation when the symptom is already measured, one authoritative source settles it, or everything is checkable.

## Inside the Task pillar

**You cannot build against a target you have not written down.** Which skill writes it depends on where the requirements live:

| The requirements live in… | Skill | Produces |
| --- | --- | --- |
| Code that already exists | **requirement-gathering** | `REQ-*` items, contracts, a gap list |
| Someone's head, one sentence long | **agentic-engineering** | a one-page brief |
| A written target that now has to be built | **long-horizon-engineering-workflow** | gates, a ledger, verified commits, on-disk state |

Extending an existing system: run extraction first, then the brief, so the new part respects published contracts. Construction runs in phases, **one phase = one branch**, grouped by contract (does anything consume what this task produces?), never by topic. Details: [phases-and-branches](bundled/long-horizon-engineering-workflow/references/phases-and-branches.md).

---

## Routing

Full table with tie-breakers: [routing](references/routing.md).

| What you have | Start at |
| --- | --- |
| One sentence, real work behind it | **Task**: agentic-engineering |
| An existing codebase and no written spec | **Task**: requirement-gathering |
| A written target, multi-session build | **Task**: long-horizon |
| A written target, one small change | Just build it |
| A choice between two approaches | **Role** |
| A symptom or a mess, no clear problem yet | **Foundation**: frame |
| Sources disagree and a call hangs on it | **Foundation**: synthesize, then Role |
| Finished work that needs writing up | **Format** |
| Agent output runs but is wrong | **Task**: agentic-engineering (the brief was the defect) |
| Agent lost the thread mid-build | **Task**: long-horizon (missing on-disk state) |
| A design job (IA, art direction, concepts) | Outside the pillars: the athena-erechtheion skill |
| Which tool, MCP server or subagent | Outside the pillars: the hermes-olympus skill |

**Default when unsure: the front of Task.** Writing the target down is the cheapest move and the most expensive to skip.

## The specialists fire inside the loop

Open a specialist at the moment its trigger applies, mid-build, without leaving the pillar you are in. On one real build the security reference was never opened and contrast was checked by hand beside an unused checker, because nothing routed to them ([regression-cases](references/regression-cases.md) RC-06).

| Trigger | Skill |
| --- | --- |
| About to write auth, crypto, access control, input handling or secrets (before writing it, not at review) | [owasp-top-10-2025](bundled/owasp-top-10-2025/SKILL.md) |
| Changed anything visual: theme, contrast, dark mode, focus, a breakpoint | [ui-checker](bundled/ui-checker/SKILL.md) |
| Deciding what "verified" means for a feature, or reporting a build's tests | [test-strategy](bundled/test-strategy/SKILL.md) |
| Creating a file or folder | [project-file-structure](bundled/project-file-structure/SKILL.md) |
| Starting a project, setting up repo or CI, merging to main, writing lessons learned | [project-pitfalls](bundled/project-pitfalls/SKILL.md) |
| Writing or revising a skill | [skill-creator](bundled/skill-creator/SKILL.md) |
| A specific bug with a reproduction | [debug-master](bundled/debug-master/SKILL.md) |

---

## What moves output quality

Ranked by effect; measurements in [output-quality](references/output-quality.md), model-specific phrasing and a paste-ready CLAUDE.md block in [model-briefing](references/model-briefing.md).

1. **Specificity of the target.** A rule with a number beats a paragraph of adjectives.
2. **Verification you actually ran.** A test that has never failed has proven nothing.
3. **State that outlives the conversation.** Compaction keeps the gist and drops the fact.
4. **Effort at decisions, not iterations.** Raise the reasoning effort level at gates and on repeat failures, not on routine loop turns.
5. **Scope held still.** A growing feature list is discovery; a drifting acceptance criterion is the build going wrong.

When output is bad, match the symptom to its cause and pillar in [failure-modes](references/failure-modes.md). The meta-tell: an agent that never pushes back on an ambiguous ask is guessing quietly.

## Operating rules

- **The target is never skipped, only sized.** A one-line change needs one line of written target, not zero.
- **Never claim a pass you did not observe.** "Implemented" ≠ "verified."
- **Mark what you could not confirm**, with where to check it: `file:line`, a URL, or the command that settles it.
- **Report blocking items first**, above the summary.
- **One artifact per handoff.** The next seat is usually a future session with no memory.
- **Occupy the role, don't narrate it.** The switch changes the work, not the wording.
- **Announce a skipped gate in one sentence, then comply.** If the user says go anyway, go, and do not re-raise it.
- **Stop after three failed attempts at the same thing.** Re-read the target, change the representation, ask the human one question ([problem-solving](references/problem-solving.md) §When stuck).
- **Write the record from real data**, not from memory.

## When not to use this

- **You already know the pillar you need.** Open its `bundled/` SKILL.md directly.
- **Trivial, fully-specified work** (a typo, a version bump, a named bug with a repro).
- **Exploration and spikes.** Set a time or scope limit instead, and write the real target afterward.
- **Non-engineering requests.** The [synthesis](references/synthesis.md) discipline still travels to any decision resting on conflicting sources.

## Maintaining this package

The `bundled/` skills are verbatim copies; refresh them from the library rather than editing them. How to handle a broken copy, the record of past local fixes, and how to verify a change: [maintenance](references/maintenance.md).
