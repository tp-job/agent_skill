# Skill authoring standard

The rubric a skill is written and reviewed against. Compiled from Anthropic's *Skill authoring best practices* (platform.claude.com, 2026), Anthropic's own skill-creator, and the community Agent Skills best-practice guides. Where they disagree, the official limit wins.

## Contents

- Hard limits
- The description
- The body
- Reference files
- Degrees of freedom
- Content rules
- Scripts
- Review checklist

## Hard limits

| Field | Limit | Why |
| --- | --- | --- |
| `name` | ≤ 64 chars, `a-z0-9-`, equals the folder name, no `anthropic`/`claude` | Spec validation |
| `description` | ≤ **1,024** chars, non-empty, no XML tags | Spec and API upload limit; Claude Code truncates at 1,536 |
| `SKILL.md` body | < 500 lines (this library: ~400) | Every loaded line competes with the conversation |
| Reference depth | One level from `SKILL.md` | Nested links get partial reads (`head -100`) |
| Long reference | > 100 lines → `## Contents` at the top | A partial read still sees the whole scope |

## The description

The description is the only text read before the skill is chosen. It carries the whole routing decision.

1. **What it does**: the capability, in third person ("Audits built UIs…"), never "I can" or "you can".
2. **When to use it**: the situations, including ones where the user won't name the skill.
3. **Trigger phrases**: the literal words users type, in every language they use.
4. **Not for**: adjacent work that should go elsewhere. This stops the wrong skill firing.

Claude tends to *under*-trigger, so a little push ("use whenever the request involves X, even if X is not named") is fine. Vagueness is the failure: `Helps with documents` never fires.

| BAD | BETTER |
| --- | --- |
| `Deep debug and auto-fix skill covering…` | `Debugs and fixes broken code and workflows in four phases…` |
| `ALWAYS use this skill when the user mentions: (60 keywords)` | `Use whenever the request involves rendering 3D in the browser. Trigger for: "Three.js", "shader", …` |
| `I can help you plan your day` | `Plans the day across Google Calendar and ClickUp…` |

## The body

`SKILL.md` is a router and a workflow, not an encyclopedia.

- **Assume Claude is already smart.** For every paragraph ask: does Claude really not know this? Cut definitions, motivation essays and history. A 50-token code sample beats a 150-token explanation of it.
- **Lead with the fast path**: a table from request → action or file.
- **Workflow as numbered steps**, with a copyable checklist for anything over ~5 steps, and a validate → fix → repeat loop for quality-critical output.
- **Explain why instead of shouting.** `ALWAYS`/`NEVER`/`MUST` in caps is a warning sign; a capable model follows a reason better than a command. Keep caps for the one or two rules where a mistake is destructive.
- **Show the wrong version next to the right one** (BAD/BETTER) for anything with a common failure.
- **Say when not to apply the advice.**
- **No maintainer content.** Changelogs, "an earlier version of this skill…", and bundle-repair history belong in a separate reference the task never loads.

## Reference files

- One concern per file, named for its content (`oauth2-and-api-keys.md`, not `doc2.md`).
- Link each from `SKILL.md` with *when* to read it, not just *what* it is.
- Organise by variant (`aws.md` / `gcp.md`) so only the relevant file loads.
- Large references cost nothing until read; put complete detail there, not in the body.

## Degrees of freedom

Match specificity to how fragile the task is.

| Freedom | Form | Use when |
| --- | --- | --- |
| High | Prose heuristics | Many valid approaches; context decides (reviews, design) |
| Medium | Template or pseudocode with parameters | A preferred pattern exists, variation is fine |
| Low | Exact script, exact command | Fragile, destructive or order-dependent (migrations, deploys) |

Give one default with an escape hatch, not a menu: "Use pdfplumber; for scanned PDFs use pytesseract", not "you can use pypdf, or pdfplumber, or…".

## Content rules

- **No time-sensitive statements.** Not "currently", "this year", "the latest". State the version ("r186+", "Tailwind v4") or file outdated material under an "Old patterns" heading.
- **One term per concept** throughout the skill.
- **Output formats as templates**, strict ("use exactly this") or flexible ("a sensible default"), not described in prose.
- **Examples as input/output pairs** when output quality depends on style.
- **Forward slashes in paths.** Fully qualified MCP tool names (`Server:tool`).
- **No README, CHANGELOG or install guide inside a skill** unless it is also a standalone package.

## Scripts

- Prefer a script for deterministic work; it is more reliable than generated code and costs only its output.
- Say whether to **run** it or **read** it.
- Handle errors in the script; don't defer them to Claude. Error messages name what is valid.
- No unexplained constants. List required packages.

## Review checklist

```
- [ ] description: what + when + trigger phrases + Not for, third person, ≤ 1,024 chars
- [ ] body under 500 lines (library: ~400), routes rather than explains
- [ ] nothing Claude already knows; no motivation essays or history
- [ ] references one level deep, each linked with when to read it
- [ ] references over 100 lines open with ## Contents
- [ ] no time-sensitive wording; versions stated where behaviour depends on them
- [ ] consistent terminology; templates for output formats
- [ ] caps emphasis only where a mistake is destructive
- [ ] at least three evaluation cases, including one that should not trigger
```
