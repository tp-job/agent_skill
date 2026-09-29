# Google Calendar — reading and writing

Written against the Google Calendar MCP connector as exposed in Claude Code (tool names end in `list_calendars`, `list_events`, `search_events`, `get_event`, `create_event`, `update_event`, `delete_event`, `respond_to_event`, `suggest_time`). The server prefix differs per install; load the schemas you need in one batch before the first call. If a parameter here disagrees with the loaded schema, the schema wins.

## What lives here

| Kind | Calendar form | `eventType` | Attendees | `availability` |
| --- | --- | --- | --- | --- |
| Schedule | Regular event, or all-day | `DEFAULT` | As given by the user | Busy |
| Schedule (away) | Out of office | `OUT_OF_OFFICE` (never all-day) | None | Busy |
| Task time block | Focus block linked to the task | `FOCUS_TIME` (never all-day) | None | Busy |
| Activity block | Regular or focus block, often recurring | `DEFAULT` or `FOCUS_TIME` | None | Busy, or Free for soft habits |

Tasks themselves never become events. A **due date** is not a calendar event; add at most a reminder on the task in ClickUp.

## Reading

| Need | Call | Notes |
| --- | --- | --- |
| Today / this week | `list_events` with `startTime`, `endTime`, `orderBy: startTime` | Pass `eventType` including `OUT_OF_OFFICE` and `FOCUS_TIME` — the defaults already include them; add `WORKING_LOCATION` only if needed |
| Find an existing event by words | `search_events` (primary) or `list_events` with `fullText` | Search **before** creating, to avoid duplicates |
| Which calendars exist | `list_calendars` | Ask before writing to a non-primary calendar |
| Free time with other people | `suggest_time` with `attendeeEmails`, `durationMinutes`, working-hour `preferences` | For the user alone, compute locally with `chronos.py slots` from `list_events` |

**Busy vs free for planning:** count an event as busy unless its availability is Free, it is all-day (an all-day event is a marker, not a block — but `OUT_OF_OFFICE` all day removes the day), or the user has declined it.

## Writing

| Action | Call | Required care |
| --- | --- | --- |
| New schedule, no attendees | `create_event` with `summary`, `startTime`, `endTime` (ISO 8601 with offset) | `notificationLevel: NONE` is irrelevant without attendees; keep default reminders |
| New schedule **with attendees** | `create_event` + `attendees` | **Sends invitations.** Confirm the exact attendee list and time first. Add Meet only if asked (`addGoogleMeetUrl`) |
| Task / activity block | `create_event` with `eventType: FOCUS_TIME`, description containing the task link | No attendees; see [sync-and-linking](sync-and-linking.md) for the marker line |
| Recurring activity | `create_event` with `recurrenceData: ["RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR"]` | Confirm the end: `COUNT=` or `UNTIL=`; an open-ended rule is forever |
| Move an event | `update_event` with `eventId`, new `startTime` (duration is preserved) | Has attendees → `notificationLevel` matters; ask whether to notify (`ALL`) or not (`NONE`) |
| Reply to an invitation | `respond_to_event` | Accept / decline sends a response to the organiser — confirm |
| Remove | Prefer declining or moving. `delete_event` only on explicit request for that exact event | Deleting a meeting you organise cancels it for everyone |

## Time zones

- Read the user's primary calendar time zone once per session and use it everywhere.
- Always send full ISO 8601 with offset: `2026-09-29T14:00:00+07:00`. Passing `timeZone` overrides the offsets.
- "Tomorrow at 9" is resolved in the user's zone, not UTC. Say the zone back when the user is travelling or the event has attendees elsewhere.
- ClickUp due dates are interpreted in the ClickUp workspace's zone — check they agree before linking.

## BAD / BETTER

| BAD | BETTER |
| --- | --- |
| Create "Report due" as an event on Friday 17:00 | Due date on the ClickUp task; a focus block Thursday afternoon to write it |
| Create a meeting with three attendees straight from "set up a sync with the team" | Propose a time from `suggest_time`, list the attendees, get a yes, then create |
| Delete yesterday's missed focus block | Leave it (history of the plan) or move it; delete only if asked |
| `startTime: "2026-09-29T14:00:00"` (no offset) | `startTime: "2026-09-29T14:00:00+07:00"` |
