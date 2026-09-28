# Design record — Clinic "Today" screen (worked example)

A complete run of the four stages on a small, real-sized job, so the method can be seen end to end. The draft it produced is [example-draft.html](example-draft.html).

---

## Stage 0 — Target

| Question | Answer |
| --- | --- |
| What | The receptionist's "Today" screen: populated, empty-slot and late states; 375px and 1440px; light and dark |
| For whom | Clinic receptionists mid-shift, often one-handed on a phone or glancing from arm's length at a desk monitor |
| Limits | Brand teal (`#0F766E`); WCAG 2.2 AA; system fonts only (no web-font download); 44px minimum touch targets |
| Judged how | "Reschedule" for a named patient is reachable in one tap from the list; every text pair ≥ 4.5:1; layout holds at 375px with no horizontal scroll |

**Lead:** the user (clinic owner). Acting lead for this example: the agent, default stated and accepted.

---

## Stage 1 — Architecture

**Inventory (this job):** Today · populated · Today · slot free · Today · patient late · Walk-in button (opens the flow, drawn later).
**Out of scope, named so it is not forgotten:** empty day, loading, API error, the Walk-in sheet.

**Flow:**

```
Today › row "Reschedule" › slot picker
          ├─ slot free  → confirm → SMS → back to Today (toast)
          └─ slot taken → inline error + next 3 free slots
```

**Token tiers:** primitive (slate, teal, red, ink) → semantic (`color-bg`, `color-text`, `color-action`, `color-danger` …) → component (inline in the draft; extracted when a second screen exists).

---

## Stage 2 — Art direction

**Thesis:** A clinic front desk at 7 a.m.: calm, legible at arm's length, nothing that blinks. References: hospital wayfinding signage and railway timetables — big numerals, strict rows. **The risk:** appointment times are set larger than patient names, because time is what the receptionist scans for.

| Choice | Decision | Reason |
| --- | --- | --- |
| Palette | slate neutrals, teal action, red only for lateness | signage uses one action colour; red is reserved so it keeps its meaning |
| Type | system UI for text, monospace numerals for times at 28px (22px mobile) | tabular numerals align down the column like a timetable |
| Density | one row per slot, no cards | scanning a column is faster than scanning a grid |
| Motion | 150 ms opacity on hover only, disabled under reduced motion | nothing on this screen needs explaining by movement |

**Never:** a gradient behind text · more than two weights on one screen · an animation on the list itself.

---

## Stage 3 — Creativity

| Criterion (weight) | Timetable | Queue | Wall |
| --- | --- | --- | --- |
| One tap to Reschedule (3) | 2 | 3 | 1 |
| Fits the thesis (2) | 3 | 2 | 2 |
| Holds at 375px (2) | 2 | 3 | 1 |
| Build cost, inverse (1) | 3 | 2 | 2 |
| **Total** | **19** | **21** | **11** |

"Queue" (one card at a time, swipe to act) scored highest. **Lead override, recorded:** Queue hides the rest of the day, and a receptionist needs to see the next hour at a glance — an unwritten constraint, now added to the target as "the next four slots are visible without scrolling at 375×667". Re-scored with that criterion (weight 3): Timetable 25, Queue 21. **Winner: Timetable.**
**Salvaged from Queue:** the single, always-visible action per row (no overflow menu), which is what makes Reschedule one tap.

---

## Stage 4 — Drafting

Climbed to rung 3–4 (hi-fi HTML) because the open question was whether the layout holds at two widths in two themes — a sketch cannot answer that.

---

## Checks run

Only checks actually observed are listed.

| Check | Result |
| --- | --- |
| Contrast, computed with the WCAG 2.x relative-luminance formula | light: text 17.06 · muted 7.24 · action on bg 5.23 · white on action 5.47 · danger 6.18. dark: text 15.19 · muted 7.30 · muted on surface 6.76 · action 10.06 · text on action 10.06 · danger 6.77. **All ≥ 4.5:1** |
| Touch targets | every button measured at 44px tall in a 375×667 browser viewport |
| 375×667, light | no horizontal scroll (scrollWidth 375 = viewport); all four slots end by y=584 < 667 — the "next four slots visible" criterion passes |
| Dark via the OS setting (`prefers-color-scheme: dark` emulated, page served over localhost, no attribute) at 375×667 | media query matched; bg `#0B1220`, surface `#111A2E`, text `#E2E8F0`, muted `#94A3B8`, action `#2DD4BF` with `#0B1220` label, late `#F87171` — every pair is one of the computed ratios above; last row still ends at y=584 |
| `data-theme="light"` while the OS is dark | page stays light (bg `#F8FAFC`, text `#0F172A`, action `#0F766E`) — the override guard works |
| Keyboard focus | Tab order Walk-in → Reschedule; `:focus-visible` gives a solid 3px outline, 2px offset, in the action colour (10.06:1 on the dark background) |
| 1440×900, dark (forced via `data-theme`) | no horizontal scroll; content capped at 960px; tokens resolve to bg `#0B1220`, text `#E2E8F0`, action `#2DD4BF` |

## Open

| Question | Owner |
| --- | --- |
| Hallway test: time to find "Reschedule" for a named patient | clinic owner |
| Empty-day, loading and error states | next design round |
