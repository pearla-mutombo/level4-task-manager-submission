# Day 3 Progress Notes — Wednesday, October 14, 2026

## Topic: Full CRUD Operations and API Validation

### What I Worked On

On Day 3, I continued developing my React and Flask Task Manager application by focusing on CRUD operations.

CRUD stands for Create, Read, Update, and Delete. These operations allow users to add tasks, view existing tasks, change task information, and remove tasks.

I worked with the Flask API endpoints responsible for managing tasks. I also practiced understanding how React sends requests to Flask and how the backend processes those requests.

Another important part of Day 3 was learning how to validate incoming information and return useful error messages when a request is invalid.

### What I Learned

I learned that each CRUD operation uses a different HTTP method:

- **POST** creates a new task.
- **GET** retrieves task information.
- **PATCH** updates an existing task.
- **DELETE** removes a task.

I also learned why the backend must generate task IDs and timestamps rather than allowing users to change those values.

One of the most important concepts I learned was the difference between a JSON string and a JSON boolean.

For example, `"false"` is a string because it contains quotation marks, while `false` is an actual JSON boolean.

I learned that validating the data before updating a task helps prevent accidental changes.

### Challenges I Experienced

One challenge was understanding how all four CRUD operations work together.

I also needed extra practice understanding how Flask handles invalid requests, especially when a request includes the wrong data type.

Another challenging concept was atomic validation. I needed to understand why a request containing both a valid field and an invalid field should not change any part of an existing task.

### How I Worked Through These Challenges

I reviewed each CRUD operation separately and studied the information sent in the request and returned in the response.

I practiced understanding how task IDs identify individual records and why IDs should not depend on the number of tasks currently stored.

For validation, I reviewed how Flask checks request data before updating a task.

I also practiced using Python functions, lists, and dictionaries to better understand how task information is organized.

### Files and Features Worked On

- `backend/app.py` — Flask CRUD endpoints and validation.
- `exercises/day-03/request-cases.json` — Manual API validation test matrix.
- `exercises/day-03/README.md` — Day 3 instructions and reflection.

The application supports creating, retrieving, updating, and deleting tasks, with validation for invalid requests.

### API Verification Results

On October 26, 2026, I performed additional manual API verification using `curl` in my Terminal.

I tested all 12 cases in `exercises/day-03/request-cases.json`.

| Test Case                            | Expected HTTP Status | Actual HTTP Status | Result |
| ------------------------------------ | -------------------- | ------------------ | ------ |
| Whitespace-only title                | 400                  | 400                | PASS   |
| Numeric title                        | 400                  | 400                | PASS   |
| Unsupported ID field during creation | 400                  | 400                | PASS   |
| JSON array instead of an object      | 400                  | 400                | PASS   |
| Plain text instead of JSON           | 415                  | 415                | PASS   |
| Malformed JSON                       | 400                  | 400                | PASS   |
| Empty PATCH request                  | 400                  | 400                | PASS   |
| Mixed valid and invalid PATCH fields | 400                  | 400                | PASS   |
| Numeric completion value             | 400                  | 400                | PASS   |
| Attempt to modify `created_at`       | 400                  | 400                | PASS   |
| Nonexistent task ID                  | 404                  | 404                | PASS   |
| Invalid status filter                | 400                  | 400                | PASS   |

**Result: All 12 manual validation cases returned their expected HTTP status codes.**

I also verified that creating a valid task returned HTTP `201 Created` and retrieving that task returned HTTP `200 OK`.

### Atomic PATCH Verification

One particularly important test involved task ID `3`.

Before the test, the task contained:

- Title: `Complete Week 1 API verification`
- Completion status: `false`

I submitted a PATCH request containing a valid replacement title and an invalid completion value:

```json
{
  "title": "This title should NOT be saved",
  "is_complete": "false"
}
```

Flask returned HTTP `400 Bad Request` with this error:

```json
{
  "error": "is_complete must be a boolean."
}
```

I then sent another GET request for task ID `3`.

The response confirmed that the original title and completion status were unchanged.

This demonstrated that the backend rejected the entire invalid update rather than saving only part of it.

### JSON File Verification

After recording the actual results in `request-cases.json`, I validated the file using:

```bash
python3 -m json.tool exercises/day-03/request-cases.json > /dev/null && echo "JSON validation passed"
```

The Terminal displayed:

```text
JSON validation passed
```

This confirmed that the updated testing file contained valid JSON syntax.

### My Reflection

Day 3 helped me better understand how a full CRUD application works and why backend validation is important.

I learned that it is not enough for an application to handle successful requests. It also needs to respond correctly when information is missing, incorrectly formatted, or not allowed.

The atomic PATCH test was especially helpful because I could see that Flask rejected invalid information without changing the original task.

Completing the additional verification gave me more confidence in understanding how my React frontend and Flask backend work together.

My biggest takeaway was that careful testing is just as important as writing the application code.
