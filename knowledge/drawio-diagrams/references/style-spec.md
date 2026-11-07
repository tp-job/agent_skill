# Style spec

Copy these strings into `style="..."`. The validator requires every key marked (req).

## Building blocks

| Name | String |
| --- | --- |
| FONT | `fontFamily=IBM Plex Sans Thai;fontSource=https%3A%2F%2Ffonts.googleapis.com%2Fcss%3Ffamily%3DIBM%2BPlex%2BSans%2BThai;fontSize=16;fontColor=#000000;` |
| BOX | `html=1;whiteSpace=wrap;rounded=0;strokeWidth=2;strokeColor=#000000;fillColor=#FFFFFF;` + FONT |
| FOCUS | BOX with `fillColor=#EEF0F8` |
| FRAME | BOX with `fillColor=none;verticalAlign=top;align=left;spacingLeft=12;spacingTop=8;fontStyle=1;` |
| LINE | `edgeStyle=orthogonalEdgeStyle;html=1;rounded=0;strokeWidth=2;strokeColor=#000000;endArrow=block;endFill=1;labelBackgroundColor=#FFFFFF;` + FONT |
| TEXT | `text;html=1;align=center;verticalAlign=middle;` + FONT |
| LOGO | `shape=image;html=1;imageAspect=0;aspect=fixed;verticalLabelPosition=bottom;verticalAlign=top;labelBackgroundColor=none;` + FONT + `image=data:...` |

Required keys (req): `fontFamily`, `fontSource`, `fontSize>=16`, `strokeWidth=2`, `strokeColor`, `fillColor` on boxes, `rounded=0`.
draw.io defaults are 12px, 1px and Helvetica, so a missing key is an error, not a pass.

## Sizes and spacing

| Item | Value |
| --- | --- |
| Minimum box | 160 × 60 |
| Box width for Thai text | about 10px per character plus 40px; wrap at 2 lines |
| Gap between boxes | at least 60; at least 100 when the line carries a label |
| Frame padding | 40 on every side, 40 extra at the top for the name |
| Logo | 64 × 64 with its name beneath, 16px |
| Grid | multiples of 10 for every x, y, width, height |

## Frame hierarchy

All outlines are 2px. Show depth by nesting and by the name, never by thicker lines:

| Level | Name style | Example |
| --- | --- | --- |
| Page frame | bold, names the diagram | ภาพรวมระบบ CMAS |
| Group frame | bold, names the group | เว็บเบราว์เซอร์ |
| Box | regular | Client (Frontend) |

At most two frame levels. A third level means split the page.

## Focus colour

`#EEF0F8` fill answers "look here first". Use it for the step or part the reader must not miss, at most 2 per frame, and say in the caption what it marks. Text and lines stay black on it.

## Dashed lines (the only exceptions)

| Where | Look |
| --- | --- |
| UML «include» / «extend» | `dashed=1;endArrow=open;` and the label `«include»` / `«extend»` |
| UML dependency | `dashed=1;endArrow=open;` |
| Sequence return message | `dashed=1;endArrow=open;` |
| Sequence lifeline | `shape=umlLifeline`, its dashed vertical line is part of the notation |

Everything else is solid.

## Edges

Set `source` and `target` on every edge so the line follows the box when it moves. A line that only ends near a box is an error. A line carries a verb label when the meaning is not obvious from its two ends; decision exits always carry a label.
