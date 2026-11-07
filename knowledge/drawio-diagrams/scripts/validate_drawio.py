#!/usr/bin/env python3
"""Check a draw.io file against the drawio-diagrams style rules.

Usage:  python validate_drawio.py diagram.drawio [more files] [--strict]
Reads .drawio, .xml and .drawio.svg (diagram embedded), compressed or plain, every page.
Exit 0 = no ERROR (with --strict, no WARN either). Python 3.8+, standard library only.
"""
import argparse
import base64
import html
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path

FONT = "IBM Plex Sans Thai"
MIN_FONT = 16
PALETTE = {"#000000", "#ffffff", "#eef0f8"}
FOCUS = "#eef0f8"
MAX_NODES = 9
MAX_FOCUS = 2
GRID = 10
COLOR_KEYS = ("fillColor", "strokeColor", "fontColor", "labelBackgroundColor",
              "labelBorderColor", "gradientColor", "swimlaneFillColor", "separatorColor")
EFFECT_KEYS = ("shadow", "glass", "sketch", "comic")


def parse_style(s):
    d, bare = {}, []
    for part in (s or "").split(";"):
        if not part:
            continue
        if "=" in part:
            k, v = part.split("=", 1)
            d[k] = v
        else:
            bare.append(part)
    return d, bare


def load_pages(path):
    raw = Path(path).read_text(encoding="utf-8")
    if "<svg" in raw[:3000]:
        m = re.search(r'\bcontent="([^"]*)"', raw)
        if not m:
            raise SystemExit("%s: no embedded diagram (export with 'Include a copy of my diagram')" % path)
        raw = html.unescape(m.group(1))
    root = ET.fromstring(raw)
    if root.tag == "mxGraphModel":
        return [("page", root)]
    pages = []
    for d in root.iter("diagram"):
        model = d.find("mxGraphModel")
        if model is None:
            xml = urllib.parse.unquote(
                zlib.decompress(base64.b64decode((d.text or "").strip()), -15).decode("utf-8"))
            model = ET.fromstring(xml)
        pages.append((d.get("name", "page"), model))
    return pages


class Cell:
    pass


def read_cells(model):
    up = {c: p for p in model.iter() for c in p}
    cells = {}
    for el in model.iter("mxCell"):
        wrap = up.get(el)
        c = Cell()
        if wrap is not None and wrap.tag in ("object", "UserObject"):
            c.id, raw = wrap.get("id"), wrap.get("label", el.get("value", ""))
        else:
            c.id, raw = el.get("id"), el.get("value", "")
        c.raw = raw or ""
        c.text = html.unescape(re.sub(r"<[^>]+>", " ", c.raw)).strip()
        c.style, c.bare = parse_style(el.get("style"))
        c.vertex, c.edge = el.get("vertex") == "1", el.get("edge") == "1"
        c.source, c.target, c.parent = el.get("source"), el.get("target"), el.get("parent")
        g = el.find("mxGeometry")
        c.rel = tuple(float(g.get(k, 0)) for k in ("x", "y", "width", "height")) if g is not None else (0, 0, 0, 0)
        if c.edge:
            c.kind = "edge"
        elif "text" in c.bare or "edgeLabel" in c.bare:
            c.kind = "text"
        elif c.style.get("shape") == "image":
            c.kind = "image"
        else:
            c.kind = "shape"
        if c.vertex or c.edge:
            cells[c.id] = c
    for c in cells.values():
        x, y, w, h = c.rel
        p = cells.get(c.parent)
        while p is not None and p.vertex:
            x, y = x + p.rel[0], y + p.rel[1]
            p = cells.get(p.parent)
        c.box = (x, y, w, h)
    return cells


def contains(a, b):
    ax, ay, aw, ah = a.box
    bx, by, bw, bh = b.box
    return (a is not b and ax <= bx and ay <= by and ax + aw >= bx + bw and ay + ah >= by + bh
            and (aw * ah > bw * bh or (aw, ah) != (bw, bh)))


def overlaps(a, b):
    ax, ay, aw, ah = a.box
    bx, by, bw, bh = b.box
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


def norm_color(v):
    v = v.strip().lower()
    m = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", v)
    return "#%02x%02x%02x" % tuple(int(n) for n in m.groups()) if m else v


def check_page(name, model, out):
    cells = read_cells(model)

    def err(c, msg, level="ERROR"):
        out.append((level, name, c.id if c else "-", msg))

    allv = [c for c in cells.values() if c.vertex]
    boxes = [c for c in allv if c.kind in ("shape", "image")]
    frames = [c for c in allv if c.kind == "shape"
              and (any(c2.parent == c.id for c2 in cells.values() if c2.vertex)
                   or any(contains(c, o) for o in boxes))]
    frame_ids = {f.id for f in frames}
    leaves = [c for c in allv if c.kind == "shape" and c.id not in frame_ids]

    for c in cells.values():
        s = c.style
        has_text = bool(c.text) or c.kind == "text"
        if has_text:
            if s.get("fontFamily") != FONT:
                err(c, "fontFamily must be '%s' (got %r)" % (FONT, s.get("fontFamily")))
            elif "fontSource" not in s:
                err(c, "fontSource missing; the font will not load in exports")
            try:
                size = float(s.get("fontSize", 12))
            except ValueError:
                size = 0
            if size < MIN_FONT:
                err(c, "fontSize %s is below %d (draw.io defaults to 12 when unset)" % (s.get("fontSize", "unset"), MIN_FONT))
            for px in re.findall(r"font-size:\s*([\d.]+)px", c.raw):
                if float(px) < MIN_FONT:
                    err(c, "inline font-size %spx is below %d" % (px, MIN_FONT))
            for fam in re.findall(r"font-family:\s*([^;\"']+)", c.raw):
                if FONT.lower() not in fam.lower():
                    err(c, "inline font-family %r is not %s" % (fam.strip(), FONT))
            for col in re.findall(r"(?:[^-]color:\s*|color=\")([^;\">]+)", c.raw):
                if norm_color(col) not in PALETTE:
                    err(c, "inline text colour %r is outside the palette" % col.strip())
        for k in COLOR_KEYS:
            if k in s and norm_color(s[k]) not in PALETTE and s[k].lower() != "none":
                err(c, "%s=%s is outside the palette (#000000, #FFFFFF, #EEF0F8)" % (k, s[k]))
        for k in EFFECT_KEYS:
            if s.get(k) == "1":
                err(c, "%s=1 is not allowed (flat, no effects)" % k)
        if c.kind == "image":
            img = s.get("image", "")
            if img.startswith("http"):
                err(c, "image is an external URL; embed it with scripts/embed_logo.py")
            elif img.startswith("data:") and "," not in img:
                err(c, "image data URI is cut at ';' - use data:image/png,<base64> (no ';base64')")
            elif not img:
                err(c, "image shape has no image= value")
            if not c.text:
                err(c, "logo has no text label; a logo is never shown alone")
        if c.kind in ("shape", "edge"):
            if s.get("strokeColor", "").lower() != "none":
                if "strokeColor" not in s:
                    err(c, "strokeColor not stated (use #000000)")
                if s.get("strokeWidth") != "2":
                    err(c, "strokeWidth must be 2 (got %s)" % s.get("strokeWidth", "unset, which is 1"))
            if s.get("rounded", "0") != "0":
                err(c, "rounded must be 0")
            if c.kind == "shape" and "fillColor" not in s:
                err(c, "fillColor not stated (use #FFFFFF, #EEF0F8 or none)")
            dashed = s.get("dashed") == "1" or s.get("dotted") == "1"
            if dashed:
                uml = ("«" in c.text or s.get("endArrow") == "open"
                       or s.get("shape") == "umlLifeline")
                if not uml:
                    err(c, "dashed line is only for UML «include»/«extend», dependency or return")
        if c.kind == "edge":
            if not c.source or not c.target:
                err(c, "edge is not connected at both ends (set source and target)")
            if "edgeStyle" not in s:
                err(c, "edgeStyle not set; the line may run diagonally", "WARN")

    # frames
    if boxes and not frames:
        err(None, "no frame: put the diagram inside a named rectangle")
    for f in frames:
        if not f.text:
            err(f, "frame has no name")
    for c in boxes:
        if c.id not in frame_ids and not any(contains(f, c) for f in frames):
            err(c, "item is outside every frame")

    # overlaps
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            if overlaps(a, b) and not contains(a, b) and not contains(b, a) and a.box != b.box:
                err(a, "overlaps '%s' (%s)" % (b.text[:20], b.id))

    # density and focus, per smallest enclosing frame
    def home(c):
        host = [f for f in frames if contains(f, c)]
        return min(host, key=lambda f: f.box[2] * f.box[3]).id if host else "(page)"
    count, focus = {}, {}
    for c in leaves:
        count[home(c)] = count.get(home(c), 0) + 1
    for c in boxes:
        if c.style.get("fillColor", "").lower() == FOCUS:
            focus[home(c)] = focus.get(home(c), 0) + 1
    for k, n in count.items():
        if n > MAX_NODES:
            err(cells.get(k), "frame holds %d boxes (max %d); split it" % (n, MAX_NODES), "WARN")
    for k, n in focus.items():
        if n > MAX_FOCUS:
            err(cells.get(k), "%d items use the focus colour (max %d)" % (n, MAX_FOCUS), "WARN")

    # grid
    off = [c.id for c in boxes if any(round(v) % GRID for v in c.rel)]
    if off:
        err(None, "off the %dpx grid: %s%s" % (GRID, ", ".join(off[:5]), " ..." if len(off) > 5 else ""), "WARN")

    # flowchart logic
    def is_decision(c):
        return "rhombus" in c.bare or "flowchart.decision" in c.style.get("shape", "")

    def is_term(c):
        return "flowchart.terminator" in c.style.get("shape", "")
    edges = [c for c in cells.values() if c.edge]
    decisions = [c for c in leaves if is_decision(c)]
    terms = [c for c in leaves if is_term(c)]
    if decisions or terms:
        for d in decisions:
            outs = [e for e in edges if e.source == d.id]
            if len(outs) < 2:
                err(d, "decision has %d exit(s); needs at least 2" % len(outs))
            for e in outs:
                if not e.text:
                    err(e, "decision exit has no label (e.g. yes/no)")
        starts = [t for t in terms if not any(e.target == t.id for e in edges)]
        ends = [t for t in terms if not any(e.source == t.id for e in edges)]
        if len(starts) != 1:
            err(None, "flowchart needs exactly 1 start (terminator with no incoming line), found %d" % len(starts))
        if not ends:
            err(None, "flowchart needs at least 1 end (terminator with no outgoing line)")
        for c in leaves:
            if not any(e.source == c.id or e.target == c.id for e in edges):
                err(c, "box has no line in or out")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+")
    ap.add_argument("--strict", action="store_true", help="treat WARN as failure")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    bad = False
    for f in a.files:
        out = []
        for name, model in load_pages(f):
            check_page(name, model, out)
        errs = [o for o in out if o[0] == "ERROR"]
        warns = [o for o in out if o[0] == "WARN"]
        for lv, pg, cid, msg in out:
            print("%s  %s [%s:%s] %s" % (lv, Path(f).name, pg, cid, msg))
        print("%s: %d error(s), %d warning(s)" % (Path(f).name, len(errs), len(warns)))
        bad = bad or bool(errs) or (a.strict and bool(warns))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
