# Planning and time-blocking

Covers: plan my day or week, block time for a task, "am I overbooked", conflicts, and rescheduling what slipped.

## Plan a day

1. **Read the day.** `list_events` for the working window (ask once for working hours; default 09:00–18:00 in the user's zone). Keep the events that are busy (see [google-calendar](google-calendar.md) §Reading).
2. **Read the work.** ClickUp tasks assigned to the user that are To Do or In Progress and due today or earlier, plus In Progress tasks with no due date, plus anything the user names.
3. **Reconcile** existing blocks against task status — [sync-and-linking](sync-and-linking.md) §Reconcile pass.
4. **Compute** with `python scripts/chronos.py plan day.json`: free minutes, demand, load, proposed blocks, and what doesn't fit.
5. **Propose** — the schedule as fixed rows, blocks as proposed rows, overflow listed with a decision each.
6. **Write on a yes:** focus blocks with the link marker; update each task's description with its block.

### Packing order

The script's rule, which you may overrule with the user's stated priorities:

1. Overdue and due-today first.
2. Then priority: urgent → high → normal → low.
3. Then earliest due date, then smallest estimate.
4. Tasks larger than a gap are split across gaps; no block shorter than `min_block_minutes` (default 25).
5. A buffer after each meeting (`buffer_minutes`, suggest 10) — back-to-back plans fail.

**Do the hardest work in the user's best hours** if they have said when those are; otherwise don't assume a chronotype.

### Load

| Load (demand ÷ free) | Read it as | Say |
| --- | --- | --- |
| ≤ 0.7 | Realistic — leaves slack for interruptions | "Fits, with room." |
| 0.7 – 1.0 | Tight — any overrun slips something | Name what slips first |
| > 1.0 | Overbooked — it will not all happen | List the overflow; ask what to drop, delegate or re-date |

Never "solve" overload by shrinking estimates without the user.

## Block time for one task

"Block 2 hours for the spec tomorrow" → find the task (or create it, asking the list), find slots with `chronos.py slots`, propose the earliest fitting slot (or the user's preferred time), create a `FOCUS_TIME` event with the marker, note the block on the task. If no slot fits, say which meeting it collides with and offer alternatives — don't double-book.

## Conflicts

| Conflict | Action |
| --- | --- |
| Two schedules overlap | Report both; the user picks. Never move an event with attendees without asking — it notifies them |
| A block overlaps a new schedule | Move the block to the next free slot and say so |
| A task's due time is before any free slot | Flag it — re-date, work outside hours (user's call), or cut scope |
| Travel / location change between events | Add a buffer only if the user confirms travel time |

## Reschedule what slipped

At the end of a day or start of the next: past blocks whose task is not Completed → ask per task (done / progressed / not started), update status, then re-plan the remaining work into the coming days. Don't silently roll every task forward — a task that has slipped three times is a decision, not a scheduling problem; say so.

## Plan a week

Same steps over five working days: place schedules, then activity targets (e.g. gym Mon/Wed/Fri 18:00), then tasks by due date. Report load per day, and flag any day above 1.0.

## BAD / BETTER

| BAD | BETTER |
| --- | --- |
| Fill every free minute with blocks | Stop at load ≈ 0.8; show the remainder as "if time allows" |
| Put a 3-hour task in a 3-hour gap between meetings | Keep buffers; split into 90-minute blocks with a break |
| Create blocks, then ask | Propose the table, get a yes, then create |
| Plan without reading ClickUp because "the calendar is the plan" | Tasks drive blocks; a calendar without tasks has no priorities |
