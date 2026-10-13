# Level 4 — React + Flask Task Manager

A continuous learning project for connecting a React frontend to a Python/Flask backend. During Week 1, you build the API and store tasks in memory. In Week 2, you continue this application with PostgreSQL, authentication, and backend deployment.

**Week 1: October 12–16, 2026 · 2 hours live + 3 hours independent each weekday · macOS instructions**

The React interface is supplied in full so you can focus on Python, HTTP, validation, and backend behavior. You build the Flask backend incrementally with your instructor.

## What you receive

```text
level4-task-manager/
├── README.md
├── frontend/       # Complete React/Vite interface and frontend tests
├── backend/        # Minimal Python starter; grows during the lessons
├── exercises/      # Daily instructions and unfinished practice files
├── postman/        # API request collection and local environment
├── sample-data/    # Inputs for the separate JSON-file exercise
└── notes/          # Your progress notes; create if absent after cloning
```

- **Frontend:** complete task forms, pages, styling, API calls, and lesson modes. You do not need to rewrite it during Week 1.
- **Backend:** `app.py` begins with construction comments. You add the first Flask application during Day 1, then extend it each day.
- **Exercises:** required student material. Complete the matching day's practice after class. Later-day folders are available in advance.
- **Instructor references and exercise answers:** kept in a separate teaching repository and released after practice. They are not part of this initial application handout.

Git branches record your progress. Creating a branch keeps the files from its starting commit; it does not hide solutions or reset your code. Frontend lesson modes control which UI features are available, while all frontend source remains supplied.

## Requirements

Use Python **3.13**, Node.js **24**, Git, a code editor, Postman, and a browser with developer tools. Check your installed versions:

```bash
python3.13 --version
node --version
npm --version
git --version
```

Python should report `3.13.x` and Node should report `v24.x.x`. Follow the instructor's preparation guide if either is missing. Use the pinned Python requirements and frontend lockfile included here.

## Get the project

If you already have this repository at `~/Desktop/level4-task-manager`, skip cloning and open that folder. Otherwise, after receiving access to the private GitHub repository:

```bash
cd "$HOME/Desktop"
git clone git@github.com:uliseslargaespada/level4-task-manager.git
cd level4-task-manager
mkdir -p notes
```

This clone command uses an SSH key registered with your GitHub account. If you use HTTPS authentication, copy the HTTPS URL from GitHub's **Code** menu instead. Repository access and GitHub authentication are both required.

Open the project root in your editor. Empty folders are not tracked by Git, so `notes/` may need to be created after cloning.

## First setup

Use two Terminal tabs: **A for Flask**, **B for React**. These setup commands install dependencies; they do not complete the backend.

### Terminal A — backend environment

```bash
cd "$HOME/Desktop/level4-task-manager/backend"
python3.13 -m venv .venv
source .venv/bin/activate
python --version
python -m pip install -r requirements-dev.txt
```

Create `.venv` once. It isolates this project's Python packages. Activate it in each new backend terminal; `python --version` should still report Python 3.13. Installation should finish without errors. `requirements-dev.txt` includes Flask, Flask-CORS, python-dotenv, and pytest for the later testing lesson.

### Terminal B — frontend dependencies

```bash
cd "$HOME/Desktop/level4-task-manager/frontend"
npm ci
if [ ! -f .env.local ]; then
  cp .env.example .env.local
fi
```

`npm ci` installs the versions in `package-lock.json`. The example configuration uses:

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:5001/api
```

The conditional preserves an existing `.env.local`. Vite reads configuration when it starts, so restart it after changing this file. Browser configuration is public; keep private credentials out of `VITE_` variables.

## Build Day 1 before starting Flask

Follow the instructor's Day 1 live build to add the Flask application and `GET /api/health` to `backend/app.py`.

If Flask reports **“Failed to find Flask application or factory in module 'app'”** while `app.py` contains only starter comments, the first application has not been built yet. Complete that lesson step before running the server. A branch change or dependency reinstall will not create the application.

Completed instructor examples are used for rehearsal in the separate teaching repository. Keep your own implementation in this project.

## Run the application

### Terminal A — Flask, after the Day 1 build

```bash
cd "$HOME/Desktop/level4-task-manager/backend"
source .venv/bin/activate
python -m flask --app app run --debug --host 127.0.0.1 --port 5001
```

Success: Flask reports `Running on http://127.0.0.1:5001`. Keep this terminal running. Open [the health endpoint](http://127.0.0.1:5001/api/health) or send a Postman GET request. The default response is status **200** with:

```json
{"status": "ok", "message": "Hello from Flask"}
```

### Terminal B — matching frontend lesson mode

```bash
cd "$HOME/Desktop/level4-task-manager/frontend"
npm run dev:day-01
```

Open **http://127.0.0.1:5173**. The home page should display the real Flask greeting.

| Day | Frontend command | Backend milestone |
|---|---|---|
| Mon, Oct 12 | `npm run dev:day-01` | First JSON route and React connection |
| Tue, Oct 13 | `npm run dev:day-02` | List, details, create, and status query filtering |
| Wed, Oct 14 | `npm run dev:day-03` | Update, completion changes, delete, and validation |
| Thu, Oct 15 | `npm run dev:day-04` | Modules, configuration, application factory, and tests |
| Fri, Oct 16 | `npm run dev:day-05` | Reliability checks and final demonstration |

Later-day controls are unavailable with explanations until their lesson mode enables them. Stop Vite with **Control+C** before selecting another mode. `npm run dev` starts the full Day 5 interface, so use the explicit daily command during lessons.

Use **127.0.0.1** consistently for both applications. `localhost` is a different browser origin. The frontend keeps port 5173 fixed; stop an existing Vite process before starting another. Flask uses port 5001.

**Stopping and restarting:** press **Control+C** in the relevant terminal to stop its server. Run its startup command again to restart it. `deactivate` exits the Python environment after stopping Flask. Dependency installation does not need to be repeated each day unless dependencies change or the environment is removed.

## How requests and storage work

```text
React page → Axios API client → Flask route → Python memory → JSON response → React update
```

React and Flask are separate processes. React sends requests to `http://127.0.0.1:5001/api`; Flask validates them and owns the task data. Tasks use `id`, `title`, `is_complete`, and `created_at`.

| Endpoint | Introduced | Purpose |
|---|---|---|
| `GET /api/health` | Day 1 | Backend status and greeting |
| `GET /api/tasks` | Day 2 | Tasks, newest first; optional `status=all`, `active`, or `completed` |
| `GET /api/tasks/<task_id>` | Day 2 | One task by integer ID |
| `POST /api/tasks` | Day 2 | Create an incomplete task from its title |
| `PATCH /api/tasks/<task_id>` | Day 3 | Change title and/or completion |
| `DELETE /api/tasks/<task_id>` | Day 3 | Delete a task; return 204 with no body |

Titles are trimmed strings of 1–80 characters. Completion values must be JSON booleans. The backend assigns IDs and timestamps. Invalid input returns 400, missing records return 404, and unsupported request content types return 415. Follow the instructor's API contract as you implement these rules.

Browser refreshes preserve the running backend's memory. Restarting Flask, including a debug reload after saving Python code, resets that memory. PostgreSQL persistence comes in Week 2. JSON-file exercises use separate files and do not save this application's tasks.

## Daily practice and Git workflow

Start with [the exercises overview](exercises/README.md), then open the current day:

- [Day 1: Python values and another JSON route](exercises/day-01/README.md)
- [Day 2: Functions and request inputs](exercises/day-02/README.md)
- [Day 3: CRUD and validation](exercises/day-03/README.md)
- [Day 4: JSON files and tests](exercises/day-04/README.md)
- [Day 5: Verification and handoff](exercises/day-05/README.md)

Use one branch and one PR per teaching day. Begin the next day's branch after the previous PR has been reviewed and merged into `main`. If a branch already exists, switch to it rather than trying to create it again.

For Day 1, from the project root, when the instructor tells you to begin:

```bash
cd "$HOME/Desktop/level4-task-manager"
git status --short
git switch -c day-01-python-flask
```

If you already created this branch, use `git switch day-01-python-flask`. The initial `main` contains the supplied starter; each accepted daily PR adds your implementation.

Record progress in `notes/day-01.md` (and the corresponding file on later days): what works, what is blocked, what you tried, and what you can explain. Include verification evidence in the daily PR.

Before committing, confirm your Git identity and review the actual changes:

```bash
git config user.name
git config user.email
git status --short
git diff
```

Your name and email should match the identity you intend to use. Ask your instructor if they are missing or incorrect. Once the day's work is ready:

```bash
git add backend exercises notes
git diff --cached
git commit -m "feat: add Flask health route"
git push -u origin day-01-python-flask
```

Use a commit message that describes your actual change. Open a pull request on GitHub from the day's branch into `main`. Include working behavior, request/test results, and remaining blockers. Keep `.venv`, `node_modules`, private environment files, generated output, and caches out of commits; the supplied ignore files exclude them.

## Verify your work

Import the collection and local environment using [the Postman instructions](postman/README.md). Select **Level 4 Week 1 Local** and confirm `base_url` is `http://127.0.0.1:5001/api`. Run only the matching day's requests: later endpoints do not exist on Day 1. Requests expecting invalid-input errors pass when they receive the documented error status.

Frontend checks, from `frontend/`:

```bash
npm run lint
npm run test:run
npm run build
```

These check source quality, supplied frontend behavior, and production packaging. They do not prove that your Flask API works.

After adding backend tests in Day 4, from `backend/` with `.venv` active:

```bash
python -m pytest -q
```

Backend tests use Flask's test client and do not require a running server. Also check real requests through Postman and the browser. By Friday, demonstrate complete CRUD, rejected input without unintended changes, loading/error/empty states, direct React route refreshes, and the difference between browser refresh and backend restart.

## When you are blocked

Read the last useful application line in the Flask traceback and inspect the browser Network panel. Record the request URL, expected result, actual status/body, and what you tried before asking for help.

| Symptom | First check |
|---|---|
| Flask cannot find the application | Has Day 1 added the application object to `backend/app.py`? Are you running from `backend/`? |
| Browser reports a request error | Is Flask running on port 5001? Does the health endpoint work directly? |
| Postman works but React cannot read the response | Check CORS allows exactly `http://127.0.0.1:5173`. |
| Frontend will not start on port 5173 | Stop the previous Vite process. |
| Task actions fail in an early lesson | Use the correct frontend mode and requests for the backend routes built so far. |
| A previously captured Postman ID stops working | Restart the day's request workflow from creation after restarting Flask. |

Additional setup details are in [the backend README](backend/README.md) and [the frontend README](frontend/README.md). The supplied frontend retains its [original MIT license](frontend/LICENSE).
