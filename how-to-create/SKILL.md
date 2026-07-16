---
name: agent-skill-creator
description: >-
  Guide for creating, structuring, and organising AI agent skills. Use this skill when building a new agent skill from scratch, setting up a .agents/ workspace, designing skill folder structures, or writing SKILL.md files with proper YAML frontmatter. Triggers on tasks involving skill creation, agent configuration, AGENT.md setup, skills folder layout, or workspace organisation. Also trigger for: "create a skill", "write a SKILL.md", "set up .agents folder", "agent workspace", "skill structure", "how do I create a skill", "agent rules", "agent context", or any request to build or improve AI agent configuration.
license: MIT
metadata:
  author: nevinas06 (enhanced by Claude)
  version: "1.0.0"
  source: Agent Skill Creator guide (compiled 2026)
---

# Agent Skill Creator

A guide for building well-structured AI agent skills. Covers the canonical folder layout for `.agents/` workspaces and the required format for `SKILL.md` files that agents can discover and execute reliably.

## When to Apply

Reference this skill when:
- Creating a new agent skill from scratch
- Setting up or reorganising a `.agents/` project workspace
- Writing or fixing a `SKILL.md` frontmatter block
- Adding context, rules, workflows, or design system files to an agent workspace
- Reviewing whether an existing skill is properly structured for agent discovery

## Skill Structure Levels

| Level | Structure | Purpose |
|-------|-----------|---------|
| 1 | Minimal — folder + SKILL.md | Single-purpose skill |
| 2 | Standard — folder + SKILL.md + references/ | Skill with supporting docs |
| 3 | Full workspace — .agents/ tree | Project-wide agent context |

## Quick Reference

### 1. Minimal Skill Layout (Always Required)
```
.agents/
└── skills/
    └── my-skill/
        └── SKILL.md          ← required; must have valid YAML frontmatter
```

### 2. Standard Skill Layout (Recommended)
```
.agents/
└── skills/
    └── my-skill/
        ├── SKILL.md           ← entry point — agent reads this first
        └── references/        ← supporting detail files
            ├── guide.md
            └── examples.md
```

### 3. Full Workspace Layout
```
.agents/
├── AGENT.md                   ← global agent instruction (always read first)
│
├── context/                   ← project context
│   ├── project.md
│   ├── architecture.md
│   └── tech-stack.md
│
├── design-system/             ← UI/UX design system
│   ├── colors.md
│   ├── typography.md
│   ├── spacing.md
│   └── motion.md
│
├── rules/                     ← coding and team rules
│   ├── frontend.md
│   ├── backend.md
│   ├── naming.md
│   └── git-workflow.md
│
├── workflows/                 ← development flow
│   ├── create-page.md
│   └── review.md
│
├── examples/                  ← reference examples
│   ├── good-ui/
│   └── components/
│
└── skills/
    └── my-skill/
        └── SKILL.md
```

### 4. SKILL.md — Required Frontmatter Format
Every `SKILL.md` **must** open with a valid YAML frontmatter block between `---` fences:

```markdown
---
name: skill-name-kebab-case
description: Specific trigger description. Use when [exact conditions]. Triggers on: "[phrase1]", "[phrase2]", "[phrase3]".
license: MIT
metadata:
  author: your-name
  version: "1.0.0"
---

# Skill Title

[Body of the skill — instructions, decision trees, examples]
```

### 5. Description Writing Rules (CRITICAL for Agent Routing)
- **Be specific** — vague descriptions cause the agent to miss or over-trigger
- **List trigger phrases** — include exact phrases in quotes that a user might type
- **State the use case** — "Use when [user does X]"
- **Include anti-triggers** — "Do NOT use when [Y]" if there's ambiguity

**Bad description:**
```yaml
description: Helps with code.
```

**Good description:**
```yaml
description: Clean Code principles for JavaScript. Use when reviewing or refactoring JS/TS code for readability and maintainability. Triggers on: "clean up my code", "code review", "bad variable names", "refactor this function".
```

### 6. Common Mistakes to Avoid
- ❌ `---` fences missing → YAML not parsed; skill not discovered
- ❌ `name` field missing → agent cannot identify the skill
- ❌ Description too vague → wrong skill triggered or skill ignored
- ❌ Skill content only in a `.md` file, not in `SKILL.md` → agent misses it
- ❌ Lowercase `skill.md` instead of `SKILL.md` → case-sensitive systems miss it
- ❌ References to absolute paths → skill breaks when moved

## How to Use

1. Choose the layout level matching your need (minimal / standard / full workspace)
2. Create the folder with a descriptive kebab-case name
3. Write `SKILL.md` with correct frontmatter using the template above
4. Add reference files for supporting detail — keep `SKILL.md` as the concise entry point
5. Test by asking the agent a trigger phrase — confirm the right skill activates

## Full Reference Document

For the complete workspace layout reference: [[agent-skill]]
