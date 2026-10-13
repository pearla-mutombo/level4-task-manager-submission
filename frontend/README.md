# Prepared Week 1 React frontend

This is the interface supplied to the student. Its components, task forms, dark/green palette, React Router pages, and SCSS/BEM structure come from the Level 3 task manager. Its data service now sends requests to Flask. The original MIT license is preserved in `LICENSE`.

The student builds the Flask API; they do not need to rewrite this frontend during Week 1. The application has no login or direct database access this week. Data lives in the running Flask process.

## First installation on macOS

Use a new Terminal window for the frontend. After copying this folder into the student's application repository as `frontend`, run:

```bash
cd ~/Desktop/level4-task-manager/frontend
node --version
npm --version
npm ci
```

The documented baseline is Node.js 24. `node --version` should show `v24.x.x`. `npm ci` installs the exact dependency versions in `package-lock.json`; it requires internet access the first time. It does not start the app. If Node is missing, follow the instructor preparation guide before continuing.

The default API URL is `http://127.0.0.1:5001/api`. No configuration file is required for that default. To override it:

```bash
cp .env.example .env.local
```

Edit `VITE_API_BASE_URL` in `.env.local`, save, then stop and restart Vite. All `VITE_` values are visible in the browser. Do not put passwords or secret keys in this file.

## Start the matching lesson mode

Keep Flask running in a separate Terminal window. From the frontend directory, choose **one** command:

```bash
npm run dev:day-01
```

Open exactly `http://127.0.0.1:5173`. The first mode shows `Hello from Flask` from `GET /api/health`. Its task navigation is disabled because Day 1 has no task routes yet.

| Teaching day | Command | Available interface |
|---|---|---|
| Monday | `npm run dev:day-01` | Home and backend connection |
| Tuesday | `npm run dev:day-02` | Home, list, client-side status filters, details, creation |
| Wednesday | `npm run dev:day-03` | Complete CRUD, completion checkbox, edit page |
| Thursday | `npm run dev:day-04` | Complete CRUD against the modular backend |
| Friday | `npm run dev:day-05` | Complete CRUD and final verification |

`npm run dev` also starts the complete Day 5 interface. Stop Vite with **Control-C** in its Terminal. Run the next day's command to change modes. The mode files only change which controls are available; all frontend implementation is already supplied.

Vite uses the fixed host and port `127.0.0.1:5173`. If the port is occupied, it exits instead of silently changing the port. Stop the previous frontend terminal before starting another. Do not open `localhost:5173`: that is a different browser origin from the one allowed by the reference Flask API.

## Read the request path

```text
React page → taskService.js → Axios apiClient.js → Flask route → JSON response
```

- `src/lib/apiClient.js`: API address, timeout, and readable request errors.
- `src/lib/taskService.js`: the six HTTP operations and their request bodies.
- `src/hooks/useTasks.js`: list loading, mutation results, and local synchronization.
- `src/hooks/useTask.js`: detail reads, cancellation, and retry behavior.
- `src/components/tasks/`: prepared create/edit forms and row controls.
- `src/pages/`: home, list, detail, edit, and missing-page views.
- `src/styles/`: familiar shared tokens and responsive SCSS/BEM styles.

The list keeps its All / Active / Completed filters in React. The Flask `status` query is practiced separately in Postman. Mutation results replace local records only after the API succeeds. A failed request leaves existing task data and form text available to retry. Loading requests are aborted when the page or task ID changes.

## Useful checks

Run these from the frontend directory when Vite is stopped or in another terminal:

```bash
npm run lint
npm run test:run
npm run build
```

- Lint checks JavaScript, SCSS, and HTML.
- Tests verify visible task workflows, error recovery, request cancellation, API calls, and lesson gates using controlled service responses. They do not require Flask to be running.
- Build writes production files to `dist/`; it is a packaging check, not evidence that the API is available.

To serve that build locally:

```bash
npm run preview
```

Open `http://127.0.0.1:5173`; Flask must still be running on port 5001. Stop preview with **Control-C**. The production build uses the complete Day 5 mode. Vite development and preview servers return the React entry page for nested routes; refresh `/tasks/1` to verify direct navigation when task 1 exists. Real hosting configuration is introduced in later weeks.

## Demonstrations

1. **Request loading:** Use browser developer tools → Network → a slow network profile, then reload `/tasks`.
2. **Backend offline:** Stop Flask with Control-C, refresh the page, observe its error, restart Flask, then press Retry.
3. **CORS failure:** Run the backend with a deliberately incorrect allowed origin using the guide's temporary configuration. Postman may still work; the browser blocks reading the response. Restore the exact origin afterward.
4. **Empty:** Delete all tasks in Day 3 or later. “No tasks yet” prompts creation.
5. **Filtered empty:** Leave active tasks, select Completed, and observe “No completed tasks.”
6. **Persistence distinction:** Refreshing React preserves tasks. Restarting Flask, or editing Python with the debug reloader enabled, resets the in-memory data.

If a request fails, inspect browser Network details and the Flask terminal. Check the request URL, body, response status, and allowed origin. See the package's troubleshooting guide for recovery steps.
