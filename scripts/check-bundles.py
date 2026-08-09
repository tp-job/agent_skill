#!/usr/bin/env python3
"""Verify bundled skill copies and every relative markdown link in the library.

    python scripts/check-bundles.py

Three checks, all of which must pass:

1. **Closure** — every host bundles every skill in the closure, including
   itself, with the same file set as the source.
2. **Fidelity** — each bundled file is byte-identical to its source, except
   that a cross-skill link may sit at a different depth (`bundled/x/` at the
   library root vs `../x/` inside a bundle). Nothing else may differ.
3. **Links** — every relative markdown link in the repository resolves to a
   file that exists, bundled copies included.

Exits non-zero on any failure. Regenerate with `python scripts/build-bundles.py`.
"""
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from importlib import import_module

_build = import_module("build-bundles")
CLOSURE, HOSTS = _build.CLOSURE, _build.HOSTS

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+?)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")
# Documentation and report templates carry deliberate placeholders in link
# position: `<file-name>`, `<url>`, and the ellipsis stand-in for an elided URL.
PLACEHOLDER = re.compile(r"[<>…]")


def canonical(text):
    """Collapse both link schemes onto one marker so only real edits survive."""
    for name in CLOSURE:
        text = re.sub(
            r"\]\((?:\.\./)*(?:bundled/)?" + re.escape(name) + "/",
            "](@" + name + "/",
            text,
        )
    return text


def files_under(root):
    return sorted(
        p.relative_to(root)
        for p in root.rglob("*")
        if p.is_file() and "bundled" not in p.relative_to(root).parts
    )


def check_bundles():
    problems = []
    exact = shifted = 0
    for host in HOSTS:
        bundle = ROOT / host / "bundled"
        if not bundle.is_dir():
            problems.append("%s: no bundled/ directory" % host)
            continue
        extra = sorted(p.name for p in bundle.iterdir() if p.is_dir())
        for name in set(extra) - set(CLOSURE):
            problems.append("%s/bundled/%s: not in the closure" % (host, name))
        for name in CLOSURE:
            src, dst = ROOT / name, bundle / name
            if not dst.is_dir():
                problems.append("%s/bundled/: missing %s" % (host, name))
                continue
            sf, df = files_under(src), files_under(dst)
            if sf != df:
                for f in set(sf) ^ set(df):
                    problems.append(
                        "%s/bundled/%s: file set differs (%s)" % (host, name, f.as_posix())
                    )
                continue
            for f in sf:
                a, b = (src / f).read_bytes(), (dst / f).read_bytes()
                if a == b:
                    exact += 1
                elif f.suffix == ".md" and canonical(a.decode("utf-8")) == canonical(
                    b.decode("utf-8")
                ):
                    shifted += 1
                else:
                    problems.append(
                        "%s/bundled/%s/%s: content differs from the source"
                        % (host, name, f.as_posix())
                    )
    print(
        "bundles: %d file(s) byte-identical, %d identical but for link depth"
        % (exact, shifted)
    )
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
    problems = check_bundles() + check_links()
    if problems:
        print("\n%d problem(s):" % len(problems))
        for p in problems:
            print("  " + p)
        return 1
    print("no problems found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
