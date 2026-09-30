# Reference analysis — deconstructing a screenshot

A reference is only useful once it has been turned into decisions you can reuse. This file is the teardown method for "analyse this website screenshot", "what style is this?", "how would I build this?". It feeds the moodboard in [art-direction](art-direction.md) and can also run on its own as a study exercise.

---

## 0. Rules before the six sections

| Rule | BAD | BETTER |
| --- | --- | --- |
| **Every claim points at a pixel.** Name the element that proves it. | "It feels premium." | "Premium: 80 px display type over ~70% whitespace, one CTA per viewport." |
| **Separate seen from guessed.** A still image shows no motion. Label every interaction claim as *inferred*, and say what cue it was inferred from. | "The cards animate on scroll." | "Inferred: the marquee row of logos is cut off mid-word at the edge, which cues a horizontal ticker." |
| **Colours are estimates.** Sample by eye, write them as hex, and mark them `~`. JPEG/WebP compression shifts colour. | "#E63946" (stated as fact) | "~#E8453C (sampled from a compressed image — confirm against the source)" |
| **Name fonts by class, not by guess.** Only name a specific typeface when its tells are visible (e.g. single-storey `a`, Futura's pointed `A`). | "They use Inter." | "Neo-grotesk sans, tight tracking at display size, likely Inter/Manrope/Neue Montreal class." |
| **Name styles by trait, not by label.** Labels like "Bento" or "Glassmorphism" are shorthand and people disagree on them. Always list the traits that earn the label. | "It's Bento." | "Bento-like: asymmetric tiles on one grid, 1 px dividers, each tile one idea." |
| **End in tokens and classes.** Adjectives cannot be built. The teardown is finished only when section 6 can be pasted into a project. | "Use soft shadows." | "`shadow-[0_1px_2px_rgb(0_0_0/0.04)]`, `rounded-3xl`" |

When there are several screenshots, analyse each one briefly, then write **one comparison table**. Contrast between references teaches more than any single description.

---

## 1. Visual style & concept

Give a primary style, a secondary influence, and the 3–5 traits that justify each.

| Style | Visible traits that earn the label |
| --- | --- |
| Swiss / International | strict column grid, flush-left sans, large numerals, hairline rules, colour used sparingly |
| Minimalist editorial | whitespace carries the hierarchy, few elements per viewport, oversized headline, restrained palette |
| Bento grid | tiles of mixed sizes on one grid, a 1 px gap or divider, one idea per tile |
| Glassmorphism | a translucent panel, `backdrop-blur` over a busy or colourful layer, a 1 px light border |
| Brutalism | raw default-looking elements, heavy borders, clashing type, visible structure, no polish |
| Neo-brutalism | brutalist structure plus flat saturated fills and hard offset shadows (`4px 4px 0 #000`) |
| Organic / blob | superellipse or blob masks, circles cropping photography, soft curves against a rigid grid |
| Cinematic / immersive | a full-bleed photo or video hero, dark or saturated tone, type set over the image |

**Close with the concept, meaning why this style suits this subject.** For example: a medical-robotics brand borrows lab-white and clinical order to signal precision.

---

## 2. Colour palette & atmosphere

| Role | Record |
| --- | --- |
| Background | the surface colour plus any second surface (cards, alternate sections) |
| Primary | the colour that carries the most ink: text and structure |
| Secondary | supporting neutrals: muted text, dividers, borders |
| Accent / CTA | the one colour that says "act here". Note how rare it is. |
| Imagery tone | a photo grade is part of the palette: warm/cool, saturation, duotone |

Then give the **proportion**, as a rough 60-30-10 split, and the **mood**, in two or three words tied to evidence.

**Check contrast on anything you plan to reuse.** Write the ratio down (WCAG 2.2 AA: 4.5:1 body text, 3:1 large text and UI). Grey-on-white captions in references often fail, so don't copy that.

---

## 3. Typography & hierarchy

| Record | How |
| --- | --- |
| Classification | geometric sans / neo-grotesk / humanist sans / serif / mono / display |
| Pairing | how many families, and which role each plays |
| Scale | estimate the display : heading : body sizes and the ratio between steps |
| Treatment | case (ALL CAPS labels?), tracking (tight display, wide caps), weight contrast, line-height |
| Hierarchy levels | list levels 1→4 with an example string from the image |

**Test the hierarchy with a squint:** blur the image mentally. Whatever is still readable is levels 1–2. If more than three things survive, the hierarchy is flat.

---

## 4. Layout & grid

| Record | How |
| --- | --- |
| Grid | column count, gutters, whether elements snap to it or break it on purpose |
| Section rhythm | the order of sections and how each is separated (rule, colour band, whitespace) |
| Spacing | the base unit you infer (4/8 px), section padding, card padding |
| Composition | symmetry, the focal point per section, how the eye moves (Z, F, centre-out) |
| Grid-breakers | the deliberate violations: bleeding images, overlapping circles, oversized type |
| Responsive guess | how the grid would collapse at 375 px. This is *inferred*, so say so. |

---

## 5. UI components & interaction

List each component with its **shape, fill, border, shadow and radius**: buttons, pills and tags, cards, navigation, media masks, stat blocks, sliders, tickers.

Then list the interactions and cite the cue for each. All of these are *inferred* from a still image:

| Cue in the screenshot | Likely interaction |
| --- | --- |
| text cut off at the viewport edge in a repeating row | marquee or ticker |
| an arrow icon in a circle | hover rotate/translate, or a link out |
| prev/next arrows, pagination dots | carousel or slider |
| a tab row with dimmed siblings and numbered labels | tab switch, often with a content crossfade |
| a large image in a mask | scroll-linked reveal or parallax |
| a translucent panel over a photo | backdrop blur, sometimes a pointer-tracked highlight |
| stat numbers | count-up on entering the viewport |
| progress bars | fill animation on entering the viewport |

---

## 6. Technical implementation

Choose tools for the effects you actually observed, not by default.

| Effect | Reach for | Not for |
| --- | --- | --- |
| layout, tokens, utilities | Tailwind CSS v4 (`@theme` tokens) | — |
| accessible primitives (tabs, dialog, menu) | shadcn/ui or Radix | a static marketing page with no widgets |
| enter/exit, hover, layout transitions | Motion (formerly Framer Motion) | a scroll-scrubbed timeline |
| scroll-scrubbed timelines, pinning | GSAP + ScrollTrigger | simple fade-ins (CSS/Motion suffices) |
| smooth scroll | Lenis | anything where native scroll is fine |
| a marquee | CSS `@keyframes` translate + a duplicated track | a JS library |
| blob and superellipse masks | SVG `clipPath` or CSS `mask-image` | a PNG cut-out |
| real 3D (rotating product, shaders) | three.js / R3F: open the threejs-3d specialist | a photo of a 3D render, which is only an image |
| charts that look designed | hand-drawn SVG or Recharts, styled | default chart themes |

Finish with a **token block and five to ten key utility classes**. Keep it short: the handful that recreate the look, not a whole page.

```css
@theme {
  --color-surface: #f4f4f2;
  --color-ink: #0b0b0c;
  --color-accent: #e8453c;
  --radius-pill: 9999px;
  --font-display: "Neue Montreal", ui-sans-serif, sans-serif;
}
```

**When not to go this deep:** someone asks "what's this style called?" in passing. Answer sections 1–2 in three lines and offer the rest.

---

## Check before handing on

- [ ] Every style label has its traits listed
- [ ] Every colour is marked `~` and given a role
- [ ] Every interaction claim is labelled *inferred*, with its cue
- [ ] Contrast has been checked on any colour pair you recommend reusing
- [ ] Section 6 ends in tokens and classes, not adjectives
- [ ] Several references means one comparison table
