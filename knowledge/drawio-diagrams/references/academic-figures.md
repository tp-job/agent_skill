# Figures for academic documents

For a thesis, report or paper. The figure is placed in a document, scaled to the text width, and often printed in black and white.

## Rules

| Rule | Why |
| --- | --- |
| Page width 800 px or less; height 1,100 px or less | At A4 text width (about 16 cm) an 800 px page scales to 57%, so 16px text lands near 9pt, still readable. Wider and the text drops below that |
| One diagram, one figure; a long flow becomes two figures joined by page connectors | A figure that needs a full landscape page is read by nobody |
| No caption, figure number, user line, source line or legend inside the picture | The document's caption does that job; keep the picture to the diagram alone |
| The frame name is the process name ("ตรวจสอบสิทธิ์ก่อนเข้าระบบ"), not "Figure 3.1" | The number belongs to the document and changes when chapters move |
| Use only standard symbols (ISO 5807 for flowcharts, UML for the rest) | A reader of a paper knows them, so no legend is needed |
| Terms in boxes match the terms in the body text | The reader should find the same word in the paragraph above the figure |
| Do not rely on the focus tint alone; name the marked box in the text ("กล่องที่แรเงา") | `#EEF0F8` can disappear in a grey-scale print |
| Same widths, same grid, same font in every figure of the document | A document looks edited when its figures agree |

## Caption and citation (in the document, not the picture)

| Item | Convention |
| --- | --- |
| Caption | Under the figure: "ภาพที่ 3.1 ขั้นตอนการตรวจสอบสิทธิ์ก่อนเข้าระบบ" (or "รูปที่", as your institution's template says; follow the template over this default) |
| Numbering | Chapter number, then a running number |
| Mention | The text refers to the figure before it appears: "ดังภาพที่ 3.1" |
| Adapted from a source | Add "ที่มา:" or "ดัดแปลงจาก" and the citation under the caption |

## Export

| For | Do |
| --- | --- |
| Word or Google Docs | PNG at 3× scale (about 300 dpi): `drawio -x -f png -s 3 -o figure.png figure.drawio`, or File → Export as → PNG in draw.io with Zoom 300% |
| LaTeX or PDF | SVG or PDF so it stays sharp; embed fonts when the export dialog offers it |
| Keep | The `.drawio` source beside the exported file, named after the figure |

Check `drawio --help` for the flags in your version. After inserting, look at the figure at its printed size: if the text looks smaller than the body text of the footnotes, the diagram is too wide; split it.

## Quick check before inserting

1. The diagram has no title block, no legend and no loose paragraph.
2. Width is 800 px or less.
3. Every exception ends at the side; no line crosses.
4. `python scripts/validate_drawio.py figure.drawio --strict` reports 0 and 0.
