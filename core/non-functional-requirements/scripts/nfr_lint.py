#!/usr/bin/env python3
"""Lint the NFR table in a spec written from assets/nfr-spec.template.md.

Finds the first markdown table whose header contains ID, Scale, Meter, Condition,
Must and Source, then reports, per row:
  - required cells that are empty (Scale, Meter, Condition, Must, Source)
  - a Must with no digit (a threshold needs a number, or a 0/100% style value)
  - vague words (English and Thai) anywhere in the row while Must has no digit

Usage:  python nfr_lint.py nfr-spec.md
Exit:   0 clean, 1 findings, 2 no NFR table found.
Python 3.10+, standard library only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED = ["Scale", "Meter", "Condition", "Must", "Source"]
VAGUE = [
    "fast", "quick", "responsive", "efficient", "easy", "simple", "intuitive",
    "user-friendly", "secure", "robust", "reliable", "stable", "scalable",
    "flexible", "appropriate", "adequate", "sufficient", "as soon as possible",
    "เร็ว", "ใช้งานง่าย", "ง่าย", "มีประสิทธิภาพ", "ปลอดภัย", "เสถียร",
    "รองรับ", "เหมาะสม", "เพียงพอ", "ยืดหยุ่น", "โดยเร็ว",
]


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def find_table(lines: list[str]) -> tuple[list[str], list[tuple[int, list[str]]]] | None:
    for i, line in enumerate(lines):
        if not line.lstrip().startswith("|"):
            continue
        header = cells(line)
        lowered = [h.lower() for h in header]
        if "id" in lowered and all(r.lower() in lowered for r in REQUIRED):
            rows = []
            for j in range(i + 2, len(lines)):
                if not lines[j].lstrip().startswith("|"):
                    break
                rows.append((j + 1, cells(lines[j])))
            return header, rows
    return None


def lint(text: str) -> list[str] | None:
    found = find_table(text.splitlines())
    if found is None:
        return None
    header, rows = found
    idx = {h.lower(): k for k, h in enumerate(header)}
    problems: list[str] = []
    for lineno, row in rows:
        row = row + [""] * (len(header) - len(row))
        rid = row[idx["id"]] or f"line {lineno}"
        for field in REQUIRED:
            if not row[idx[field.lower()]]:
                problems.append(f"{rid} (line {lineno}): {field} is empty")
        must = row[idx["must"]]
        if must and not re.search(r"\d", must):
            problems.append(f"{rid} (line {lineno}): Must has no number: {must!r}")
        if not re.search(r"\d", must):
            joined = " ".join(row).lower()
            hits = [w for w in VAGUE if re.search(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", joined)
                    or (not w.isascii() and w in joined)]
            if hits:
                problems.append(f"{rid} (line {lineno}): vague word(s) with no numeric threshold: {', '.join(sorted(set(hits)))}")
    return problems


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 0 if len(argv) == 2 else 2
    text = Path(argv[1]).read_text(encoding="utf-8")
    problems = lint(text)
    if problems is None:
        print("no NFR table found (need columns: ID, " + ", ".join(REQUIRED) + ")")
        return 2
    for p in problems:
        print(p)
    print("no problems found" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
