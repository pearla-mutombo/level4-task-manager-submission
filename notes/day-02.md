# Day 2 Progress Notes — Tuesday, October 13, 2026

## Topic: Python Functions and Flask Request Inputs

### What I Worked On

On Day 2, I focused on understanding how Python functions work and how they help organize code into smaller, reusable pieces.

I practiced writing functions using parameters, return statements, `for` loops, and `if` statements.

I worked with three functions:

- `get_active_tasks()` — returns tasks that have not been completed.
- `find_task()` — searches for a task using its ID.
- `clean_title()` — removes extra spaces from the beginning and end of a task title.

I also worked on understanding how the Flask backend receives information through API requests, including URL paths, query parameters, and JSON request bodies.

### What I Learned

One important lesson was understanding the difference between a function's parameters and its return value.

Parameters allow a function to receive information. The function processes that information, and a `return` statement sends the result back to the code that called it.

I also learned that different parts of an HTTP request serve different purposes.

For example:

- `/api/tasks/3` uses a URL path to identify a particular task.
- `/api/tasks?status=active` uses a query parameter to filter tasks.
- `{"title": "Learn functions"}` sends task information through a JSON request body.

Understanding these differences helped me see how React communicates with Flask.

### Challenges I Experienced

I needed extra practice understanding how parameters and return values work together.

I also found it challenging at first to distinguish between URL path parameters, query parameters, and JSON request bodies.

### How I Worked Through These Challenges

I practiced writing functions with simple loops and conditional statements so I could follow the logic step by step.

I reviewed examples of finding a task by its ID, filtering incomplete tasks, and removing extra spaces from a title.

For the Flask API, I compared different request examples and reviewed how the backend handles valid and invalid information.

### Files and Features Worked On

- `exercises/day-02/functions.py` — Python function practice.
- `backend/app.py` — Flask task API endpoints.
- `exercises/day-02/README.md` — Day 2 instructions and reflection.

The Day 2 exercises cover listing tasks, retrieving an individual task, creating tasks, and filtering tasks by completion status.

### Verification and Testing

The Day 2 instructions include checking task creation, task IDs, filtering, and error handling.

During the later Week 1 verification, I confirmed these API responses:

- Creating a valid task returned HTTP `201 Created`.
- Retrieving that task by ID returned HTTP `200 OK`.
- Requesting a nonexistent task returned HTTP `404 Not Found`.
- Using an invalid status filter returned HTTP `400 Bad Request`.
- Submitting a blank title returned HTTP `400 Bad Request`.
- Sending plain text instead of JSON returned HTTP `415 Unsupported Media Type`.

These results were verified during the October 26, 2026, review, rather than being presented as tests performed on Day 2.

### My Reflection

Day 2 helped me better understand why functions are important when writing Python programs.

Breaking larger problems into smaller functions makes the code easier for me to read, understand, and troubleshoot.

I also gained a clearer understanding of how Flask receives information and why the backend must validate requests before accepting them.

I am becoming more comfortable following the logic of a program instead of only focusing on the final result.
