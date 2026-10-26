# Day 5 Progress Notes — Friday, October 16, 2026

## Topic: Python Modules, Reading List Report, and Week 1 Verification

### What I Worked On

For Day 5, I created a Python Reading List Report program that reads book information from a JSON file, counts the books, and generates a text report showing the book titles.

This exercise helped me practice working with Python functions, importing functions from another Python file, reading and writing files, and handling errors.

I also continued preparing my React and Flask Task Manager for the Week 1 handoff by reviewing the application, checking its API behavior, and documenting the testing results.

### My Reading List Report Program

I organized the Reading List Report into two Python files.

The first file, `reading_report.py`, handles reading the JSON data, generating the report, displaying it in Terminal, and saving the results to a text file.

The second file, `report_utils.py`, contains helper functions that count the books and collect their titles.

The program reads from `sample-data/reading-list.json` and generates `exercises/day-05/reading-report.txt`.

The report contains two books:

1. Flask quickstart
2. Python virtual environments

The program successfully displayed the report and saved it to a text file without changing the original JSON data.

### What I Learned

Day 5 helped me understand how multiple Python files can work together.

I learned that using separate modules makes code easier to organize because each file can have a specific responsibility.

I also practiced using imports, functions, loops, JSON, and file handling.

Another important lesson was understanding how to check whether files exist before trying to open them.

### Challenges I Experienced

One challenge was understanding how to organize my Python program into separate files and import functions from another module.

I also encountered a problem when I tried to open `report_utils.py` in Visual Studio Code before creating the file.

The Terminal could not open the file because it did not exist yet.

### How I Resolved the Problem

I reviewed the file location and realized that I needed to create `report_utils.py` first.

I used the Terminal command `touch` to create the missing file.

After creating it, I opened it in Visual Studio Code and added the helper functions.

I then organized the program so that each file had a clear responsibility.

After completing the program, I ran it from Terminal and confirmed that it generated the Reading List Report.

### Files and Features Worked On

- `exercises/day-05/reading_report.py` — Main Reading List Report program.
- `exercises/day-05/report_utils.py` — Helper functions.
- `sample-data/reading-list.json` — Source book information.
- `exercises/day-05/reading-report.txt` — Generated report.
- `exercises/day-05/README.md` — Day 5 documentation and reflection.
- `exercises/day-03/request-cases.json` — Updated with verified API test results during the later handoff review.
- `notes/day-01.md` through `notes/day-05.md` — Daily progress documentation prepared for submission.

## Additional Week 1 Verification — October 26, 2026

As part of preparing my final Week 1 submission, I performed additional verification of my React and Flask Task Manager.

These checks were completed during the October 26 review, not during the original October 16 classroom exercise.

### Backend Automated Tests

I ran pytest twice to confirm that the backend tests passed consistently.

First run:

```text
5 passed in 0.73s
```

Second run:

```text
5 passed in 0.46s
```

Both runs passed.

### Frontend Verification

I also ran the frontend validation commands.

- `npm run lint` — Passed.
- `npm run test:run` — 17 tests passed across 5 test files.
- `npm run build` — Completed successfully using Vite.

These checks helped verify that the frontend code passed its automated checks and could be built successfully.

### Manual Flask API Verification

I used Terminal commands to send requests directly to my Flask backend.

The verified results included:

| Request or Test                        | Actual HTTP Status | Result |
| -------------------------------------- | ------------------ | ------ |
| GET `/api/health`                      | 200                | PASS   |
| POST a valid task                      | 201                | PASS   |
| GET the created task                   | 200                | PASS   |
| POST an invalid title                  | 400                | PASS   |
| POST an invalid title type             | 400                | PASS   |
| POST an unsupported field              | 400                | PASS   |
| POST an invalid JSON body type         | 400                | PASS   |
| POST with plain-text content type      | 415                | PASS   |
| POST malformed JSON                    | 400                | PASS   |
| PATCH with no update fields            | 400                | PASS   |
| PATCH with an invalid completion value | 400                | PASS   |
| PATCH with a protected timestamp field | 400                | PASS   |
| GET a nonexistent task                 | 404                | PASS   |
| GET with an invalid status filter      | 400                | PASS   |

### Atomic PATCH Verification

I also verified that an invalid PATCH request did not partially update a task.

I created task ID `3` with the title `Complete Week 1 API verification` and a completion status of `false`.

I then sent an update containing a valid replacement title and an invalid completion value.

Flask rejected the request with HTTP `400 Bad Request`.

Afterward, I retrieved task ID `3` again and confirmed that the original title and completion status had not changed.

This helped me understand why the backend must validate all requested changes before saving them.

### Documentation Verification

I updated `exercises/day-03/request-cases.json` with the actual HTTP results for all 12 validation cases.

I also used Python's JSON validation tool to confirm that the updated file contained valid JSON syntax.

The Terminal displayed:

```text
JSON validation passed
```

### Current Project Status

The React and Flask Task Manager has passed the automated checks and manual API validation cases listed above.

The application currently stores task information in memory, so task changes are not permanently saved when Flask restarts.

Before final submission, I still need to complete the Week 1 report, review the backend's required module structure, confirm the daily pull requests, and prepare the final GitHub submission information.

### My Final Reflection

Day 5 helped me understand the importance of organizing Python code into smaller files and functions.

The Reading List Report exercise gave me more practice working with JSON, imports, file handling, and error messages.

The additional Week 1 verification also helped me understand that finishing an application involves more than writing code. I need to test the application, document the results, and make sure the project is organized so someone else can review it.

One of my biggest lessons this week was learning to approach problems one step at a time.

When I take the time to read error messages, understand what caused a problem, and test my corrections, I become more confident in my programming skills.

I am proud of the progress I made during Week 1, especially in understanding Python, Flask, API requests, automated testing, and debugging.
