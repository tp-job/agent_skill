"""Build assets/workflow.drawio for the project-pitfalls skill, plus an SVG preview.

One coordinate table feeds both outputs, so the preview shows what draw.io will draw.
Checks: unique ids, every edge endpoint exists, no two boxes in the same layer overlap,
labels roughly fit their boxes.
"""
import sys
from html import escape
from pathlib import Path

OUT = Path(sys.argv[1])
SVG = Path(sys.argv[2])

PAGE_W, PAGE_H = 1720, 1640

COL = {
    "A": ("#e1d5e7", "#9673a6"),
    "B": ("#dae8fc", "#6c8ebf"),
    "C": ("#d5e8d4", "#82b366"),
    "D": ("#fff2cc", "#d6b656"),
    "dec": ("#ffe6cc", "#d79b00"),
    "proc": ("#f5f5f5", "#666666"),
    "term": ("#e6e6e6", "#4d4d4d"),
    "warn": ("#f8cecc", "#b85450"),
}

nodes = []  # (id, kind, x, y, w, h, title, sub, color)
edges = []  # (id, src, tgt, label, points, exit, entry)


def node(i, kind, x, y, w, h, title, sub="", color="proc"):
    nodes.append((i, kind, x, y, w, h, title, sub, color))


def edge(i, s, t, label="", points=(), exit=None, entry=None):
    edges.append((i, s, t, label, list(points), exit, entry))


# ---- header -------------------------------------------------------------
node("title", "text", 40, 24, 560, 70, "project-pitfalls · workflow",
     "Run the checkpoint for the stage you are in · every item needs evidence", "proc")
node("start", "term", 740, 20, 240, 64, "Project event", "kickoff · setup · phase close · retro", "term")
node("locate", "dec", 730, 110, 260, 120, "1 · Which stage?", "", "dec")

node("legend", "legend", 1240, 24, 440, 190, "", "", "proc")

# ---- lanes ----------------------------------------------------------------
LANES = [
    ("A", "A · Before design", "ก่อนออกแบบ · proposal / schema exists", [
        ("Root problem → feature table", "fishbone + 5 Why"),
        ("Schema scope vs objective", "no unrequested boundary"),
        ("Calculation rules signed", "worked example + hand sheet"),
        ("Undefined states defined", "no score ≠ 0 ≠ at risk"),
        ("Baseline measured", "time the manual process"),
        ("Permission matrix counted", "what moves if roles merge"),
        ("Costly data shapes decided", "sections · groupings · keys"),
        ("One official file per diagram", "generated, content-checked"),
    ]),
    ("B", "B · Day zero", "วันแรก · repo / CI / database", [
        ("Clean clone → one setup cmd", "run it twice, nothing breaks"),
        ("Line endings · runtime pinned", ".gitattributes · .nvmrc"),
        ("One runtime major everywhere", ".nvmrc · engines · CI · Docker"),
        ("CI required, each gate seen red", "break it on a throwaway branch"),
        ("Workflow lint clean", "SHA pins · permissions · timeouts"),
        ("No secret in image or file", "**/.env* ignored · old URLs gone"),
        ("DB region + pooler measured", "SELECT 1 ×20 · per-query log"),
        ("Hosted data API locked", "RLS on · no anon grants"),
    ]),
    ("C", "C · During build", "ระหว่างพัฒนา · phase close · pre-merge · slow", [
        ("Measure first", "no-DB endpoint vs DB endpoint"),
        ("Count round trips", "bulk write · Promise.all reads"),
        ("One request per screen", "no per-row calls"),
        ("Access gate fails boot", "404 for not-yours · token typ"),
        ("Tests isolated, seen failing", "serial DB tests · mutants"),
        ("Docs regenerated, checked", "code is the source of truth"),
    ]),
    ("D", "D · Handoff & retro", "ส่งต่อ · สรุปบทเรียน", [
        ("One concern per commit", "subject says what changed"),
        ("PR lists what was not tested", "honest > all boxes ticked"),
        ("Guide + do-not-run list", "seed · migrate dev on shared DB"),
        ("Irreversible steps → human", "keep old until new verified"),
        ("Mine history oldest-first", "commit bodies · docs · sessions"),
        ("Write the lessons file", "problem · cause · fix · lesson"),
    ]),
]

LANE_W, LANE_GAP, LANE_X0, LANE_Y = 390, 30, 40, 290
STEP_W, STEP_H, STEP_GAP, HEAD_H = 330, 58, 18, 64
LANE_H = HEAD_H + 8 * (STEP_H + STEP_GAP) + 10
lane_center = {}

for li, (key, title, sub, steps) in enumerate(LANES):
    lx = LANE_X0 + li * (LANE_W + LANE_GAP)
    node(f"lane{key}", "lane", lx, LANE_Y, LANE_W, LANE_H, title, sub, key)
    lane_center[key] = lx + LANE_W // 2
    prev = None
    for si, (t, s) in enumerate(steps):
        sx = lx + (LANE_W - STEP_W) // 2
        sy = LANE_Y + HEAD_H + si * (STEP_H + STEP_GAP)
        nid = f"{key}{si + 1}"
        node(nid, "step", sx, sy, STEP_W, STEP_H, f"{key}{si + 1} · {t}", s, key)
        if prev:
            edge(f"e_{prev}_{nid}", prev, nid)
        prev = nid
    lane_center[key + "_last"] = prev

LANE_BOTTOM = LANE_Y + LANE_H
CX = 860  # trunk x for the shared steps below the lanes

edge("e_start_locate", "start", "locate")

# locate -> lanes (bus at y = 258). No edge labels: each lane's subtitle says when it runs,
# and a label on a shared trunk lands on top of the trunk line.
for key, *_ in LANES:
    cx = lane_center[key]
    edge(f"e_locate_{key}", "locate", f"lane{key}", "",
         [(CX, 258), (cx, 258)], exit=(0.5, 1), entry=(0.5, 0))

# ---- shared loop below the lanes -----------------------------------------
Y0 = LANE_BOTTOM + 60
node("mark", "proc", CX - 170, Y0, 340, 66, "2 · Mark every item",
     "pass · fail · n/a · unchecked — with evidence", "proc")
node("anyfail", "dec", CX - 140, Y0 + 110, 280, 120, "Any fail or", "unchecked?", "dec")
node("report", "proc", 1160, Y0 + 137, 330, 66, "3 · Report blocking items first",
     "above the summary", "proc")
node("fix", "proc", 1160, Y0 + 240, 330, 66, "4 · Fix in order of measured effect",
     "one change → re-measure", "proc")
node("thrice", "dec", 1185, Y0 + 340, 280, 120, "Same thing failed", "3 times?", "dec")
node("escalate", "term", 1240, Y0 + 500, 170, 60, "Escalate", "re-frame · ask one question", "warn")
node("record", "proc", CX - 170, Y0 + 290, 340, 66, "5 · Record new lessons",
     "lessons file · add to this skill", "proc")
node("end", "term", CX - 70, Y0 + 400, 140, 54, "Done", "", "term")

for key, *_ in LANES:
    edge(f"e_{key}_mark", lane_center[key + "_last"], "mark", "",
         [(lane_center[key], LANE_BOTTOM + 30), (CX, LANE_BOTTOM + 30)],
         exit=(0.5, 1), entry=(0.5, 0))

edge("e_mark_any", "mark", "anyfail")
edge("e_any_report", "anyfail", "report", "yes", exit=(1, 0.5), entry=(0, 0.5))
edge("e_any_record", "anyfail", "record", "no", exit=(0.5, 1), entry=(0.5, 0))
edge("e_report_fix", "report", "fix")
edge("e_fix_thrice", "fix", "thrice")
edge("e_thrice_esc", "thrice", "escalate", "yes", exit=(0.5, 1), entry=(0.5, 0))
edge("e_thrice_mark", "thrice", "mark", "no — re-check",
     [(1560, Y0 + 400), (1560, Y0 + 33)], exit=(1, 0.5), entry=(1, 0.5))
edge("e_record_end", "record", "end")

# ---- checks ---------------------------------------------------------------
ids = [n[0] for n in nodes] + [e[0] for e in edges]
assert len(ids) == len(set(ids)), "duplicate id"
known = {n[0] for n in nodes}
for e in edges:
    assert e[1] in known and e[2] in known, f"dangling edge {e[0]}"


def box(n):
    return n[2], n[3], n[2] + n[4], n[3] + n[5]


def overlap(a, b):
    ax0, ay0, ax1, ay1 = box(a)
    bx0, by0, bx1, by1 = box(b)
    return ax0 < bx1 and bx0 < ax1 and ay0 < by1 and by0 < ay1


solid = [n for n in nodes if n[1] != "lane"]
problems = []
for i, a in enumerate(solid):
    for b in solid[i + 1:]:
        if overlap(a, b):
            problems.append(f"overlap {a[0]} / {b[0]}")
    if a[2] + a[4] > PAGE_W or a[3] + a[5] > PAGE_H:
        problems.append(f"off page {a[0]}")
lanes = [n for n in nodes if n[1] == "lane"]
for i, a in enumerate(lanes):
    for b in lanes[i + 1:]:
        if overlap(a, b):
            problems.append(f"lane overlap {a[0]} / {b[0]}")
# text fit: ~7.2 px per Latin char at 12-13px
for n in nodes:
    if n[1] in ("step", "proc"):
        for line in (n[6], n[7]):
            if len(line) * 7.0 > n[4] - 16:
                problems.append(f"tight text {n[0]}: {line!r}")
if problems:
    print("\n".join(problems))
    sys.exit(1)

# ---- draw.io XML ----------------------------------------------------------


def label(n):
    t, s = escape(n[6]), escape(n[7])
    if n[1] == "lane":
        return f"<b>{t}</b><br><span style=\"font-weight:normal;font-size:11px\">{s}</span>"
    if n[1] == "dec":
        return f"<b>{t}</b>" + (f"<br>{s}" if s else "")
    if n[1] == "text":
        return f"<b style=\"font-size:18px\">{t}</b><br><span style=\"font-size:12px\">{s}</span>"
    return f"<b>{t}</b>" + (f"<br><span style=\"font-size:11px\">{s}</span>" if s else "")


def style(n):
    fill, stroke = COL[n[8]]
    k = n[1]
    if k == "lane":
        return (f"rounded=1;arcSize=4;whiteSpace=wrap;html=1;verticalAlign=top;spacingTop=8;"
                f"fillColor={fill};strokeColor={stroke};opacity=45;fontSize=14;")
    if k == "step":
        return f"rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor={stroke};strokeWidth=1.5;fontSize=12;"
    if k == "dec":
        return f"rhombus;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=12;"
    if k == "term":
        return f"ellipse;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=12;"
    if k == "text":
        return "text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;"
    return f"rounded=1;whiteSpace=wrap;html=1;fillColor={fill};strokeColor={stroke};fontSize=12;"


def legend_html():
    rows = [("A", "Before design"), ("B", "Day zero"), ("C", "During build (every phase)"),
            ("D", "Handoff &amp; retro"), ("dec", "Decision")]
    cells = "".join(
        f"<tr><td style=\"background:{COL[k][0]};border:1px solid {COL[k][1]};width:18px\"></td>"
        f"<td style=\"padding-left:6px\">{t}</td></tr>" for k, t in rows)
    return (f"<b>Legend</b><table style=\"font-size:11px;margin-top:4px\">{cells}</table>"
            f"<div style=\"font-size:11px;margin-top:6px\">Details: references/&lt;stage&gt;.md · "
            f"evidence: references/case-cmas.md</div>")


cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>']
order = sorted(nodes, key=lambda n: 0 if n[1] == "lane" else 1)
for n in order:
    if n[1] == "legend":
        v, st = legend_html(), "rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=10;fillColor=#ffffff;strokeColor=#999999;"
    else:
        v, st = label(n), style(n)
    cells.append(
        f'<mxCell id="{n[0]}" value="{escape(v)}" style="{st}" vertex="1" parent="1">'
        f'<mxGeometry x="{n[2]}" y="{n[3]}" width="{n[4]}" height="{n[5]}" as="geometry"/></mxCell>')
for eid, s, t, lab, pts, ex, en in edges:
    st = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;strokeColor=#555555;fontSize=11;labelBackgroundColor=#ffffff;"
    if ex:
        st += f"exitX={ex[0]};exitY={ex[1]};exitDx=0;exitDy=0;"
    if en:
        st += f"entryX={en[0]};entryY={en[1]};entryDx=0;entryDy=0;"
    pxml = ""
    if pts:
        pxml = '<Array as="points">' + "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts) + "</Array>"
    cells.append(
        f'<mxCell id="{eid}" value="{escape(lab)}" style="{st}" edge="1" parent="1" source="{s}" target="{t}">'
        f'<mxGeometry relative="1" as="geometry">{pxml}</mxGeometry></mxCell>')

xml = (f'<mxfile host="project-pitfalls">\n<diagram id="project-pitfalls-flow" name="Workflow">\n'
       f'<mxGraphModel dx="1600" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
       f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{PAGE_W}" pageHeight="{PAGE_H}" math="0" shadow="0">\n'
       f'<root>\n' + "\n".join(cells) + '\n</root>\n</mxGraphModel>\n</diagram>\n</mxfile>\n')
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(xml, encoding="utf-8", newline="\n")

# ---- SVG preview (same coordinates) ----------------------------------------
byid = {n[0]: n for n in nodes}


def anchor(n, rel):
    return n[2] + n[4] * rel[0], n[3] + n[5] * rel[1]


def default_ports(a, b):
    ax, ay = a[2] + a[4] / 2, a[3] + a[5] / 2
    bx, by = b[2] + b[4] / 2, b[3] + b[5] / 2
    if abs(by - ay) >= abs(bx - ax):
        return ((0.5, 1), (0.5, 0)) if by > ay else ((0.5, 0), (0.5, 1))
    return ((1, 0.5), (0, 0.5)) if bx > ax else ((0, 0.5), (1, 0.5))


svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{PAGE_W}" height="{PAGE_H}" '
       f'font-family="Segoe UI, Tahoma, sans-serif"><rect width="100%" height="100%" fill="#fff"/>',
       '<defs><marker id="ar" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto">'
       '<path d="M0,0 L10,4 L0,8 z" fill="#555"/></marker></defs>']
for n in order:
    x, y, w, h = n[2], n[3], n[4], n[5]
    fill, stroke = COL[n[8]]
    k = n[1]
    if k == "lane":
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" fill-opacity="0.45" stroke="{stroke}"/>')
        svg.append(f'<text x="{x + w / 2}" y="{y + 24}" text-anchor="middle" font-size="15" font-weight="bold">{escape(n[6])}</text>')
        svg.append(f'<text x="{x + w / 2}" y="{y + 44}" text-anchor="middle" font-size="11">{escape(n[7])}</text>')
        continue
    if k == "dec":
        svg.append(f'<polygon points="{x + w / 2},{y} {x + w},{y + h / 2} {x + w / 2},{y + h} {x},{y + h / 2}" fill="{fill}" stroke="{stroke}"/>')
    elif k == "term":
        svg.append(f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" fill="{fill}" stroke="{stroke}"/>')
    elif k == "text":
        svg.append(f'<text x="{x}" y="{y + 22}" font-size="18" font-weight="bold">{escape(n[6])}</text>')
        svg.append(f'<text x="{x}" y="{y + 44}" font-size="12">{escape(n[7])}</text>')
        continue
    elif k == "legend":
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#fff" stroke="#999"/>')
        svg.append(f'<text x="{x + 10}" y="{y + 20}" font-size="12" font-weight="bold">Legend</text>')
        for i, (kk, t) in enumerate([("A", "Before design"), ("B", "Day zero"), ("C", "During build (every phase)"), ("D", "Handoff & retro"), ("dec", "Decision")]):
            svg.append(f'<rect x="{x + 10}" y="{y + 32 + i * 22}" width="18" height="14" fill="{COL[kk][0]}" stroke="{COL[kk][1]}"/>')
            svg.append(f'<text x="{x + 36}" y="{y + 44 + i * 22}" font-size="11">{escape(t)}</text>')
        svg.append(f'<text x="{x + 10}" y="{y + h - 14}" font-size="11">Details: references/&lt;stage&gt;.md · evidence: references/case-cmas.md</text>')
        continue
    else:
        sw = 1.5 if k == "step" else 1
        f2 = "#fff" if k == "step" else fill
        svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{f2}" stroke="{stroke}" stroke-width="{sw}"/>')
    ty = y + h / 2 - (6 if n[7] else -4)
    svg.append(f'<text x="{x + w / 2}" y="{ty}" text-anchor="middle" font-size="12.5" font-weight="bold">{escape(n[6])}</text>')
    if n[7]:
        svg.append(f'<text x="{x + w / 2}" y="{ty + 16}" text-anchor="middle" font-size="11">{escape(n[7])}</text>')

for eid, s, t, lab, pts, ex, en in edges:
    a, b = byid[s], byid[t]
    de, dn = default_ports(a, b)
    p0, p1 = anchor(a, ex or de), anchor(b, en or dn)
    path = [p0] + pts + [p1]
    if not pts and p0[0] != p1[0] and p0[1] != p1[1]:
        path = [p0, (p0[0], (p0[1] + p1[1]) / 2), (p1[0], (p0[1] + p1[1]) / 2), p1]
    d = " ".join(f"{'M' if i == 0 else 'L'}{x},{y}" for i, (x, y) in enumerate(path))
    svg.append(f'<path d="{d}" fill="none" stroke="#555" stroke-width="1.4" marker-end="url(#ar)"/>')
    if lab:
        mx, my = path[len(path) // 2 - (1 if len(path) % 2 == 0 else 0)]
        nx, ny = path[len(path) // 2]
        lx, ly = (mx + nx) / 2, (my + ny) / 2
        svg.append(f'<rect x="{lx - len(lab) * 3.3}" y="{ly - 9}" width="{len(lab) * 6.6}" height="16" fill="#fff"/>')
        svg.append(f'<text x="{lx}" y="{ly + 3}" text-anchor="middle" font-size="11">{escape(lab)}</text>')
svg.append("</svg>")
SVG.write_text("\n".join(svg), encoding="utf-8")
print(f"ok: {len(nodes)} nodes, {len(edges)} edges -> {OUT}")
