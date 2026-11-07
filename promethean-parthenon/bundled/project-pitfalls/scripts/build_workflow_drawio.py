"""Build assets/workflow.drawio for the project-pitfalls skill.

Run: python scripts/build_workflow_drawio.py assets/workflow.drawio

Layout follows the drawio-diagrams rules: one named frame per page, the main path down the centre,
every decision splitting left (continue) and right (exception, ending below), at most six
boxes per frame. The stage checklists are the LANES table below; edit it, then rebuild.
Standard library only.
"""
import sys
import html
from xml.sax.saxutils import quoteattr

FONT = ("fontFamily=IBM Plex Sans Thai;fontSource=https%3A%2F%2Ffonts.googleapis.com%2F"
        "css%3Ffamily%3DIBM%2BPlex%2BSans%2BThai;fontSize=16;fontColor=#000000;")
BASE = "html=1;whiteSpace=wrap;rounded=0;strokeWidth=2;strokeColor=#000000;"
FILL = "fillColor=#FFFFFF;"
FOCUSF = "fillColor=#EEF0F8;"
TERM = "shape=mxgraph.flowchart.terminator;"
EDGE = ("edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;strokeWidth=2;strokeColor=#000000;"
        "endArrow=block;endFill=1;labelBackgroundColor=#FFFFFF;")
SIDE = "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"
LOOP = "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"
FRAME = (BASE + "fillColor=none;" + FONT + "fontStyle=1;verticalAlign=top;align=left;"
         "spacingLeft=12;spacingTop=8;")

MX, MW = 310, 260      # main column (centre of the frame)
CAPW = 200             # start / end capsule in the main column
SX, SW = 630, 200      # right zone: exception box
HOOK = 270             # x of the vertical run for the continuing branch (left zone)
GAP = 60
DH = 120               # decision height


class S:
    def __init__(self, text, focus=False):
        self.text, self.focus = text, focus


class D:
    """Decision: `down` continues (leaves the left corner, then runs down),
    `side` is the exception (leaves the right corner into a box, then ends below)."""
    def __init__(self, text, side_text, down="ไม่ใช่", side="ใช่", end="จบ", loop=None, loop_label=""):
        self.text, self.side_text, self.down, self.side = text, side_text, down, side
        self.end, self.loop, self.loop_label = end, loop, loop_label


def cell(i, value, style, x, y, w, h):
    return ('<mxCell id="%s" value=%s style=%s vertex="1" parent="1"><mxGeometry x="%d" y="%d" '
            'width="%d" height="%d" as="geometry"/></mxCell>'
            % (i, quoteattr(value), quoteattr(style), x, y, w, h))


def edge(i, src, tgt, label="", extra="", points=()):
    geo = '<mxGeometry relative="1" as="geometry"/>'
    if points:
        geo = ('<mxGeometry relative="1" as="geometry"><Array as="points">%s</Array></mxGeometry>'
               % "".join('<mxPoint x="%d" y="%d"/>' % p for p in points))
    return ('<mxCell id="%s" value=%s style=%s edge="1" parent="1" source="%s" target="%s">%s</mxCell>'
            % (i, quoteattr(label), quoteattr(EDGE + FONT + extra), src, tgt, geo))


def side_h(text):
    return 60 if len(text) <= 21 else (80 if len(text) <= 42 else 100)


def page(pid, name, items, start="เริ่ม", end="จบ", frame_name=None):
    cells, edges = [], []
    cx = MX + MW // 2
    y = 100
    cells.append(cell("start", start, TERM + BASE + FILL + FONT, cx - CAPW // 2, y, CAPW, 60))
    centre = {"start": y + 30}
    left = {"start": cx}
    y += 60 + GAP
    geo = []                                   # (id, top, height, kind)
    for k, it in enumerate(items):
        h = DH if isinstance(it, D) else 60
        geo.append(("m%d" % k, y, h))
        gap = GAP
        if isinstance(it, D) and k + 1 < len(items) and isinstance(items[k + 1], D):
            gap = 100
        y += h + gap
    end_y = y - GAP if False else y
    # fix: the gap after the last item is GAP
    if items and isinstance(items[-1], D):
        end_y = geo[-1][1] + DH + GAP
    else:
        end_y = geo[-1][1] + 60 + GAP
    centre_y = {g[0]: g[1] + g[2] // 2 for g in geo}
    centre_y["end"] = end_y + 30
    bottom = end_y + 60
    prev, prev_item = "start", None
    for k, it in enumerate(items):
        i, top, h = geo[k]
        if isinstance(it, S):
            cells.append(cell(i, it.text, BASE + (FOCUSF if it.focus else FILL) + FONT + "spacingLeft=8;spacingRight=8;",
                              MX, top, MW, h))
        else:
            cells.append(cell(i, it.text, "rhombus;" + BASE + FILL + FONT + "spacingLeft=8;spacingRight=8;", MX, top, MW, h))
        if isinstance(prev_item, D):
            edges.append(edge("e_%s" % i, prev, i, prev_item.down,
                              "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
                              [(HOOK, centre_y[prev]), (HOOK, centre_y[i])]))
        else:
            edges.append(edge("e_%s" % i, prev, i, ""))
        if isinstance(it, D):
            sid, eid = "x%d" % k, "z%d" % k
            if it.loop is not None and any(isinstance(items[m], D) for m in range(it.loop + 1, k)):
                print('note: loop on', name, 'k=%d' % k, 'turned into an end')
                it.end = 'แก้แล้วตรวจใหม่'; it.loop = None
            sh = side_h(it.side_text)
            cyy = top + h // 2
            cells.append(cell(sid, it.side_text, BASE + FILL + FONT + "spacingLeft=8;spacingRight=8;", SX, cyy - sh // 2, SW, sh))
            edges.append(edge("e_%s_s" % i, i, sid, it.side,
                              "exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;"))
            if it.loop is None:
                ey = cyy + sh // 2 + 60
                cells.append(cell(eid, it.end, TERM + BASE + FILL + FONT, SX + (SW - 160) // 2, ey, 160, 60))
                edges.append(edge("e_%s_z" % i, sid, eid, "",
                                  "exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;"))
                bottom = max(bottom, ey + 60)
            else:
                edges.append(edge("e_%s_l" % i, sid, "m%d" % it.loop, it.loop_label,
                                  "exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;"))
        prev, prev_item = i, it
    cells.append(cell("end", end, TERM + BASE + FILL + FONT, cx - CAPW // 2, end_y, CAPW, 60))
    if isinstance(prev_item, D):
        edges.append(edge("e_end", prev, "end", prev_item.down,
                          "exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;",
                          [(HOOK, centre_y[prev]), (HOOK, centre_y["end"])]))
    else:
        edges.append(edge("e_end", prev, "end", ""))
    fh = bottom + 40 - 40
    frame = cell("frame", frame_name or name, FRAME, 40, 40, 800, fh)
    body = "".join([frame] + cells + edges)
    return ('<diagram id=%s name=%s><mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" '
            'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="900" '
            'pageHeight="%d" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>%s'
            '</root></mxGraphModel></diagram>' % (quoteattr(pid), quoteattr(name), fh + 120, body))


def write(path, pages):
    out = ['<mxfile host="app.diagrams.net">']
    for n, (name, items, kw) in enumerate(pages, 1):
        out.append(page("p%d" % n, name, items, **kw))
    out.append("</mxfile>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")


# ---- the project-pitfalls workflow: stage picker, one checklist per stage, report loop ----
LANES = {
    "A": ("ก่อนออกแบบ", [
        "Root problem to feature table", "Schema scope vs objective", "Calculation rules signed",
        "Undefined states defined", "Baseline measured", "Permission matrix counted",
        "Costly data shapes decided", "One official file per diagram"]),
    "B": ("วันแรกของ repo", [
        "Clean clone, one setup command", "Line endings and runtime pinned", "One runtime major everywhere",
        "CI required, each gate seen red", "Workflow lint clean", "No secret in image or file",
        "DB region and pooler measured", "Hosted data API locked"]),
    "C": ("ระหว่างพัฒนา", [
        "Measure first", "Count round trips", "One request per screen",
        "Access gate fails boot", "Tests isolated, seen failing", "Docs regenerated, checked"]),
    "D": ("ส่งต่อและสรุปบทเรียน", [
        "One concern per commit", "PR lists what was not tested", "Guide and do-not-run list",
        "Irreversible steps go to a human", "Mine history oldest-first", "Write the lessons file"]),
}


def build(out):
    pages = [("เลือกช่วงของโครงการ", [
        D("ยังไม่ได้ออกแบบ?", "ชุด A: ตรวจก่อนออกแบบ"),
        D("เพิ่งเปิด repo หรือ CI?", "ชุด B: วันแรกของ repo"),
        D("กำลังพัฒนา หรือช้า?", "ชุด C: ระหว่างพัฒนา"),
    ], dict(start="เริ่ม", end="ชุด D: ส่งต่อและสรุปบทเรียน"))]
    for key, (title, steps) in LANES.items():
        chunks = [steps[i:i + 4] for i in range(0, len(steps), 4)] if len(steps) > 6 else [steps]
        for n, chunk in enumerate(chunks, 1):
            name = "ชุด %s: %s" % (key, title) + (" (%d)" % n if len(chunks) > 1 else "")
            last = n == len(chunks)
            pages.append((name, [S(t, False) for t in chunk],
                          dict(start="เริ่มชุด %s" % key if n == 1 else "ต่อจากหน้าก่อน",
                               end="ไปตรวจผล" if last else "ต่อ: ชุด %s (%d)" % (key, n + 1))))
    pages.append(("ตรวจผลและรายงาน", [
        S("ทำเครื่องหมายทุกข้อ พร้อมหลักฐาน"),
        D("มี fail หรือยังไม่ได้ตรวจ?", "รายงาน แก้ทีละเรื่อง ครบ 3 ครั้งถามคน",
          down="ไม่มี", side="มี", loop=0, loop_label="ตรวจใหม่"),
        S("บันทึกบทเรียนใหม่ลงไฟล์", True),
    ], dict(start="เริ่ม", end="จบ")))
    named = [("%d %s" % (n, t), it, dict(kw, frame_name=t)) for n, (t, it, kw) in enumerate(pages, 1)]
    write(out, named)


if __name__ == "__main__":
    build(sys.argv[1])
