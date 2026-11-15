# Category 5 — Accessibility and color (WCAG 2.2 AA)

## Contents

- Which WCAG version
- Contrast: the formula and thresholds
- Color must not carry meaning alone
- NFR catalogue
- Tools
- Method for a whole site (WCAG-EM)

---

## Which WCAG version

Use **WCAG 2.2** (W3C Recommendation, October 2023). It contains every 2.1 criterion except 4.1.1 Parsing, which is now obsolete, and adds criteria that matter for data-entry apps: **2.4.11 Focus Not Obscured (Minimum)**, **2.5.8 Target Size (Minimum)**, **3.3.7 Redundant Entry** and **3.3.8 Accessible Authentication (Minimum)**. Level **AA** is the usual contractual and legal target.

If a document already cites 2.1, switch every mention to 2.2 at once. Do not mix the two versions.

## Contrast: the formula and thresholds

Contrast ratio = (L1 + 0.05) / (L2 + 0.05), where L1 is the relative luminance of the lighter color and L2 that of the darker one. The ratio runs from 1:1 to 21:1.

Relative luminance L = 0.2126 R + 0.7152 G + 0.0722 B, computed on linearised sRGB channels. For each channel c in 0–1: c ≤ 0.04045 → c / 12.92, else ((c + 0.055) / 1.055) ^ 2.4. WCAG 2.x's text uses an older 0.03928 cutoff; the difference never changes a result at 8-bit precision.

| What | AA | AAA | SC |
| --- | --- | --- | --- |
| Body text | ≥ 4.5:1 | ≥ 7:1 | 1.4.3 / 1.4.6 |
| Large text (≥ 24 px, or ≥ 18.66 px bold) | ≥ 3:1 | ≥ 4.5:1 | 1.4.3 / 1.4.6 |
| UI components and meaningful graphics: input borders, icons, chart lines and bars, status badges, focus indicators | ≥ 3:1 against adjacent colors | — | 1.4.11 |
| Disabled controls, pure decoration, logos | exempt | exempt | 1.4.3 |

Reference point: `#767676` on `#FFFFFF` is 4.54:1, which is the lightest grey that passes AA for body text on white.

Run `scripts/contrast_check.py` over every foreground/background pair in the design tokens and in **each theme**. Dark mode is a separate set of pairs and must be checked separately.

## Color must not carry meaning alone

SC 1.4.1 Use of Color. Traffic-light status (green/amber/red), charts that identify series only by color, and red-only error borders all fail this criterion.

BAD: risk status shown as a red, yellow or green dot.
BETTER: the dot plus a text label ("High risk") and a distinct icon shape. Chart series get direct labels or different line styles.

Then check it under simulation in Chrome DevTools: Rendering → Emulate vision deficiencies, using protanopia, deuteranopia, tritanopia and achromatopsia. Every status must stay distinguishable. Red-green deficiency affects roughly 8% of men of Northern European descent and fewer women (Birch, 2012).

## NFR catalogue

| ID | Statement | Must | SC |
| --- | --- | --- | --- |
| AX-01 | Body text contrast | ≥ 4.5:1 in every theme | 1.4.3 |
| AX-02 | Large text contrast | ≥ 3:1 | 1.4.3 |
| AX-03 | Non-text contrast: borders, icons, chart marks, status badges, focus ring | ≥ 3:1 | 1.4.11 |
| AX-04 | Meaning never by color alone | every status has text or icon; charts labelled | 1.4.1 |
| AX-05 | Color-vision simulation | all statuses distinguishable under 4 simulations | 1.4.1 |
| AX-06 | Token pair table | every pair passes AX-01–03 (appendix table) | 1.4.3, 1.4.11 |
| AX-07 | Full keyboard operation | every core task completed without a mouse; no keyboard trap | 2.1.1, 2.1.2 |
| AX-08 | Visible, unobscured focus | focus ring visible, not hidden by sticky header or modal | 2.4.7, 2.4.11 |
| AX-09 | Logical focus order | tab order follows visual reading order | 2.4.3 |
| AX-10 | Target size | ≥ 24 × 24 CSS px or sufficient spacing | 2.5.8 |
| AX-11 | Text resize | 200% zoom, no loss or overlap | 1.4.4 |
| AX-12 | Reflow | usable at 320 CSS px width without 2-D scrolling (data tables exempt) | 1.4.10 |
| AX-13 | Page language | `<html lang="…">` correct (e.g. `th`) | 3.1.1 |
| AX-14 | Structure | tables use `<th>`/`scope`; inputs have labels | 1.3.1, 3.3.2 |
| AX-15 | Errors identified with a fix | names field or row, cause, and how to fix | 3.3.1, 3.3.3 |
| AX-16 | Status messages announced | toasts and "saved" use `role="status"` / `aria-live` | 4.1.3 |
| AX-17 | Automated scan | axe: 0 critical/serious; Lighthouse Accessibility ≥ 90 on key pages | — |
| AX-18 | Screen reader pass | core tasks completed with NVDA (Windows) or VoiceOver (macOS/iOS) | — |

## Tools

| Tool | Checks |
| --- | --- |
| `scripts/contrast_check.py` | all token pairs at once, AA and AAA |
| WebAIM Contrast Checker | a single pair, by hand |
| Chrome DevTools → Inspect → contrast | the computed pair on the live element |
| axe DevTools / `@axe-core/playwright` | automated WCAG rules; fail CI on serious |
| Lighthouse Accessibility | subset of axe rules, scored |
| Chrome DevTools → Rendering → Emulate vision deficiencies | AX-05 |
| NVDA (free, Windows) | AX-18 |

Automated tools catch only part of WCAG. Focus order, whether error text is useful, and color-only meaning in images need a person.

## Method for a whole site (WCAG-EM)

W3C's WCAG-EM 1.0 gives the evaluation method in five steps:

1. Define the scope and target (2.2 AA).
2. Explore the site to find the key pages and functions.
3. Select a sample: every core task, every page template, and a random sample of other pages.
4. Audit the sample against each criterion.
5. Report the results per criterion.

A thesis or report should cite this as its method.
