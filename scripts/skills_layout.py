"""Where every skill lives, which skills are aggregators, and what each one bundles.

The single source of truth for the library's shape, imported by build-index.py,
build-bundles.py, check-bundles.py and lint-skills.py. Change the layout here and
nowhere else.

Layout (see CLAUDE.md §Layout):

    <hub>/SKILL.md                 an aggregator, top level — the names a user remembers
    <realm>/<skill>/SKILL.md       every other skill, filed under one realm folder

A realm is a plain directory, never a skill. A hub is named in the library's Greek
and Roman register as two words, like promethean-parthenon: the power or quality
that governs that kind of work, then its place. A realm is named as one plain,
literal English word for its category — core, design, web, stack, knowledge — so
a reader can guess where a skill lives without opening the file.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Aggregators and the skills each one routes between. A hub links to its spokes and
# carries a verbatim copy of each under <hub>/bundled/. A spoke links to nothing
# outside itself, and loads only through its hub — never on its own.
HUBS = {
    "promethean-parthenon": [
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
    ],
    "athena-erechtheion": [
        "css-architecture",
        "frontend-design",
        "google-design-system",
        "threejs-3d",
    ],
}

# Realm folder -> (heading, what it holds). Order is the README order.
REALMS = {
    "core": (
        "Core — the engineering specialists",
        "Reached only through promethean-parthenon.",
    ),
    "design": (
        "Design — the design specialists",
        "Reached only through athena-erechtheion.",
    ),
    "web": (
        "Web — web delivery and quality",
        "Speed, shipping and the quality of what reaches the user.",
    ),
    "stack": (
        "Stack — application stacks",
        "Where a particular stack is built well.",
    ),
    "knowledge": (
        "Knowledge — knowledge and teaching",
        "Reference knowledge, notes, analysis and course design.",
    ),
}

HUB_NOTE = {
    "promethean-parthenon": "engineering",
    "athena-erechtheion": "design",
    "hermes-olympus": "AI agents and MCP",
}


def spokes():
    """Every skill that loads only through a hub, mapped to that hub."""
    return {s: hub for hub, members in HUBS.items() for s in members}


def discover():
    """{skill name: path of its folder relative to ROOT}, bundled copies excluded."""
    found = {}
    for skill_md in sorted(ROOT.glob("*/SKILL.md")) + sorted(ROOT.glob("*/*/SKILL.md")):
        rel = skill_md.parent.relative_to(ROOT)
        if "bundled" in rel.parts:
            continue
        found[rel.name] = rel.as_posix()
    return found


def active(found=None):
    """Skills that load on their own: everything except the hubs' spokes."""
    found = found or discover()
    inner = spokes()
    return sorted(n for n in found if n not in inner)
