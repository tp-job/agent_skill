# Architecture — the structure of a design

The first discipline. It decides *what exists and how it is organised* before anyone decides how it looks. Styling an unknown screen set styles the wrong things.

---

## 1. Screen inventory

List every surface in scope, including the ones nobody draws first.

| Include | Usually forgotten |
| --- | --- |
| Primary screens | Empty state — first run, no data |
| Modals, sheets, drawers | Loading and skeleton states |
| Navigation shells | Error states — validation, network, permission |
| Transactional emails, notifications | Success and confirmation states |
| Print or export views | The 375px and the 1440px layout of each |

**BAD:** "Home, Dashboard, Settings."
**BETTER:** "Home (empty / populated), Dashboard (loading / populated / API error), Settings › Profile, Settings › Billing (card declined state), Invite modal (sent / already a member)."

An inventory is done when a builder could count the screens and get the same number you did.

---

## 2. Information architecture

Group content by how the audience looks for it, not by how the database stores it.

| Step | Method | Output |
| --- | --- | --- |
| Gather | list every content item and action | flat list |
| Group | open card sort — real users if you can reach them; if not, label it *inferred* | clusters |
| Name | use the audience's words, not internal jargon | labelled sections |
| Depth | keep any task within 3 levels; flatten anything deeper | IA tree |

Write the tree as plain text so it survives every tool:

```
App
├── Today            (default landing)
│   ├── Appointments
│   └── Walk-ins
├── Patients
│   └── Patient › History · Billing · Notes
└── Settings
    ├── Clinic
    └── Staff
```

---

## 3. User flows

One flow per job-to-be-done. Every flow has a start trigger, the happy path, and at least one failure branch that ends somewhere real.

```
Reschedule:  Today › tap appointment › "Reschedule" › pick slot
               ├─ slot free   → confirm → SMS sent → back to Today (toast)
               └─ slot taken  → inline error + next 3 free slots
```

A flow that ends at "error" with nowhere to go is not finished.

---

## 4. Design-system token architecture

Tokens are the architecture of the visual layer. Use three tiers so a rebrand touches one tier, not every component.

| Tier | Holds | Example | Changes when |
| --- | --- | --- | --- |
| **Primitive** | raw values | `teal-700: #0F766E` | the brand changes |
| **Semantic** | intent | `color-action-primary → teal-700` | a theme (dark, high-contrast) is added |
| **Component** | one component's slot | `button-primary-bg → color-action-primary` | one component is redesigned |

**BAD:** a button styled with `#0F766E` directly — dark mode now needs a find-and-replace.
**BETTER:** the button reads `button-primary-bg`; dark mode remaps one semantic token.

Define tiers for colour, type scale, spacing, radius, elevation and motion duration. Name the dark-mode mapping *now*, even if it ships later — retrofitting it is the expensive path.

**When not to apply:** a one-off poster or illustration needs a palette, not a token system. Tokens earn their cost when more than one screen or more than one theme exists.

---

## Handoff to art direction

Pass forward: the inventory, the IA tree, the flows, and the empty token tiers (names without values). Art direction fills the values.
