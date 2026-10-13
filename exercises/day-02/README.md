# Tuesday Practice — Functions and Request Inputs

**180 minutes.** Keep extending Monday's backend. Run the frontend in Day 2 mode.

## 0–45 minutes: functions

Complete `functions.py`:

- `get_active_tasks(tasks)` returns a new list containing incomplete tasks.
- `find_task(tasks, task_id)` returns the matching dictionary, or `None` when missing.
- `clean_title(title)` returns a trimmed string.

Use explicit `for` loops and `if` statements before trying list comprehensions. Explain each parameter, return value, and condition.

```bash
cd "$HOME/Desktop/level4-task-manager"
backend/.venv/bin/python exercises/day-02/functions.py
```

Add print calls that demonstrate one match, one missing ID, and a title with surrounding spaces.

## 45–120 minutes: API practice

Implement or finish list, detail, and create routes. Use `status=active`, `completed`, and `all` in Postman. Create two tasks, capture their actual returned IDs, and fetch each through its detail route.

Compare these inputs:

| Input | Location | Example |
|---|---|---|
| Identifier | Route path | `/api/tasks/3` |
| Filter | Query string | `/api/tasks?status=active` |
| New title | JSON body | `{"title":"Learn functions"}` |

Verify that newly created tasks appear first, remain incomplete initially, and use IDs supplied by Flask. Do not calculate IDs from list length; Wednesday's deletion would expose collisions.

## 120–150 minutes: failures and boundaries

Request a missing ID, an unknown filter, a blank title, and a request sent as text rather than JSON. Record the observed status and returned error. Update/delete controls are intentionally unavailable until Wednesday.

## 150–180 minutes: notes and PR

Include the script, request examples, and one explanation of how a loop finds a record. List the supported routes in your PR. State that application data is currently held in memory.

**Optional:** Add a separate count-only route without changing the agreed task-list response shape.
