---
name: design:css-architecture
description: >-
  Scaffold and manage CSS file architecture for TailwindCSS-first projects. Use this skill whenever the user needs to organize CSS files, prevent or fix CSS hell, add custom styles alongside Tailwind, create a styles folder, set up structural design tokens, configure PostCSS for CSS imports, enforce CSS linting rules, migrate a messy stylesheet to a clean structure, or when CSS is growing out of control and causing conflicts. Trigger on any of these: "css structure", "css folder", "css hell", "css mess", "custom css with tailwind", "css organization", "css architecture", "stylesheet management", "css conflicts", "css specificity", or any request to set up, audit, fix, or improve CSS organization. Use this skill even when the user casually says "my CSS is getting messy" or "styles are conflicting" or "how should I organize my styles".
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: CSS Architecture / TailwindCSS best practices (compiled 2026)
---

# CSS Architecture Manager — Tailwind-First

Prevent CSS hell and manage scalable CSS file structure in projects where **TailwindCSS is primary** and custom CSS files play a deliberate supporting role. Focus: clear structure, zero conflicts, maintainability at scale.

This skill does NOT cover theming systems, dark mode, or multi-brand design tokens — it covers architectural concerns only.

---

## Step 0 — Intake (Always Do This First)

Before generating any file or advice, gather context silently (check files, don't always ask):

1. **Tailwind version** — read `package.json` → `tailwindcss` version. v3 and v4 have different `@import` patterns.
2. **Framework** — Vite, Next.js, Nuxt, CRA, or plain HTML. Affects PostCSS config needs.
3. **CSS Modules?** — If the project uses CSS Modules (`.module.css`), those files follow different rules and must NOT be placed inside `src/styles/`. Flag this to the user.
4. **Project state** — New project (scaffold mode) or existing project (audit + migration mode)?

**Default output mode:** When the user's intent is unclear, default to scaffold mode — produce: (1) recommended folder structure as a tree, (2) ready-to-use `main.css`, (3) starter `tokens/_root.css`. Always produce runnable code, not explanatory prose alone.

**When migrating:** Do not suggest rewriting everything at once. Follow the 3-phase migration plan in [[migration-guide]].

---

## The Golden Rule

> **If TailwindCSS can do it, use Tailwind. Custom CSS files are for things Tailwind cannot or should not do.**

| Styling Need | Use |
|---|---|
| Layout, spacing, colors, typography, responsive states | ✅ Tailwind utilities |
| Complex `@keyframes` animations | ✅ Custom CSS → `animations/` |
| Third-party library overrides | ✅ Custom CSS → `vendors/` |
| Structural CSS custom properties | ✅ Custom CSS → `tokens/` |
| Complex `::before` / `::after` content | ✅ Custom CSS → `components/` |
| Scroll-driven or complex CSS-only patterns | ✅ Custom CSS → `layouts/` |
| Anything Tailwind already provides | ❌ Never duplicate in CSS files |
| Rewriting Tailwind utilities with custom CSS | ❌ Never — use `@apply` sparingly instead |
| Using `!important` to win a specificity battle | ❌ Never — use `@layer` instead |

---

## Standard Folder Structure

```
src/
└── styles/                        ← Root CSS directory. Never put CSS files at project root.
    ├── tokens/
    │   └── _root.css              ← ALL CSS custom properties (structural tokens only)
    ├── base/
    │   ├── _reset.css             ← Minimal additions to Tailwind's preflight
    │   └── _typography.css        ← Base HTML element typographic rules
    ├── components/
    │   ├── _buttons.css           ← Component-level styles Tailwind can't handle
    │   ├── _forms.css             ← Input/autofill vendor overrides
    │   └── _[name].css            ← One file per component concern
    ├── layouts/
    │   └── _grid.css              ← Complex container/grid patterns
    ├── animations/
    │   └── _keyframes.css         ← ALL @keyframes live here, nowhere else
    ├── vendors/
    │   ├── _overrides.css         ← Third-party library style patches
    │   └── _vendor-map.md         ← Document: what library, why override, what the alternative is
    └── main.css                   ← Single entry point — imports everything in order
```

**File naming rules:**
- `_filename.css` = partial (never loaded directly, always imported by `main.css`)
- `main.css` = the only non-partial; one per project
- kebab-case for all filenames; no `styles.css`, no `global.css`, no `custom.css`
- One concern per file. If a file exceeds ~150 lines, that's a signal — not a hard rule — to split by sub-concern
- `@keyframes` never in component files. Always in `animations/_keyframes.css`

> For project-size variants (small / medium / large), see [[folder-templates]]

---

## CSS Cascade Layers — The Core Conflict Prevention Tool

`@layer` makes the cascade explicit. It eliminates specificity wars, removes the need for `!important`, and makes CSS predictable at scale.

**Always declare the full layer order at the very top of `main.css`:**
```css
@layer tokens, reset, base, components, layouts, utilities, vendors, overrides;
```

**Layer priority (lowest → highest):**
```
tokens → reset → base → components → layouts → utilities → vendors → overrides
```

Styles in a higher-priority layer always win, regardless of selector specificity. This means:
- A rule in `overrides` beats `components`, even with a simpler selector
- Unlayered CSS (not inside any `@layer`) beats everything — never leave CSS unlayered

**`main.css` — Tailwind v3:**
```css
@layer tokens, reset, base, components, layouts, utilities, vendors, overrides;

@tailwind base;
@tailwind components;
@tailwind utilities;

@import "./tokens/_root.css";
@import "./base/_reset.css";
@import "./base/_typography.css";
@import "./components/_buttons.css";
@import "./components/_forms.css";
@import "./animations/_keyframes.css";
@import "./vendors/_overrides.css";
```

**`main.css` — Tailwind v4:**
```css
@import "tailwindcss";

@import "./tokens/_root.css" layer(tokens);
@import "./base/_reset.css" layer(reset);
@import "./base/_typography.css" layer(base);
@import "./components/_buttons.css" layer(components);
@import "./animations/_keyframes.css";
@import "./vendors/_overrides.css" layer(vendors);
```

**Each partial declares its layer (v3 pattern):**
```css
/* components/_buttons.css */
@layer components {
  .btn-icon-only {
    aspect-ratio: 1;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--radius-md);
    transition: opacity var(--duration-fast) var(--ease-out);
  }
}
```

> For `@layer` deep dive, common mistakes, and v3/v4 specificity charts, see [[layer-system]]

---

## Structural Design Tokens — `tokens/_root.css`

Tokens belong here if they are **structural** (spacing, sizing, radius, animation, z-index, shadow). Color and theme tokens are out of scope for this skill.

All tokens live in `:root` inside `@layer tokens`. Components reference them via `var()` — never hardcode values.

```css
/* tokens/_root.css */
@layer tokens {
  :root {
    /* === SPACING === */
    --space-1: 0.25rem;   /* 4px */
    --space-2: 0.5rem;    /* 8px */
    --space-3: 0.75rem;   /* 12px */
    --space-4: 1rem;      /* 16px */
    --space-6: 1.5rem;    /* 24px */
    --space-8: 2rem;      /* 32px */
    --space-12: 3rem;     /* 48px */
    --space-16: 4rem;     /* 64px */

    /* === BORDER RADIUS === */
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 1rem;
    --radius-full: 9999px;

    /* === Z-INDEX SCALE (prevents z-index arms races) === */
    --z-base:    0;
    --z-raised:  10;    /* cards, dropdowns */
    --z-sticky:  100;   /* sticky headers */
    --z-overlay: 200;   /* backdrops */
    --z-modal:   300;   /* modals, drawers */
    --z-popover: 400;   /* tooltips, popovers */
    --z-toast:   500;   /* notifications */

    /* === ANIMATION === */
    --duration-fast:   150ms;
    --duration-base:   250ms;
    --duration-slow:   400ms;
    --ease-out:        cubic-bezier(0.0, 0, 0.2, 1);
    --ease-spring:     cubic-bezier(0.34, 1.56, 0.64, 1);

    /* === SHADOWS === */
    --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.06);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1), 0 4px 6px rgba(0,0,0,0.05);

    /* === COMPONENT TOKENS === */
    /* Per-component structural values — prevents hardcoded values inside component files */
    --btn-height-sm:  2rem;
    --btn-height-md:  2.5rem;
    --btn-height-lg:  3rem;
    --btn-padding-x:  1rem;
    --input-height:   2.5rem;
    --input-radius:   var(--radius-md);
    --card-padding:   var(--space-6);
    --card-radius:    var(--radius-lg);
  }
}
```

**Token naming rules:**
- Follow Tailwind's scale for spacing: 1 = 0.25rem, 2 = 0.5rem, 4 = 1rem
- If a value appears in more than two component files, make it a token
- `--component-property` format for component tokens (e.g. `--btn-height-md`, `--card-padding`)
- Never use raw `px`/`rem` values inside component files — always `var(--token)`

---

## Tailwind Config Alignment

Tailwind utilities and custom CSS tokens must reference the same values. Otherwise `gap-4` (1rem) and `var(--space-4)` (1rem) are maintained separately and will drift.

```js
// tailwind.config.js — reference CSS variables, don't duplicate values
module.exports = {
  theme: {
    extend: {
      spacing: {
        // Map Tailwind's spacing scale to CSS variables
        'sm': 'var(--space-2)',
        'md': 'var(--space-4)',
        'lg': 'var(--space-8)',
      },
      borderRadius: {
        'sm': 'var(--radius-sm)',
        'md': 'var(--radius-md)',
        'lg': 'var(--radius-lg)',
      },
      transitionDuration: {
        'fast': 'var(--duration-fast)',
        'base': 'var(--duration-base)',
      },
      zIndex: {
        'sticky': 'var(--z-sticky)',
        'modal':  'var(--z-modal)',
        'toast':  'var(--z-toast)',
      },
      boxShadow: {
        'sm': 'var(--shadow-sm)',
        'md': 'var(--shadow-md)',
        'lg': 'var(--shadow-lg)',
      },
    },
  },
}
```

This way `rounded-lg` and `var(--radius-lg)` always resolve to the same value. Change the token once, both Tailwind and custom CSS update.

---

## Workflow — Adding New Styles

Follow this decision tree silently — do not surface it as a series of questions to the user. Execute and produce the correct file.

```
Can Tailwind utilities achieve this in the HTML?
├── YES → Use Tailwind classes. Stop.
└── NO ↓
    Is this a repeated raw value (spacing, radius, z-index, animation)?
    ├── YES → Add to tokens/_root.css as @layer tokens. Reference via var(). Stop.
    └── NO ↓
        Is this a @keyframes animation?
        ├── YES → Add ONLY to animations/_keyframes.css (outside any @layer). Stop.
        └── NO ↓
            Is this overriding a third-party library?
            ├── YES → Add to vendors/_overrides.css as @layer vendors. Document in _vendor-map.md. Stop.
            └── NO ↓
                Is this a base HTML element style?
                ├── YES → Add to base/_typography.css or base/_reset.css as @layer base. Stop.
                └── NO → Add to appropriate components/ or layouts/ file as @layer components.
```

---

## PostCSS Setup (Required for v3 `@import`)

Tailwind v3 does not resolve `@import` natively. Without `postcss-import`, your `main.css` imports will silently fail.

```bash
npm install -D postcss-import
```

```js
// postcss.config.js
module.exports = {
  plugins: [
    require('postcss-import'),   // must come FIRST — resolves @import before Tailwind
    require('tailwindcss'),
    require('autoprefixer'),
  ],
}
```

Tailwind v4 uses native CSS `@import` resolution via Lightning CSS — no `postcss-import` needed.

> **CSS Modules note:** If the project uses CSS Modules (`.module.css` files), those are component-scoped and follow different rules. They must NOT be placed inside `src/styles/`. CSS Modules and the `src/styles/` architecture coexist without conflict — they serve different purposes.

---

## Anti-Patterns Quick Reference

| ❌ Anti-Pattern | ✅ Fix |
|---|---|
| `!important` anywhere except vendors/ | Use `@layer` to control cascade priority |
| Selectors nested 4+ levels deep | Flatten — max 2 levels in custom CSS |
| Hardcoded `px`/`rem` in component files | Use `var(--token-name)` |
| `@keyframes` scattered across component files | Consolidate in `animations/_keyframes.css` |
| `z-index: 9999` without a scale | Define `--z-modal`, `--z-toast` etc. in tokens |
| One large `styles.css` file | Split by concern — one file per responsibility |
| CSS rules not inside any `@layer` | Always layer custom CSS; unlayered CSS beats everything |
| `@apply` used heavily (10+ times) | Compose utilities in HTML instead |
| Duplicate Tailwind utilities in CSS | Remove — use Tailwind classes directly |
| Third-party overrides without documentation | Add to `_vendor-map.md` explaining why |

> For detailed before/after examples of all 10 patterns, see [[anti-patterns]]

---

## QA Validation Checklist

**Structure:**
- [ ] All custom CSS lives inside `src/styles/` — no stray `.css` files elsewhere
- [ ] `main.css` is the single entry point; no other file is imported directly by the app
- [ ] File names use kebab-case and `_` prefix for partials
- [ ] No file named `custom.css`, `global.css`, or `styles.css`

**Layers:**
- [ ] `@layer` order declared at the very top of `main.css`
- [ ] Every custom rule is wrapped in an `@layer` block
- [ ] No unlayered CSS in any partial file
- [ ] `!important` appears only in `vendors/_overrides.css`

**Tokens:**
- [ ] All `px`/`rem` values in component files use `var(--token)`
- [ ] No hardcoded values repeated across 2+ component files
- [ ] `animations/_keyframes.css` is the only file containing `@keyframes`

**Tailwind alignment:**
- [ ] `tailwind.config.js` references CSS variables (not duplicate raw values)
- [ ] No CSS file replicates what a Tailwind utility already does
- [ ] `@apply` used sparingly (5 or fewer uses project-wide is a soft limit)

**Linting (automated):**
- [ ] Stylelint configured and passing
- [ ] `max-nesting-depth: 2` rule active
- [ ] `declaration-no-important` rule active (with vendor exception)
- [ ] `no-duplicate-selectors` rule active

> For Stylelint setup and `.stylelintrc` config, see [[linting-setup]]

---

## Success Metrics

A well-structured CSS codebase should achieve:

| Metric | Target |
|---|---|
| `!important` count outside vendors/ | 0 |
| Hardcoded hex/px values in component files | 0 |
| CSS files outside `src/styles/` | 0 |
| Selector nesting depth | ≤ 2 |
| `@keyframes` not in `animations/_keyframes.css` | 0 |
| Stylelint errors on CI | 0 |
| File count > 150 lines without a documented reason | 0 |

---

## Reference Files

| File | Read When |
|---|---|
| [[folder-templates]] | Scaffolding a new project or choosing structure size |
| [[layer-system]] | Debugging specificity conflicts or learning `@layer` |
| [[anti-patterns]] | Auditing existing CSS or diagnosing CSS hell |
| [[linting-setup]] | Setting up Stylelint for automated enforcement |
| [[migration-guide]] | Migrating an existing messy codebase incrementally |
| `assets/main.css.template` | Starter `main.css` ready to copy into a project |
