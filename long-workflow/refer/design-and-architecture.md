# Design & Architecture (Stage 2)

Design is how you think before you code, not a formality between requirements and the keyboard. Skipping it doesn't save time — it moves the thinking into the debugging phase, where it's more expensive.

## Required before moving to development

- [ ] **Wireframe or UI mockup** — for any user-facing change, even a small one. A rough sketch in words or ASCII is enough; the point is that the shape exists somewhere other than your head.
- [ ] **Logic flow** — a sequence diagram, flowchart, or even a numbered list showing system behavior branch by branch.
- [ ] **Use case** — who does what, when, and what the system responds with. This becomes the QA and UAT script later, so write it in testable terms now.
- [ ] **Data model or API contract** — the agreed schema or endpoint shape, not assumed from memory.
- [ ] **Error and fallback behavior** — defined up front, not left to whatever feels right while coding.

## How to reason through the logic

- Map the happy path first, then deliberately ask "what if" for every step: what if the input is empty, what if the call fails, what if it's called twice, what if the user doesn't have permission.
- Use a flow sketch even for something that feels obvious — gaps show up in the act of drawing them, not in the act of imagining them.
- For anything non-trivial, state the design back to the user in a sentence or two before writing code, the same way you'd confirm a requirement. This is the cheapest point in the whole workflow to catch a wrong assumption.

## Failure mode this prevents

Writing code that satisfies the happy path and discovering the edge cases in production, where each one becomes an incident instead of a design-time decision.