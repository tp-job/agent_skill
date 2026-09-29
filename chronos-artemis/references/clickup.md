# ClickUp — reading and writing tasks

Written against the ClickUp MCP connector as exposed in Claude Code (tools named `clickup_*`: `clickup_get_workspace_hierarchy`, `clickup_get_list`, `clickup_filter_tasks`, `clickup_search`, `clickup_get_task`, `clickup_create_task`, `clickup_update_task`, `clickup_add_time_entry`, `clickup_start_time_tracking`, `clickup_stop_time_tracking`, `clickup_get_time_entries`, `clickup_resolve_assignees`, plus `clickup_get_operators` / `clickup_execute_operator` for bulk operations). Load the schemas you need in one batch. If a parameter here disagrees with the loaded schema, the schema wins.

## What lives here

| Kind | ClickUp form |
| --- | --- |
| Task | A task in a list, with status, due date, priority, time estimate |
| Task milestone of an activity ("finish unit 3") | A task — it has an outcome |
| Activity (actual time spent) | A time entry — on the related task if there is one, otherwise on a standing "Routines" task the user chooses |
| Schedule | Not here. Mention the event link in a task's description if a task depends on it |

## Structure to resolve once per session

1. `clickup_get_workspace_hierarchy` → spaces, folders, lists. Note the lists the user actually uses.
2. **Ask which list** for new tasks. The tool itself requires it; never guess. Remember the answer ("Work tasks go to Work › Inbox").
3. `clickup_get_list` for each list you will write statuses to → its statuses and their **types**, needed for [task-status-model](task-status-model.md).
4. `clickup_resolve_assignees` with `"me"` → the user's ID, for filtering "my tasks".

## Reading

| Need | Call |
| --- | --- |
| My open tasks due by today | `clickup_filter_tasks` with `assignees: [me]`, `due_date_to: <today>` |
| Everything In Progress | `clickup_filter_tasks` with `statuses:` every In Progress-class name across the relevant lists |
| Completed this week | `clickup_filter_tasks` with `include_closed: true`, `date_closed_from`, `date_closed_to` |
| Find a task by words ("the pricing email") | `clickup_search`, then `clickup_get_task` to confirm |
| Time spent | `clickup_get_time_entries` for a date range |

**Paginate.** `clickup_filter_tasks` returns 100 per page with `has_more`; keep calling with `next_page` until it is false. A summary built from page one is wrong.

## Writing

| Action | Call | Care |
| --- | --- | --- |
| Create task | `clickup_create_task` with `name`, `list_id`, and what is known: `due_date` (`YYYY-MM-DD` or `YYYY-MM-DD HH:MM`), `priority`, `time_estimate` (minutes, string), `markdown_description` | Omit `status` to get the list's default (To Do class) |
| Subtask | `clickup_create_task` with `parent` | For a hybrid's concrete milestones |
| Change status | `clickup_update_task` with `status` = the list's own name for the target class | Never the canonical label unless the list uses it |
| Re-date | `clickup_update_task` with `due_date` (or `"none"` to clear) | Tell the user the old and new date |
| Start / stop working | `clickup_start_time_tracking` / `clickup_stop_time_tracking` | Starting a timer is evidence for In Progress — propose the move |
| Log time after the fact | `clickup_add_time_entry` | Activities and finished blocks |
| Many tasks at once | `clickup_get_operators`, then `clickup_execute_operator` | Don't loop single-task updates over a list |
| Delete | `clickup_delete_task` only on explicit request for that exact task | Prefer a cancelled/closed status — history survives |

## Presenting tasks

Write a task as an inline link with its name as anchor text: `[Write Q3 spec](https://app.clickup.com/t/abc123)`. Never a bare URL on its own line.

## BAD / BETTER

| BAD | BETTER |
| --- | --- |
| Create the task in the first list returned | Ask "Which list — Work › Inbox or Personal?" |
| `status: "Completed"` | Read the list's statuses; write `"complete"` (its `done`-type status) |
| One task named "Exercise" left In Progress for months | An activity: calendar blocks + time entries; milestones as tasks |
| Report "you have 100 open tasks" from one page | Page until `has_more` is false; report the real count |
