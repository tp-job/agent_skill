---
name: daedalus-atelier
description: >-
  Single entry point to design work and to four bundled design specialists. Runs a whole job from a
  one-line ask to a handoff-ready draft in four stages: architecture (IA, screen inventory, token
  tiers), art direction (a written visual thesis), creativity (divergent concepts, scored), drafting
  (wireframes, prototypes, Figma, Canva, Blender), under the Promethean-Parthenon Role · Task ·
  Format doctrine. Routes to: a distinctive look for one page or component, typography, less
  templated UI (frontend-design); Material 3 Expressive, Google design, motion, UX writing, Google
  Sans (google-design-system); Tailwind-first CSS files, CSS hell, specificity, design tokens,
  PostCSS (css-architecture); three.js, WebGL/WebGPU, shaders, GLTF/GLB, R3F, 3D scenes, product
  viewers (threejs-3d). Trigger for: "design this from scratch", "art direction for", "give me
  concepts", "wireframe this", "moodboard", "what should this look like", "make this look less
  generic", "follow Material 3", "organise my Tailwind CSS", "build a 3D scene", "ออกแบบทั้งระบบ",
  "ช่วยคิดคอนเซปต์ดีไซน์", "ทำเว็บ 3D". On a specialist trigger, open that bundled skill at once —
  do not run the four stages for a one-component tweak. Not for implementing a finished design (a Figma
  frame, a mockup) in code, auditing a built UI for contrast or dark-mode bugs, or software and
  system architecture.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "3.0.0"
  source: >-
    Promethean-Parthenon Role · Task · Format doctrine applied to design practice; information
    architecture, art-direction and double-diamond ideation methods (compiled 2026)
---

# Daedalus Atelier

**Daedalus** — the master craftsman of myth: architect of the labyrinth, sculptor, inventor. Every stage here is his trade — structure, art, invention, the drawing before the build.
**Atelier** — the workshop where the Muses' crafts are practised: the four design specialists in `bundled/` work here.

## Fast path — read this first

This skill is the **only** entry point to the four skills under `bundled/`; none of them loads on its own. When the request already names its specialist, skip everything below and open it:

| The request is… | Open now |
| --- | --- |
| A distinctive look for one page or component, typography, "less generic" | [frontend-design](bundled/frontend-design/SKILL.md) |
| Material 3, Google design standards, motion, UX writing | [google-design-system](bundled/google-design-system/SKILL.md) |
| Tailwind-first CSS files, CSS hell, specificity, token files, PostCSS | [css-architecture](bundled/css-architecture/SKILL.md) |
| three.js, WebGL/WebGPU, shaders, GLTF, R3F, a 3D scene | [threejs-3d](bundled/threejs-3d/SKILL.md) |

Everything else — a new product, site, brand or scene, an unclear design ask, a design that keeps being redone — reads on.

A design job fails in the same three silent ways an engineering job does, and this skill carries the same three defenses:

| Pillar | In design it answers | Fails as |
| --- | --- | --- |
| **Role** | Who is the design lead, and whose taste is final? | a committee average: every concept "fine", none chosen |
| **Task** | What is being designed, for whom, in what medium, judged how? | a beautiful draft of the wrong screen set |
| **Format** | What survives the session — tokens, decisions, a spec? | a mockup nobody can rebuild or defend next month |

The work runs through **four disciplines in order**. Each hands the next a written artifact; the handoff *is* the structure.

```
  ARCHITECTURE ──► ART DIRECTION ──► CREATIVITY ──► DRAFTING ──► design record
  what exists,     the visual         many concepts,  the cheapest     tokens + decisions
  how it is        thesis, in         then one,       medium that      + spec, handed to
  organised        writing            scored          answers it       the build
```

**Why this order:** art direction over an unknown screen set styles the wrong things; ideation without a thesis produces variety, not choices; drafting before convergence produces three polished directions and no decision.

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

Then set the **Role**: name who has final taste (the user, a brand owner, or you as acting lead) and state it. When the answer turns on taste, history or stakes, ask the human one question and attach the default you will take.

---

## The four disciplines

| Discipline | Produces | Done when | Depth |
| --- | --- | --- | --- |
| **Architecture** | screen inventory, IA map, user flows, token tiers | every screen in scope is named and every flow ends somewhere | [architecture](references/architecture.md) |
| **Art direction** | a one-paragraph visual thesis, palette + type with reasons, three "never" rules | a stranger could reject an off-brand draft using only the thesis | [art-direction](references/art-direction.md) |
| **Creativity** | 3–5 divergent concepts, one scored winner, the runner-up's best idea salvaged | the scorecard picks a concept the lead accepts | [creative-process](references/creative-process.md) |
| **Drafting** | wireframes, diagrams, a clickable or rendered draft, the design record | the draft answers the open question and the record lets someone rebuild it | [drafting](references/drafting.md) |

**Worked example:** one small job taken through every stage — target, inventory, thesis, scored concepts with a lead override, a hi-fi draft and a record listing only the checks actually run: [example-design-record](assets/example-design-record.md) · [example-draft.html](assets/example-draft.html). Trigger tests for this skill's description: [trigger-evals.json](assets/trigger-evals.json).

---

## Sizing: how much design for how much work

Applying all four stages at full weight to a small change is this skill's failure mode.

| Job | Architecture | Art direction | Creativity | Drafting |
| --- | --- | --- | --- | --- |
| Tweak one screen in an existing system | — (inventory is known) | reuse the existing thesis | — | one annotated draft |
| New feature, 2–5 screens | flow + inventory | reuse, note any extension | 2–3 concepts, quick score | wireframe → one hi-fi screen |
| New product, site or brand | full IA + token tiers | full thesis | 3–5 concepts, full scorecard | wireframes → prototype → record |
| Illustration, poster, 3D scene | composition only | full thesis | 3–5 thumbnails | one rendered draft |

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
| An audit of the built result — contrast, dark mode, focus states | a UI-review skill (in this library, via the promethean-parthenon router) |
| Figma, Canva or Blender tool calls | that tool's own skill or MCP instructions — see [drafting](references/drafting.md) §Media |

---

## Operating rules

- **The target is never skipped, only sized.** One line of target for a one-screen tweak. Not zero.
- **Write the thesis before the palette.** A palette without a sentence behind it is a preference, and preferences lose every argument.
- **Diverge before you polish.** No concept gets hi-fi treatment until the scorecard has run.
- **Draft in the cheapest medium that answers the question.** ASCII answers "what goes where"; only a render answers "does this feel right".
- **Never claim a design passes a test you did not run.** "Accessible" means a checked contrast ratio, not an intention.
- **The record is written from the final draft**, not from memory of the concepts.
- **Stop after three rejected drafts of the same thing.** The thesis or the target is wrong, not the draft. Go back one stage and ask the lead one question.

---

## Bundled skills

This is an aggregator, like promethean-parthenon: every skill it links to travels with it as a verbatim copy under `bundled/`, so dropping this folder into a project brings the design cluster with it and nothing dangles. The copies are regenerated by `scripts/build-bundles.py` from the sources in the library's `muses/` folder — change the source, never the copy.

---

## When not to use this

- **The design already exists and needs building.** That is engineering; write the build target instead.
- **One component needs to look better.** A four-stage plan over a button is ceremony — open [frontend-design](bundled/frontend-design/SKILL.md) from the fast path instead.
- **Pure exploration or mood play.** Time-box it, skip the scorecard, and write the target afterward if something is worth keeping.
- **Software architecture** (services, data models, APIs). "Architecture" here means the architecture of a design.
