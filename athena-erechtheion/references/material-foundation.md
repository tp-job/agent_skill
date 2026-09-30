# Material foundation — M3 as the system, the brand as the expression

Material 3 has two layers, and they are worth separating on purpose:

- a **system layer**: token tiers, surfaces, state, accessibility and motion physics. Nobody sees it, and everybody benefits from it.
- an **expression layer**: colour, shape, type and imagery. This is the part people recognise as "a Google app".

Adopt the first by default. Tune the second to the thesis. That is how a design gets Material's rigour without Material's face.

Component specs, research and motion detail live in the specialist. This file is the workflow on top of it: [google-design-system](../bundled/google-design-system/SKILL.md) · [M3 Expressive](../bundled/google-design-system/references/material-3-expressive.md) · [motion](../bundled/google-design-system/references/motion-design.md) · [accessibility](../bundled/google-design-system/references/global-accessibility.md).

**Versions:** this file targets Material 3 with the Expressive update (2025). Platform support differs:

| Platform | Support |
| --- | --- |
| Jetpack Compose `material3` | fullest support, including Expressive |
| Flutter | M3 by default |
| Web | Material Web (`@material/web`) is in maintenance mode, and MUI's defaults lean M2 |

On the web, plan to implement the tokens yourself. Check current library status before committing to one.

---

## 1. The system decision (Stage 0)

Write this down alongside the design target. One line.

| Decision | Choose when | You get |
| --- | --- | --- |
| **Full M3** | an Android app, a Google-ecosystem product, or a team that wants stock components and speed | M3 components as shipped, a dynamic colour scheme, stock motion |
| **M3 foundation** (default for web and brand work) | you want Material's rigour but a distinctive look | M3 token tiers, surfaces, state layers, a11y rules and motion physics, with the brand's own expression layer |
| **None** | a strong existing design system already answers these questions | cite that system and skip this file |

**BAD:** "Use Material Design." This doesn't say which layer, so the draft ends up looking like Gmail.
**BETTER:** "M3 foundation: sys-token names, tonal surfaces, state layers, 48 dp targets and spring motion. Expression per the thesis: neutral scheme, pill actions, and our display face."

---

## 2. What is fixed and what is yours

| Fixed. Keep these even in "M3 foundation" | Yours. Tune them to the thesis |
| --- | --- |
| Token tiers: `ref` → `sys` → `comp` | the seed colour and scheme variant (tonal spot, neutral, monochrome, fidelity, expressive…) |
| Colour roles in pairs: `primary`/`on-primary`, `surface`/`on-surface` | the typeface: M3 names the *roles* (display, headline, title, body, label), not the font |
| Depth comes from tonal surface containers (`surface-container-lowest` … `highest`) before shadow | the shape scale: from sharp to fully round, and where each shape is used |
| State layers: an overlay on hover, focus, pressed and dragged | the imagery: its treatment, masks and grade |
| Targets ≥ 48×48 dp, contrast ≥ 4.5:1 for body text and ≥ 3:1 for large text and UI | the motion scheme: *standard* (calm) or *expressive* (bouncy), and where each applies |
| Motion is physics-based (springs), never linear, and always has a `prefers-reduced-motion` path | grid, density and whitespace |

Everything in the left column is invisible and protects users. Everything in the right column is visible and belongs to the brand.

---

## 3. The four stages on an M3 foundation

| Stage | What changes |
| --- | --- |
| **Architecture** | Your token tiers are M3's: `ref` (raw palette), `sys` (roles), `comp` (per-component). Name the sys tokens with M3 role names so any M3 tooling still works. |
| **Art direction** | The thesis picks each expression lever with a reason: the scheme variant, shape family, type pairing and motion scheme. One of the three "never" rules must protect a fixed item, for example "never remove the focus state layer". |
| **Creativity** | Concepts differ by **lever combinations** (§4). The invariants stay identical across every concept, so scoring compares ideas, not rule-breaking. |
| **Drafting** | In Figma, start from the M3 Design Kit and generate the scheme with Material Theme Builder. In code, generate it with `@material/material-color-utilities` and map it into Tailwind `@theme` (§6). |

---

## 4. Expression levers for divergent concepts

Use these on top of the levers in [creative-process](creative-process.md). Each concept picks a different setting on at least two rows.

| Lever | Quiet end | Expressive end |
| --- | --- | --- |
| Scheme variant | monochrome / neutral | vibrant / expressive |
| Shape | small radius, sharp containers | full pills, morphing shapes, blob masks |
| Type emphasis | one weight, a modest scale | an emphasized display style, a huge scale jump |
| Motion scheme | standard springs, short | expressive springs, overshoot on the hero moment |
| Surface | flat tonal containers | layered containers with imagery behind them |

**BAD:** three concepts that differ only in seed colour.
**BETTER:** "Gallery" (monochrome, sharp, quiet motion), "Studio" (neutral, pill actions, one expressive hero), "Playground" (vibrant, morphing shapes, expressive throughout). Score them against the thesis.

---

## 5. Recipe: "Quiet Material", elegant and modern

This is the house default when the thesis asks for refined and contemporary. It is the pattern shared by premium editorial sites, rebuilt on M3 rules.

| Lever | Setting | Why it reads as refined |
| --- | --- | --- |
| Scheme | a neutral or monochrome variant, with **one** accent (put it on the `tertiary` role) reserved for the primary action | colour becomes rare, so it becomes meaningful |
| Depth | tonal surface containers plus 1 px `outline-variant` dividers, with shadow only on the few elements that really float | depth without visual noise |
| Shape | `full` (pill) for actions and chips, `extra-large` for media containers, small radius elsewhere | a curve marks what is touchable or special |
| Type | a display role at a large scale jump, tight tracking, used once per screen; everything else at the body and label roles | hierarchy survives a squint test |
| Motion | the standard scheme everywhere, and the expressive spring **only** on the hero moment (one per page) | playful exactly once, so it is remembered |
| Space | 8 dp base, generous section padding | whitespace carries the hierarchy |

**When not to use it:** products for kids or games, or any brand whose thesis is energy and play. There, "Quiet" reads as cold, so move the levers to the expressive end.

---

## 6. M3 tokens in Tailwind v4

Keep the M3 role names so the mapping stays obvious. Generate the hex values from the seed. Don't hand-pick them.

```css
@theme {
  --color-primary: #1f1f1f;          /* sys.color.primary (monochrome scheme) */
  --color-on-primary: #ffffff;
  --color-surface: #fbfbf9;
  --color-surface-container: #f0f0ee;
  --color-surface-container-high: #e8e8e6;
  --color-on-surface: #1b1c1b;
  --color-on-surface-variant: #474746;
  --color-outline-variant: #c8c7c4;
  --color-tertiary: #e8453c;         /* the one reserved accent, on an M3 role: primary action only */
  --radius-extra-large: 28px;        /* M3 extra-large → rounded-extra-large */
}
```

**Name new radii after M3, not after Tailwind's scale.** `--radius-xl: 28px` looks equivalent, but it silently redefines every `rounded-xl` already in the project (Tailwind's is 12 px). Pills need nothing new, because `rounded-full` already exists.

```html
<!-- Button with an M3 state layer: overlay on hover/focus/press, 48px target -->
<button class="relative min-h-12 rounded-full bg-primary px-6 text-on-primary
  after:absolute after:inset-0 after:rounded-full after:bg-on-primary after:opacity-0
  hover:after:opacity-[0.08] focus-visible:after:opacity-[0.10] active:after:opacity-[0.10]
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary">Book a demo</button>
```

For motion on the web, use spring transitions in Motion (`type: "spring"`) rather than duration and easing pairs, and gate them with `useReducedMotion`.

---

## Check before handing on

- [ ] The system decision is written: full, foundation, or none
- [ ] Sys tokens use M3 role names, and every colour role has its `on-` pair
- [ ] Contrast is checked on each `on-` pair, with the ratio recorded
- [ ] Targets are ≥ 48 dp, and every interactive element has visible state layers and a focus ring
- [ ] Every expression lever has a reason that points back at the thesis
- [ ] Motion uses springs and has a reduced-motion path; expressive motion is limited to named moments
