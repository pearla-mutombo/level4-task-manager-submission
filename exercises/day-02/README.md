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

| Input      | Location     | Example                       |
| ---------- | ------------ | ----------------------------- |
| Identifier | Route path   | `/api/tasks/3`                |
| Filter     | Query string | `/api/tasks?status=active`    |
| New title  | JSON body    | `{"title":"Learn functions"}` |

Verify that newly created tasks appear first, remain incomplete initially, and use IDs supplied by Flask. Do not calculate IDs from list length; Wednesday's deletion would expose collisions.

## 120–150 minutes: failures and boundaries

Request a missing ID, an unknown filter, a blank title, and a request sent as text rather than JSON. Record the observed status and returned error. Update/delete controls are intentionally unavailable until Wednesday.

## 150–180 minutes: notes and PR

Include the script, request examples, and one explanation of how a loop finds a record. List the supported routes in your PR. State that application data is currently held in memory.

**Optional:** Add a separate count-only route without changing the agreed task-list response shape.

---

## My Day 2 Reflection: Challenges, Solutions, and What I Learned

### What I Worked On

For Day 2, I practiced writing Python functions, using loops and conditional statements, and returning information from functions.

I worked with `get_active_tasks()`, `find_task()`, and `clean_title()` to understand how functions can help organize code and perform specific tasks.

I also practiced working with Flask API endpoints and learned how information is passed through URL paths, query parameters, and JSON request bodies.

### Challenges I Experienced

One area I found challenging was understanding the difference between a function's parameters and its return value. I needed to understand how information gets passed into a function, how the function processes it, and how the result is returned.

I also spent time understanding the difference between route parameters, query parameters, and JSON request bodies because they are different ways of sending information to the backend.

### How I Worked Through These Challenges

I practiced writing functions using simple `for` loops and `if` statements so I could follow the logic more easily.

I also tested examples of finding a task by its ID, filtering incomplete tasks, and removing extra spaces from a title.

For the Flask API, I compared different requests to understand when information should be included in the URL path, query string, or JSON body. I reviewed how Flask validates information and returns error messages when a request is invalid.

### What I Learned

Day 2 helped me understand that functions make code easier to organize, read, and reuse.

I learned that parameters allow functions to receive information and that return statements send results back to the code that called them.

I also gained a better understanding of how React and Flask communicate through API requests and why validating information is important.

One of my biggest takeaways was that breaking a problem into smaller functions makes the code easier for me to understand and troubleshoot.
