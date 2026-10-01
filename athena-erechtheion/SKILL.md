---
name: athena-erechtheion
description: >-
  Single entry point to design work and to five bundled design specialists. Runs a job from a
  one-line ask to a handoff-ready draft in five stages: architecture (IA, screens, token tiers), art
  direction (a written visual thesis), creativity (divergent concepts, scored), drafting (wireframes,
  prototypes, Figma, Canva, Blender), review (critique a draft against its thesis). Routes to: a
  distinctive look for one page or component, typography, less templated UI (frontend-design);
  Material 3 Expressive, Google design, motion, UX writing (google-design-system); Tailwind-first
  CSS files, CSS hell, specificity, design tokens (css-architecture); three.js, WebGL/WebGPU,
  shaders, GLTF, R3F, 3D scenes (threejs-3d); this year's web design trends, filed by launch year,
  scored before adoption (web-design-trends). Tears down a reference screenshot: style, palette,
  type, grid, build stack. Trigger for: "design this from scratch", "art direction for", "give
  me concepts", "wireframe this", "moodboard", "make this look less generic", "follow Material 3",
  "organise my Tailwind CSS", "build a 3D scene", "analyse this design screenshot", "critique this
  draft", "web design trends 2026", "is this design dated", "วิเคราะห์ดีไซน์เว็บ", "เทรนด์เว็บ 2026",
  "ช่วยคิดคอนเซปต์ดีไซน์". On a specialist trigger, open that bundled skill at once — do not run the
  stages for a one-component tweak. Not for implementing a finished design (a Figma frame, a
  mockup) in code, auditing a built UI for contrast or dark-mode bugs, or software architecture.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "3.5.0"
  source: >-
    Promethean-Parthenon Role · Task · Format doctrine applied to design practice; information
    architecture, art-direction and double-diamond ideation methods (compiled 2026)
---

# Athena Erechtheion

**Athena** — goddess of wisdom and of craft (Athena Ergane, patron of weavers, potters and every skilled hand): the judgement that turns a raw idea into a considered form.
**Erechtheion** — her temple on the Acropolis, built to hold several sacred functions under one roof: the five design specialists in `bundled/` work here, each answering a different part of the same commission.

## Fast path — read this first

This skill is the **only** entry point to the five skills under `bundled/`; none of them loads on its own. When the request already names its specialist, skip everything below and open it:

| The request is… | Open now |
| --- | --- |
| A distinctive look for one page or component, typography, "less generic" | [frontend-design](bundled/frontend-design/SKILL.md) |
| Material 3, Google design standards, motion, UX writing | [google-design-system](bundled/google-design-system/SKILL.md) |
| Tailwind-first CSS files, CSS hell, specificity, token files, PostCSS | [css-architecture](bundled/css-architecture/SKILL.md) |
| three.js, WebGL/WebGPU, shaders, GLTF, R3F, a 3D scene | [threejs-3d](bundled/threejs-3d/SKILL.md) |
| What's trending this year, "make it feel current", "is this dated" | [web-design-trends](bundled/web-design-trends/SKILL.md) |
| Analyse a screenshot or reference site: its style, palette, type, grid, and how to build it | [reference-analysis](references/reference-analysis.md), which needs no stages |
| Critique a design draft or mockup that isn't built yet | [critique](references/critique.md), which needs no stages |

Everything else — a new product, site, brand or scene, an unclear design ask, a design that keeps being redone — reads on.

A design job fails in the same three silent ways an engineering job does, and this skill carries the same three defenses:

| Pillar | In design it answers | Fails as |
| --- | --- | --- |
| **Role** | Who is the design lead, and whose taste is final? | a committee average: every concept "fine", none chosen |
| **Task** | What is being designed, for whom, in what medium, judged how? | a beautiful draft of the wrong screen set |
| **Format** | What survives the session — tokens, decisions, a spec? | a mockup nobody can rebuild or defend next month |

The work runs through **five disciplines in order**. Each one hands the next a written artifact, and that handoff *is* the structure.

```
  ARCHITECTURE ──► ART DIRECTION ──► CREATIVITY ──► DRAFTING ──► REVIEW ──► design record
  what exists,     the visual         many concepts,  the cheapest   critique vs   tokens + decisions
  how it is        thesis, in         then one,       medium that    thesis and    + checks run,
  organised        writing            scored          answers it     target        handed to the build
                                                          ▲              │
                                                          └── blockers ──┘  (two loops at most)
```

**Why this order:**
- Art direction over an unknown screen set styles the wrong things.
- Ideation without a thesis produces variety, not choices.
- Drafting before convergence produces three polished directions and no decision.
- A draft that skips review hands its bugs to the build, where they cost ten times more to fix.

---

## Stage 0 — write the design target (Task)

Before any pixel, answer the four questions in writing. One line each is enough for a small job; never zero.

| Question | BAD | BETTER |
| --- | --- | --- |
| What is being designed? | "a landing page" | "the signup page and its three error states, desktop and 375px" |
| For whom? | "users" | "clinic receptionists, mid-shift, one hand on a phone" |
| Under what limits? | "modern, clean" | "existing brand teal #0F766E, WCAG 2.2 AA, no custom fonts over 60 KB" |
| Judged how? | "looks good" | "a receptionist finds 'reschedule' in under 5 s in a hallway test; lead signs off on one concept" |

If "judged how" has no observable test, the design will be judged by whoever speaks last. Write one.

Then write the **system decision** in one line: full Material 3, Material 3 as the foundation under the brand's own look (the default for web and brand work), or none because an existing system already answers it. See [material-foundation](references/material-foundation.md).

Then set the **Role**: name who has final taste (the user, a brand owner, or you as acting lead) and state it. When the answer turns on taste, history or stakes, ask the human one question and attach the default you will take.

---

## The five disciplines

| Discipline | Produces | Done when | Depth |
| --- | --- | --- | --- |
| **Architecture** | screen inventory, IA map, user flows, token tiers | every screen in scope is named and every flow ends somewhere | [architecture](references/architecture.md) · M3 tiers in [material-foundation](references/material-foundation.md) |
| **Art direction** | a one-paragraph visual thesis, palette + type with reasons, three "never" rules | a stranger could reject an off-brand draft using only the thesis | [art-direction](references/art-direction.md) · references torn down with [reference-analysis](references/reference-analysis.md) |
| **Creativity** | 3–5 divergent concepts, one scored winner, the runner-up's best idea salvaged | the scorecard picks a concept the lead accepts | [creative-process](references/creative-process.md) |
| **Drafting** | wireframes, diagrams, a clickable or rendered draft, the design record | the draft answers the open question and the record lets someone rebuild it | [drafting](references/drafting.md) · real copy and images first: [imagery-and-content](references/imagery-and-content.md) |
| **Review** | a review note: what to keep, blockers, and passes not run | no blockers remain, and every check in the record was actually run | [critique](references/critique.md) |

**Worked example:** one small job taken through every stage — target, inventory, thesis, scored concepts with a lead override, a hi-fi draft and a record listing only the checks actually run: [example-design-record](assets/example-design-record.md) · [example-draft.html](assets/example-draft.html). Trigger tests for this skill's description: [trigger-evals.json](assets/trigger-evals.json).

---

## Sizing: how much design for how much work

Applying all five stages at full weight to a small change is this skill's failure mode.

| Job | Architecture | Art direction | Creativity | Drafting | Review |
| --- | --- | --- | --- | --- | --- |
| Tweak one screen in an existing system | — (inventory is known) | reuse the existing thesis | — | one annotated draft | passes 1, 3, 7 |
| New feature, 2–5 screens | flow + inventory | reuse, note any extension | 2–3 concepts, quick score | wireframe → one hi-fi screen | all passes on the hi-fi screen |
| New product, site or brand | full IA + token tiers | full thesis | 3–5 concepts, full scorecard | wireframes → prototype → record | all passes + a hallway test |
| Illustration, poster, 3D scene | composition only | full thesis | 3–5 thumbnails | one rendered draft | passes 1–3 |

**Rule of thumb:** if an existing design system already answers a stage, cite it and skip the stage. Re-deriving a brand that exists is waste dressed as rigor.

---

## Handing off

This skill plans and drafts. When a stage needs deeper craft, open the bundled specialist mid-stage and keep the plan here.

| The stage needs… | Open |
| --- | --- |
| A distinctive visual identity for one page or component | [frontend-design](bundled/frontend-design/SKILL.md) |
| Material 3 / Google design conformance | [google-design-system](bundled/google-design-system/SKILL.md) |
| Tailwind-first CSS file and token layout — the *files* behind the token tiers from architecture | [css-architecture](bundled/css-architecture/SKILL.md) |
| A 3D scene in three.js | [threejs-3d](bundled/threejs-3d/SKILL.md) |
| Whether a current trend belongs in the thesis: baseline rules plus at most two scored statements for the launch year | [web-design-trends](bundled/web-design-trends/SKILL.md) |
| An audit of the built result — contrast, dark mode, focus states | a UI-review skill (in this library, via the promethean-parthenon router) |
| Charts, dashboards, KPI tiles inside the design | a data-visualization skill, if one is installed; otherwise treat chart colours as tokens and run review pass 7 on them |
| UX writing rules for buttons, errors and empty states | [google-design-system](bundled/google-design-system/SKILL.md) — its UX-writing domain |
| Figma, Canva or Blender tool calls | that tool's own skill or MCP instructions — see [drafting](references/drafting.md) §Media |

---

## Operating rules

- **The target is never skipped, only sized.** One line of target for a one-screen tweak. Not zero.
- **Write the thesis before the palette.** A palette without a sentence behind it is a preference, and preferences lose every argument.
- **Diverge before you polish.** No concept gets hi-fi treatment until the scorecard has run.
- **Draft in the cheapest medium that answers the question.** ASCII answers "what goes where"; only a render answers "does this feel right".
- **Never claim a design passes a test you did not run.** "Accessible" means a checked contrast ratio, not an intention.
- **No lorem ipsum in hi-fi.** Draft around the longest real string, or the layout is untested.
- **Review before you hand off, and run the passes you claim.** A review with nothing listed under "not run" and no evidence is just an opinion.
- **The record is written from the final draft**, not from memory of the concepts.
- **Stop after three rejected drafts of the same thing.** The thesis or the target is wrong, not the draft. Go back one stage and ask the lead one question.

---

## Bundled skills

This is an aggregator, like promethean-parthenon: every skill it links to travels with it as a verbatim copy under `bundled/`, so dropping this folder into a project brings the design cluster with it and nothing dangles. The copies are regenerated by `scripts/build-bundles.py` from the sources in the library's `design/` folder — change the source, never the copy.

---

## When not to use this

- **The design already exists and needs building.** That is engineering; write the build target instead.
- **One component needs to look better.** A five-stage plan over a button is ceremony — open [frontend-design](bundled/frontend-design/SKILL.md) from the fast path instead.
- **Pure exploration or mood play.** Time-box it, skip the scorecard, and write the target afterward if something is worth keeping.
- **Software architecture** (services, data models, APIs). "Architecture" here means the architecture of a design.
