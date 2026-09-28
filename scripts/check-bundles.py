#!/usr/bin/env python3
"""Verify the hub-and-spoke invariant and every relative markdown link.

    python scripts/check-bundles.py

Three checks, all of which must pass:

1. **Spokes are link-free.** Every skill that is not a hub must carry no
   relative link into another skill's folder, and no `bundled/` directory of
   its own. A skill is a standalone component; only a hub combines them, and a
   hub may link only into its own `bundled/`.
2. **Each hub's bundle is exact.** `<hub>/bundled/` holds a byte-identical copy
   of every skill the hub lists in `skills_layout.HUBS` — no summarising, no
   trimming, no drift from the source.
3. **Links resolve.** Every relative markdown link in the repository points at
   a file that exists.

Exits non-zero on any failure. Regenerate with `python scripts/build-bundles.py`.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skills_layout import HUBS, ROOT, discover  # noqa: E402

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")
# Documentation and report templates carry deliberate placeholders in link
# position: `<file-name>`, `<url>`, and the ellipsis stand-in for an elided URL.
PLACEHOLDER = re.compile(r"[<>…]")

FOUND = discover()
SKILL_DIRS = {name: (ROOT / rel).resolve() for name, rel in FOUND.items()}


def files_under(root):
    return sorted(
        p.relative_to(root)
        for p in root.rglob("*")
        if p.is_file() and "bundled" not in p.relative_to(root).parts
    )


def owner(path):
    """The skill whose source folder contains `path`, or None."""
    for name, d in SKILL_DIRS.items():
        if path == d or d in path.parents:
            return name
    return None


def cross_skill_links(skill):
    """Relative links in `skill`'s own files that resolve into another skill's folder."""
    root = SKILL_DIRS[skill]
    hits = []
    for md in sorted(root.rglob("*.md")):
        if "bundled" in md.relative_to(root).parts:
            continue
        for lineno, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            for m in LINK.finditer(line):
                href = m.group(1).split("#")[0]
                if not href or href.startswith(("http://", "https://", "mailto:")) or PLACEHOLDER.search(href):
                    continue
                target = (md.parent / href).resolve()
                if "bundled" in target.relative_to(ROOT).parts if ROOT in target.parents else False:
                    if skill in HUBS and root / "bundled" in target.parents:
                        continue  # a hub linking into its own bundle
                    hits.append((md, lineno, m.group(1)))
                    continue
                other = owner(target)
                if other and other != skill:
                    hits.append((md, lineno, m.group(1)))
    return hits


def check_spokes():
    problems = []
    for skill in sorted(FOUND):
        root = SKILL_DIRS[skill]
        if skill not in HUBS and (root / "bundled").exists():
            problems.append("%s: only a hub may carry a bundled/ directory" % FOUND[skill])
        for md, lineno, href in cross_skill_links(skill):
            problems.append(
                "%s:%d: links to another skill (%s) — %s"
                % (md.relative_to(ROOT).as_posix(), lineno, href,
                   "a hub links only into its own bundled/" if skill in HUBS else "inline the mention instead")
            )
    print("spokes: %d skill(s) checked for cross-skill links" % len(FOUND))
    return problems


def check_bundles():
    problems = []
    exact = 0
    for hub, members in HUBS.items():
        bundle = ROOT / FOUND.get(hub, hub) / "bundled"
        if not bundle.is_dir():
            problems.append("%s: no bundled/ directory" % hub)
            continue
        extra = sorted(p.name for p in bundle.iterdir() if p.is_dir())
        for name in set(extra) - set(members):
            problems.append("%s/bundled/%s: not in the hub's list" % (hub, name))
        for name in members:
            src, dst = ROOT / FOUND[name], bundle / name
            if not dst.is_dir():
                problems.append("%s/bundled/: missing %s" % (hub, name))
                continue
            sf, df = files_under(src), files_under(dst)
            if sf != df:
                for f in set(sf) ^ set(df):
                    problems.append("%s/bundled/%s: file set differs (%s)" % (hub, name, f.as_posix()))
                continue
            for f in sf:
                if (src / f).read_bytes() == (dst / f).read_bytes():
                    exact += 1
                else:
                    problems.append("%s/bundled/%s/%s: content differs from the source" % (hub, name, f.as_posix()))
    print("bundles: %d hub(s), %d file(s) byte-identical" % (len(HUBS), exact))
    return problems


def check_links():
    problems = []
    checked = 0
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        fenced = False
        for lineno, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced:
                continue
            for m in LINK.finditer(line):
                href = m.group(1)
                if href.startswith(("http://", "https://", "#", "mailto:")) or PLACEHOLDER.search(href):
                    continue
                path = href.split("#")[0]
                if not path:
                    continue
                checked += 1
                if not (md.parent / path).resolve().exists():
                    problems.append("%s:%d: dangling link -> %s" % (md.relative_to(ROOT).as_posix(), lineno, href))
    print("links: %d relative link(s) checked" % checked)
    return problems


def main():
    problems = check_spokes() + check_bundles() + check_links()
    if problems:
        print("\n%d problem(s):" % len(problems))
        for p in problems:
            print("  " + p)
        return 1
    print("no problems found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
