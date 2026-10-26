# Level 4 — Week 1 Final Report

**Project:** React + Flask Task Manager  
**Course:** Level 4 — Week 1  
**Classwork period:** October 12–16, 2026  
**Additional verification:** October 26, 2026  
**Submission deadline:** October 31, 2026, at 12:00 AM

## 1. Project Overview

For my Level 4 Week 1 assignment, I worked on a Task Manager application using React for the frontend and Flask for the backend.

The application allows users to create tasks, view existing tasks, update task information, mark tasks as completed, and delete tasks.

The Flask backend stores task information in memory. This means the application can manage tasks while the server is running, but changes are not permanently saved to a database.

Throughout the week, I practiced Python fundamentals, Flask API development, JSON handling, automated testing, debugging, and GitHub collaboration.

## 2. Daily Progress Summary

### Day 1 — Monday, October 12

**Topic: Python Fundamentals and Flask Introduction**

I practiced Python variables, lists, dictionaries, and data types.

I also worked with Flask routes, including `/api/about`, and learned how a backend sends JSON responses to a frontend.

One challenge was understanding the difference between lists and dictionaries. I worked through smaller examples to understand how Python stores and retrieves information.

### Day 2 — Tuesday, October 13

**Topic: Python Functions and Flask Request Inputs**

I practiced writing functions, using loops and conditionals, and returning values.

I also learned the difference between URL route parameters, query parameters, and JSON request bodies.

This helped me understand how Flask receives information from React and determines which task or operation a request refers to.

### Day 3 — Wednesday, October 14

**Topic: CRUD Operations and API Validation**

I worked on the four CRUD operations: Create, Read, Update, and Delete.

I learned how Flask processes POST, GET, PATCH, and DELETE requests.

I also studied why the backend must validate request data before changing a task.

An important lesson was understanding that `"false"` is a JSON string, while `false` is a JSON boolean.

### Day 4 — Thursday, October 15

**Topic: JSON Files, Modules, and Automated Tests**

I practiced reading and writing JSON files using Python.

I also worked with pytest to test important Flask API behavior.

One major challenge was resolving a Git merge conflict. After the conflict was resolved, all five backend tests failed because some helper functions were missing.

I reviewed the error messages, restored the missing functions, and ran the tests again.

All five tests passed after the corrections.

### Day 5 — Friday, October 16

**Topic: Python Modules and Reading List Report**

I created a Python Reading List Report program.

The program reads book information from JSON, counts the books, and generates a text report containing their titles.

I separated the code into a main program and a helper module.

I also learned how to troubleshoot a missing file by creating `report_utils.py` before opening it in Visual Studio Code.

Additional Week 1 verification and handoff documentation were completed on October 26.

## 3. Flask API Endpoints

The Task Manager backend includes these six main endpoints:

| HTTP Method | Endpoint          | Purpose                                        |
| ----------- | ----------------- | ---------------------------------------------- |
| GET         | `/api/health`     | Check whether the backend is responding        |
| GET         | `/api/tasks`      | Retrieve tasks, with optional status filtering |
| GET         | `/api/tasks/<id>` | Retrieve one task                              |
| POST        | `/api/tasks`      | Create a task                                  |
| PATCH       | `/api/tasks/<id>` | Update a task                                  |
| DELETE      | `/api/tasks/<id>` | Delete a task                                  |

The backend validates incoming data and returns appropriate HTTP status codes and JSON error messages.

The `/api/tasks` endpoint supports the `all`, `active`, and `completed` status filters.

## 4. Example API Request and Response

During my October 26 verification, I created a task using the following request.

**Request:**

```http
POST /api/tasks
Content-Type: application/json
```

**Request body:**

```json
{
  "title": "Complete Week 1 API verification"
}
```

**Result:** HTTP `201 Created`

The backend returned a new task with ID `3`, a server-generated creation timestamp, and an initial completion status of `false`.

I then retrieved the task.

**Request:**

```http
GET /api/tasks/3
```

**Result:** HTTP `200 OK`

The response confirmed that the task existed and contained its original title and completion status.

## 5. API Validation Results

On October 26, I completed additional manual verification using Terminal requests.

I tested all 12 cases recorded in `exercises/day-03/request-cases.json`.

| Validation Test                        | Expected | Actual | Result |
| -------------------------------------- | -------- | ------ | ------ |
| Whitespace-only task title             | 400      | 400    | PASS   |
| Numeric task title                     | 400      | 400    | PASS   |
| Unsupported field during task creation | 400      | 400    | PASS   |
| JSON array instead of object           | 400      | 400    | PASS   |
| Plain-text request body                | 415      | 415    | PASS   |
| Malformed JSON                         | 400      | 400    | PASS   |
| Empty PATCH request                    | 400      | 400    | PASS   |
| Mixed valid and invalid PATCH fields   | 400      | 400    | PASS   |
| Numeric completion value               | 400      | 400    | PASS   |
| Attempt to change `created_at`         | 400      | 400    | PASS   |
| Nonexistent task ID                    | 404      | 404    | PASS   |
| Invalid status filter                  | 400      | 400    | PASS   |

**Result: 12 out of 12 validation cases passed.**

## 6. Atomic PATCH Verification

One important test was checking whether the backend protected an existing task from a partially invalid update.

I submitted the following PATCH request for task ID `3`:

```json
{
  "title": "This title should NOT be saved",
  "is_complete": "false"
}
```

The title was valid, but the completion value was invalid because `"false"` is a string instead of a boolean.

The backend returned HTTP `400 Bad Request` with this message:

```json
{
  "error": "is_complete must be a boolean."
}
```

I then retrieved task ID `3` again.

The task still contained its original title, `Complete Week 1 API verification`, and its original completion status, `false`.

This confirmed that the invalid request did not partially update the task.

## 7. Automated Testing Results

### Backend — pytest

I ran the backend automated tests twice during the October 26 review.

**First run:**

```text
5 passed in 0.73s
```

**Second run:**

```text
5 passed in 0.46s
```

Both runs passed.

### Frontend — React

I also completed the following checks:

| Command            | Result                         |
| ------------------ | ------------------------------ |
| `npm run lint`     | PASS                           |
| `npm run test:run` | 17 tests passed across 5 files |
| `npm run build`    | PASS                           |

The frontend build completed successfully using Vite.

These results confirmed that the automated checks passed at the time of verification.

## 8. Debugging Challenges and Corrections

One of my biggest challenges was resolving a Git merge conflict in my Flask application.

Although I initially thought the conflict was resolved, pytest showed that all five tests were failing.

After reviewing the errors, I discovered that important helper functions were missing:

- `find_task()`
- `read_json_object()`
- `validate_title()`

I restored the missing functions and corrected the Flask application.

Afterward, all five tests passed.

Another challenge involved organizing my Day 5 Python program into separate modules.

I tried to open `report_utils.py` before creating it. After reviewing the error, I created the file using `touch` and continued with the assignment.

Both experiences taught me to read error messages carefully, verify file locations, and test my changes instead of assuming they work.

## 9. Application Storage and Configuration

The Flask Task Manager uses in-memory storage.

Tasks can be created, updated, retrieved, and deleted while the backend is running. Changes are not permanently stored in a database.

The application is configured for local development with:

- Flask backend: `http://127.0.0.1:5001`
- React frontend: `http://127.0.0.1:5173`

The frontend and backend communicate through HTTP requests.

The application also includes configuration for cross-origin requests between the React frontend and Flask backend.

## Backend Module Refactoring — October 26, 2026

During my final Week 1 review, I identified that my Flask application still contained its task storage and validation helper functions inside `app.py`.

To meet the assignment's requirement for separate modules, I reorganized the backend into:

- `app.py` — Flask application setup and API routes.
- `storage.py` — Starting task data and task lookup.
- `validation.py` — JSON request and title validation.
- `config.py` — Application configuration.

I preserved the existing API routes, error messages, and in-memory storage behavior.

After refactoring, I checked the Python syntax of all three affected files. The command completed without errors.

I then ran the backend automated tests twice.

**First run:**
`5 passed in 0.42s`

**Second run:**
`5 passed in 0.44s`

Both test runs passed successfully.

This experience helped me understand how separating code into modules makes an application easier to organize and maintain. It also reinforced the importance of running automated tests after changing existing code.

## 10. Additional Verification Still Required

Before final submission, I will review the remaining requirements and document the results of any additional checks.

These include:

- Rechecking the refactored backend through the remaining manual application tests.
- Verifying the complete create, read, update, delete, and filter workflow in the browser.
- Confirming DELETE returns HTTP 204 with an empty response body.
- Checking that task IDs are not reused after deletion during the same server process.
- Demonstrating what happens when Flask restarts and in-memory task changes reset.
- Reviewing the final GitHub branches and daily pull requests.

These checks are listed as remaining work rather than completed results.

## 11. freeCodeCamp Progress

The required freeCodeCamp coursework has a separate November 20, 2026 deadline.

**Week 1 progress:** To be updated with my actual completed lessons or exercises before submission.

## 12. GitHub and Submission Information

**Submission repository:**  
https://github.com/pearla-mutombo/level4-task-manager-submission

**Working branch:** `day-05-verify-handoff`

**Daily progress notes:** `notes/day-01.md` through `notes/day-05.md`

**API validation matrix:** `exercises/day-03/request-cases.json`

**Daily pull request links:** To be confirmed during final GitHub review.

**Final commit SHA:** To be recorded after final verification and commits.

**Submission snapshot and ZIP archive:** To be prepared from the same final commit.

## 13. My Week 1 Reflection

This week helped me understand how Python, Flask, React, and HTTP requests work together.

I learned that frontend development and backend development have different responsibilities. React provides the interface, while Flask processes requests, validates information, and returns responses.

I also learned that testing is an important part of development.

The merge conflict was difficult, but it taught me how to use error messages and automated tests to identify missing functionality.

The API validation exercises helped me understand why the backend must protect data from invalid requests.

I am becoming more comfortable using Terminal, working with Git branches, reading errors, and organizing my code into smaller functions and modules.

My biggest takeaway is that learning programming requires patience, practice, and careful verification. I have made progress in understanding not only how to write code, but also how to investigate and correct problems when something does not work.

## 14. Final Submission Checklist

- [x] Complete five daily progress notes.
- [x] Record the 12 verified API validation cases.
- [x] Verify the atomic PATCH behavior.
- [x] Run backend pytest twice successfully.
- [x] Run frontend lint, automated tests, and build.
- [ ] Complete remaining manual application checks.
- [x] Separate Flask storage and validation modules and pass backend tests twice.
- [ ] Update freeCodeCamp progress.
- [ ] Confirm daily GitHub pull requests.
- [ ] Record final commit SHA.
- [ ] Prepare matching GitHub snapshot and ZIP archive.
- [ ] Submit the required materials to Moodle.

---

**Report prepared from the Week 1 project documentation and additional verification completed on October 26, 2026.**
