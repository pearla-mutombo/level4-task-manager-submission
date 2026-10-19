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

---

## My Day 1 Reflection: Challenges, Solutions, and What I Learned

### What I Worked On

For Day 1, I practiced using Python variables, lists, dictionaries, and different data types. I also worked with the Flask backend and added an `/api/about` endpoint that returns information about the application in JSON format.

### Challenges I Experienced

One area I had to spend extra time understanding was how Python lists and dictionaries work together. I wanted to understand how to access a particular task, update its information, and add another task without confusing the list with the dictionaries inside it.

I also needed to understand how Flask routes work, especially the purpose of a route decorator and how Python indentation affects the code.

### How I Worked Through These Challenges

I broke the exercises into smaller steps and reviewed what each line of code was doing. I practiced accessing dictionary values, changing task information, and printing the results to understand how the data changed.

For the Flask endpoint, I reviewed how the route decorator connects a URL to a Python function and how `jsonify()` returns information in JSON format.

### What I Learned

Day 1 helped me become more comfortable reading Python code and understanding how information is organized in lists and dictionaries.

I also learned that the frontend and backend have different responsibilities. React sends requests, and Flask processes those requests and sends responses.

One important lesson for me was to take my time understanding the code rather than just getting it to run.
