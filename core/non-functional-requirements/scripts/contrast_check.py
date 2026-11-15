#!/usr/bin/env python3
"""WCAG 2.x contrast ratios for color pairs, checked against AA and AAA.

Input CSV with a header row:  name,foreground,background,kind
  foreground / background : hex colors, #RGB or #RRGGBB (no alpha)
  kind                    : text (default) | large | non-text

Thresholds (WCAG 2.2):
  text      AA 4.5   AAA 7.0   (SC 1.4.3 / 1.4.6)
  large     AA 3.0   AAA 4.5   (>= 24px, or >= 18.66px bold)
  non-text  AA 3.0   AAA  -    (SC 1.4.11: borders, icons, chart marks, focus)

Usage:  python contrast_check.py pairs.csv
        python contrast_check.py --pair "#767676" "#FFFFFF"
Exit:   0 all pass AA, 1 any AA failure.
Python 3.10+, standard library only.

>>> round(ratio("#767676", "#FFFFFF"), 2)
4.54
>>> round(ratio("#000", "#fff"), 1)
21.0
"""
from __future__ import annotations

import csv
import sys

AA = {"text": 4.5, "large": 3.0, "non-text": 3.0}
AAA = {"text": 7.0, "large": 4.5, "non-text": None}


def parse_hex(value: str) -> tuple[float, float, float]:
    h = value.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"not a #RGB/#RRGGBB color: {value!r}")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))  # type: ignore[return-value]


def luminance(value: str) -> float:
    def lin(c: float) -> float:
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in parse_hex(value))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: str, bg: str) -> float:
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def verdict(r: float, kind: str) -> tuple[str, str]:
    aa = "pass" if r >= AA[kind] else "FAIL"
    aaa_t = AAA[kind]
    aaa = "n/a" if aaa_t is None else ("pass" if r >= aaa_t else "fail")
    return aa, aaa


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 0
    if argv[1] == "--pair" and len(argv) >= 4:
        kind = argv[4] if len(argv) > 4 else "text"
        rows = [{"name": "pair", "foreground": argv[2], "background": argv[3], "kind": kind}]
    else:
        with open(argv[1], newline="", encoding="utf-8-sig") as fh:
            rows = list(csv.DictReader(fh))
    failed = 0
    print("| Name | Foreground | Background | Kind | Ratio | AA | AAA |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for row in rows:
        kind = (row.get("kind") or "text").strip().lower()
        if kind not in AA:
            raise SystemExit(f"unknown kind {kind!r} in row {row.get('name')!r}")
        r = ratio(row["foreground"], row["background"])
        aa, aaa = verdict(r, kind)
        failed += aa == "FAIL"
        # Floor to 2 dp so 4.499 never displays as a passing 4.50.
        shown = int(r * 100) / 100
        print(f"| {row.get('name', '')} | {row['foreground']} | {row['background']} | {kind} | {shown:.2f}:1 | {aa} | {aaa} |")
    print(f"\n{len(rows)} pair(s), {failed} AA failure(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
