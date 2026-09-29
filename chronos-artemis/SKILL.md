---
name: chronos-artemis
description: >-
  Time and task management across Google Calendar and ClickUp. Sorts every captured item into
  one of three kinds before touching a tool: a schedule (fixed clock time, lives in Google
  Calendar), a task (an outcome with a done state, lives in ClickUp) or an activity (ongoing time
  spent with no done state — habits, focus blocks, practice — planned as calendar blocks and
  logged as time). Classifies every task as To Do, In Progress or Completed whatever the list's
  own status names are, and moves tasks between them. Runs capture and triage, daily planning and
  time-blocking, status updates, meeting prep, overload and conflict checks, rescheduling and
  weekly reviews, and keeps each calendar block linked to its task. Use when asked "plan my day",
  "what's on my plate", "add this to my calendar", "make a task for", "I finished X", "mark it in
  progress", "block time for", "am I overbooked", "weekly review", "what slipped this week",
  "sync my calendar with ClickUp", "จัดตารางวันนี้", "วันนี้มีงานอะไรบ้าง", "เพิ่มนัด", "สร้างงานใน
  ClickUp", "งานนี้เสร็จแล้ว", "สรุปงานประจำสัปดาห์". Not for setting up or debugging the Calendar or
  ClickUp MCP connection itself (hermes-olympus), sprint or team capacity planning across many
  people, project roadmaps, or building a scheduling feature into an application.
license: MIT
metadata:
  author: tp-job (enhanced by Claude)
  version: "1.0.0"
  source: >-
    Personal time-management practice (capture, time-blocking, weekly review) mapped onto the
    Google Calendar MCP connector and the ClickUp MCP connector as exposed in Claude Code, and
    ClickUp's status types (open, custom, done, closed) (compiled 2026)
---

# Chronos Artemis

**Chronos** — time itself, the clock that runs whether you act or not: the schedule.
**Artemis** — the huntress who chooses her quarry and follows it to the end: the task, pursued until it is done.

Most time-management failures are **filing errors**, not effort errors: a deadline booked as a meeting blocks an afternoon it never needed; a meeting kept as a task is missed; a habit kept as a task sits "In Progress" forever. So the first move is always the same — decide what kind of thing this is, then send it to the tool that owns that kind.

| Kind | Defining test | Lives in | Has a status? | Measured by |
| --- | --- | --- | --- | --- |
| **Schedule** | Bound to a clock time it can't move without renegotiating with someone or something | Google Calendar event | No — it is upcoming, happening or past | Attendance |
| **Task** | Produces an outcome that someone can check off | ClickUp task | **To Do · In Progress · Completed** | Done or not, on time or not |
| **Activity** | Time invested in something ongoing that is never "done" | Calendar block (plan) + ClickUp time entry (actual) | No — planned or logged | Minutes and frequency against a target |

**Tools in this folder:** [chronos.py](scripts/chronos.py) classifies an item, maps any status name to the three classes, finds free slots and packs tasks into them (`python scripts/chronos.py plan day.json`); [test_chronos.py](scripts/test_chronos.py) covers it. [example-daily-plan](assets/example-daily-plan.md) walks one morning through the whole loop. [trigger-evals.json](assets/trigger-evals.json) holds the tests for this skill's description.

---

## The operating loop

```
  CAPTURE ──► CLASSIFY ──► ROUTE ──► PLAN ──► CONFIRM ──► WRITE ──► TRACK ──► REVIEW
  take it     schedule /   Calendar  fit into  show the    create /   move      what got
  in raw      task /       or        free      diff,       update,    status,   done, what
              activity     ClickUp   time      get a yes   link both  log time  slipped
```

| Need | Read |
| --- | --- |
| Decide whether an item is a schedule, a task or an activity — and the hybrids | [item-classification](references/item-classification.md) |
| Classify a task as To Do / In Progress / Completed, and when to move it | [task-status-model](references/task-status-model.md) |
| Read or write Google Calendar — events, focus time, time zones, notifications | [google-calendar](references/google-calendar.md) |
| Read or write ClickUp — lists, statuses, filters, time tracking | [clickup](references/clickup.md) |
| Link a calendar block to its task and keep the two from drifting | [sync-and-linking](references/sync-and-linking.md) |
| Turn a pile of notes into classified, routed items | [capture-and-triage](references/capture-and-triage.md) |
| Plan a day, time-block tasks, check overload and conflicts, reschedule | [planning-and-time-blocking](references/planning-and-time-blocking.md) |
| Daily brief, weekly review, "what slipped", activity streaks | [reviews-and-reporting](references/reviews-and-reporting.md) |
| The full use-case list and the requirements every workflow must meet | [requirements](references/requirements.md) |

---

## Classify first — the three questions, in order

1. **Is it pinned to a clock time by someone or something other than me?** (a person, a venue, a flight, a class) → **schedule**.
2. **Does it end in an outcome I can check off?** → **task** — even if a time is mentioned: that time is a *due date* or a *planned block*, not an event.
3. **Otherwise it is time invested in something ongoing** → **activity**.

Still unsure after the three questions? Ask the user one short question. If they don't answer, file it as a **task** — a task can be scheduled later, but a wrong calendar event blocks time and may notify other people.

| Said | BAD | BETTER |
| --- | --- | --- |
| "Submit the report by Friday 5pm" | Calendar event Fri 17:00 | ClickUp task, due Fri 17:00 · optional work block before it |
| "Sync with Mai at 2" | ClickUp task "Sync with Mai" | Calendar event 14:00–14:30 with Mai |
| "Go to the gym 3× a week" | ClickUp task that is never Completed | Activity: 3 recurring calendar blocks · target 3/week |
| "Prep for the board meeting Tuesday 10:00" | One event | Schedule (the meeting) **+** task (prep, due before 10:00) |
| "Work on the thesis 2h today" | Task "Thesis" moved to In Progress forever | Activity block today, linked to the thesis task's next concrete subtask |

---

## Task status — three classes, whatever the list calls them

ClickUp lists use their own status names. Always reduce them to three classes, and write back using the list's own name for the class you want.

| Class | ClickUp status type | Typical names | Move here when |
| --- | --- | --- | --- |
| **To Do** | `open` · a `custom` status named like backlog / ready | to do, backlog, open, ready, planned | Captured; not started; reopened |
| **In Progress** | `custom` | in progress, doing, in review, blocked, waiting | Work has started: user says so, a timer runs, a block for it has begun |
| **Completed** | `done` · `closed` | complete, done, shipped, closed | The user confirms the outcome exists |

Rules: **never mark Completed without the user's word**; never move Completed back without asking; "blocked" and "in review" stay In Progress but are reported with their flag. Depth: [task-status-model](references/task-status-model.md).

---

## Operating rules

- **Read before write.** Look at today's calendar and the open tasks before proposing anything; search for an existing event or task before creating one.
- **Show the change, then write.** Present a table of what will be created, moved or changed; write after a clear yes. One approval covers the batch shown, not later batches.
- **Anything that notifies another person needs its own yes.** Adding attendees, or moving or cancelling an event that has them, sends email. For events with no attendees, set `notificationLevel: NONE`.
- **Never delete.** Cancel, decline or move instead — and only on request. Deleting an event or task is irreversible and needs an explicit confirmation of that exact item.
- **Ask which ClickUp list.** Never guess a list for a new task; remember the answer for the rest of the session.
- **One time zone.** Use the user's primary calendar time zone and send ISO 8601 with an offset. Say the time zone when it could be misread.
- **Estimates are the user's.** If a task has no estimate, propose one, label it as a guess, and let the user correct it.
- **Link, don't duplicate.** A time block for a task holds the task's link in its description; the task gets the block's time. See [sync-and-linking](references/sync-and-linking.md).
- **Report what happened.** Say which writes succeeded and which failed; never report a write you did not observe.
- **Connectors missing?** If Calendar or ClickUp tools are deferred, load them; if they need authentication, tell the user to authorise the connector — never ask for tokens. Plan with what is available and say what was skipped.

---

## When not to use this

- **One quick lookup.** "What time is my 3 o'clock?" — just read the calendar; no classification pass needed.
- **Team capacity and sprints.** Allocating work across a team's people and velocity is sprint planning, not personal time management.
- **Connector setup.** A Calendar or ClickUp MCP server that won't connect is an orchestration problem, not a planning one.
- **Building a scheduler.** Writing code for a booking or calendar feature is a software task.
- **The user wants to decide.** Don't impose a plan on someone thinking aloud about priorities — offer the numbers (free time, load, due dates) and let them choose.
