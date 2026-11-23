"""Zip the active skill set for upload to claude.ai, so it runs the same skills as Claude Code.

Claude Code loads the active set from the plugin (.claude-plugin/plugin.json, generated
by build-index.py). claude.ai takes skills one zip at a time under Settings → Capabilities
→ Skills. This script makes one zip per active skill from the same folders, so both
places run one source:

    python scripts/build-claude-ai.py            # writes dist/claude-ai/<skill>.zip
    python scripts/build-claude-ai.py --check    # checks only, writes nothing

Each zip holds the skill's folder at its root (<skill>/SKILL.md, references/, ...).
Hubs carry their bundled/ copies, so a hub works on claude.ai with nothing else
uploaded. Spokes are not zipped: like the plugin, claude.ai reaches them through
their hub. Run build-bundles.py first so the copies are current.

Exits non-zero when a skill folder is missing, has no SKILL.md, its name: differs from
the folder, or its description is over the 1,024-character upload limit.
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "claude-ai"
SKIP_DIRS = {"__pycache__", ".git", "node_modules"}
SKIP_SUFFIXES = {".pyc", ".pyo"}
LIMIT = 1024


def active_skills() -> list[Path]:
    manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    return [(ROOT / entry).resolve() for entry in manifest.get("skills", [])]


def frontmatter(skill_md: Path) -> dict[str, str]:
    text = skill_md.read_text(encoding="utf-8")
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if match is None:
        return {}
    block = match.group(1)
    name = re.search(r"^name:\s*(\S+)", block, re.M)
    desc = re.search(r"^description:\s*>-\n((?:  .*\n?)+)", block, re.M)
    description = " ".join(line.strip() for line in desc.group(1).splitlines()) if desc else ""
    return {"name": name.group(1) if name else "", "description": description}


def files_of(folder: Path):
    for path in sorted(folder.rglob("*")):
        if path.is_dir() or path.suffix in SKIP_SUFFIXES:
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(folder).parts):
            continue
        yield path


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    problems: list[str] = []
    built: list[tuple[str, int, int]] = []

    if not check_only:
        OUT.mkdir(parents=True, exist_ok=True)

    for folder in active_skills():
        skill_md = folder / "SKILL.md"
        if not skill_md.is_file():
            problems.append(f"{folder.relative_to(ROOT)}: no SKILL.md")
            continue
        meta = frontmatter(skill_md)
        if meta.get("name") != folder.name:
            problems.append(f"{folder.name}: name: is {meta.get('name')!r}, not the folder name")
        if len(meta.get("description", "")) > LIMIT:
            problems.append(f"{folder.name}: description is {len(meta['description'])} characters (limit {LIMIT})")

        files = list(files_of(folder))
        if not check_only:
            target = OUT / f"{folder.name}.zip"
            with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
                for path in files:
                    zf.write(path, Path(folder.name) / path.relative_to(folder))
            built.append((folder.name, len(files), target.stat().st_size))

    for problem in problems:
        print(f"problem: {problem}")

    if check_only:
        print(f"checked {len(active_skills())} active skills")
    else:
        for name, count, size in built:
            print(f"{name}.zip  {count} files  {size // 1024} KB")
        print(f"wrote {len(built)} zips to {OUT.relative_to(ROOT)}")
        print("Upload each on claude.ai (Settings → Capabilities → Skills), replacing the old copy,")
        print("and turn off the claude.ai plugin that holds the same skills so each loads once.")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
