# Reviews and reporting

Covers: daily brief ("what's on my plate"), end-of-day wrap-up, weekly review ("what slipped this week"), and activity tracking against targets.

## Daily brief

Read-only. Keep it on one screen.

```
Tue 29 Sep · Asia/Bangkok · 5h 10m free · load 0.9

Schedule
  10:00–10:30  Standup
  14:00–14:30  Sync with Mai (launch)

Tasks — To Do / In Progress
  ! Send revised budget to Mai        due 13:45 · To Do · 30m
    Write Q3 spec                      due Thu   · In Progress · 2h left
    Fix mobile nav bug                 due —     · In Progress — blocked (waiting on design)

Activities
  Gym 18:00 (2/3 this week)

Overdue: 1 — Renew domain (due 26 Sep)
```

Order: schedule by time → tasks by class (In Progress before To Do when due equally), then due → activities → overdue. Offer to plan (time-block) only after the brief.

## End-of-day wrap-up

1. List today's blocks and the tasks they served.
2. For each task not Completed, ask one question: done / progressed / not started.
3. Update statuses from the answers; log time entries if the user tracks time.
4. Offer to re-plan tomorrow with what's left.

## Weekly review

| Section | Source | Notes |
| --- | --- | --- |
| **Completed** | `clickup_filter_tasks` with `include_closed`, `date_closed_from/to` = the week | Separate `cancelled` from done |
| **Slipped** | Tasks whose due date fell in the week and aren't Completed | Show how many times each was re-dated, if known |
| **Stale** | In Progress, no update in 7+ days | Ask: still active, blocked, or drop? |
| **Time** | Calendar: hours in meetings vs focus blocks. ClickUp: time entries | Planned vs actual, if both exist |
| **Activities** | Blocks and entries per activity | Actual vs target ("gym 2/3") |
| **Next week** | Calendar load per day + tasks due next week | Flag days above load 1.0 |

End with **three decisions for the user**, not a list of observations — e.g. "Drop or re-date 'Renew domain' (slipped 3×)?"

## Activity tracking

| Activity | Target | Planned | Done | Streak |
| --- | --- | --- | --- | --- |
| Gym | 3/week | 3 | 2 | — |
| Reading | 20 min × 5/week | 5 | 5 | 3 weeks |

"Done" counts logged time entries or blocks the user confirmed — not blocks that merely existed. A missed habit is reported plainly; don't moralise.

## Rules for every report

- State the date range and time zone at the top.
- Counts come from complete data — paginate ClickUp to the end.
- Link tasks by name: `[Write Q3 spec](https://app.clickup.com/t/...)`.
- Distinguish **facts** (status, time entries) from **inferences** (a block that ended "probably" meant progress).
- Reports are read-only: propose changes, don't make them inside a report.
