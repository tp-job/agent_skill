# Task status model — To Do, In Progress, Completed

Only **tasks** have a status. Schedules have a time state (upcoming / happening / past); activities have a plan state (planned / logged). Don't put either on a status board.

## The three classes

| Class | Means | Entry condition | Exit |
| --- | --- | --- | --- |
| **To Do** | Accepted, not started | Created, or reopened by the user | → In Progress when work starts |
| **In Progress** | Work has started and the outcome doesn't exist yet | The user says so; a ClickUp timer runs on it; a planned block for it has started and the user confirms working | → Completed on the user's word · → To Do if parked back (ask) |
| **Completed** | The outcome exists, or the task was consciously dropped | The user confirms | → To Do only on explicit request (reopen) |

Flags ride on top of the class, they are not classes:

| Flag | Class it stays in | Report as |
| --- | --- | --- |
| `blocked` (blocked, on hold, waiting, รอ) | In Progress | "In Progress — blocked: <reason if known>" |
| `in_review` (review, QA, approval) | In Progress | "In Progress — awaiting review" |
| `cancelled` (cancelled, won't do, duplicate) | Completed | Count separately from real completions in reviews |

## Mapping ClickUp statuses

ClickUp lists define their own statuses; each has a **type**: `open` (first), `custom` (middle), `done`, `closed`. The type is authoritative; the name is a fallback.

| ClickUp type | Class | Exception |
| --- | --- | --- |
| `open` | To Do | — |
| `custom` | In Progress | A custom status named like backlog / ready / planned / not started → To Do |
| `done` | Completed | — |
| `closed` | Completed | Usually hidden from default views; prefer `done` when writing |

Unknown type (e.g. only the name came back): match the name against to-do words, then done words; anything else is In Progress. `python scripts/chronos.py status "<name>" --type <type>` applies exactly these rules and prints the `basis` it used.

## Writing a status back

The canonical class is not a valid ClickUp status on its own — the list accepts only its own names.

1. Get the list's statuses (`clickup_get_list` returns them with their types).
2. Pick the **first status by order** in the target class that carries no flag — `pick_list_status()` in [chronos.py](../scripts/chronos.py) does this.
3. For Completed, prefer the `done`-type status over `closed`.
4. If no clean status exists for the class (a list with only "open" and "closed"), ask the user which status to use and remember it for that list.

| Intent | BAD | BETTER |
| --- | --- | --- |
| Mark started | `status: "In Progress"` on a list whose middle status is "doing" → API error | Read list statuses → write `"doing"` |
| Mark finished | `status: "closed"` → the task vanishes from the user's board | Write the `done`-type status, e.g. `"complete"` |

## Transition rules

| Evidence | Proposed move | Needs the user's yes? |
| --- | --- | --- |
| "I started X", "working on X", "กำลังทำ X" | To Do → In Progress | No — the user said it |
| "X is done", "finished X", "X เสร็จแล้ว" | → Completed | No — the user said it (confirm *which* task if the name is ambiguous) |
| A ClickUp timer is running on X | To Do → In Progress | Yes — propose it |
| A planned block for X has ended | none automatically | Ask: "Did X get done, move forward, or not start?" |
| All subtasks and checklist items are done | → Completed | Yes — the parent may have its own final step |
| Due date passed, task still To Do | none — flag as **overdue** | Offer: reschedule, re-date, or drop |
| In Progress with no update for 7+ days | none — flag as **stale** | Ask in the weekly review |
| User wants to reopen a Completed task | Completed → To Do or In Progress | Yes — confirm the task |

Never infer Completed from time passing, from a block ending, or from a meeting about the task happening.

## Reporting

Group by class, then by due date. Always show counts:

```
To Do (4)        · 1 overdue
In Progress (3)  · 1 blocked · 1 in review
Completed (6)    this week · 1 cancelled
```
