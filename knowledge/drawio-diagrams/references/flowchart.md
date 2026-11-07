# Flowchart

Symbols follow ISO 5807. Use these shapes and no others.

| Meaning | Shape | Style start |
| --- | --- | --- |
| Start / end | capsule | `shape=mxgraph.flowchart.terminator;` |
| Step | rectangle | (none) |
| Decision | diamond | `rhombus;` |
| Data in / out | parallelogram | `shape=parallelogram;perimeter=parallelogramPerimeter;` |
| Another process (linked page) | rectangle with double sides | `shape=process;backgroundOutline=1;` |

Append BOX from [style-spec.md](style-spec.md) after the shape part. The template [template-flowchart.drawio](../assets/template-flowchart.drawio) is a complete example: start, step, decision with a loop back, focus step, end.

## Rules

| Rule | Why |
| --- | --- |
| Exactly one start; one or more ends | A reader must know where to begin and when it is over |
| A step says a verb and an object: "ตรวจว่ากรอกครบ" | A noun alone does not say what happens |
| A decision is a yes/no question ending in "?" | Two exits stay two exits |
| Every decision exit carries a label ("ใช่" / "ไม่ใช่") | Unlabelled exits force the reader to guess |
| Flow runs top to bottom; the main happy path stays in one column | The eye follows the straight line first |
| A decision splits left and right; the error branch goes right, then ends below or loops back with a labelled line | Keeps the main path clean |
| Every box has a line in and a line out, except start (no in) and ends (no out) | A floating box is a mistake the reader cannot tell from an intention |
| Max 9 boxes per frame | Past 9, readers lose the thread; use the linked-process box and a second page |

## Layout: one main column, decisions split left and right

The page is three zones. The main column sits in the middle and always flows down. A decision splits its two exits 180 degrees apart, one out of each corner, never one sideways and one down.

```text
   left zone          main column (260)        right zone (200)
                      [ เริ่ม ]
                          ↓
                      [ ผู้ใช้กรอกข้อมูล ]
                          ↓
     ┌─ ใช่ ──────  < ข้อมูลถูกต้อง? > ─ ไม่ใช่ →  [ แจ้งว่าไม่ถูกต้อง ]
     │                                                    ↓
     └──────────→  [ เข้าสู่ระบบ ]                    [ จบ ]
                          ↓
                      [ จบ ]
```

| Rule | Value |
| --- | --- |
| The continuing branch ("ใช่", the path the process wants) leaves the left corner, runs down the left zone and enters the next box from its left side | Both exits leave horizontally, so they are 180 degrees apart |
| The exception ("ไม่ใช่": failure, cancel, rejected) leaves the right corner into a box | The exception never rejoins the main path, so no lines cross |
| The exception box ends in its own "จบ" directly below it, an arrow pointing down | Flow always travels downward |
| An exception that should retry loops back to an earlier main box by its right side, with a labelled line | The only line that goes upward; do not use it when another decision lies between |
| Widths | Main 260, right box 200, capsules 200 in the main column and 160 below the exception; frame padding 40; page width 800 |
| Heights | Steps 60, decisions 120, exception boxes 60 to 100 by text length |
| Vertical gap | 60 between boxes; 100 after a decision that is followed by another decision, so the exception capsule clears the next exception box |
| Decision label | 20 characters at most; the diamond holds about two lines |

Terminators do not count toward the box limit, so a flowchart may hold six steps, decisions and exception boxes in total plus any number of ends. Start from [template-flowchart.drawio](../assets/template-flowchart.drawio); it already sits on this grid.

Set `exitX=0;exitY=0.5` and `entryX=0;entryY=0.5` with two waypoints on the left-zone run, and `exitX=1;exitY=0.5` with `entryX=0;entryY=0.5` on the exception, so draw.io draws them as the template does.

## Splitting

When the outline has more than 6 steps and decisions, cut at a natural hand-off (a different person, system or phase). Page 1 shows the cut parts as single "linked process" boxes; each following page opens with a start capsule named after that box.

Within one page, a flow that must continue on the next sheet ends in a page connector: a 40 × 40 circle (`ellipse;`) holding one letter. The next sheet starts with the same letter. The validator treats a connector as an end or a start.

## Check before saving

1. Trace the happy path with a finger: start to end without lifting it.
2. Trace each "no" exit: it ends or returns to a named earlier step.
3. Run the validator; the flowchart checks (one start, an end, labelled exits, no floating box) run on any page that contains a capsule or a diamond.
