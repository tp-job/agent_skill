#!/usr/bin/env python3
"""System Usability Scale (Brooke, 1996) scores from raw answers.

Input CSV: one row per respondent. Either 10 columns of answers (1-5), or a
first column with a respondent ID followed by 10 answers. A header row is
skipped automatically.

Scoring: odd items contribute (answer - 1), even items (5 - answer);
SUS = sum x 2.5 (0-100). Adjectives use the mean scores reported by
Bangor, Kortum and Miller (2009); treat them as approximate cut-offs.

Usage:  python sus_score.py answers.csv
Python 3.10+, standard library only.

>>> sus([5, 1, 5, 1, 5, 1, 5, 1, 5, 1])
100.0
>>> sus([3] * 10)
50.0
>>> adjective(72.0)
'Good'
"""
from __future__ import annotations

import csv
import statistics
import sys

ADJECTIVES = [(85.5, "Excellent"), (71.4, "Good"), (50.9, "OK"), (35.7, "Poor"), (0.0, "Awful")]


def sus(answers: list[int]) -> float:
    if len(answers) != 10 or any(a not in (1, 2, 3, 4, 5) for a in answers):
        raise ValueError(f"need 10 answers in 1-5, got {answers}")
    total = sum((a - 1) if i % 2 == 0 else (5 - a) for i, a in enumerate(answers))
    return total * 2.5


def adjective(score: float) -> str:
    return next(label for cut, label in ADJECTIVES if score >= cut)


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    if len(argv) != 2 or argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 0
    scores: list[tuple[str, float]] = []
    with open(argv[1], newline="", encoding="utf-8-sig") as fh:
        for n, row in enumerate(csv.reader(fh), start=1):
            row = [c.strip() for c in row if c.strip()]
            if not row:
                continue
            nums = row[-10:]
            if not all(c.isdigit() for c in nums):
                continue  # header or malformed line
            rid = row[0] if len(row) == 11 else f"R{len(scores) + 1}"
            scores.append((rid, sus([int(c) for c in nums])))
    if not scores:
        print("no valid rows (need 10 answers of 1-5 per row)")
        return 2
    print("| Respondent | SUS |")
    print("| --- | --- |")
    for rid, s in scores:
        print(f"| {rid} | {s:.1f} |")
    values = [s for _, s in scores]
    mean = statistics.mean(values)
    sd = statistics.stdev(values) if len(values) > 1 else 0.0
    print(f"\nn = {len(values)} · mean = {mean:.1f} · SD = {sd:.1f} · adjective = {adjective(mean)}")
    print(f"benchmark: {'at or above' if mean >= 68 else 'below'} the cross-study average of 68")
    if len(values) < 12:
        print("note: n < 12, so the confidence interval around the mean is wide; report it as indicative")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
