# CSS Anti-Patterns — Root Causes of CSS Hell

Ten patterns with before/after fixes. Each is independently common; together they are multiplicative.

---

## 1. The `!important` Addiction

```css
/* ❌ */
.card-title { color: var(--color-text) !important; }
.sidebar .card-title { color: white !important; }
.sidebar .card-title.active { color: yellow !important; }
```
One `!important` requires more `!important` to override it. Escalates until everything is `!important`.

```css
/* ✅ */
@layer components { .card-title { color: var(--color-text); } }
@layer overrides  { .sidebar .card-title { color: white; }
                    .sidebar .card-title.active { color: yellow; } }
```

**Allowed exception:** `vendors/_overrides.css` only, when fighting third-party inline styles.

---

## 2. Deep Selector Nesting

```css
/* ❌ — 5 levels */
.dashboard .sidebar .nav-list .nav-item .nav-link.active { color: blue; }
```
High specificity, impossible to override cleanly. Breaks when DOM structure changes.

```css
/* ✅ — max 2 levels */
@layer components {
  .nav-link--active { color: blue; }
}
```
**Rule:** Max 2 nesting levels in any custom CSS rule. Create a new class before going deeper.

---

## 3. Hardcoded Values in Component Files

```css
/* ❌ */
.btn   { border-radius: 6px; transition: all 250ms cubic-bezier(0,0,0.2,1); }
.card  { border-radius: 8px; }
.input { border-radius: 4px; }
```
Changing a design decision requires a global search-and-replace. Values drift.

```css
/* ✅ */
/* tokens/_root.css */
@layer tokens {
  :root {
    --radius-sm: 4px; --radius-md: 6px; --radius-lg: 8px;
    --duration-base: 250ms; --ease-out: cubic-bezier(0,0,0.2,1);
  }
}
/* components/ files */
@layer components {
  .btn   { border-radius: var(--radius-md); transition: all var(--duration-base) var(--ease-out); }
  .card  { border-radius: var(--radius-lg); }
  .input { border-radius: var(--radius-sm); }
}
```

---

## 4. Recreating Tailwind Utilities

```css
/* ❌ */
@layer components {
  .centered   { display: flex; justify-content: center; align-items: center; }
  .hidden     { display: none; }
  .full-width { width: 100%; }
}
```
Maintains two systems. Tailwind utilities have JIT optimizations this breaks.

```html
<!-- ✅ — use Tailwind in HTML -->
<div class="flex items-center justify-center">
<div class="hidden">
<div class="w-full">
```

---

## 5. Global Style Leaks

```css
/* ❌ — applies to ALL links, not just sidebar */
a { color: var(--color-primary); text-decoration: none; }

/* ❌ — applies to ALL inputs inside sidebar */
@layer components { .sidebar input { border: none; } }
```
New elements inside the component unexpectedly inherit the style.

```css
/* ✅ — explicit class selectors */
@layer base {
  a { color: inherit; text-decoration: underline; }
}
@layer components {
  .sidebar-link { color: var(--color-primary); text-decoration: none; }
  .sidebar-search { border: none; }
}
```

---

## 6. The z-index Arms Race

```css
/* ❌ */
.modal    { z-index: 100; }
.tooltip  { z-index: 200; }
.toast    { z-index: 9999; }
.dropdown { z-index: 99999; }
```
No system, only reactions. Every new element needs a higher number.

```css
/* ✅ — define a scale as tokens */
@layer tokens {
  :root {
    --z-raised:  10;   --z-sticky:  100;
    --z-overlay: 200;  --z-modal:   300;
    --z-popover: 400;  --z-toast:   500;
  }
}
@layer components {
  .modal   { z-index: var(--z-modal); }
  .tooltip { z-index: var(--z-popover); }
  .toast   { z-index: var(--z-toast); }
}
```

---

## 7. Fighting Tailwind's Preflight with a Heavy Reset

```css
/* ❌ — duplicates what Tailwind already resets */
* { margin: 0; padding: 0; box-sizing: border-box; }
*, *::before, *::after { border: 0; font-size: 100%; }
```
Double resets cause unpredictable browser inconsistencies.

```css
/* ✅ — only add what Tailwind preflight doesn't cover */
@layer reset {
  html { scroll-behavior: smooth; }
  img, video { max-width: 100%; }
  input[type="search"]::-webkit-search-cancel-button { display: none; }
}
```

---

## 8. Keyframes Scattered Across Component Files

```css
/* ❌ _buttons.css */    @keyframes button-pulse { ... }
/* ❌ _cards.css */      @keyframes card-reveal { ... }
/* ❌ _modals.css */     @keyframes button-pulse { ... }  /* duplicate! */
```
Name conflicts, duplicates, no way to audit existing animations.

```css
/* ✅ — ALL keyframes in animations/_keyframes.css (outside any @layer) */
@keyframes pulse   { ... }
@keyframes reveal  { ... }
@keyframes fade-in { ... }

/* Usage inside component files */
@layer components {
  .modal { animation: fade-in var(--duration-base) var(--ease-out); }
}
```

---

## 9. Overusing `@apply`

```css
/* ❌ — defeats Tailwind's JIT, breaks variant generation */
.card {
  @apply bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow;
}
```

```html
<!-- ✅ — compose in HTML -->
<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
```

**When `@apply` IS acceptable:**
- Third-party elements you cannot add classes to (e.g., CMS-generated `.prose` content)
- Base HTML element styling in `base/_typography.css`
- Hard limit: 5 uses per project. If you need more, your architecture needs review.

---

## 10. The One-Big-File Catch-All

```css
/* ❌ custom.css — 2000 lines, no structure */
:root { ... }
h1, h2, h3 { ... }
.btn { ... }
.card { ... }
.modal { ... }
/* ... 1800 more lines ... */
```
Merge conflicts on every PR. Impossible to find anything. No isolation of concerns.

**Fix:** One file per concern. See [[folder-templates]].

---

## CSS Hell Smell Test

If you see any of these, CSS hell is present or approaching:

| Signal | Threshold |
|---|---|
| `!important` count outside vendors/ | > 5 |
| Selector nesting depth | > 3 levels |
| `z-index` values without a token system | > 1000 |
| Single CSS file length | > 300 lines |
| `@keyframes` files affected | > 2 files |
| `@apply` usage count | > 10 |
| Hardcoded hex/px values in component files | Any |
| Files named `custom.css`, `global.css`, `styles.css` with mixed content | Any |
