# Week 1 — Day 2: Python Fundamentals and Flask API

## What I Learned

During Day 2, I practiced Python conditionals, loops, and functions. I also learned how to use Flask API routes to retrieve tasks, create new tasks, and handle errors.

## Python Functions

I completed three functions in `functions.py`:

**1. `get_active_tasks(tasks)`**

This function uses a `for` loop to go through the task list. It uses an `if` statement to check whether each task is incomplete. If the task is incomplete, it adds it to a new list and returns that list.

**2. `find_task(tasks, task_id)`**

This function loops through the tasks and compares each task's ID with the requested ID. If it finds a match, it returns that task. If no matching task exists, it returns `None`.

**3. `clean_title(title)`**

This function uses `.strip()` to remove extra spaces from the beginning and end of a task title.

## Difference Between a Loop and a Function

A **loop** repeats instructions, such as checking every task in a list.

A **function** groups instructions together so I can call them whenever I need them.

A function can also contain a loop. For example, my `find_task()` function uses a loop to search for a matching task.

## Flask API Routes Tested

| Method | Route                         | Result                     |
| ------ | ----------------------------- | -------------------------- |
| GET    | `/api/tasks`                  | Retrieved the task list    |
| GET    | `/api/tasks?status=all`       | Retrieved all tasks        |
| GET    | `/api/tasks?status=active`    | Retrieved incomplete tasks |
| GET    | `/api/tasks?status=completed` | Retrieved completed tasks  |
| GET    | `/api/tasks/3`                | Retrieved task 3           |
| GET    | `/api/tasks/4`                | Retrieved task 4           |
| POST   | `/api/tasks`                  | Created two new tasks      |

I created the tasks "Learn Python functions" and "Practice Python loops and conditionals." Flask automatically assigned them IDs 3 and 4.

I also verified that the newest tasks appear first in the task list.

### Example POST Request

```bash
curl -i -X POST "http://127.0.0.1:5001/api/tasks" \
  -H "Content-Type: application/json" \
  -d '{"title":"Learn Python functions"}'
```

The API returned HTTP status `201 Created`, and the new task was initially marked incomplete.

## Error-Handling Tests

| Test                             | Expected and Observed Status | Error Message                                     |
| -------------------------------- | ---------------------------- | ------------------------------------------------- |
| Request nonexistent task ID 999  | 404 Not Found                | `Task not found.`                                 |
| Use unsupported status `pending` | 400 Bad Request              | `Status must be all, active, or completed.`       |
| Create a task with a blank title | 400 Bad Request              | `Title must contain between 1 and 80 characters.` |
| Send plain text instead of JSON  | 415 Unsupported Media Type   | `Send the request body as application/json.`      |

All four error-handling tests passed.

## How the Task Search Works

When the API receives a request for a particular task ID, it searches through the tasks to find a matching record. If a task matches, the API returns it. If there is no match, the API responds with a `404 Not Found` error.

## Where the Tasks Are Stored

The Flask application currently stores tasks **in memory**, rather than in a database.

This means tasks created while the server is running will disappear when the Flask application restarts.

## Day 2 Reflection

Day 2 helped me understand how Python functions, loops, and conditions work together. I also learned how to communicate with a Flask backend using GET and POST requests and how HTTP status codes explain whether a request was successful or unsuccessful.

I am becoming more comfortable reading Terminal output and understanding how the backend handles requests.
