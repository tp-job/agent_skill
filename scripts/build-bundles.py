#!/usr/bin/env python3
"""Regenerate the `bundled/` directory of every skill that carries one.

A skill folder has to work when copied out of this library on its own, so a
skill that links to another skill ships a verbatim copy of it under
`bundled/`. Run from the repository root after editing any skill in the
closure:

    python scripts/build-bundles.py

Idempotent. Sources are staged with `bundled/` excluded and with any
`bundled/x/` link normalised back to the sibling `../x/` form, so a copy
placed inside a bundle resolves against its bundle siblings.

Verify the result with `python scripts/check-bundles.py`.
"""
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The link closure of the bundling cluster: every skill reachable by a relative
# markdown link from any host below. Add a skill here the moment a host links
# to it, or that host's copy will dangle.
CLOSURE = [
    "agentic-engineering",
    "debug-master",
    "github-report",
    "long-horizon-engineering-workflow",
    "owasp-top-10-2025",
    "project-file-structure",
    "promethean-parthenon",
    "requirement-gathering",
    "senior-leadership-advisor",
    "skill-creator",
    "ui-checker",
]

# The skills that carry a bundle. Each gets the full closure, including its own
# copy — bundled skills link back at their host.
HOSTS = [
    "promethean-parthenon",
    "agentic-engineering",
    "long-horizon-engineering-workflow",
    "senior-leadership-advisor",
    "github-report",
]

IGNORE = shutil.ignore_patterns("bundled", "__pycache__", ".DS_Store")


def link_prefix(depth, name, inside_bundle):
    """How a file `depth` levels below a skill root refers to skill `name`."""
    if inside_bundle:
        return "](" + "../" * depth + "bundled/" + name + "/"
    return "](" + "../" * (depth + 1) + name + "/"


def rewrite(root, to_bundle, skip_bundled=False):
    """Flip cross-skill links under `root` between the two schemes."""
    for md in sorted(root.rglob("*.md")):
        rel = md.relative_to(root)
        if skip_bundled and "bundled" in rel.parts:
            continue
        depth = len(rel.parts) - 1
        text = original = md.read_text(encoding="utf-8")
        for name in CLOSURE:
            src = link_prefix(depth, name, not to_bundle)
            dst = link_prefix(depth, name, to_bundle)
            text = text.replace(src, dst)
        if text != original:
            md.write_text(text, encoding="utf-8", newline="\n")
            yield md


def main():
    missing = [n for n in CLOSURE if not (ROOT / n / "SKILL.md").is_file()]
    if missing:
        print("closure names a skill that does not exist: " + ", ".join(missing))
        return 1
    if not set(HOSTS) <= set(CLOSURE):
        print("every host must also appear in the closure — its copies link back at it")
        return 1

    stage = Path(tempfile.mkdtemp(prefix="skill-bundle-"))
    try:
        for name in CLOSURE:
            shutil.copytree(ROOT / name, stage / name, ignore=IGNORE)
            list(rewrite(stage / name, to_bundle=False))

        for host in HOSTS:
            # The host's own files point into its bundle, not out of the folder.
            for md in rewrite(ROOT / host, to_bundle=True, skip_bundled=True):
                print("  repointed %s" % md.relative_to(ROOT).as_posix())
            dest = ROOT / host / "bundled"
            if dest.exists():
                shutil.rmtree(dest)
            dest.mkdir()
            for name in CLOSURE:
                shutil.copytree(stage / name, dest / name)
            print("%s/bundled/ <- %d skills" % (host, len(CLOSURE)))
    finally:
        shutil.rmtree(stage, ignore_errors=True)

    print("\nbundled %d skills into %d hosts" % (len(CLOSURE), len(HOSTS)))
    return 0


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(main())
