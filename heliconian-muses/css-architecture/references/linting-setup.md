# Stylelint Setup — Automated CSS Enforcement

Stylelint turns the QA checklist into CI failures. Rules catch violations that code review misses.

---

## Install

```bash
npm install -D stylelint stylelint-config-standard stylelint-order
```

---

## `.stylelintrc.json`

```json
{
  "extends": ["stylelint-config-standard"],
  "plugins": ["stylelint-order"],
  "rules": {

    "max-nesting-depth": 2,

    "declaration-no-important": [true, {
      "message": "Use @layer to control cascade priority instead of !important"
    }],

    "no-duplicate-selectors": true,

    "no-descending-specificity": true,

    "color-no-invalid-hex": true,

    "selector-id-pattern": null,
    "selector-class-pattern": "^[a-z][a-z0-9]*(-[a-z0-9]+)*(__[a-z0-9]+(-[a-z0-9]+)*)?(--[a-z0-9]+(-[a-z0-9]+)*)?$",

    "custom-property-pattern": "^[a-z][a-z0-9]*(-[a-z0-9]+)*$",

    "declaration-property-value-disallowed-list": {
      "z-index": ["/^[0-9]{4,}$/"],
      "message": "z-index above 999 not allowed. Use --z-* tokens instead."
    },

    "order/properties-order": [
      "content",
      "position", "top", "right", "bottom", "left", "z-index",
      "display", "flex", "flex-direction", "flex-wrap", "align-items", "justify-content", "gap",
      "grid", "grid-template-columns", "grid-template-rows", "grid-area",
      "width", "min-width", "max-width", "height", "min-height", "max-height",
      "margin", "margin-top", "margin-right", "margin-bottom", "margin-left",
      "padding", "padding-top", "padding-right", "padding-bottom", "padding-left",
      "border", "border-radius", "outline",
      "background", "color", "opacity",
      "font", "font-size", "font-weight", "font-family", "line-height", "letter-spacing",
      "text-align", "text-decoration", "text-transform", "white-space",
      "transition", "animation", "transform",
      "cursor", "pointer-events", "user-select", "overflow"
    ]
  },

  "overrides": [
    {
      "files": ["src/styles/vendors/**/*.css"],
      "rules": {
        "declaration-no-important": null
      }
    }
  ],

  "ignoreFiles": [
    "node_modules/**",
    "dist/**",
    "build/**",
    "**/*.module.css"
  ]
}
```

---

## What Each Rule Does

| Rule | Catches |
|---|---|
| `max-nesting-depth: 2` | Selectors nested 3+ levels (specificity bombs) |
| `declaration-no-important` | Any `!important` outside vendors/ |
| `no-duplicate-selectors` | Same selector defined in multiple places |
| `no-descending-specificity` | Rules that will always lose to an earlier rule |
| `color-no-invalid-hex` | Typos in hex color values |
| `selector-class-pattern` | Class names not following kebab-case / BEM pattern |
| `custom-property-pattern` | CSS variable names not following kebab-case |
| `declaration-property-value-disallowed-list` | z-index values above 999 (should use tokens) |
| `order/properties-order` | Inconsistent property declaration order |

---

## Running Stylelint

```bash
# Check all CSS files
npx stylelint "src/styles/**/*.css"

# Auto-fix what's fixable (ordering, whitespace)
npx stylelint "src/styles/**/*.css" --fix

# Exclude vendor overrides from !important rule (already in config above)
# Nothing extra needed — the overrides block handles it
```

---

## Add to `package.json` scripts

```json
{
  "scripts": {
    "lint:css": "stylelint 'src/styles/**/*.css'",
    "lint:css:fix": "stylelint 'src/styles/**/*.css' --fix"
  }
}
```

---

## Add to CI (GitHub Actions)

```yaml
# .github/workflows/lint.yml
name: CSS Lint
on: [push, pull_request]
jobs:
  stylelint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20 }
      - run: npm ci
      - run: npm run lint:css
```

---

## VS Code Integration

Install the **Stylelint** extension (`stylelint.vscode-stylelint`) for inline error highlighting.

Add to `.vscode/settings.json`:
```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.stylelint": true
  },
  "css.validate": false,
  "stylelint.validate": ["css"]
}
```

This makes violations visible inline during development — not just in CI.
