# Agent Workspace Bootstrap

This `.agents/` folder is an install/wiring layer for the existing content library.

## Skills

Routable skills are exposed through:

- `.agents/skills/*` (junctions to source skill folders)
- `.cursor/skills/*` (junctions to source skill folders)

Do not edit skill content in this folder layer. Edit source folders at repository root.

## Source of truth

The source-of-truth layout and conventions are documented in:

- `how-to-create/agent-skill.md`

## Non-skill knowledge

Use repository root folders as persistent context/rules/workflows/examples:

- `role/`
- `owasp-top-10-2025/`
- `architecture.md`
- `component-based-architecture.md`
- `software-design-2024.md`
- `security.md`