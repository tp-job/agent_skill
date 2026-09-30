# Drafting — the cheapest medium that answers the question

The fourth discipline. A draft exists to answer one open question. Pick the medium by the question, not by habit.

---

## 1. Fidelity ladder

Climb only as far as the open question requires.

| Rung | Medium | Answers | Cost |
| --- | --- | --- | --- |
| 1 | ASCII / box sketch in markdown | what goes where, in what order | minutes |
| 2 | Diagram (Mermaid, SVG, FigJam) | flows, IA, state machines | minutes |
| 3 | Grey-box HTML | does the layout hold at 375px and 1440px? | < 1 hour |
| 4 | Hi-fi screen (HTML/CSS, Figma, Canva) | does it *feel* right, is the thesis visible? | hours |
| 5 | Prototype (clickable HTML, Figma prototype) | can a user complete the flow? | hours–day |
| 6 | Render (Blender, three.js) | lighting, material, spatial composition | hours+ |

**BAD:** a pixel-perfect Figma file to decide whether the filter goes above or beside the list.
**BETTER:** two ASCII sketches, decided in two minutes, then hi-fi on the winner only.

```
+------------------------------------------+
| Today          [search........] (+ Walk-in)|
+----------+-------------------------------+
| 08:00    | Somchai P. · check-up   [···] |
| 08:30    | — free —                      |
| 09:00    | Anna K. · follow-up     [···] |
+----------+-------------------------------+
```

---

## 2. Media — using design tools through MCP

When a design tool is connected as an MCP server, its own instructions govern the calls. The rules here are about *choosing* and *sequencing* them.

| Need | Typical medium | Before the first call |
| --- | --- | --- |
| Editable screens, components, a design system | Figma | load the Figma server's required usage skill; read existing variables and components before creating new ones |
| Marketing graphics, social, decks from a brand kit | Canva | list the brand kits and templates first; reuse before generating |
| 3D scene, product shot, spatial composition | Blender | inspect the scene summary first; never assume object names; confirm before destructive changes |
| A shareable draft with no tool dependency | a single HTML file | define colours as tokens with a dark-mode mapping |

Rules that hold across every tool:

- **Read before you write.** Existing tokens, components and scenes first — duplicating a component that exists is the design equivalent of a fourth copy of a utility.
- **One draft answers one question.** Say which question in the draft's title or first line.
- **Failed or unauthorised tool = fall back one rung,** not stall. A disconnected Figma server means an HTML draft today, not no draft.
- **Never publish or share outward without asking.** Drafts start private.

---

## 3. The design record (Format)

Every job ends with a record, written from the final draft. Without it, the next session redesigns from zero.

```markdown
# Design record — <job>

Target:     <the four answers from Stage 0>
Lead:       <who had final taste>
Thesis:     <one paragraph>
Never:      <three rules>
Tokens:     <link or table: primitive → semantic → component>
Concepts:   <names + scores; winner; salvaged idea>
Screens:    <inventory with the state of each: drafted / hi-fi / prototyped>
Checks run: <contrast ratios, breakpoint tests, hallway test result — only what was actually run>
Open:       <questions still unanswered, each with an owner>
```

"Checks run" lists only checks that were observed. An intended check goes under "Open".

---

## 4. Done when

- [ ] The draft answers the question it was made for — stated in the draft
- [ ] Every screen in the inventory has a state in the record
- [ ] The record lets someone who missed the session rebuild the design
- [ ] Nothing was shared or published without the human's yes

## Handoff to review

Pass forward: the draft, the question it answers, and its rung. Review sizes its passes to the rung. See [critique](critique.md).
