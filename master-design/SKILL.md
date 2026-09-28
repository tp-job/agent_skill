---
name: master-design
description: >-
  Runs a whole design job from a one-line ask to a handoff-ready draft, in four disciplines taken
  in order: architecture (information architecture, screen inventory, design-system token
  structure), art direction (a written visual thesis, mood, palette and type rationale), creativity
  (divergent concepts under stated constraints, then a scored convergence), and drafting
  (wireframes, diagrams, spec drafts and prototypes in the cheapest medium that answers the open
  question — paper-grade ASCII, HTML, Figma, Canva or Blender). Built on the Promethean-Parthenon
  Role · Task · Format doctrine: set the design seat, write the design target before drawing, land a
  design record. Use when starting a new product, site, brand or scene and unsure where the design
  work begins; when several design skills could apply and the job needs one plan; when a design
  keeps getting redone; or when asked "design this from scratch", "art direction for", "give me
  concepts", "wireframe this", "draft the layout", "what should this look like", "design system
  structure", "moodboard", "ออกแบบทั้งระบบ", "ช่วยคิดคอนเซปต์ดีไซน์". Not for polishing the
  aesthetics of one component (frontend-design), applying Material or Google rules
  (google-design-system), organising CSS files (css-architecture), auditing a built UI for contrast
  or dark-mode bugs, 3D scene code, or software/system architecture.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: >-
    Promethean-Parthenon Role · Task · Format doctrine applied to design practice; information
    architecture, art-direction and double-diamond ideation methods (compiled 2026)
---

# Master Design

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

This skill plans and drafts. When a stage needs deeper craft and the matching skill is installed, hand that stage over and keep the plan here. These are mentions, not dependencies — every stage works without them.

| The stage needs… | Hand to (if installed) |
| --- | --- |
| A distinctive visual identity for one page or component | the frontend-design skill |
| Material 3 / Google design conformance | the google-design-system skill |
| Tailwind-first CSS file and token layout | the css-architecture skill |
| A 3D scene in three.js | the threejs-3d skill |
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

## When not to use this

- **The design already exists and needs building.** That is engineering; write the build target instead.
- **One component needs to look better.** A four-stage plan over a button is ceremony — use a visual-identity skill directly.
- **Pure exploration or mood play.** Time-box it, skip the scorecard, and write the target afterward if something is worth keeping.
- **Software architecture** (services, data models, APIs). "Architecture" here means the architecture of a design.
