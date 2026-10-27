# Day 4 Progress Notes — Thursday, October 15, 2026

## Topic: JSON Files, Python Modules, Automated Testing, and Debugging

### What I Worked On

On Day 4, I continued working on my React and Flask Task Manager project. My focus was on understanding how Python handles JSON files, organizing Flask code, and using automated tests to check whether the application works correctly.

I practiced reading and writing JSON files using Python. I worked with `json_practice.py` to understand how information is loaded from a JSON file, converted into Python objects, and written back to another file.

I also worked with pytest to test my Flask API and verify that it handles both valid and invalid requests correctly.

### What I Learned About JSON Files

I learned that JSON is a format used to store and exchange information.

Python can read JSON using the `json` module and convert it into Python lists and dictionaries.

I also learned about:

- `with` statements, which help manage files safely.
- `Path`, which helps work with file locations.
- `json.load()`, which reads JSON data from a file.
- `json.dump()`, which writes Python data into JSON format.
- `FileNotFoundError`, which occurs when a file cannot be found.
- `json.JSONDecodeError`, which occurs when JSON content is not formatted correctly.

I learned that the JSON practice exercise is separate from the Flask Task Manager's in-memory storage.

### Automated Testing With pytest

I worked on automated tests that check important Flask API behavior.

The tests covered:

1. Creating a task successfully.
2. Rejecting an invalid task title.
3. Handling a task that does not exist.
4. Rejecting an invalid completion value.
5. Making sure a rejected update does not change an existing task.

I learned that automated tests help identify problems and confirm that changes have not broken important features.

### Challenges I Experienced

One of my biggest challenges on Day 4 was resolving a Git merge conflict in my Flask application.

After resolving the conflict, I ran pytest and discovered that all five tests were failing.

At first, I thought the merge conflict had already been corrected, so seeing the test failures was frustrating.

When I reviewed the error messages and examined my Flask application, I realized that important helper functions had been lost during the merge.

The missing functions included:

- `find_task()`
- `read_json_object()`
- `validate_title()`

Without these functions, parts of my Flask application could not work correctly.

### How I Resolved the Problem

I carefully reviewed the pytest error messages and checked my Flask application to identify what was missing.

I restored the helper functions, corrected the application structure, and ran the automated tests again.

After making these corrections, all five tests passed.

I also checked that my Flask API routes were registered correctly.

This experience taught me that resolving a merge conflict involves more than removing conflict markers. I also need to make sure that important functionality has not been accidentally removed.

### Files and Features Worked On

- `exercises/day-04/json_practice.py` — JSON file-handling exercise.
- `sample-data/reading-list.json` — Sample JSON data.
- `sample-data/malformed.json` — Invalid JSON used for error-handling practice.
- `backend/app.py` — Flask application and helper functions.
- `backend/tests/test_tasks.py` — Automated API tests.
- `exercises/day-04/README.md` — Day 4 instructions and reflection.

### Verification and Testing

During the October 26, 2026, Week 1 review, I ran the backend automated tests twice.

**First pytest run:**

```text
5 passed in 0.73s
```

**Second pytest run:**

```text
5 passed in 0.46s
```

Both runs passed successfully.

Running the tests twice helped verify that the tests did not depend on data left behind by a previous run.

I also reviewed the backend's API behavior through manual requests during the Week 1 verification.

### Important Note About Application Storage

The Task Manager currently stores tasks in memory.

This means the application can create, update, and delete tasks while Flask is running, but task changes are not permanently saved to a database.

The JSON file-handling exercise is separate from the Task Manager's storage.

### My Reflection

Day 4 was challenging, but it was also one of the most valuable learning experiences for me.

I learned that debugging requires patience and careful attention to error messages.

The Git merge conflict taught me not to assume that my application is working simply because Git no longer reports a conflict.

I need to run tests and review the results to make sure the code still works correctly.

I also learned that pytest is an important tool because it can identify problems that may not be obvious just by looking at the code.

My biggest takeaway from Day 4 was that making mistakes and correcting them is part of becoming a better developer. Understanding why something failed helped me learn more than simply getting the application to run.
