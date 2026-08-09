# Routing

Which pillar carries this work. Read the first table that matches your situation and stop.

---

## By what you are holding right now

| You have | Pillar | Then |
| --- | --- | --- |
| A one-line ask with real work behind it | **Foresight** | → Structure if multi-session |
| A written brief, build spans sessions | **Structure** | → Record at the end |
| A written brief, one small change | *None* — just build it | Verify against the brief's proof lines |
| Two viable approaches and a preference for neither | **Judgment** | → Foresight to brief the winner |
| Finished work that needs writing up | **Record** | — |
| A spec someone else wrote | **Foresight**, in check mode | Test it against the four questions, fill gaps, do not rewrite |
| A vague complaint that something is broken | **Structure** — structured feedback | → debug-master once there is a repro |

---

## By what went wrong

| Symptom | Pillar | The actual defect |
| --- | --- | --- |
| Output runs, solves the wrong problem | **Foresight** | Q1/Q2 never answered — the code is fine, the target was wrong |
| Rules appeared you never agreed to | **Foresight** | Q3 answered with adjectives; the agent filled the gaps |
| "Done" that isn't | **Foresight** → Structure | No proof list before the build, so nothing to check against |
| Session two contradicts session one | **Structure** | No on-disk state; the transcript was the state |
| Same bug fixed three times | **Structure** | Re-run decomposition — a recurring bug is a design flaw in disguise |
| Fourth copy of an existing utility | **Structure** | Pattern recognition skipped at Stage 2 |
| Integrations fail on field names and types | **Structure** | Data mapping skipped at Stage 2 |
| Confident answer, no trade-offs named | **Judgment** | You got a summary where you needed a position |
| Scope keeps growing | **Judgment** | Decide: is this discovery, or is the acceptance criterion drifting? |
| "What did we ship?" is unanswerable | **Record** | No conventions in the history; fix forward |

---

## Sizing: how much pillar for how much work

The pillars scale. Applying all four at full weight to a small change is the failure mode of this skill.

| Work size | Foresight | Structure | Judgment | Record |
| --- | --- | --- | --- | --- |
| One-line fix, known cause | One sentence | — | — | Commit message |
| Small feature, one session | Half-page brief | Gates, no harness | — | Commit + PR body |
| Multi-component, one session | Full brief | Gates + ledger | At the design gate | PR body |
| Multi-session build | Full brief | Gates + full harness | Gates, 2× failures, irreversibles | Full report |
| Irreversible or public-facing | Full brief | Full, plus security features on the ledger | Mandatory, before commit | Full report |

**Rule of thumb:** skip the harness under ~10 sub-tasks and one session — below that, the gates carry it alone. Never skip Foresight; size it down instead.

---

## Tie-breakers

**Foresight vs. Structure.** Is the *target* unclear, or the *path*? Unclear target is always Foresight first — running gates against a wrong target produces a well-verified wrong thing.

**Structure vs. Judgment.** Structure asks "is this built correctly?" Judgment asks "should this be built?" If you cannot tell, ask what a wrong answer costs: recoverable → Structure, expensive or irreversible → Judgment.

**Foresight vs. Judgment.** Foresight writes down a decision. Judgment *makes* one. If the brief has an **Open questions** section with a real trade-off in it, that item belongs to Judgment; everything else in the brief belongs to Foresight.

**Record vs. nothing.** If the work took more than a day or crossed a team boundary, it needs a record. Below that, the commit history is the record.

---

## Handing off to skills outside the Parthenon

These pillars cover *constructing software with an agent*. Requests that touch adjacent concerns route out:

| Request | Skill |
| --- | --- |
| A specific bug with a stack trace or repro | [debug-master](../../debug-master/SKILL.md) |
| Extracting requirements from code that already exists | [requirement-gathering](../../requirement-gathering/SKILL.md) |
| Security review of written code | [owasp-top-10-2025](../../owasp-top-10-2025/SKILL.md) |
| UI quality, theme, accessibility audit | [ui-checker](../../ui-checker/SKILL.md) |
| Where does this file go, what is it called | [project-file-structure](../../project-file-structure/SKILL.md) |
| Writing or improving a skill itself | [skill-creator](../../skill-creator/SKILL.md) |

Route out early. A pillar applied to work it was not built for produces confident output about the wrong dimension — which is the exact failure this skill exists to prevent.

---

## The default

**When routing is genuinely unclear, start at Foresight.** It costs minutes, it produces the artifact every other pillar consumes, and its absence is the single most common cause of bad agent output. If after briefing the answer is "this is a one-liner", you have lost ten minutes. If you skip it and the target was wrong, you lose the build.
