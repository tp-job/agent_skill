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

## Splitting

When the outline has more than 9 boxes, cut at a natural hand-off (a different person, system or phase). Page 1 shows the cut parts as single "linked process" boxes; each following page opens with a start capsule named after that box.

## Check before saving

1. Trace the happy path with a finger: start to end without lifting it.
2. Trace each "no" exit: it ends or returns to a named earlier step.
3. Run the validator; the flowchart checks (one start, an end, labelled exits, no floating box) run on any page that contains a capsule or a diamond.
