# Migration Guide — Moving to Clean CSS Architecture

For teams with an existing messy codebase. This is a 3-phase plan designed to be done incrementally — no big-bang rewrite.

**Rule #1: Never rewrite all CSS at once.** The risk of visual regression is too high. Migrate one layer at a time.

---

## Before You Start — Audit First

Run the CSS smell test to understand the scope:

```bash
# Count !important occurrences
grep -r "!important" src/ --include="*.css" | wc -l

# Find hardcoded hex values in non-token files
grep -rE "#[0-9a-fA-F]{3,6}" src/ --include="*.css" \
  | grep -v "tokens/" | wc -l

# Find keyframes outside animations/
grep -rn "@keyframes" src/ --include="*.css" \
  | grep -v "animations/"

# Find deeply nested selectors (3+ descendant combinators)
grep -rE "(\S+\s+){4,}\S+\s*\{" src/ --include="*.css"

# Find files over 150 lines
find src/ -name "*.css" | xargs wc -l | sort -rn | head -20
```

Document the numbers. These become your **before** metrics to compare against after migration.

---

## Phase 1 — Create the Structure (Zero Risk)

**Goal:** Create the folder structure and `main.css` without moving a single existing rule.

**Effort:** 1–2 hours. **Risk:** Zero. **Can be done immediately.**

1. Create the folder structure inside `src/styles/`:
   ```
   src/styles/
   ├── tokens/
   ├── base/
   ├── components/
   ├── layouts/
   ├── animations/
   ├── vendors/
   └── main.css
   ```

2. Create `main.css` with the layer order declared and your existing CSS import at the end:
   ```css
   @layer tokens, reset, base, components, layouts, utilities, vendors, overrides;

   @tailwind base;
   @tailwind components;
   @tailwind utilities;

   /* Phase 1: existing CSS still in its original location */
   @import "../path/to/your/existing/styles.css";

   /* Phase 2: new files will be added here as migration progresses */
   ```

3. Install and configure `postcss-import` (if v3) — see [[linting-setup]]

4. Install Stylelint but run it in **warning mode** only (don't make it block CI yet):
   ```json
   { "scripts": { "lint:css": "stylelint 'src/styles/**/*.css' --allow-empty-input" } }
   ```

5. Verify the app still works. If yes, Phase 1 is done.

---

## Phase 2 — Migrate Tokens (Low Risk)

**Goal:** Extract all structural tokens (spacing, radius, z-index, animation) into `tokens/_root.css`.

**Effort:** 2–4 hours per sprint. **Risk:** Low — tokens are additive.

**Do not touch existing rules in this phase.** Only extract values.

### Step 2a — Extract z-index values

Find every `z-index` in the codebase:
```bash
grep -rn "z-index:" src/ --include="*.css"
```

Create a z-index scale in `tokens/_root.css`:
```css
@layer tokens {
  :root {
    --z-raised:  10;
    --z-sticky:  100;
    --z-overlay: 200;
    --z-modal:   300;
    --z-popover: 400;
    --z-toast:   500;
  }
}
```

Replace raw values in existing CSS (one file at a time):
```css
/* Before */
.modal { z-index: 300; }

/* After */
.modal { z-index: var(--z-modal); }
```

### Step 2b — Extract animation tokens

```css
@layer tokens {
  :root {
    --duration-fast: 150ms;
    --duration-base: 250ms;
    --ease-out: cubic-bezier(0.0, 0, 0.2, 1);
  }
}
```

### Step 2c — Extract spacing and radius tokens

Follow the Tailwind scale (1 = 0.25rem, 2 = 0.5rem, 4 = 1rem, etc.) so utilities and tokens stay aligned.

### Step 2d — Extract component tokens

For any value that appears in 2+ component files:
```css
:root {
  --btn-height-md: 2.5rem;
  --card-padding:  1.5rem;
  --input-radius:  0.5rem;
}
```

**After Phase 2:** Verify no visual changes. Run Stylelint and count errors (don't block on them yet).

---

## Phase 3 — Migrate Rules (One Component Per Sprint)

**Goal:** Move existing CSS rules into the correct layered partial files.

**Effort:** 1 component per sprint (or per PR). **Risk:** Moderate — do one file at a time with visual review.

### Sequence (lowest risk first)

1. `animations/_keyframes.css` — Move all `@keyframes` first. Low risk — they're declarations, not rules.
2. `vendors/_overrides.css` — Move all third-party overrides. Easy to isolate.
3. `base/_reset.css` and `base/_typography.css` — Base element styles.
4. `components/_[name].css` — One component file per PR.
5. `layouts/_grid.css` — Layout patterns last.

### Per-file migration process

For each component CSS block:

1. Create `src/styles/components/_[name].css`
2. Wrap the rules in `@layer components { }`
3. Replace any hardcoded values with `var(--token)` 
4. Remove deeply nested selectors (flatten to max 2 levels)
5. Remove any `!important` (use `@layer overrides` or fix specificity instead)
6. Add `@import "./components/_[name].css"` to `main.css`
7. Remove the block from the old file
8. Visual review: check the component in browser. Screenshot before/after if complex.
9. Merge PR. Do not batch multiple components in one PR.

### When to remove the old file

Remove the original `styles.css` / `custom.css` / `global.css` when:
- All rules have been migrated to the new structure
- It is empty or contains only comments
- Visual regression testing passes (even manual side-by-side comparison)

---

## After Migration — Enable Strict Linting

Once Phase 3 is complete, enable Stylelint as a CI blocker:

```json
{
  "scripts": {
    "lint:css": "stylelint 'src/styles/**/*.css'"
  }
}
```

Run the audit metrics again and compare:
```bash
grep -r "!important" src/styles/ --include="*.css" | wc -l
# Target: 0 (outside vendors/)
```

---

## Migration Risk Matrix

| Phase | Visual Risk | Time Risk | Can Be Reverted? |
|---|---|---|---|
| Phase 1 — Structure | None | Hours | Yes, trivially |
| Phase 2 — Tokens | Very low | 1–2 sprints | Yes, find/replace back |
| Phase 3 — Rules | Moderate | 3–6 sprints | Yes, per PR |

If any phase causes visual regressions, roll back that PR only. The other phases remain in place.
