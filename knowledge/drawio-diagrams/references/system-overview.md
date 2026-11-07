# System overview

Answers "what parts does it have and who talks to whom". It is the diagram most readers see first, so it is the one that must need no prior knowledge.

## Layout

| Part | Rule |
| --- | --- |
| Outer frame | Names the system ("ภาพรวมระบบ CMAS") |
| Group frames | One per place the parts live: the user's device, the server, outside services, storage. Name each in plain words, technical word in brackets |
| Parts | A logo with its name beneath, or a plain box when no logo exists. 3 to 5 per group |
| Lines | One per conversation between groups, labelled with a verb ("ส่งคำขอ", "ตอบกลับ"). Two arrowheads only when both sides really start conversations |
| Order | Person or device on the left, storage on the right; the request goes left to right |

## What to leave out

Libraries, build tools, file names and version numbers. Keep a part only if removing it would change what the system does for a user. A build tool such as Vite is a candidate to drop; the framework the user's screen runs on is not.

## Focus

Mark the single part the reader is being told about (the new one, the risky one, the one this document is about) with `#EEF0F8`, and say so in the caption.

## BAD / BETTER

| BAD | BETTER |
| --- | --- |
| 14 logos in one frame, names at 12px | 4 groups of 3 to 4 logos, names at 16px |
| A line labelled "API" | A line labelled "ขอดูรายชื่อนักศึกษา" |
| Group named "Infra" | Group named "เซิร์ฟเวอร์ (Server)" |
| Logo with no name | Logo with its name beneath |

Logos: [logos.md](logos.md).
