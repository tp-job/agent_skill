# Folder Structure Templates

Three sizes. Start smaller than you think you need — it's easy to expand, hard to consolidate.

> **CSS Modules note:** Files ending in `.module.css` are component-scoped and do NOT belong in `src/styles/`. CSS Modules and the `src/styles/` architecture coexist without conflict.

---

## Small — Landing page, portfolio, micro-app

```
src/
└── styles/
    ├── tokens/
    │   └── _root.css          ← Structural tokens (spacing, radius, z-index, animation)
    ├── base/
    │   └── _typography.css    ← Base HTML element styles
    ├── components/
    │   └── _ui.css            ← All component styles (combined OK at this scale)
    ├── animations/
    │   └── _keyframes.css     ← Only if animations exist; omit if not
    └── main.css               ← Entry point
```

**main.css (small project):**
```css
@layer tokens, reset, base, components, utilities;

@tailwind base;
@tailwind components;
@tailwind utilities;

@import "./tokens/_root.css";
@import "./base/_typography.css";
@import "./components/_ui.css";
/* @import "./animations/_keyframes.css"; */
```

---

## Medium — App, dashboard, multi-page site

```
src/
└── styles/
    ├── tokens/
    │   └── _root.css
    ├── base/
    │   ├── _reset.css
    │   └── _typography.css
    ├── components/
    │   ├── _buttons.css
    │   ├── _forms.css
    │   ├── _cards.css
    │   ├── _modals.css
    │   └── _navigation.css
    ├── layouts/
    │   ├── _grid.css
    │   └── _sidebar.css
    ├── animations/
    │   ├── _keyframes.css
    │   └── _transitions.css
    ├── vendors/
    │   ├── _overrides.css
    │   └── _vendor-map.md     ← Document every override: what, why, alternative
    └── main.css
```

**main.css (medium project):**
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
@import "./components/_cards.css";
@import "./components/_modals.css";
@import "./components/_navigation.css";

@import "./layouts/_grid.css";
@import "./layouts/_sidebar.css";

@import "./animations/_keyframes.css";
@import "./animations/_transitions.css";

@import "./vendors/_overrides.css";
```

---

## Large — Design system, enterprise app, multi-product

```
src/
└── styles/
    ├── tokens/
    │   └── _root.css              ← All structural tokens (never split this file)
    ├── base/
    │   ├── _reset.css
    │   ├── _typography.css
    │   └── _focus.css             ← Focus ring / keyboard nav standards
    ├── components/
    │   ├── _buttons.css
    │   ├── _forms.css
    │   ├── _inputs.css
    │   ├── _checkboxes.css
    │   ├── _selects.css
    │   ├── _cards.css
    │   ├── _badges.css
    │   ├── _alerts.css
    │   ├── _modals.css
    │   ├── _drawers.css
    │   ├── _tooltips.css
    │   ├── _dropdowns.css
    │   ├── _navigation.css
    │   ├── _tabs.css
    │   └── _tables.css
    ├── layouts/
    │   ├── _grid.css
    │   ├── _sidebar.css
    │   ├── _header.css
    │   └── _containers.css
    ├── patterns/
    │   ├── _auth.css              ← Use only when 3+ components share unique page-level styles
    │   └── _dashboard.css
    ├── animations/
    │   ├── _keyframes.css
    │   ├── _transitions.css
    │   └── _scroll.css            ← Scroll-driven animations (CSS @scroll-timeline)
    ├── vendors/
    │   ├── _overrides.css
    │   └── _vendor-map.md
    └── main.css
```

---

## Splitting Rules

When a component file exceeds ~150 lines:
```
Before:                          After:
components/                      components/
└── _forms.css (220 lines)       ├── _forms.css (base vars + shared)
                                 ├── _forms-inputs.css
                                 └── _forms-selects.css
```

When to create a `patterns/` file:
- 3+ component files share styles that only make sense in a specific page context
- A feature has its own visual language distinct from the design system
- The component files would need to import from each other without a pattern layer

When NOT to create `patterns/`:
- You're trying to avoid splitting a large component file (split it instead)
- The styles could live in the component file with a modifier class
