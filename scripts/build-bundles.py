#!/usr/bin/env python3
"""Regenerate every hub's `bundled/` directory from its source skills.

Skills are hub-and-spoke, not mesh: an ordinary skill is a standalone
component and must not link to another skill. Only a hub — an aggregator
listed in `skills_layout.HUBS` — may link out to the skills it routes
between, and it carries a verbatim copy of each under `bundled/` so the
folder still works when copied out of this library on its own. Run from the
repository root after editing a hub or any skill it bundles:

    python scripts/build-bundles.py

Idempotent. Because spokes carry no outbound cross-skill links, a bundled
copy needs no link-depth rewriting and a hub never bundles itself.

Verify the result with `python scripts/check-bundles.py`.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skills_layout import HUBS, ROOT, discover  # noqa: E402

IGNORE = shutil.ignore_patterns("bundled", "__pycache__", ".DS_Store")


def main():
    found = discover()
    status = 0
    for hub, members in HUBS.items():
        if hub not in found:
            print("hub skill missing: " + hub)
            status = 1
            continue
        missing = [n for n in members if n not in found]
        if missing:
            print("%s bundles a skill that does not exist: %s" % (hub, ", ".join(missing)))
            status = 1
            continue
        dest = ROOT / found[hub] / "bundled"
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir()
        for name in members:
            shutil.copytree(ROOT / found[name], dest / name, ignore=IGNORE)
        print("%s/bundled/ <- %d skills" % (hub, len(members)))
    return status


if __name__ == "__main__":
    os.chdir(ROOT)
    sys.exit(main())
