# Agent Skill Library — Conventions

This repository is a library of Claude Code skills. There is no application code here: every folder is one skill, and the deliverable is the skills themselves.

Browse them in [README.md](README.md). The machine-readable index is [skill.json](skill.json).

---

## Layout

Every skill is one top-level folder whose name **exactly matches** the `name:` in its `SKILL.md`:

```
<skill-name>/
├── SKILL.md          required — the entry point
├── references/       optional — deep-dive docs, loaded on demand
├── scripts/          optional — executable helpers
├── assets/           optional — templates, images, non-executable files
├── bundled/          optional — verbatim copies of every skill this one links to
└── README.md         optional — only for skills that are also standalone packages
```

Fixed vocabulary. Do not introduce `refer/`, `resources/`, `docs/`, or `lib/` — a reader (human or model) should be able to guess a path without looking.

Two skills deviate deliberately: `vercel-react-best-practices/rules/` holds ~68 single-rule files that are built into a rules bundle, and `senior-leadership-advisor/roles/` holds per-discipline role definitions. Both are documented in their own SKILL.md.

---

## Cross-skill links and `bundled/`

**A skill folder must work when copied out of this library on its own.** That rules out `../other-skill/SKILL.md`: it resolves here and dangles everywhere else. So a skill that links to another skill carries a copy of it.

```
promethean-parthenon/
├── SKILL.md                     links to bundled/agentic-engineering/SKILL.md
└── bundled/
    ├── agentic-engineering/     verbatim copy
    ├── promethean-parthenon/    verbatim copy — see below
    └── …
```

Rules:

- **Bundle the whole link closure, not just direct targets.** A bundled copy keeps its own `../other-skill/` links, which resolve to its *siblings inside the bundle*. If a skill two hops away is missing, that copy dangles.
- **The closure includes the host itself.** Bundled skills link back at their host, so `<host>/bundled/<host>/` has to exist. It nests one level and no further — copies are staged with `bundled/` excluded.
- **Copies are verbatim.** The only permitted difference from the original is the depth of a relative link: a host at the library root writes `bundled/x/SKILL.md`, a copy inside a bundle writes `../x/SKILL.md`. Nothing else may differ — no summarising, no trimming.
- **Never hand-edit a copy.** Change the source skill, then regenerate the bundles.

Six skills currently bundle — the Role · Task · Format cluster routed by `promethean-parthenon`: `senior-leadership-advisor` (Role), `requirement-gathering` · `agentic-engineering` · `long-horizon-engineering-workflow` (Task), `github-report` (Format), plus the router itself. They share one 11-skill closure. `scripts/build-index.py` globs `*/SKILL.md`, so nested copies are never indexed as skills.

Verify with `python scripts/check-bundles.py` — it re-checks the closure, the copies, and every relative link in the repo.

---

## SKILL.md frontmatter

```yaml
---
name: skill-name                 # required — kebab-case, must equal the folder name
description: >-                  # required — see below
  What it does. When to use it. Explicit trigger phrases.
allowed-tools: Read Write Edit   # optional — only if the skill must be restricted
argument-hint: "<what to pass>"  # optional — only for skills invoked with an argument
license: MIT
metadata:
  author: <handle> (enhanced by Claude)
  version: "1.0.0"               # semver, quoted
  source: <where the knowledge came from> (compiled <year>)
---
```

**The description is the trigger.** It is the only thing loaded before the skill is selected, so it has to carry the whole routing decision. Write it as three parts: what the skill does, when to reach for it, and the literal phrases a user would say. Include negative scope — "not for X" — when two skills are adjacent, because that is what stops the wrong one from firing.

Bump `metadata.version` when the guidance changes, not when a typo is fixed.

---

## Progressive disclosure

`SKILL.md` is a router, not an encyclopedia. Keep it under ~400 lines. It should state the workflow and point at depth:

```markdown
| Need | Read |
| --- | --- |
| <one specific need> | [<file-name>](references/<file-name>.md) |
| <another specific need> | [<other-file>](references/<other-file>.md) |
```

Rules:

- **Every reference must be a relative markdown link**, not a bare path in backticks and not an Obsidian `[[wikilink]]`. Markdown links resolve for both Claude and Obsidian; wikilinks only work in Obsidian, and a backticked path is a string the model has to guess at.
- **Never link a file that does not exist.** A dangling pointer is worse than an omission — it promises depth that isn't there and sends the reader on a failed lookup.
- **One concern per reference file.** If a file covers two topics, split it, so loading one doesn't drag in the other.

Run the checks below before committing; they catch both problems.

---

## Checks

```bash
python scripts/build-index.py
```

Regenerates `skill.json` and `README.md`, and reports any skill whose folder name, `name:`, or description is out of line. Exits non-zero when something is wrong. Run it after adding, renaming, or removing a skill — curated summaries in `skill.json` are preserved across rebuilds. It globs `*/SKILL.md`, so copies under `bundled/` are never indexed as skills.

```bash
python scripts/build-bundles.py && python scripts/check-bundles.py
```

Rebuilds every `bundled/` directory from its sources, then verifies the closure, the fidelity of each copy, and every relative markdown link in the repository. Run it after editing any skill in the bundling cluster — a source edit does not reach the copies on its own. The build step is idempotent; the check step exits non-zero on any dangling link or drifted copy.

Before committing a skill change, confirm:

- [ ] Folder name == `name:` in frontmatter
- [ ] `description` names what it does, when to use it, and literal trigger phrases
- [ ] `license` and `metadata` blocks present
- [ ] Every reference is a relative markdown link to a file that exists
- [ ] No link leaves the skill folder — a cross-skill link points at `bundled/`, never `../`
- [ ] `SKILL.md` routes rather than explains; depth lives in `references/`
- [ ] No credentials, tokens, or personal paths in any file
- [ ] `python scripts/build-index.py` exits clean
- [ ] `python scripts/build-bundles.py && python scripts/check-bundles.py` exits clean

---

## Writing style for skill content

These files are read by a model under context pressure, mid-task. That shapes the prose:

- **Prescriptive over descriptive.** "Read the plan inside-out" beats "plans can be read in various orders."
- **Tables and checklists over paragraphs** for anything enumerable.
- **Show the wrong version next to the right one.** A BAD/BETTER pair transfers more than a rule stated abstractly.
- **State the version or dialect** whenever behavior depends on it — SQL engine, Python version, C standard, library major version. Guidance graded against the wrong version is worse than no guidance.
- **Say when *not* to apply the advice.** A rule with no stated limits gets over-applied.

---

## Obsidian

This library lives inside an Obsidian vault, so the markdown is read both ways. Relative markdown links satisfy both: Obsidian resolves and graphs them, and Claude can follow them to a real path. Prefer them to wikilinks in all new content.
