# CSS Architecture Skill — Implementation Checklist

Copy this checklist to your project. Check off as you implement.

---

## Setup Checklist

### Phase 0 — Skill Installation
- [ ] Download all 7 files from the skill deliverable
- [ ] Create directory structure: `design:css-architecture/` with [[css-manage/SKILL|SKILL.md]] and `references/` folder
- [ ] Store in project repo or team documentation system
- [ ] Share with team — make it discoverable

### Phase 1 — Folder Structure (Pick Your Starting Point)

**Small project:**
- [ ] Create `src/styles/tokens/`, `base/`, `components/`, `animations/`
- [ ] Copy `main.css.template` → `src/styles/main.css`
- [ ] Create `tokens/_root.css` with starter tokens

**Medium project:**
- [ ] Create `src/styles/tokens/`, `base/`, `components/`, `layouts/`, `animations/`, `vendors/`
- [ ] Copy `main.css.template` → `src/styles/main.css`
- [ ] Create all partial files listed in folder structure

**Large project:**
- [ ] Create `src/styles/` with all folders (tokens, base, components, layouts, patterns, animations, vendors)
- [ ] Create separate files per component (not one combined file)
- [ ] Create `_vendor-map.md` documenting every third-party override

### Phase 2 — PostCSC Setup (Required for Tailwind v3)
- [ ] Run `npm install -D postcss-import` (v3 only)
- [ ] Update `postcss.config.js` to load `postcss-import` BEFORE `tailwindcss`
- [ ] Verify `@import` chains in `main.css` resolve correctly
- [ ] Test: `npm run build` or dev server should work without blank screen

### Phase 3 — Design Tokens
- [ ] Create `tokens/_root.css` with `@layer tokens` block
- [ ] Extract all structural tokens: spacing, radius, z-index, animation durations
- [ ] Add component-level tokens: `--btn-height-md`, `--card-padding`, `--input-radius`
- [ ] Never add raw `px`/`rem` values to component files (use `var()` instead)

### Phase 4 — Tailwind Config Alignment
- [ ] Update `tailwind.config.js` to reference CSS variables in `extend` section
- [ ] Example: `spacing: { 'md': 'var(--space-4)' }` instead of hard `1rem`
- [ ] Verify utilities like `gap-md` and custom `var(--space-4)` are identical

### Phase 5 — Stylelint Setup
- [ ] Run `npm install -D stylelint stylelint-config-standard stylelint-order`
- [ ] Copy `.stylelintrc.json` from [[linting-setup]]
- [ ] Add npm scripts: `"lint:css": "stylelint 'src/styles/**/*.css'"`
- [ ] Run `npm run lint:css` — should pass (or have known violations)
- [ ] Add to CI: `npm run lint:css` must pass before merge

### Phase 6 — Enforce Conventions
- [ ] Install VS Code Stylelint extension (for inline errors)
- [ ] Run `pre-commit` hook or pre-push to catch violations early
- [ ] Enable "format on save" to auto-fix spacing/ordering
- [ ] Document no-nos in team onboarding

---

## If Migrating Existing Project

Follow the 3-phase plan in [[migration-guide]]:

### Audit First
- [ ] Run: `grep -r "!important" src/ --include="*.css" | wc -l` → document count
- [ ] Run: `grep -r "@keyframes" src/ --include="*.css" | grep -v "animations/"` → find scattered animations
- [ ] Run: `find src/ -name "*.css" | xargs wc -l | sort -rn` → find large files
- [ ] Screenshot the current "mess" for before/after comparison

### Phase 1 — Structure (1–2 hours, zero risk)
- [ ] Create new `src/styles/` folder structure
- [ ] Create `main.css` with layer order declared
- [ ] Keep existing CSS import at the end temporarily
- [ ] Verify app still works (no visual changes)
- [ ] Commit: "CSS: add new folder structure (non-breaking)"

### Phase 2 — Tokens (1–2 sprints, low risk)
- [ ] Extract z-index values → `tokens/_root.css` → use in existing CSS
- [ ] Extract animation timing → `tokens/_root.css` → use in existing CSS
- [ ] Extract spacing/radius → `tokens/_root.css` → use in existing CSS
- [ ] Replace hardcoded values one file at a time
- [ ] Verify no visual changes after each replacement
- [ ] Commit incrementally: "CSS: extract [category] tokens"

### Phase 3 — Rules (3–6 sprints, moderate risk)
- [ ] Migrate `@keyframes` → `animations/_keyframes.css` (move all at once — low risk)
- [ ] Migrate vendor overrides → `vendors/_overrides.css`
- [ ] Migrate base styles → `base/_reset.css`, `base/_typography.css`
- [ ] Migrate component rules one file per PR → `components/_[name].css`
- [ ] Remove old file only when completely migrated
- [ ] Commit per component: "CSS: migrate [component] to new structure"

### Completion
- [ ] All CSS now in `src/styles/`
- [ ] Old CSS files removed
- [ ] Stylelint passing
- [ ] Re-run metrics: `grep -r "!important"` → should be 0 outside vendors/
- [ ] Create before/after screenshot comparison

---

## Testing Checklist

**Before merging any CSS PR:**
- [ ] Stylelint passes: `npm run lint:css`
- [ ] No new `!important` outside vendors/
- [ ] No hardcoded hex or px values (use tokens)
- [ ] No selector nesting > 2 levels
- [ ] All `@keyframes` in `animations/` only
- [ ] Visual regression check: side-by-side screenshot of affected component

---

## Success Metrics (Measure After Implementation)

Run these commands monthly to track progress:

```bash
# Should be 0 (except vendors/)
grep -r "!important" src/styles/ --include="*.css" | grep -v "vendors/" | wc -l

# Should be 0 (all tokens)
grep -rE "[0-9]+px|[0-9]+rem" src/styles/components/ --include="*.css" | wc -l

# Should be 0 (all in animations/)
grep -rn "@keyframes" src/styles/ --include="*.css" | grep -v "animations/" | wc -l

# Should be 0 (max 2 levels)
grep -rE "(\S+\s+){3,}\S+\s*\{" src/styles/ --include="*.css" | wc -l

# Stylelint should pass
npm run lint:css

# CSS bundle size (track trend)
wc -c src/styles/main.css
```

---

## Common Issues & Fixes

| Issue | Fix |
|---|---|
| `@import` in `main.css` produces blank styles | Missing `postcss-import` — install and configure it |
| Stylelint errors on valid `@layer` rules | Update Stylelint config — see [[linting-setup]] |
| Tailwind utilities not working alongside custom CSS | Missing layer order declaration at top of `main.css` |
| `!important` doesn't override Tailwind utility | Use `@layer overrides` instead — see [[layer-system]] |
| Old CSS still being loaded | Make sure old CSS file is NOT imported by app entry point |
| Component tokens not working | Verify `tailwind.config.js` references the CSS variables |

---

## Team Onboarding

**For new team members:**
1. Read: [[css-manage/SKILL|SKILL.md]] (sections: Golden Rule, Folder Structure, Workflow)
2. Reference: Keep [[anti-patterns]] open during PR review
3. Check: Use QA checklist before submitting CSS PRs
4. Questions: Link to relevant reference file (e.g., "!important issue? See [[anti-patterns]] #1")

**For code review:**
- Use the QA Validation Checklist when reviewing CSS PRs
- Link to specific anti-patterns if violated
- Use success metrics as conversation starters: "We're at 12 !important, target is 0"

---

## Quick Links to Each Reference

| Need | File | Sections |
|---|---|---|
| Start a new project | [[folder-templates]] | Small/Medium/Large variants |
| Migrate existing CSS | [[migration-guide]] | Phase 1/2/3, audit checklist |
| Understand @layer | [[layer-system]] | Why @layer, v3/v4 integration |
| Prevent CSS hell | [[anti-patterns]] | 10 patterns, smell test |
| Set up linting | [[linting-setup]] | Stylelint config, CI setup |
| Main skill reference | [[css-manage/SKILL|SKILL.md]] | All sections, decision tree |
| Copy starter code | `main.css.template` | Ready-to-use template |
