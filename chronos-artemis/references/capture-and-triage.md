# Capture and triage — from a pile of notes to routed items

Use when the user dumps several things at once: a brain dump, meeting notes, an email with action items, a voice-note transcript, "here's everything on my mind".

## Steps

1. **Split** the input into one line per item. One item = one kind. "Call Anna and send her the deck by Friday" is two items (a call — task or schedule — and a task).
2. **Classify** each with the three questions in [item-classification](item-classification.md). Use `chronos.py classify` on anything unclear; keep its signals for the table.
3. **Fill the fields** each kind needs. Leave unknowns empty and mark them — don't invent them.

   | Kind | Needs | Nice to have |
   | --- | --- | --- |
   | Schedule | Title, date, start, end (or duration), time zone | Attendees, location, calendar |
   | Task | Name as an outcome ("Send deck to Anna"), list | Due date, priority, estimate, parent |
   | Activity | Name, target (minutes × frequency) | Preferred days and time, related task |

4. **Deduplicate.** Search Calendar and ClickUp for each item before proposing it as new.
5. **Show the triage table** — kind, destination, fields, and "new / exists / update" — and ask about every empty required field in one message.
6. **Write on a yes**, in this order: schedules, tasks, then activity blocks (blocks need free time that schedules consume). Report each result.

## Name tasks as outcomes

| BAD | BETTER |
| --- | --- |
| "Anna" | "Send pricing deck to Anna" |
| "Taxes" | "Submit 2026 tax return" |
| "Website" | Split: "Draft homepage copy", "Fix mobile nav bug" |
| "Think about hiring" | "Decide: hire contractor or full-time (write one page)" |

## Don't

- Don't create items the user only mentioned as context ("the launch went badly" is not a task).
- Don't guess dates from vague words — "soon", "next week sometime" → ask, or file with no due date.
- Don't set priority to urgent unless the user said so; urgency inflation makes priority useless.
- Don't assign tasks to other people unless the user named them and asked for it.

## Example

Input: *"Sync with Mai at 2 about the launch, need to send her the revised budget before that. Also gym tonight and every Mon/Wed/Fri. Taxes due end of month."*

| # | Item | Kind | Destination | Fields | State |
| --- | --- | --- | --- | --- | --- |
| 1 | Sync with Mai — launch | Schedule | Calendar | Today 14:00–14:30 · Mai (email?) | New — **attendee email needed** |
| 2 | Send revised budget to Mai | Task | ClickUp › **which list?** | Due today 13:45 · estimate 30 min (guess) | New |
| 3 | Gym | Activity | Calendar, recurring | Mon/Wed/Fri 18:00, 60 min, tonight included · until? | New |
| 4 | Submit tax return | Task | ClickUp › Personal | Due 2026-09-30 | Exists — "Taxes 2026" found; reuse? |
