---
name: drawio-diagrams
description: >-
  Draws flowcharts and diagrams as editable draw.io files for readers who do not know the subject:
  IBM Plex Sans Thai at 16px or larger, 2px solid square-cornered lines, black and white only with
  one #EEF0F8 focus colour, every rectangle a named frame, real logos beside plain-language labels.
  Covers flowchart (ISO 5807), system overview, UML sequence and use case, and ER, laid out for
  reports and theses; a validator script checks every rule. Trigger for: "draw a flowchart", "make a diagram in draw.io",
  "system overview diagram", "sequence diagram", "ER diagram", "วาด flowchart", "ทำแผนภาพ drawio",
  "แผนภาพภาพรวมระบบ", "วาด use case", "ภาพประกอบวิทยานิพนธ์". Not for Mermaid or PlantUML text, Figma or FigJam diagrams,
  data charts, UI mockups, or diagrams in another brand's style.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.4.0"
  source: Requirements from the CMAS system-overview draw.io files; ISO 5807, UML 2.5, draw.io style reference (compiled 2026)
---

# draw.io Diagrams

One diagram tells one idea to someone who does not know the subject. Fewer boxes, plain words, a logo where a name alone would not mean anything.

## Workflow

1. **Ask at most 3 things**, skipping any the request already answers: who reads it and what they already know; the one thing they should understand afterwards; where it starts and ends.
2. **Pick the type** from the table below.
3. **Write the outline as text** (boxes, then lines as "A → B: verb") and get a yes before drawing. Skip this only when the user already gave the full list.
4. **Build** from [template-flowchart.drawio](assets/template-flowchart.drawio) and the style strings in [style-spec.md](references/style-spec.md). Save `<name>.drawio` where the user says, else the working directory.
5. **Validate** until it reports 0 errors and 0 warnings:
   `python scripts/validate_drawio.py <file> --strict`
6. **Look at it** (see [export-and-check.md](references/export-and-check.md)): crossings, clipped Thai text, labels sitting on lines. The script cannot see these.
7. **Report** the path, one sentence on what the diagram says, and any rule you had to bend and why.

## Pick the type

| The reader needs to know | Type | Read |
| --- | --- | --- |
| The steps and decisions of a process | Flowchart | [flowchart.md](references/flowchart.md) |
| What parts a system has and who talks to whom | System overview | [system-overview.md](references/system-overview.md) |
| Who sends what to whom, in order | UML sequence | [sequence.md](references/sequence.md) |
| What each kind of user can do | UML use case | [use-case.md](references/use-case.md) |
| What data is stored and how it relates | ER (crow's foot) | [er.md](references/er.md) |

Going into a thesis, report or paper? Also read [academic-figures.md](references/academic-figures.md): page width, caption outside the picture, export.

Needs two types (for example overview plus login steps)? Make two pages in one file, never one crowded page.

## The rules

| # | Rule | Checked by script |
| --- | --- | --- |
| 1 | Font `IBM Plex Sans Thai` with `fontSource`, size 16 or larger everywhere, including labels under logos and on lines | yes |
| 2 | Lines and outlines `strokeWidth=2`, `rounded=0`, solid; lines are square-cornered, except UML use case lines, which are straight and may run diagonally | yes |
| 3 | Dashed only for UML «include», «extend», dependency and return | yes |
| 4 | Colours `#000000`, `#FFFFFF` only; `#EEF0F8` fill marks what to look at, at most 2 per frame, never text colour | yes |
| 5 | Every box sits inside a frame, and every frame has a name at its top left | yes |
| 6 | A logo is embedded in the file (no URL), never alone, always with its name beneath | yes |
| 7 | Each line joins two boxes; flowchart decisions have 2 or more labelled exits, one start, one or more ends | yes |
| 8 | No shadow, gradient, glass or sketch effect | yes |
| 9 | At most 6 boxes per frame and 12 per page (start and end capsules do not count); more means split | warns |
| 10 | Positions on a 10px grid | warns |
| 11 | One fact per box, 40 characters at most, no bullet lists, no code-like IDs (S1, F2, E01), no `·` strings | bullets error, rest warn |
| 12 | At most 3 loose text blocks on the page; prose goes in your reply, not on the diagram | warns |
| 13 | Flowchart: the happy path runs down one centre column, each decision splits left (continue) and right (exception, ending below) ([layout](references/flowchart.md)); lines do not cross; no line passes through a box | judgement |
| 14 | A title frame names the diagram; a one-line caption says what it shows | judgement |

**Never shrink the font or the box spacing to fit more in.** Split the diagram instead; a 12px label fails the reader before it fails the rule.

**Where the rules stop:** logos keep their own colours (they are pictures, not diagram ink). Flowchart terminators and decisions may be capsule and diamond shapes, ellipses are allowed for use cases; every other box is a square-cornered rectangle.

## Keep it light

A diagram that looks machine-made is dense, coded and self-explaining. Before drawing, run the cut test from [plain-and-light.md](references/plain-and-light.md): delete anything the reader would not miss, then do it again. Typical cuts: bullet lists in boxes, Input/Process/Output columns, code legends, header text above the diagram, edge cases on the main page.

## Wording for non-experts

| BAD | BETTER |
| --- | --- |
| `POST /auth/login → JWT` | ส่งอีเมลและรหัสผ่าน → ได้บัตรผ่านชั่วคราว (JWT) |
| `Validate input` | ตรวจว่ากรอกครบ |
| `DB` (alone) | ฐานข้อมูล (Database) with its logo |

Use the reader's language for the plain word and keep the product name as written (Supabase, React).

## Scripts

| Script | Use |
| --- | --- |
| [validate_drawio.py](scripts/validate_drawio.py) | Checks rules 1 to 12 on `.drawio` or `.drawio.svg`, every page; exit 1 on error |
| [embed_logo.py](scripts/embed_logo.py) | Turns a logo file or https URL into the `image=` style value |

Logo sources and sizing: [logos.md](references/logos.md).
