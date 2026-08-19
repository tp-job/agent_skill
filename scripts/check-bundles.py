#!/usr/bin/env python3
"""Verify the hub-and-spoke invariant and every relative markdown link.

    python scripts/check-bundles.py

Three checks, all of which must pass:

1. **Spokes are link-free.** Every skill except the aggregator
   (`promethean-parthenon`) must carry no relative link to another skill's
   folder, and no `bundled/` directory of its own. A skill is a standalone
   component; only the aggregator combines them.
2. **The aggregator's bundle is exact.** `promethean-parthenon/bundled/`
   holds a byte-identical copy of every skill in its closure — no
   summarising, no trimming, no drift from the source.
3. **Links resolve.** Every relative markdown link in the repository points
   at a file that exists.

Exits non-zero on any failure. Regenerate with `python scripts/build-bundles.py`.
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module

_build = import_module("build-bundles")
HOST, CLOSURE = _build.HOST, _build.CLOSURE

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")
# Documentation and report templates carry deliberate placeholders in link
# position: `<file-name>`, `<url>`, and the ellipsis stand-in for an elided URL.
PLACEHOLDER = re.compile(r"[<>…]")

ALL_SKILLS = sorted(p.parent.name for p in ROOT.glob("*/SKILL.md"))


def files_under(root):
    return sorted(
        p.relative_to(root)
        for p in root.rglob("*")
        if p.is_file() and "bundled" not in p.relative_to(root).parts
    )


def cross_skill_links(root):
    """Relative links inside `root` that point at another skill's folder."""
    hits = []
    for md in sorted(root.rglob("*.md")):
        if "bundled" in md.relative_to(root).parts:
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for m in LINK.finditer(line):
                href = m.group(1)
                if not href.startswith("../") and "bundled/" not in href:
                    continue
                # ../<skill>/... or bundled/<skill>/...
                parts = href.split("/")
                name = parts[1] if parts[0] in ("..", "bundled") else None
                if name in ALL_SKILLS:
                    hits.append((md, lineno, href))
    return hits


def check_spokes():
    problems = []
    checked = 0
    for skill in ALL_SKILLS:
        if skill == HOST:
            continue
        checked += 1
        root = ROOT / skill
        if (root / "bundled").exists():
            problems.append("%s: spoke skill must not carry a bundled/ directory" % skill)
        for md, lineno, href in cross_skill_links(root):
            problems.append(
                "%s:%d: spoke skill links to another skill (%s) — inline the mention instead"
                % (md.relative_to(ROOT).as_posix(), lineno, href)
            )
    print("spokes: %d skill(s) checked for cross-skill links" % checked)
    return problems


def check_bundle():
    problems = []
    exact = 0
    bundle = ROOT / HOST / "bundled"
    if not bundle.is_dir():
        return ["%s: no bundled/ directory" % HOST]
    extra = sorted(p.name for p in bundle.iterdir() if p.is_dir())
    for name in set(extra) - set(CLOSURE):
        problems.append("%s/bundled/%s: not in the closure" % (HOST, name))
    for name in CLOSURE:
        src, dst = ROOT / name, bundle / name
        if not dst.is_dir():
            problems.append("%s/bundled/: missing %s" % (HOST, name))
            continue
        sf, df = files_under(src), files_under(dst)
        if sf != df:
            for f in set(sf) ^ set(df):
                problems.append(
                    "%s/bundled/%s: file set differs (%s)" % (HOST, name, f.as_posix())
                )
            continue
        for f in sf:
            a, b = (src / f).read_bytes(), (dst / f).read_bytes()
            if a == b:
                exact += 1
            else:
                problems.append(
                    "%s/bundled/%s/%s: content differs from the source"
                    % (HOST, name, f.as_posix())
                )
    print("bundle: %d file(s) byte-identical" % exact)
    return problems


def check_links():
    problems = []
    checked = 0
    for md in sorted(ROOT.rglob("*.md")):
        fenced = False
        for lineno, line in enumerate(
            md.read_text(encoding="utf-8", errors="replace").splitlines(), 1
        ):
            if FENCE.match(line):
                fenced = not fenced
                continue
            if fenced:
                continue
            for m in LINK.finditer(line):
                href = m.group(1)
                if href.startswith(("http://", "https://", "#", "mailto:")):
                    continue
                if PLACEHOLDER.search(href):
                    continue
                path = href.split("#")[0]
                if not path:
                    continue
                checked += 1
                if not (md.parent / path).resolve().exists():
                    problems.append(
                        "%s:%d: dangling link -> %s"
                        % (md.relative_to(ROOT).as_posix(), lineno, href)
                    )
    print("links: %d relative link(s) checked" % checked)
    return problems


def main():
    problems = check_spokes() + check_bundle() + check_links()
    if problems:
        print("\n%d problem(s):" % len(problems))
        for p in problems:
            print("  " + p)
        return 1
    print("no problems found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
