#!/usr/bin/env python3
"""Regenerate `promethean-parthenon/bundled/` from its source skills.

Skills are hub-and-spoke, not mesh: an ordinary skill is a standalone
component and must not link to another skill. Only an aggregator — today,
`promethean-parthenon` — is allowed to link out to the skills it routes
between, and it carries a verbatim copy of each under `bundled/` so the
folder still works when copied out of this library on its own. Run from the
repository root after editing `promethean-parthenon` or any skill it links to:

    python scripts/build-bundles.py

Idempotent. Because spokes carry no outbound cross-skill links, a bundled
copy needs no link-depth rewriting and the aggregator does not need to bundle
a copy of itself — nothing inside the bundle links back to it.

Verify the result with `python scripts/check-bundles.py`.
"""
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# The aggregator, and the skills it links to directly. Every one of these must
# itself be link-free (checked below) — if a skill in here ever needs to link
# to another skill, it becomes an aggregator too and this list grows.
HOST = "promethean-parthenon"

CLOSURE = [
    "agentic-engineering",
    "debug-master",
    "github-report",
    "long-horizon-engineering-workflow",
    "owasp-top-10-2025",
    "project-file-structure",
    "requirement-gathering",
    "senior-leadership-advisor",
    "skill-creator",
    "ui-checker",
]

IGNORE = shutil.ignore_patterns("bundled", "__pycache__", ".DS_Store")


def main():
    missing = [n for n in CLOSURE if not (ROOT / n / "SKILL.md").is_file()]
    if missing:
        print("closure names a skill that does not exist: " + ", ".join(missing))
        return 1
    if (ROOT / HOST / "bundled").exists() is False and not (ROOT / HOST / "SKILL.md").is_file():
        print("host skill missing: " + HOST)
        return 1

    dest = ROOT / HOST / "bundled"
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir()
    for name in CLOSURE:
        shutil.copytree(ROOT / name, dest / name, ignore=IGNORE)
    print("%s/bundled/ <- %d skills" % (HOST, len(CLOSURE)))
    return 0


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(main())
