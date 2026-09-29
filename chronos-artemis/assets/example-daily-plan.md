# Example — one morning through the whole loop

A worked example, not a template to copy verbatim. Times are Asia/Bangkok (+07:00); names and IDs are invented.

## 1. The ask

> "Plan my day. Also: sync with Mai at 2 about the launch, and I need to send her the revised budget before that."

## 2. Classify

| Item | Kind | Why |
| --- | --- | --- |
| Sync with Mai at 2 | Schedule | Clock time, another person |
| Send revised budget to Mai | Task | Outcome verb + deadline ("before that") → due 13:45 |

Mai's email is not known → ask. List for the task is not known → ask.

## 3. Read

- Calendar today: Standup 10:00–10:30, Lunch 12:00–13:00.
- ClickUp (mine, To Do / In Progress, due ≤ today, plus In Progress without due):
  - [Write Q3 spec](https://app.clickup.com/t/demo1) — `doing` (custom → In Progress), est. 120 min, due Thu, high
  - [Renew domain](https://app.clickup.com/t/demo2) — `to do` (open → To Do), est. 15 min, due 26 Sep → **overdue**
- Reconcile: no existing `chronos:task=` blocks today.

## 4. Compute

`day.json` → `python scripts/chronos.py plan day.json` with working hours 09:00–18:00, buffer 10, the new 14:00 sync added as busy, and the new budget task (30 min, due today 13:45):

```
free 390 min · demand 165 min · load 0.42
09:00–09:15  Renew domain               (overdue first)
09:15–09:45  Send revised budget to Mai (due today)
10:40–12:00  Write Q3 spec (80 of 120)
13:10–13:50  Write Q3 spec (40)
unscheduled: none
```

The 15-minute gap before standup is skipped: it is below `min_block_minutes`, and the 10-minute buffers after standup and lunch are kept.

## 5. Propose

| Time | What | Kind | Action |
| --- | --- | --- | --- |
| 09:00–09:15 | Renew domain | Block → task | create FOCUS_TIME, marker |
| 09:15–09:45 | Send revised budget to Mai | Block → task | create task (list?) + block |
| 10:00–10:30 | Standup | Schedule | — |
| 10:40–12:00 | Write Q3 spec | Block → task | create |
| 13:10–13:50 | Write Q3 spec | Block → task | create |
| 14:00–14:30 | Sync with Mai — launch | Schedule | create with Mai as attendee → **sends an invitation** |

> "Load 0.42 — fits with room. Two things I need: which ClickUp list for the budget task, and Mai's email for the invite. OK to create the rest?"

## 6. Write (after "Work › Inbox, mai@example.com, yes")

1. Event "Sync with Mai — launch" 14:00–14:30, attendee mai@example.com → created.
2. Task [Send revised budget to Mai](https://app.clickup.com/t/demo3) in Work › Inbox, due today 13:45, est. 30 → created (status default `to do`).
3. Four focus blocks, each description carrying its own task, e.g.:
   ```
   ClickUp: [Write Q3 spec](https://app.clickup.com/t/demo1)
   chronos:task=demo1
   ```
   → created.
4. Each task's description gets `Calendar blocks: 2026-09-29 10:40–12:00` etc.

Reported: "6 of 6 writes succeeded."

## 7. Track

11:55 — "Budget's sent." → `clickup_get_list` for Work › Inbox → done-type status is `complete` → task [Send revised budget to Mai](https://app.clickup.com/t/demo3) → `complete`. Reported as Completed.

## 8. End of day

Blocks for *Write Q3 spec* ended; task still `doing`. Asked: "Spec — done, progressed or not started?" → "About half." Status stays In Progress; estimate updated to 60 min left; tomorrow's plan picks it up first.
