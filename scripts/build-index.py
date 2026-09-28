#!/usr/bin/env python3
"""Regenerate skill.json and README.md from the SKILL.md files on disk.

Run from the repository root after adding, renaming, or removing a skill:

    python scripts/build-index.py

Curated `description` and `content` summaries already present in skill.json are
preserved and re-keyed by skill name, so hand-written summaries survive a
rebuild. A skill with no curated entry falls back to its frontmatter
description, truncated at the first sentence.
"""
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'skill.json')
README = os.path.join(ROOT, 'README.md')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skills_layout import HUB_NOTE, HUBS, REALMS, active, discover, spokes  # noqa: E402

# Inserted verbatim right after the intro, before Install. Skills fire from their
# `description` automatically — a user should never need to remember a folder name to
# get one. Keep this short; it is a pointer to that fact, not a full lookup table.
FINDING = [
    "## Finding a skill without knowing its name",
    "",
    "Only three names are worth remembering — the hubs below. Everything else is opened for "
    "you: Claude Code reads each active skill's `description` and opens the match, and a hub "
    "opens the specialists filed under it. Describe the task in plain language and let it pick.",
    "",
    "| Instead of recalling… | Just say… | Opens via |",
    "| --- | --- | --- |",
    "| `debug-master` | \"why is this not working\" | promethean-parthenon |",
    "| `owasp-top-10-2025` | \"is this secure\" | promethean-parthenon |",
    "| `ui-checker` | \"does dark mode work on this page\" | promethean-parthenon |",
    "| `agentic-engineering` / `requirement-gathering` | \"plan this build\" | promethean-parthenon |",
    "| `frontend-design` | \"make this page look less generic\" | master-design |",
    "| `css-architecture` | \"organise my Tailwind CSS\" | master-design |",
    "| `threejs-3d` | \"build a 3D scene with three.js\" | master-design |",
    "| `master-agent` | \"which MCP server should handle this\" | itself |",
    "| `deploy-to-vercel` | \"deploy this app\" | itself |",
    "",
    "Unsure which skill fits, or the request spans several? Say that — "
    "\"which skill should I use\" is itself a promethean-parthenon trigger. A name is only "
    "needed to invoke an *active* skill directly by its namespaced form "
    "(`agent-skill:promethean-parthenon`), which is optional; a hub's specialists have no "
    "namespaced entry of their own.",
    "",
]


REPO = 'https://github.com/tp-job/agent_skill.git'

INSTALL = [
    '## Install',
    '',
    'Claude Code loads a skill from `<skills-dir>/<name>/SKILL.md`, one level deep. '
    'Pick one of the three routes below.',
    '',
    '**1. As a plugin (recommended).** Claude Code clones the repo and keeps it updated. '
    'Run inside Claude Code:',
    '',
    '```',
    '/plugin marketplace add tp-job/agent_skill',
    '/plugin install agent-skill@tp-job-skills',
    '```',
    '',
    'Active skills are then namespaced, e.g. `agent-skill:promethean-parthenon`. '
    'Update later with `/plugin marketplace update tp-job-skills`.',
    '',
    '**2. Clone and link.** Keeps a normal git checkout you can `git pull`; '
    'each skill is linked into `~/.claude/skills/` without touching skills already there.',
    '',
    '```bash',
    'git clone %s ~/.claude/agent-skill' % REPO,
    'sh ~/.claude/agent-skill/scripts/install.sh',
    '```',
    '',
    'On Windows PowerShell:',
    '',
    '```powershell',
    'git clone %s $HOME\\.claude\\agent-skill' % REPO,
    'powershell -ExecutionPolicy Bypass -File $HOME\\.claude\\agent-skill\\scripts\\install.ps1',
    '```',
    '',
    'Pass a path to install into one project instead: '
    '`sh scripts/install.sh ./.claude/skills` or `install.ps1 .\\.claude\\skills`.',
    '',
    '**3. Clone straight into a skills folder.** Only works when that folder does not exist yet:',
    '',
    '```bash',
    'git clone %s .claude/skills' % REPO,
    '```',
    '',
]


def parse_frontmatter(path):
    """Minimal YAML frontmatter reader — enough for the fields we index."""
    text = open(path, encoding='utf-8').read()
    if not text.startswith('---'):
        return None
    end = text.find('\n---', 3)
    if end == -1:
        return None
    block = text[3:end]

    fields = {}
    key = None
    for line in block.splitlines():
        m = re.match(r'^([a-zA-Z-]+):\s*(.*)$', line)
        if m and not line.startswith(' '):
            key = m.group(1)
            value = m.group(2).strip()
            # A block scalar indicator carries no text of its own — the value
            # is entirely in the indented lines that follow.
            fields[key] = '' if value in ('>', '>-', '|', '|-') else value
        elif key and line.strip():
            # continuation of a folded/literal block scalar
            fields[key] = (fields[key] + ' ' + line.strip()).strip()
    return fields


def first_sentence(text, limit=240):
    text = re.sub(r'\s+', ' ', text).strip()
    m = re.match(r'^(.+?\.)(\s|$)', text)
    out = m.group(1) if m else text
    return out if len(out) <= limit else out[:limit].rsplit(' ', 1)[0] + '…'


PLUGIN = os.path.join(ROOT, '.claude-plugin', 'plugin.json')


def write_plugin_skills(found):
    """Active set = every skill except the hubs' spokes, which load via their hub."""
    with open(PLUGIN, encoding='utf-8') as f:
        manifest = json.load(f)
    manifest['skills'] = ['./' + found[n] for n in active(found)]
    with open(PLUGIN, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write('\n')
    return len(manifest['skills']), len(spokes())


def main():
    os.chdir(ROOT)

    curated = {}
    if os.path.exists(INDEX):
        old = json.load(open(INDEX, encoding='utf-8'))
        for s in old.get('skills', []):
            curated[s['name']] = s

    skills = []
    problems = []
    found = discover()
    inner = spokes()
    for name_dir, folder_rel in sorted(found.items(), key=lambda kv: kv[1]):
        rel = folder_rel + '/SKILL.md'
        folder = name_dir
        parts = folder_rel.split('/')
        if len(parts) == 1 and folder not in HUB_NOTE:
            problems.append('%s: only a hub sits at the top level — file it under a realm' % rel)
        if len(parts) == 2 and parts[0] not in REALMS:
            problems.append('%s: %s/ is not a realm in skills_layout.REALMS' % (rel, parts[0]))
        fm = parse_frontmatter(rel)
        if not fm or 'name' not in fm:
            problems.append('%s: missing or unreadable frontmatter' % rel)
            continue
        name = fm['name']
        if name != folder:
            problems.append('%s: folder name != skill name (%s)' % (rel, name))
        if 'description' not in fm or not fm['description']:
            problems.append('%s: missing description' % rel)

        prev = curated.get(name, {})
        skills.append({
            'name': name,
            'path': rel,
            'description': prev.get('description') or first_sentence(fm.get('description', '')),
            'content': prev.get('content', ''),
        })

    index = {
        '$schema': 'https://json.schemastore.org/skill-index.json',
        'version': '1.1.0',
        'generated': date.today().isoformat(),
        'root': os.path.basename(ROOT),
        'count': len(skills),
        'skills': skills,
    }
    with open(INDEX, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
        f.write('\n')

    by_name = {s['name']: s for s in skills}
    n_active = len(active(found))
    lines = [
        '# Agent Skills',
        '',
        'A library of %d Claude Code skills. Three hubs sit at the top level; every other skill '
        'is filed under a realm folder named for the power that governs its kind of work. Each '
        'skill folder is named for the `name:` in its `SKILL.md`, with deep-dive material under '
        '`references/` and any executable helpers under `scripts/`.' % len(skills),
        '',
        '**%d skills load on their own**; the %d marked *via* a hub are opened by that hub, which '
        'routes to them. The active list lives in `.claude-plugin/plugin.json` and is regenerated '
        'by `build-index.py`.' % (n_active, len(inner)),
        '',
        'Conventions and the authoring checklist are in [CLAUDE.md](CLAUDE.md). '
        'The machine-readable index is [skill.json](skill.json) — regenerate it with '
        '`python scripts/build-index.py` after adding or renaming a skill.',
        '',
    ] + FINDING + INSTALL

    def row(s):
        hub = inner.get(s['name'])
        note = ' *Via %s.*' % hub if hub else ''
        return '| [%s](%s) | %s%s |' % (s['name'], s['path'], s['description'], note)

    lines += ['## Hubs — the three names to remember', '',
              '| Skill | Opens | What it does |', '| --- | --- | --- |']
    for hub, area in HUB_NOTE.items():
        if hub in by_name:
            s = by_name[hub]
            routes = ', '.join(HUBS.get(hub, [])) or '—'
            lines.append('| [%s](%s) | %s: %s | %s |' % (s['name'], s['path'], area, routes, s['description']))
    lines.append('')
    for realm, (heading, meaning) in REALMS.items():
        members = [s for s in skills if s['path'].startswith(realm + '/')]
        if not members:
            continue
        lines += ['## %s' % heading, '', '*%s*' % meaning, '', '| Skill | What it does |', '| --- | --- |']
        lines += [row(s) for s in members]
        lines.append('')

    with open(README, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))

    print('indexed %d skills -> skill.json, README.md' % len(skills))
    n, m = write_plugin_skills(found)
    print('plugin.json: %d active skills, %d spokes via %d hubs' % (n, m, len(HUBS)))
    if problems:
        print('\n%d problem(s):' % len(problems))
        for p in problems:
            print('  ' + p)
        return 1
    print('no problems found')
    return 0


if __name__ == '__main__':
    sys.exit(main())
