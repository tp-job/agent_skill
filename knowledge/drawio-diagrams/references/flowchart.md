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
| Flow runs top to bottom; the main happy path stays in one straight column | The eye follows the straight line first |
| The "no" or error branch goes to the side, then either ends or loops back with a labelled line | Keeps the main path clean |
| Every box has a line in and a line out, except start (no in) and ends (no out) | A floating box is a mistake the reader cannot tell from an intention |
| Max 9 boxes per frame | Past 9, readers lose the thread; use the linked-process box and a second page |

## Layout: one main column, exits to the side

The page is three columns. The happy path runs down the left one without turning; every exception leaves a decision sideways and ends at once.

```text
   main column (260)        side column (220)      end (120)
   [ เริ่ม ]
       ↓
   [ ผู้ใช้กรอกข้อมูล ]
       ↓
   < ข้อมูลถูกต้อง? > ─ไม่ใช่→ [ แจ้งว่าไม่ถูกต้อง ] → [ จบ ]
       ↓ ใช่
   [ เข้าสู่ระบบ ]
       ↓
   [ จบ ]
```

| Rule | Value |
| --- | --- |
| "ใช่" (the path the process wants) continues straight down | Never turns |
| "ไม่ใช่" (failure, cancel, rejected) leaves to the right | A second different exit leaves to the left |
| The side box is centred on the decision, so the exit line is one straight horizontal | Same `y` centre |
| The side box ends in its own "จบ" in the end column, same row | The exception never rejoins the main path, so no lines cross |
| An exception that should retry loops back to the earlier box with a labelled line | The only line that goes upward |
| Widths | Main 260, side 220, end 120; gaps 80 and 40; frame padding 40; page width 800 |
| Vertical gap | 60 between boxes in the main column |
| Decision | 260 × 100; steps 260 × 60; terminators 160 × 60 in the main column, 120 × 60 in the end column |

Terminators do not count toward the box limit, so a flowchart may hold six steps and decisions plus any number of ends. Start from [template-flowchart.drawio](../assets/template-flowchart.drawio); it already sits on this grid.

Set `exitX=1;exitY=0.5` and `entryX=0;entryY=0.5` on the side exits so draw.io draws them straight.

## Splitting

When the outline has more than 6 steps and decisions, cut at a natural hand-off (a different person, system or phase). Page 1 shows the cut parts as single "linked process" boxes; each following page opens with a start capsule named after that box.

Within one page, a flow that must continue on the next sheet ends in a page connector: a 40 × 40 circle (`ellipse;`) holding one letter. The next sheet starts with the same letter. The validator treats a connector as an end or a start.

## Check before saving

1. Trace the happy path with a finger: start to end without lifting it.
2. Trace each "no" exit: it ends or returns to a named earlier step.
3. Run the validator; the flowchart checks (one start, an end, labelled exits, no floating box) run on any page that contains a capsule or a diamond.
