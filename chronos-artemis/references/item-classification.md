# Item classification — schedule, task or activity

Every item gets exactly one **primary kind**. Hybrids are split into two linked items, never filed as one item in two places.

## Definitions

| Kind | It is… | It is not… | Ends when |
| --- | --- | --- | --- |
| **Schedule** | A commitment at a fixed time, usually set by someone or something else: meetings, calls, appointments, classes, flights, events | A deadline. A deadline is when a task is *due*, not an event you attend | The clock passes its end time |
| **Task** | A unit of work with a checkable outcome: a document written, a bill paid, a bug fixed, an email sent | An aspiration ("be healthier") or an area ("marketing") — those are projects or activities | The user confirms the outcome exists → Completed |
| **Activity** | Time invested in something ongoing: habits, routines, practice, study, exercise, open-ended "work on X" blocks, admin time | Something with a done state. If it has one, it is a task, and the block is only the *time* for it | Never — it is measured by minutes and frequency |

## The decision procedure

```
Is it pinned to a clock time by someone or something other than the user?
  ├─ yes → SCHEDULE
  └─ no → Does it end in an outcome someone can check off?
            ├─ yes → TASK   (a mentioned time becomes due date or planned block)
            └─ no  → ACTIVITY
Signals conflict and the user is available → ask ONE question.
No answer → TASK (safest default: nothing blocked, nobody notified).
```

The script gives a first pass: `python scripts/chronos.py classify "<text>"` returns `kind`, `confidence` and the `signals` it used, or `kind: "ask"` with the two candidates. Treat it as evidence, not a verdict — context the script can't see (who the user works with, what "review" means in their job) wins.

## Signals

| Signal | Points to | Watch for |
| --- | --- | --- |
| A clock time with no deadline word ("at 10", "14:00–15:00") | Schedule | "before 5pm" is a deadline → task |
| Event nouns: meeting, call, standup, interview, appointment, class, flight, ประชุม, นัด | Schedule | "Prepare for the meeting" is a task about a schedule |
| Another person ("with Anna", "กับทีม") | Schedule | "Email Anna" is a task |
| Deadline words: by, due, before, deadline, ภายใน, กำหนดส่ง | Task | — |
| Outcome verbs: write, fix, send, submit, pay, book, เขียน, ส่ง, แก้ | Task | "Write every morning" → activity (recurrence, no outcome) |
| Practice words: gym, read, study, meditate, deep work, ออกกำลังกาย, อ่านหนังสือ | Activity | "Read the contract" → task (it has an end) |
| Recurrence: every, daily, 3× a week, ทุกวัน | Activity (or recurring schedule if clock-bound by others) | "Weekly 1:1 Mon 10:00" → recurring schedule |
| Duration with no clock time ("for 2 hours") | Activity | "Takes 2 hours" on a task is its estimate |

## Hybrids — split and link

| Input | Split into | Link |
| --- | --- | --- |
| "Prep for board meeting Tue 10:00" | Schedule: the meeting (if not already on the calendar) · Task: "Prepare board deck", due Tue 09:30 | Task description holds the event link; due ≥ 30 min before the start |
| "Block 2h tomorrow for the API migration" | Task: "API migration" (existing or new) · Activity block: Focus time 2h | Block description holds the task URL — see [sync-and-linking](sync-and-linking.md) |
| "Dentist Thursday 3pm, remember to bring X-rays" | Schedule: dentist · Task: "Find X-rays", due Thu before 15:00 | Task mentions the appointment |
| "Weekly report every Friday" | Recurring task in ClickUp (outcome each week) — **not** an activity | Optional recurring Friday block |
| "Learn Spanish" | Activity with a target (e.g. 20 min × 5/week) · optional tasks for concrete milestones ("Finish unit 3") | Milestones are tasks; practice is activity |

## Edge cases

| Case | Kind | Why |
| --- | --- | --- |
| All-day "Mai's birthday" | Schedule (all-day event) | Pinned to a date by the world |
| "Call the bank" (no time) | Task | Outcome: the call happened; the user picks when |
| "Call with the bank at 11" | Schedule | The bank set the time |
| Out-of-office, holiday | Schedule (`OUT_OF_OFFICE` or all-day) | It removes free time; planning must read it |
| "Inbox zero" daily | Activity | Recurs, never finally done |
| "Answer Tom's email about pricing" | Task | Specific outcome |
| A ClickUp task whose name is a whole area ("Marketing") | Ask to split into a list/folder plus concrete tasks | A task with no checkable outcome never reaches Completed |

## Record the classification

When triaging several items, show the result before writing anything:

```
| # | Item                         | Kind      | Goes to                      | Key fields                   |
|---|------------------------------|-----------|------------------------------|------------------------------|
| 1 | Sync with Mai at 2           | Schedule  | Calendar (primary)           | today 14:00–14:30, Mai       |
| 2 | Submit report by Fri 5pm     | Task      | ClickUp › Work › Reports     | due Fri 17:00, To Do         |
| 3 | Gym 3× a week                | Activity  | Calendar blocks (recurring)  | Mon/Wed/Fri 18:00, 60 min    |
```
