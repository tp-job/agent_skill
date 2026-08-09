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
    ("Frontend & UI", [
        "frontend-design", "web-design-guidelines", "google-design-system",
        "css-architecture", "ui-checker", "vercel-react-best-practices",
        "threejs-3d", "flutter",
    ]),
    ("Backend & Data", [
        "java-api-performance", "supabase-senior", "data-analyze",
    ]),
    ("Quality, Security & Performance", [
        "owasp-top-10-2025", "security", "clean-code-javascript",
        "lighthouse", "ai-web-product-craft", "debug-master",
        "tracking-and-debugging",
    ]),
    ("Process & Delivery", [
        "promethean-parthenon", "agentic-engineering",
        "long-horizon-engineering-workflow", "requirement-gathering",
        "senior-leadership-advisor", "deploy-to-vercel",
        "vercel-cli-with-tokens",
    ]),
    ("Knowledge & Authoring", [
        "knowledge-base", "skill-creator", "agent-skill-creator",
        "cs-course-designer", "obsidian-vault", "view-pdf",
    ]),
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
    placed = set()
    lines = [
        '# Agent Skills',
        '',
        'A library of %d Claude Code skills. Each lives in its own folder, named for the '
        '`name:` in its `SKILL.md`, with deep-dive material under `references/` and any '
        'executable helpers under `scripts/`.' % len(skills),
        '',
        'Conventions and the authoring checklist are in [CLAUDE.md](CLAUDE.md). '
        'The machine-readable index is [skill.json](skill.json) — regenerate it with '
        '`python scripts/build-index.py` after adding or renaming a skill.',
        '',
    ]
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
            lines.append('| [%s](%s) | %s |' % (s['name'], s['path'], s['description']))
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
    if problems:
        print('\n%d problem(s):' % len(problems))
        for p in problems:
            print('  ' + p)
        return 1
    print('no problems found')
    return 0


if __name__ == '__main__':
    sys.exit(main())
