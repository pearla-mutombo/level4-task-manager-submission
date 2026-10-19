# Wednesday Practice — Full CRUD and Validation

**180 minutes.** Use the Day 3 frontend and your continuous backend. `request-cases.json` is a manual verification matrix; it does not send requests by itself.

## 0–75 minutes: complete CRUD

Create a task through React, open its details, edit its title, change completion, and delete it. After each step, inspect the actual request in Network and read the task through Postman when it still exists.

Verify deletion returns HTTP 204 with an empty response body. Create another task and compare its ID with the deleted one: an ID must not be reused during the running process.

## 75–120 minutes: test rejected requests

Capture a new task's ID and run the cases in `request-cases.json`. Replace `TASK_ID` with that actual ID. An 81-character title can be prepared with:

```bash
cd "$HOME/Desktop/level4-task-manager"
backend/.venv/bin/python -c 'print("x" * 81)'
```

Most importantly, submit a valid new title with an invalid completion value. Fetch the record afterward and prove neither original field changed. Validate all input before mutating memory.

Stop the backend during a create attempt in React. Check that the failed submission keeps its title and re-enables its controls after failure. Restart and retry.

## 120–150 minutes: document requests

Record one example for each method, including success status, failure status, body, and response. Explain why `"false"` is a string while `false` is a JSON boolean. Explain why server-generated fields cannot be changed through PATCH.

## 150–180 minutes: PR

Submit implementation changes, the completed request matrix, and your notes. The main checklist is full CRUD, useful errors, actual boolean validation, and unchanged data after a rejected update.

**Optional:** Add additional tests after Thursday introduces pytest; prioritize the required manual cases today.

---

## My Day 3 Reflection: Challenges, Solutions, and What I Learned

### What I Worked On

For Day 3, I continued developing the Task Manager application by working with CRUD operations: Create, Read, Update, and Delete.

I practiced creating tasks, retrieving task information, updating titles and completion statuses, and deleting tasks through the Flask API.

I also worked on a separate Python exercise that helped me understand how to summarize task information using functions, lists, and dictionaries.

### Challenges I Experienced

One of the more challenging areas for me was understanding how the different CRUD operations work together and how Flask handles each request.

I also needed to understand the difference between valid and invalid request data, especially when updating a task's completion status.

For example, I learned that `"false"` in quotation marks is a string, while `false` without quotation marks is a Boolean value in JSON.

Another important concept was understanding why an invalid update should not change any part of an existing task.

### How I Worked Through These Challenges

I reviewed each CRUD operation separately and practiced understanding what information the request sends to Flask and what response the backend returns.

I also reviewed how task IDs are used to find specific records and why the backend should generate those IDs instead of relying on the number of tasks in a list.

For validation, I studied how Python checks the information received in a request before updating the stored task.

I also worked through the task summary exercise to practice using functions and organizing information from Python lists and dictionaries.

### What I Learned

Day 3 helped me better understand how a frontend and backend work together to manage information.

I learned that CRUD operations are the foundation of many applications because they allow users to create, view, modify, and remove information.

I also learned why validation and error handling are important. A backend should reject invalid information and protect existing data from unintended changes.

One of my biggest takeaways was understanding that a successful application needs to handle both valid requests and situations where something goes wrong.
