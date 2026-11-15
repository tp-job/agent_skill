#!/usr/bin/env python3
"""Summarise timings as n / median / p95 / p99 / max in a markdown table.

Accepts either:
  - a k6 summary export (k6 run --summary-export=summary.json script.js):
    reports every Trend metric (http_req_duration, custom trends) found in it.
    k6 exports only the aggregates it computed, so n is "-" and p99 needs
    summaryTrendStats to include "p(99)".
  - a CSV or plain text file with one number (milliseconds) per line; a header
    line is skipped. Percentiles use the nearest-rank method.

Usage:  python latency_summary.py summary.json
        python latency_summary.py timings.csv [--unit s]
Python 3.10+, standard library only.

>>> summarize([100, 200, 300, 400, 500, 600, 700, 800, 900, 1000])["p95"]
1000.0
>>> summarize([5, 1, 3])["median"]
3.0
"""
from __future__ import annotations

import json
import math
import statistics
import sys
from pathlib import Path


def nearest_rank(sorted_vals: list[float], p: float) -> float:
    k = max(1, math.ceil(p / 100 * len(sorted_vals)))
    return sorted_vals[k - 1]


def summarize(values: list[float]) -> dict[str, float]:
    s = sorted(values)
    return {
        "n": len(s),
        "median": float(statistics.median(s)),
        "p95": float(nearest_rank(s, 95)),
        "p99": float(nearest_rank(s, 99)),
        "max": float(s[-1]),
    }


def fmt(v: object, scale: float) -> str:
    return "-" if v is None else f"{float(v) / scale:.3f}".rstrip("0").rstrip(".")


def from_k6(data: dict) -> list[tuple[str, dict]]:
    out = []
    for name, metric in sorted(data.get("metrics", {}).items()):
        vals = metric.get("values", metric)  # k6 >= 0.30 nests under "values"
        if "med" in vals and "max" in vals:
            out.append((name, {"n": None, "median": vals.get("med"), "p95": vals.get("p(95)"),
                               "p99": vals.get("p(99)"), "max": vals.get("max")}))
    return out


def from_lines(text: str) -> list[float]:
    vals = []
    for line in text.splitlines():
        token = line.split(",")[0].strip()
        try:
            vals.append(float(token))
        except ValueError:
            continue
    return vals


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    if len(argv) < 2 or argv[1] in {"-h", "--help"}:
        print(__doc__)
        return 0
    unit = "s" if "--unit" in argv and argv[argv.index("--unit") + 1] == "s" else "ms"
    scale = 1000.0 if unit == "s" else 1.0
    text = Path(argv[1]).read_text(encoding="utf-8-sig")
    try:
        rows = from_k6(json.loads(text))
    except json.JSONDecodeError:
        vals = from_lines(text)
        if not vals:
            print("no numeric values found")
            return 2
        rows = [(Path(argv[1]).stem, summarize(vals))]
    print(f"| Metric | n | median ({unit}) | p95 ({unit}) | p99 ({unit}) | max ({unit}) |")
    print("| --- | --- | --- | --- | --- | --- |")
    for name, s in rows:
        n = "-" if s["n"] is None else str(s["n"])
        print(f"| {name} | {n} | {fmt(s['median'], scale)} | {fmt(s['p95'], scale)} | {fmt(s['p99'], scale)} | {fmt(s['max'], scale)} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
