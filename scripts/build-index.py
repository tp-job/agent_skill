#!/usr/bin/env python3
"""Regenerate skill.json and README.md from the SKILL.md files on disk.

Run from the repository root after adding, renaming, or removing a skill:

    python scripts/build-index.py

Curated `description` and `content` summaries already present in skill.json are
preserved and re-keyed by skill name, so hand-written summaries survive a
rebuild. A skill with no curated entry falls back to its frontmatter
description, truncated at the first sentence.
"""
import glob
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, 'skill.json')
README = os.path.join(ROOT, 'README.md')

# Grouping is editorial — a skill not listed here lands in "Other".
GROUPS = [
    ("Design & Agent Orchestration", [
        "master-design", "master-agent",
    ]),
    ("Frontend & UI", [
        "frontend-design", "google-design-system",
        "css-architecture", "ui-checker", "vercel-react-best-practices",
        "threejs-3d", "flutter",
    ]),
    ("Backend & Data", [
        "java-api-performance", "supabase-senior", "data-analyze",
    ]),
    ("Quality, Security & Performance", [
        "owasp-top-10-2025", "clean-code-javascript",
        "lighthouse", "ai-web-product-craft", "debug-master",
    ]),
    ("Process & Delivery", [
        "promethean-parthenon", "agentic-engineering",
        "long-horizon-engineering-workflow", "requirement-gathering",
        "senior-leadership-advisor", "deploy-to-vercel",
        "vercel-cli-with-tokens", "github-report",
    ]),
    ("Knowledge & Authoring", [
        "knowledge-base", "skill-creator", "project-file-structure",
        "cs-course-designer", "obsidian-vault",
    ]),
]

# Inserted verbatim right after the intro, before Install. Skills fire from their
# `description` automatically — a user should never need to remember a folder name to
# get one. Keep this short; it is a pointer to that fact, not a full lookup table.
FINDING = [
    "## Finding a skill without knowing its name",
    "",
    "You do not need to remember any name on this page. Claude Code reads each active skill's "
    "`description` and opens the matching one on its own; the *Core* skills are opened by "
    "[promethean-parthenon](promethean-parthenon/SKILL.md), whose description carries their "
    "triggers. Either way, describe the task in plain language and let it pick.",
    "",
    "| Instead of recalling… | Just say… | Opens via |",
    "| --- | --- | --- |",
    "| `debug-master` | \"why is this not working\" | promethean-parthenon |",
    "| `owasp-top-10-2025` | \"is this secure\" | promethean-parthenon |",
    "| `ui-checker` | \"does dark mode work on this page\" | promethean-parthenon |",
    "| `agentic-engineering` / `requirement-gathering` | \"plan this build\" | promethean-parthenon |",
    "| `master-design` | \"design this screen from scratch\" | itself |",
    "| `master-agent` | \"which MCP server should handle this\" | itself |",
    "| `deploy-to-vercel` | \"deploy this app\" | itself |",
    "",
    "Unsure which skill fits, or the request spans several? Say that — "
    "\"which skill should I use\" is itself a promethean-parthenon trigger. A name is only "
    "needed to invoke an *active* skill directly by its namespaced form "
    "(`agent-skill:promethean-parthenon`), which is optional; *Core* skills have no "
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


def core_spokes():
    """Skills reached only through the aggregator: the CLOSURE list in build-bundles.py."""
    src = open(os.path.join(ROOT, 'scripts', 'build-bundles.py'), encoding='utf-8').read()
    start = src.index('CLOSURE = [')
    return re.findall(r'"([a-z0-9-]+)"', src[start:src.index(']', start)])


def write_plugin_skills(names):
    """Active set = every skill except the core spokes, which load via promethean-parthenon."""
    spokes = set(core_spokes())
    with open(PLUGIN, encoding='utf-8') as f:
        manifest = json.load(f)
    manifest['skills'] = ['./' + n for n in sorted(names) if n not in spokes]
    with open(PLUGIN, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write('\n')
    return len(manifest['skills']), len(spokes)


def main():
    os.chdir(ROOT)

    curated = {}
    if os.path.exists(INDEX):
        old = json.load(open(INDEX, encoding='utf-8'))
        for s in old.get('skills', []):
            curated[s['name']] = s

    skills = []
    problems = []
    for path in sorted(glob.glob('*/SKILL.md')):
        rel = path.replace(os.sep, '/')
        folder = rel.split('/')[0]
        fm = parse_frontmatter(path)
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
    spokes = set(core_spokes())
    placed = set()
    lines = [
        '# Agent Skills',
        '',
        'A library of %d Claude Code skills. Each lives in its own folder, named for the '
        '`name:` in its `SKILL.md`, with deep-dive material under `references/` and any '
        'executable helpers under `scripts/`.' % len(skills),
        '',
        '**%d skills load on their own**; the %d marked *Core* are reached through '
        '[promethean-parthenon](promethean-parthenon/SKILL.md), which routes to them. '
        'The active list lives in `.claude-plugin/plugin.json` and is regenerated by `build-index.py`.' % (len(skills) - len(spokes), len(spokes)),
        '',
        'Conventions and the authoring checklist are in [CLAUDE.md](CLAUDE.md). '
        'The machine-readable index is [skill.json](skill.json) — regenerate it with '
        '`python scripts/build-index.py` after adding or renaming a skill.',
        '',
    ] + FINDING + INSTALL
    for title, members in GROUPS:
        present = [m for m in members if m in by_name]
        if not present:
            continue
        lines.append('## %s' % title)
        lines.append('')
        lines.append('| Skill | What it does |')
        lines.append('| --- | --- |')
        for m in present:
            s = by_name[m]
            placed.add(m)
            note = ' *Core — loads via promethean-parthenon.*' if m in spokes else ''
            lines.append('| [%s](%s) | %s%s |' % (s['name'], s['path'], s['description'], note))
        lines.append('')

    rest = [s for s in skills if s['name'] not in placed]
    if rest:
        lines += ['## Other', '', '| Skill | What it does |', '| --- | --- |']
        for s in rest:
            lines.append('| [%s](%s) | %s |' % (s['name'], s['path'], s['description']))
        lines.append('')

    with open(README, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))

    print('indexed %d skills -> skill.json, README.md' % len(skills))
    active, spokes = write_plugin_skills([s['name'] for s in skills])
    print('plugin.json: %d active skills, %d core spokes via promethean-parthenon' % (active, spokes))
    if problems:
        print('\n%d problem(s):' % len(problems))
        for p in problems:
            print('  ' + p)
        return 1
    print('no problems found')
    return 0


if __name__ == '__main__':
    sys.exit(main())
