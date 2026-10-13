# Monday Practice — Values and the First API

**180 minutes.** Begin in your separate student application, with Monday's Flask server and `npm run dev:day-01` frontend.

## 0–45 minutes: Python values and collections

Open `values.py`. Inspect the supplied list of two dictionaries and predict the result before printing:

1. Print the first task's title and the second task's completion value.
2. Print the number of tasks using `len(tasks)`.
3. Change the first task's title by assigning its dictionary key, then print it again.
4. Append a third task dictionary and print the new list length.
5. Print `type()` for a title, identifier, completion value, list, and dictionary.
6. Write a comment explaining why Python `False` appears as JSON `false` in a response.

Run from the project root using the backend's interpreter:

```bash
cd "$HOME/Desktop/level4-task-manager"
backend/.venv/bin/python exercises/day-01/values.py
```

This executes a separate practice script; it does not start Flask or change the running application's tasks.

## 45–105 minutes: another small JSON route

In `backend/app.py`, add `GET /api/about`. Return an object with `language`, `framework`, and `storage` values describing this application. Keep the existing health route working. Explain the decorator, function name, indentation, and returned dictionary.

Use Postman and a spare terminal:

```bash
curl -i http://127.0.0.1:5001/api/about
```

Expect HTTP 200 and the object you chose. The provided frontend calls health, not this extra route. Change the health message and prove React displays the changed server response.

## 105–150 minutes: trace requests

Find the health request in the browser Network panel. Record its URL, method, status, response body, and the matching backend log. Explain which process sends the request and which process returns it.

Stop Flask with Control+C and retry in React. Record the visible error. Restart Flask and prove the connection recovers.

## 150–180 minutes: notes and PR

Submit the Python script, extra route, request evidence, and a short explanation of Python lists/dictionaries. Include your first daily PR and any blockers. Do not commit `.venv`, `.env.local`, or `node_modules`.

**Optional after required work:** Use a query parameter to personalize a greeting, after reviewing Tuesday's request-input explanation with your instructor.
