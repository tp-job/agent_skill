# Plain and light

A diagram that reads as machine-made is dense, labelled in code, and explains itself in paragraphs. A diagram a person drew has few things, short words and room to breathe. Apply this before drawing, not after.

## The cut test

For every box, line and word, ask: **if I delete this, does the reader lose the one thing the diagram is for?** If not, delete it. Do the pass twice.

## Budgets

| Item | Limit | Validator |
| --- | --- | --- |
| Boxes per frame | 6 | warns |
| Boxes per page | 12 | warns |
| One label | 40 characters, 2 lines | warns |
| Loose text on the page (title, caption, one note) | 3 blocks | warns |
| Facts per box | 1 | bullets are an error |
| Frame levels | 2 | judgement |

Over a budget means split the page or cut. Never shrink the font or the spacing.

## Patterns to avoid

| Pattern | Why it looks machine-made | Instead |
| --- | --- | --- |
| Bullet lists inside boxes | A box becomes a paragraph | One phrase; extra detail goes in your reply |
| Input / Process / Output columns as a template | Fits every topic, says nothing about this one | Draw the actual steps in order |
| Codes such as S1–S15, F1–F4, E01–E23 and a legend that decodes them | The reader must learn a language to read the picture | Plain words; if you need a reference, number the boxes 1, 2, 3 |
| Lines of context above the diagram (who uses it, which files, what it does) | The diagram is not doing its job | Put them in your reply or in the file's caption |
| `·` strings that join several facts | A table squeezed into one cell | Split into boxes or cut |
| Grey header bars, many tints | Decoration without meaning | White boxes; one `#EEF0F8` focus |
| Icons that fail to load, logos as decoration | Looks unfinished | Embed every logo, or use none |
| Every case drawn (edge cases, error paths, all columns) | Completeness feels thorough but hides the main story | Happy path in the diagram; a second page for the one exception that matters |
| Identical weight on everything | No entry point | One focus box, one bold frame title, the rest regular |

## What carries the meaning

Shape, position and arrows tell the story; words only name things. Test: cover all text and check that the layout still shows a start, an order and a split. If it does not, the layout is weak, not the wording.

## Space

| Rule | Value |
| --- | --- |
| Gap between boxes | 60 or more, 100 when a line carries a label |
| Frame padding | 40 |
| Empty margin around the page frame | 40 |
| Alignment | Boxes in a row share a top edge; boxes in a column share a centre line |

Empty space is not waste; it is how the eye finds the next step.

## Wording

| BAD | BETTER |
| --- | --- |
| `ผู้ใช้ตรวจ แก้/ติ๊ก แล้วกดยืนยัน (ซ้ำให้ข้าม)` | ผู้ใช้ตรวจและยืนยัน |
| `คัดลอกโครงรายวิชา 7 ตาราง (หน้า 2)` | คัดลอกรายวิชา |
| `ระบบเลือกวิชาตาม STUDY_PLAN เก็บ copiedFrom` | ระบบเลือกวิชาตามแผนการเรียน |

Write the way you would explain it across a table: verb first, no abbreviations, no slashes.

## Worked rewrite

A one-page overview that came out as three text columns (input list, 6-step process, output list, rules list), a page map, and a code legend. As a diagram it is four boxes and one focus:

```text
[ เลือกชั้นปีและปีการศึกษาใหม่ ] → [ ระบบจับคู่วิชาจากแผนการเรียน ] → [ ผู้ใช้ตรวจและยืนยัน ]* → [ ได้รายวิชาชุดใหม่ ]
```

`*` is the focus (`#EEF0F8`): the one step where a person decides. The 7 tables, the edge cases and the rules go on later pages or in a separate document, one idea per page.
