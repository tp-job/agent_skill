# Sync and linking — keeping a block and its task together

There is no automatic two-way sync between Google Calendar and ClickUp in this workflow. What keeps them consistent is a **link written into both sides** and a **reconcile pass** whenever planning or reviewing.

## The link

| Side | Where | What |
| --- | --- | --- |
| Calendar block | First line of the event description | `ClickUp: [<task name>](<task url>)` then a line `chronos:task=<task id>` |
| ClickUp task | End of the markdown description | `Calendar blocks: <date> <start>–<end>` — one line per block, newest last |

The `chronos:task=<id>` marker is what makes the link machine-findable: `list_events` with `fullText: "chronos:task=<id>"` finds every block for a task. Keep the marker exact; don't translate or reformat it.

Event title for a block: `▸ <task name>` (short, recognisable on a phone). Don't put the status in the title — it goes stale.

## Idempotency — never create twice

Before creating a block for a task, search for its marker on that date. Before creating a task from a captured note, search ClickUp for the name. If something matches, show it and ask: reuse, update or create another.

| BAD | BETTER |
| --- | --- |
| Re-running "plan my day" creates a second set of blocks | Search `chronos:task=` markers for today; update the existing blocks' times |
| Creating "Write spec" when "Write Q3 spec" exists | Search first; offer the match |

## Reconcile pass

Run it at the start of every plan and every review. Each row is a finding to report, never an automatic fix.

| Condition | Found by | Offer |
| --- | --- | --- |
| Block exists, task is Completed | Marker → task status | Free the block (move to another task, or leave as history) |
| Block ended, task still To Do | Past blocks with markers | Ask: done, progressed, or not started? Update status on the answer |
| Task due today or overdue, no block and no free time | Filter + slots | Re-date, drop scope, or move something |
| Block's task no longer exists | Marker → `clickup_get_task` fails | Remove the marker or the block (ask) |
| Task moved to another list | Task found, list changed | Nothing — the link is by ID |
| Event with attendees overlaps a block | Slots overlap | Move the block, never the meeting |

## Direction of truth

| Field | Source of truth | Why |
| --- | --- | --- |
| Whether the work is done | ClickUp status | The task owns the outcome |
| When the work happens | Calendar block | The calendar owns time |
| Due date | ClickUp | A deadline is a task property |
| Actual time spent | ClickUp time entries | Blocks are plans; entries are facts |
| Meeting time | Calendar | Other people depend on it |

When the two disagree, update the side that is **not** the source of truth — and say what changed.
