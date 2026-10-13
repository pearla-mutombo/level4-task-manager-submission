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
