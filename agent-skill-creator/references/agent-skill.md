Layout

```
.agents/
└── skills/
    └── my-skill/
        └── SKILL.md
```

```
.agents/
├── AGENT.md                 # global instruction
│
├── context/                 # project context
│   ├── project.md
│   ├── architecture.md
│   └── tech-stack.md
│
├── design-system/           # UI/UX system
│   ├── colors.md
│   ├── typography.md
│   ├── spacing.md
│   └── motion.md
│
├── rules/                   # coding/team rules
│   ├── frontend.md
│   ├── backend.md
│   ├── naming.md
│   └── git-workflow.md
│
├── workflows/               # development flow
│   ├── create-page.md
│   └── review.md
│
├── examples/                # reference examples
│   ├── good-ui/
│   └── components/
│
└── skills/
    └── my-skill/
        └── SKILL.md
```

Create Agent skill

```markdown
---
name: skill name
description: desc name
license: Nevinas06
metadata:
  author: nevinas06
  version: "1.0"
---
```