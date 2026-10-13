# Thursday Practice — Files, Modules, and Tests

**180 minutes.** The application continues to use memory. File persistence below belongs only to the practice script.

## 0–45 minutes: JSON-file exercise

Complete `json_practice.py`. Its paths are already resolved relative to the script, so running it from another folder does not change which sample file it uses.

1. Read `sample-data/reading-list.json` using UTF-8.
2. Parse JSON into Python values and print the first entry's title.
3. Append one reading-list dictionary and write the new list to `output/reading-list.json` inside this exercise folder.
4. Catch `FileNotFoundError` when reading a deliberately missing file.
5. Catch `json.JSONDecodeError` when reading `sample-data/malformed.json`.
6. Explain `with`, `Path`, JSON serialization, and the difference between a Python list and its on-disk JSON text.

```bash
cd "$HOME/Desktop/level4-task-manager"
backend/.venv/bin/python exercises/day-04/json_practice.py
```

Keep the source sample unchanged. Generated output is ignored by Git. Do not connect the task-manager store to these files.

## 45–120 minutes: meaningful API tests

Write tests for a successful creation, invalid title, missing record, invalid completion, and a rejected mixed-field update. Create a fresh application/store through the fixture before each test.

```bash
cd "$HOME/Desktop/level4-task-manager/backend"
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m pytest -q
```

Both runs should pass; the second run checks that tests do not depend on data left by the first. Explain why Flask's test client sends requests without requiring the live Flask server.

## 120–150 minutes: configuration and refactoring

Repeat Wednesday's CRUD sequence against your reorganized backend. Compare responses with the contract. Change `FRONTEND_ORIGIN` deliberately, restart Flask, observe the browser failure, then restore `http://127.0.0.1:5173` and restart again. Postman can still reach an API when the browser blocks cross-origin access.

## 150–180 minutes: PR

Submit modules, tests, example configuration, and your completed exercise script. Include two passing pytest runs, one JSON error demonstration, and a statement that task data still resets on restart.

**Optional:** Add another meaningful test for a failure that you encountered personally, with a short explanation of what it protects.
