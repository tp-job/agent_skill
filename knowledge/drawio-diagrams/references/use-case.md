# UML use case diagram

Answers "what can each kind of user do". Notation: UML 2.5.

## Parts

| Part | How |
| --- | --- |
| Page frame | A named outer frame holding the whole diagram, so actors outside the boundary are still inside a frame |
| System boundary | A named frame inside the page frame, around all use cases; actors stay outside it |
| Actor | A person-shaped icon (`shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;`) with the role beneath, outline 2px black |
| Use case | An ellipse (`ellipse;`) holding a verb and an object: "ดูคะแนนของตัวเอง" |
| Association | Solid line, no arrowhead, from actor to use case |
| «include» | Dashed line, open arrowhead, from the larger use case to the one it always uses; label `«include»` |
| «extend» | Dashed line, open arrowhead, from the optional case to the base case; label `«extend»` |
| Generalisation | Solid line, hollow triangle, from the specific actor to the general one |

## Rules

| Rule | Why |
| --- | --- |
| Actors are roles ("อาจารย์"), never named people or systems' internals | A role stays true when the person changes |
| Every use case is a goal the actor cares about, not a button | "สมัครเรียน", not "กดปุ่มส่ง" |
| 5 to 9 use cases per boundary | Past that, split by actor group |
| Use «include» and «extend» only when two cases really share or branch; otherwise leave them out | Most diagrams need neither, and non-experts misread them |
| Direction of «include» points to the included case; «extend» points to the case being extended | The two are routinely swapped; check the arrow before saving |

These are the dashed lines the 2px solid rule allows.
