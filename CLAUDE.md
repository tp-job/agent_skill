# Agent Skill Library — Conventions

This repository is a library of Claude Code skills. There is no application code here: every skill folder is one skill, and the deliverable is the skills themselves.

Browse them in [README.md](README.md). The machine-readable index is [skill.json](skill.json).

---

## Layout

The repository root holds only the **hubs** — the few skills a user is expected to remember — and five **realm** folders. Every other skill lives inside exactly one realm. A realm is a plain directory, never a skill:

```
promethean-parthenon/   hub — engineering; routes to core/
athena-erechtheion/     hub — design; routes to design/
hermes-olympus/         hub — AI agents and MCP; routes to nothing
chronos-artemis/        hub — time and task management (Google Calendar, ClickUp); routes to nothing
core/          engineering specialists — promethean-parthenon's spokes
design/        design specialists — athena-erechtheion's spokes
web/           web delivery and quality
stack/         application stacks
knowledge/     knowledge, notes, analysis, teaching
```

**A hub is named in the library's Greek and Roman register as two words, like `promethean-parthenon`**: the power or quality first, then its place. It is one of the few names a user is expected to remember, so the name is allowed to be memorable rather than literal. **A realm is named as one plain, literal English word for its category** — `core`, `design`, `web`, `stack`, `knowledge` — never a myth name: nobody needs to remember a realm's name, only guess it correctly from the skill inside, and a plain word guesses better than a myth reference does. Keep new hubs and realms in their respective form. Skill folders inside a realm keep plain descriptive names too — they are found by description, not remembered. The list, the hubs and each hub's spokes live in one file, `scripts/skills_layout.py` — every build and check script reads it, so change the layout there and nowhere else. `build-index.py` fails on a non-hub skill at the top level, a skill in an unknown realm, a hub name that isn't two words, or a realm name that isn't one.

Each skill folder's name **exactly matches** the `name:` in its `SKILL.md`, and the folder is self-contained — copy it out of its realm into any project and it works:

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

Two skills deviate deliberately: `web/vercel-react-best-practices/rules/` holds ~68 single-rule files that are built into a rules bundle, and `core/senior-leadership-advisor/roles/` holds per-discipline role definitions. Both are documented in their own SKILL.md.

---

## Skills are components: hub-and-spoke, not mesh

**A skill is a standalone component.** It must not link to another skill, and it must not carry a `bundled/` folder — full stop — unless it is itself an aggregator that routes between other skills. An ordinary skill's value has to be usable in complete isolation: copy the one folder into any project and it works, with no other skill present.

**Only an aggregator (a hub) combines skills, and there are exactly two: `promethean-parthenon` for engineering and `athena-erechtheion` for design.** A hub is allowed to link out to the skills it routes between, because routing *is* what it does. The skills it points at do not point back, and do not point at each other. That asymmetry is the whole rule:

```
   promethean-parthenon  ──links to──►  agentic-engineering
                          ──links to──►  requirement-gathering
                          ──links to──►  long-horizon-engineering-workflow
                          ──links to──►  senior-leadership-advisor
                          ──links to──►  github-report

   agentic-engineering, requirement-gathering, long-horizon-engineering-workflow,
   senior-leadership-advisor, github-report  ──link to──►  nothing outside themselves
```

If you are tempted to add "see also [other-skill]" inside one of the spokes, don't — mention the *concept* in plain prose if it helps ("this consumes a target written elsewhere"), never a markdown link to another skill's folder. A link is a dependency; a mention in prose is not.

**Why:** the alternative is a mesh — every skill linking to every other skill it's ever used alongside — which forces every one of them to carry a full `bundled/` copy of the others just to stay portable. That was tried and reverted: five skills each bundling an 11-skill closure, 490+ duplicated files, all to preserve links that added no capability the plain-language mention doesn't. Hub-and-spoke gets the same "nothing dangles when copied out" property from one skill's `bundled/` folder instead of six.

**A skill folder must still work when copied out of this library on its own.** For a hub, that rules out `../core/other-skill/SKILL.md`: it resolves here and dangles everywhere else. So each hub carries a verbatim copy of everything it links to.

```
promethean-parthenon/
├── SKILL.md                     links to bundled/agentic-engineering/SKILL.md
└── bundled/
    ├── agentic-engineering/     verbatim copy
    ├── requirement-gathering/   verbatim copy
    └── …
```

Rules for a hub's `bundled/`:

- **Bundle every skill it links to, directly.** Because spokes never link onward, the closure is just the aggregator's own direct targets — no second-hop skills to chase.
- **Copies are verbatim, with no self-copy.** A bundled copy is byte-for-byte the source skill; since a spoke carries no outbound links, it needs no link-depth rewriting either. The aggregator does not need to bundle a copy of itself, because nothing inside its bundle links back to it.
- **Never hand-edit a copy.** Change the source skill, then regenerate the bundle.

The two hubs are the only skills with a `bundled/` folder. `promethean-parthenon` holds the five skills in its Role · Task · Format cluster (`senior-leadership-advisor`, `requirement-gathering`, `agentic-engineering`, `long-horizon-engineering-workflow`, `github-report`) plus the leaf skills its routing table hands off to (`debug-master`, `owasp-top-10-2025`, `project-file-structure`, `skill-creator`, `ui-checker`) — all ten filed in `core/`. `athena-erechtheion` holds the four design specialists filed in `design/` (`frontend-design`, `google-design-system`, `css-architecture`, `threejs-3d`). Discovery skips anything under `bundled/`, so the copies are never indexed as skills.

**Adding a third hub is a deliberate change**, not a convenience: it costs a bundle, a description that must carry every spoke's triggers within the cap, and a trigger-eval run. Only add one when a cluster of skills genuinely shares one front door, as design did.

Verify with `python scripts/check-bundles.py` — it checks that every non-hub skill is link-free, that each hub links only into its own `bundled/`, that every bundle matches its sources verbatim, and that every relative link in the repo resolves.

---

## Active set: what actually loads

Every skill description sits in the model's context in every session, so the plugin loads **only the active set** — every skill except the hubs' spokes. The spokes listed in `HUBS` (`scripts/skills_layout.py`) stay as source folders in their realm, because the bundles are built from them, but they load only through their hub, whose description carries their triggers and whose fast-path table opens them directly.

- `.claude-plugin/plugin.json` → `skills` is **generated** by `build-index.py`. Do not hand-edit it; change `HUBS` in `scripts/skills_layout.py` instead. Entries are `./<hub>` or `./<realm>/<skill>`.
- `scripts/install.sh` / `install.ps1` read the same list, so every install route loads the same set.
- Adding a spoke to a hub in `HUBS` deactivates it as a standalone skill. Its trigger phrases must then be added to the aggregator's description and fast-path table, or nothing will route to it.
- A description is truncated at **1,536 characters** in the skill listing. The hubs' descriptions are the tightest; measure them after every change.

**Before adding a new skill, check whether an active skill or a core specialist already owns its triggers.** If one does, add the content as a `references/` file of that skill instead. `security`, `tracking-and-debugging`, `agent-skill-creator` and `web-design-guidelines` were merged this way into `owasp-top-10-2025`, `debug-master`, `skill-creator` and `ui-checker`.

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

Regenerates `skill.json` and `README.md`, and reports any skill whose folder name, `name:`, or description is out of line. Exits non-zero when something is wrong. Run it after adding, renaming, or removing a skill — curated summaries in `skill.json` are preserved across rebuilds. It discovers hubs at the top level and skills one level inside each realm, and never indexes copies under `bundled/`.

```bash
python scripts/build-bundles.py && python scripts/check-bundles.py
```

Rebuilds every `bundled/` directory from its sources, then verifies the closure, the fidelity of each copy, and every relative markdown link in the repository. Run it after editing any skill in the bundling cluster — a source edit does not reach the copies on its own. The build step is idempotent; the check step exits non-zero on any dangling link or drifted copy.

```bash
python scripts/lint-skills.py
```

Checks what the other two cannot: description over the 1,536-character listing cap, no negative scope in the description, orphaned reference files, broken `#heading` anchors (GitHub slugs — `## Cloud & Network` is `#cloud--network`), Obsidian wikilinks, skill frontmatter left inside a reference file, mojibake, personal paths, and credential-shaped strings. Exits non-zero on any finding.

Before committing a skill change, confirm:

- [ ] Folder name == `name:` in frontmatter
- [ ] `description` names what it does, when to use it, literal trigger phrases, and what it is **not** for — within 1,536 characters
- [ ] `license` and `metadata` blocks present
- [ ] Every reference is a relative markdown link to a file that exists
- [ ] No link leaves the skill folder — a cross-skill link points at `bundled/`, never `../`
- [ ] `SKILL.md` routes rather than explains; depth lives in `references/`
- [ ] No credentials, tokens, or personal paths in any file
- [ ] `python scripts/build-index.py` exits clean
- [ ] `python scripts/build-bundles.py && python scripts/check-bundles.py` exits clean
- [ ] `python scripts/lint-skills.py` exits clean

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
