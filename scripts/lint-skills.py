#!/usr/bin/env python3
"""Lint every skill against the CLAUDE.md checklist and the limits Claude Code enforces.

Run from the repository root:

    python scripts/lint-skills.py

Exits non-zero on any finding. Complements build-index.py (names, index) and
check-bundles.py (link targets, bundle fidelity): this one checks what those two do not —
description length, negative scope, orphaned references, heading anchors, wikilinks,
stray frontmatter in reference files, mojibake, and credential-shaped strings.
"""
import collections
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skills_layout import active as active_skills, discover  # noqa: E402
DESC_LIMIT = 1536       # Claude Code truncates description + when_to_use at this length
LINE_LIMIT = 400        # CLAUDE.md: SKILL.md is a router, keep it under ~400 lines
FENCE = re.compile(r'```.*?```', re.S)
NEGATIVE = re.compile(r'(?i)\bnot for\b|do not (use|trigger)|don.t use|when not|skip (this|when|for)|instead use|use .* instead')


def frontmatter(text):
    return text.split('---', 2)[1] if text.startswith('---') else None


def description(fm):
    m = re.search(r'^description:\s*(?:>-?|\|-?)?\s*\n?(.*?)(?=\n[a-z_-]+:|\Z)', fm, re.S | re.M)
    return re.sub(r'\s+', ' ', m.group(1)).strip() if m else ''


def slug(heading):
    """GitHub heading anchor: lowercase, drop punctuation, each space becomes a hyphen."""
    h = heading.strip().lower().replace('`', '')
    return re.sub(r'\s', '-', re.sub(r'[^\w\s-]', '', h))


_anchors = {}


def anchors(path):
    if path not in _anchors:
        text = FENCE.sub('', open(path, encoding='utf-8').read())
        seen, out = {}, set()
        for h in re.findall(r'^#{1,6} (.+?)\s*#*$', text, re.M):
            s = slug(h)
            n = seen.get(s, 0)
            out.add(s if n == 0 else '%s-%d' % (s, n))
            seen[s] = n + 1
        _anchors[path] = out
    return _anchors[path]


def main():
    os.chdir(ROOT)
    found = collections.defaultdict(list)

    for skill in sorted(discover().values()):
        text = open(os.path.join(skill, 'SKILL.md'), encoding='utf-8').read()
        fm = frontmatter(text) or ''
        desc = description(fm)
        if len(desc) > DESC_LIMIT:
            found['description over %d chars (tail is truncated)' % DESC_LIMIT].append('%s (%d)' % (skill, len(desc)))
        if not re.search(r'^license:', fm, re.M):
            found['missing license'].append(skill)
        if not re.search(r'^\s+version:\s*"\d+\.\d+\.\d+"', fm, re.M):
            found['missing quoted semver metadata.version'].append(skill)
        if not re.search(r'^\s+source:', fm, re.M):
            found['missing metadata.source'].append(skill)
        lines = text.count('\n') + 1
        if lines > LINE_LIMIT:
            found['SKILL.md over %d lines' % LINE_LIMIT].append('%s (%d)' % (skill, lines))
        if not NEGATIVE.search(desc):
            found['description has no negative scope ("Not for ...")'].append(skill)
        refs = glob.glob(os.path.join(skill, 'references', '*.md'))
        pool = [os.path.join(skill, 'SKILL.md')] + refs
        for ref in refs:
            name = os.path.basename(ref)
            if not any(name in open(p, encoding='utf-8').read() for p in pool if p != ref):
                found['orphaned reference (nothing links to it)'].append(ref)

    for path in glob.glob('**/*.md', recursive=True):
        norm = path.replace('\\', '/')
        if '/bundled/' in norm or norm.startswith('node_modules/'):
            continue
        raw = open(path, encoding='utf-8', errors='replace').read()
        body = FENCE.sub('', raw)
        if '�' in raw or re.search(r'Ã[©¨]|â€[”“™˜œ"]', raw):
            found['mojibake / broken encoding'].append(path)
        if re.search(r'(?<!`)\[\[[^\]]+\]\](?!`)', body):
            found['Obsidian wikilink (use a relative markdown link)'].append(path)
        if '/references/' in norm and raw.startswith('---') and re.search(r'^name:', frontmatter(raw) or '', re.M):
            found['skill frontmatter inside a reference file'].append(path)
        if re.search(r'sk-ant-[A-Za-z0-9_-]{10,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|xox[bp]-[0-9A-Za-z-]{10,}', raw):
            found['credential-shaped string'].append(path)
        if re.search(r'[A-Za-z]:\\Users\\[^\\\s]+|/Users/[a-z][\w.-]+/|/home/[a-z][\w.-]+/', body):
            found['personal path'].append(path)
        for target, anchor in re.findall(r'\]\(([^)\s#]*)#([^)\s]+)\)', body):
            if target.startswith(('http:', 'https:', 'mailto:')):
                continue
            dest = os.path.normpath(os.path.join(os.path.dirname(path), target)) if target else path
            if os.path.isfile(dest) and anchor.lower() not in anchors(dest):
                found['broken heading anchor'].append('%s -> %s#%s' % (path, target, anchor))

    # A namespaced `agent-skill:<name>` only exists for skills in the active set, and a
    # lookup row saying a skill opens "itself" is only true of an active skill; core
    # spokes load through the aggregator. Both slipped into README once — keep them out.
    active = set(active_skills())
    scanned = ['README.md', 'CLAUDE.md'] + glob.glob('scripts/*.py') + [
        p for p in glob.glob('*/**/*.md', recursive=True) if '/bundled/' not in p.replace(os.sep, '/')]
    for path in scanned:
        text = open(path, encoding='utf-8').read()
        for name in sorted(set(re.findall(r'agent-skill:([a-z0-9-]+)', text))):
            if name not in active:
                found['namespaced example names an inactive skill'].append('%s -> agent-skill:%s' % (path, name))
    for name in re.findall(r'^\| `([a-z0-9-]+)`[^\n]*\| itself \|$', open('README.md', encoding='utf-8').read(), re.M):
        if name not in active:
            found['lookup says a core spoke opens by itself'].append(name)

    total = sum(len(v) for v in found.values())
    for kind in sorted(found):
        print('%s: %d' % (kind, len(found[kind])))
        for item in found[kind]:
            print('    ' + item)
    print('no problems found' if total == 0 else '\n%d problem(s)' % total)
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
