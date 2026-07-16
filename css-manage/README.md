# CSS Architecture Skill — Complete Package

A comprehensive skill for managing and scaling CSS in TailwindCSS-first projects. Prevents CSS hell through structure, automation, and clear conventions.

## 📦 Package Contents

```
design:css-architecture/
├── README.md                          ← You are here
├── IMPLEMENTATION-CHECKLIST.md        ← Quick setup guide
├── SKILL.md                           ← Main skill (387 lines)
│
├── references/                        ← Read as needed
│   ├── linting-setup.md               ← Stylelint config (QA automation)
│   ├── migration-guide.md             ← 3-phase migration plan
│   ├── layer-system.md                ← @layer deep dive
│   ├── folder-templates.md            ← Small/medium/large structures
│   └── anti-patterns.md               ← 10 CSS hell patterns
│
└── assets/
    └── main.css.template              ← Starter main.css file
```

**Total: 8 files, ~1,400 lines of documentation + templates**

---

## 🚀 Quick Start

### For a New Project
1. Read: [[css-manage/SKILL|SKILL.md]] Step 0 + Golden Rule
2. Choose: Small/Medium/Large from [[folder-templates]]
3. Copy: `main.css.template` → `src/styles/main.css`
4. Create: `tokens/_root.css` with starter tokens
5. Install: Stylelint config from [[linting-setup]]

### For an Existing Project
1. Audit: Run checklist from [[migration-guide]]
2. Plan: Follow 3-phase migration plan
3. Enforce: Add Stylelint to CI
4. Track: Monitor success metrics

---

## 📖 What Each File Does

| File | Purpose | Read When |
|---|---|---|
| **SKILL.md** | Complete skill definition | Always — this is the main reference |
| **linting-setup.md** | Stylelint config + CI setup | Setting up automated CSS enforcement |
| **migration-guide.md** | 3-phase incremental migration | Refactoring existing messy CSS |
| **layer-system.md** | @layer technical reference | Debugging specificity conflicts |
| **folder-templates.md** | Project structure variants | Choosing folder layout |
| **anti-patterns.md** | 10 CSS hell patterns | Code review or self-audit |
| **main.css.template** | Starter configuration | Copying into new projects |
| **IMPLEMENTATION-CHECKLIST.md** | Setup checklist | Following through implementation |

---

## 🎯 What This Skill Solves

✅ **Prevents CSS Hell**
- Eliminates `!important` abuse via `@layer`
- Prevents specificity conflicts
- Stops scattered `@keyframes`
- Eliminates hardcoded values

✅ **Scales to Large Teams**
- Clear folder structure
- Zero ambiguity in conventions
- Automated enforcement via Stylelint
- Safe migration path for existing projects

✅ **Works with TailwindCSS**
- Tailwind is primary (utilities in HTML)
- Custom CSS is deliberate (only when needed)
- No theming complexity (out of scope)
- Config alignment prevents duplication

---

## 🔑 Core Principles

1. **TailwindCSS First** — Use utilities before custom CSS
2. **@layer for Control** — Never use `!important` (except vendors/)
3. **Tokens for Values** — No hardcoded `px`/`rem`/`#colors`
4. **One Concern Per File** — Max ~150 lines; split if bigger
5. **Lint Early, Lint Often** — Enforce in CI, not just code review

---

## 📊 By the Numbers

- **387 lines** — SKILL.md (main reference)
- **5 reference files** — 949 lines total
- **2 new files** — linting-setup.md + migration-guide.md (incorporates QA + PM feedback)
- **11 feedback items** — integrated from leadership council
- **7 deliverable files** — everything needed to implement

---

## 🤝 How to Use This Skill

### With Claude / Claude API
Register this skill in your custom skill library. Claude will reference it when users ask:
- "How should I organize my CSS?"
- "My CSS is a mess"
- "CSS styles are conflicting"
- "Set up CSS linting"
- Any CSS organization question

### In Code Review
Use the `QA Validation Checklist` from SKILL.md when reviewing CSS PRs. Link to specific anti-patterns in [[anti-patterns]] if violations occur.

### In Team Onboarding
Point new developers to:
1. [[css-manage/SKILL|SKILL.md]] — Golden Rule + Folder Structure sections
2. [[anti-patterns]] — What not to do
3. Keep this README as the index

---

## 📋 Leadership Feedback Integrated

This skill incorporates feedback from:
- **Frontend Lead** — PostCSS setup, CSS Modules note, layer system
- **Designer** — Component tokens, Tailwind config alignment
- **QA** — Stylelint config, CI automation, validation checklist
- **PM** — Migration guide, success metrics, incremental adoption
- **Prompt Engineer** — Default output mode, step-by-step intake

---

## ✅ Success Looks Like

After implementing this skill across your project:

| Metric | Target |
|---|---|
| `!important` outside vendors/ | 0 |
| Hardcoded hex/px values in components | 0 |
| Stylelint CI failures | 0 |
| CSS files outside `src/styles/` | 0 |
| Selector nesting depth | ≤ 2 |
| Max file size without split | ~150 lines |
| Developer time wasted on CSS conflicts | ↓ significantly |

---

## 🔧 Next Steps

1. **Download all 8 files** — Use the links above
2. **Store in project** — Create `skills/design:css-architecture/` or similar
3. **Follow IMPLEMENTATION-CHECKLIST.md** — Phase by phase
4. **Share with team** — Make it discoverable
5. **Monitor metrics** — Track progress monthly

---

## 📞 Questions?

Each reference file has examples and detailed explanations:
- CSS conflicts? → [[layer-system]]
- Folder structure? → [[folder-templates]]
- Setting up Stylelint? → [[linting-setup]]
- Migrating existing CSS? → [[migration-guide]]
- What went wrong? → [[anti-patterns]]
- How to decide? → [[css-manage/SKILL|SKILL.md]] Workflow section

---

**Created:** June 2026 | **Status:** Ready for use | **Scope:** TailwindCSS-first CSS management (no theming depth)
