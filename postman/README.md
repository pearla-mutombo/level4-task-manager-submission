# Postman — Week 1 Flask Requests

## Import once

1. Open Postman and choose **Import**.
2. Import `week-1-task-manager.postman_collection.json`.
3. Import `local.postman_environment.json`.
4. Select **Level 4 Week 1 Local** in the environment selector.
5. Confirm `base_url` is `http://127.0.0.1:5001/api`.
6. Start the matching Flask checkpoint or your own backend. Postman does not start the server.

No access tokens, accounts, passwords, or provider keys are needed this week.

## Use the matching day folder

| Folder | What it checks | Required backend |
|---|---|---|
| Day 01 | First JSON greeting | Day 1 or later |
| Day 02 | Lists, query filters, create, detail, early failures | Day 2 or later |
| Day 03 | CRUD, atomic validation, request errors, ID counter | Day 3 or later |
| Day 04 | Regression after the factory/module refactor | Day 4 or later |
| Day 05 | Final API workflow | Day 5 |

Select a folder and use **Run** to execute requests in their listed order, or click each request and **Send** while teaching. Running later folders against Monday's backend will fail because those routes do not exist yet.

Each workflow folder creates a practice task first. Its response script stores the server's actual `id` as environment variable `task_id`. Detail/update/delete requests use `{{task_id}}`. Do not hard-code an ID copied from another student's result.

After restarting Flask, begin the folder again from its create step. A previously captured ID may no longer refer to the same record. The Day 3 deletion request also records `previous_deleted_id`; the next creation proves that the running process advances its counter.

## Inspect a successful request

For **Create and capture actual ID**, inspect:

- Method: POST.
- URL: `{{base_url}}/tasks`.
- Body: raw JSON containing a title.
- Header: `Content-Type: application/json`.
- Response: status 201 and a task object with server-assigned ID/time.
- Tests: status, JSON, fields, trimmed title, and incomplete initial state.
- Environment: the new `task_id` captured for the next request.

The **Tests** or **Scripts → Post-response** area shows the supplied assertions, depending on your Postman interface version. A failed assertion should be investigated using the actual request and response rather than hidden by changing its expectation blindly.

## Inspect rejected requests

The collection deliberately sends blank/oversized titles, non-object JSON, malformed JSON, strings or numbers as completion values, protected fields, and an empty update. These requests are expected to return errors. A 400 response is a passing result for a request whose test expects 400.

For the mixed-field update, the following GET compares the saved title and completion with the last successful response. This proves validation ran before mutation. Delete expects an empty body with HTTP 204; the next GET expects 404.

## Browser and persistence demonstrations

Postman is an API verification tool. It does not verify React's rendering, loading states, or browser CORS policy. Use the daily guide for those demonstrations.

To compare persistence, create a task, refresh React, and fetch the same ID. Then stop/restart Flask and fetch again. Restart restores seed data. Repeat the create step before continuing subsequent requests.

If you intentionally change the health greeting during practice, the health assertion only checks that a nonempty message exists; inspect its actual value in React. The supplied checkpoint's default is `Hello from Flask`.

See [API contract](../../guides/api-contract.md) for body shapes, status codes, and validation rules. From a copied student project, use the daily guide supplied by your instructor for that reference.
