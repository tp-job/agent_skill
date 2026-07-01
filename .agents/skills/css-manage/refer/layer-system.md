# CSS Cascade Layers — Technical Reference

## Why @layer Solves CSS Hell

Before `@layer`, specificity conflicts were resolved by:
- More specific selectors → more conflicts → more specificity needed
- `!important` → escalates to `!important` arms races  
- File ordering → implicit, brittle, breaks when imports change

`@layer` makes cascade priority **explicit and structural**. Layer position always wins over selector specificity across layers.

```css
/* Without @layer — specificity war */
.card .title { color: red; }           /* 0,2,0 */
.title { color: blue !important; }     /* wins with !important — fragile */

/* With @layer — no conflict, fully predictable */
@layer components { .card .title { color: red; } }
@layer overrides { .title { color: blue; } }
/* overrides always beats components, regardless of specificity */
```

---

## Declaration Rules

**Always pre-declare the full layer order at the top of `main.css`.** Never rely on implicit layer creation.

```css
/* CORRECT */
@layer tokens, reset, base, components, layouts, utilities, vendors, overrides;

/* WRONG — creates layers implicitly as they appear */
@import "./components/_buttons.css";  /* creates "components" layer */
@import "./tokens/_root.css";         /* creates "tokens" — now lower than components! */
```

---

## Layer Priority Reference

```
Lowest ─────────────────────────────────────────────── Highest
tokens → reset → base → components → layouts → utilities → vendors → overrides
```

**The unlayered CSS trap — critical:**
```css
/* This is UNLAYERED — beats everything, including overrides */
.btn { background: red; }

/* This is in overrides layer — LOSES to unlayered .btn above */
@layer overrides {
  .btn { background: blue; }  /* lost despite being in the highest layer */
}
```
**Always wrap custom CSS in `@layer`. No exceptions.**

---

## Tailwind v3 — Full Integration

```css
/* main.css */
@layer tokens, reset, base, components, layouts, utilities, vendors, overrides;

/* Tailwind uses its own internal layers */
@tailwind base;       /* → @layer base */
@tailwind components; /* → @layer components */
@tailwind utilities;  /* → @layer utilities */

/* Custom partials — each declares its layer internally */
@import "./tokens/_root.css";
@import "./base/_reset.css";
@import "./base/_typography.css";
@import "./components/_buttons.css";
@import "./animations/_keyframes.css";
@import "./vendors/_overrides.css";
```

**Partial pattern (v3):** Each file declares its own layer:
```css
/* components/_buttons.css */
@layer components {
  .btn-icon-only { ... }
}
```

---

## Tailwind v4 — Full Integration

```css
/* main.css */
@import "tailwindcss";

/* Layer is assigned at the import site */
@import "./tokens/_root.css"  layer(tokens);
@import "./base/_reset.css"   layer(reset);
@import "./base/_typography.css" layer(base);
@import "./components/_buttons.css" layer(components);
@import "./animations/_keyframes.css";
@import "./vendors/_overrides.css" layer(vendors);
```

In v4, partials don't need internal `@layer` declarations — cleaner.

---

## Cross-Layer Specificity (How Conflicts Resolve)

Within a single layer, specificity still breaks ties:
```css
@layer components {
  .btn { color: red; }           /* 0,1,0 — loses */
  .btn.active { color: green; }  /* 0,2,0 — wins within this layer */
}
```

Across layers, layer position always wins regardless of specificity:
```css
@layer components {
  #very-specific-id.btn.active.focused { color: red; }  /* 1,3,0 — loses */
}
@layer overrides {
  .btn { color: blue; }  /* 0,1,0 — wins because overrides > components */
}
```

---

## Common Mistakes

**1. Nested @layer declarations:**
```css
/* WRONG */
@layer base { @layer components { .btn {} } }

/* CORRECT */
@layer components { .btn {} }
```

**2. Putting @keyframes inside @layer:**
```css
/* WRONG — @keyframes inside a layer may not be globally accessible */
@layer components {
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
}

/* CORRECT — @keyframes are always global, outside @layer */
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* The usage goes inside @layer */
@layer components {
  .fade { animation: fadeIn var(--duration-base) var(--ease-out); }
}
```

**3. Putting `:root` tokens in a component layer:**
```css
/* WRONG */
@layer components { :root { --btn-height: 2.5rem; } }

/* CORRECT */
@layer tokens { :root { --btn-height: 2.5rem; } }
```

**4. Empty @layer blocks:**
Remove unused `@layer blocks` — they add noise and can confuse the declaration order.
