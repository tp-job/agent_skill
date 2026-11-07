# UML sequence diagram

Answers "who sends what to whom, in what order". Notation: UML 2.5.

## Parts

| Part | How |
| --- | --- |
| Participant | A named box at the top; a logo may sit above its name. Style `shape=umlLifeline;perimeter=lifelinePerimeter;container=1;collapsible=0;recursiveResize=0;` plus BOX |
| Lifeline | The vertical line below a participant; its dashes are part of UML and allowed |
| Message | Solid line, `endArrow=block`, label is a verb phrase in the reader's language |
| Return | `dashed=1;endArrow=open;`, label says what comes back |
| Activation | Thin rectangle on the lifeline while that participant is working |
| Alternative | A frame named `alt` with a one-line condition per part |

## Rules

| Rule | Why |
| --- | --- |
| 3 to 5 participants | Wider than five and 16px labels no longer fit |
| Time runs top to bottom; messages never point upward except returns | The order has to be readable without numbers |
| Number each message (1, 2, 3 …) at the start of its label | A non-expert can say "step 4" aloud |
| Name participants as the reader knows them: "ผู้ใช้", "เว็บ", "Google" | Class names mean nothing to them |
| One happy path per page; error paths go in an `alt` frame or a second page | Keeps the main story straight |

Validate with the script: every participant must be inside the page frame, messages must have `source` and `target`, and the only dashes are returns and lifelines.
