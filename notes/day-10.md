# Day 10 — Render Deployment and Production Verification

## Objective

The goal for Day 10 was to deploy my Flask backend to Render, connect it to my hosted Supabase PostgreSQL database, and verify that my React frontend could communicate with the deployed backend.

I also needed to confirm that authentication, task management, and user ownership continued to work after deployment.

## What I Completed

### 1. Preparing Flask for Deployment

I updated my Flask backend to support deployment on Render.

I added Gunicorn version 26.2.0 to `backend/requirements.txt` so Render could run my application using a production WSGI server.

I configured Render to start the application with Gunicorn using one worker.

### 2. PostgreSQL Connection Pooling

I updated `backend/app.py` to configure SQLAlchemy database connection pooling.

I used a pool size of two connections, disabled additional overflow connections, enabled connection health checks, and configured connection recycling after 300 seconds.

These settings helped me understand how to manage database connections more carefully when using a hosted application and database.

### 3. Deploying the Backend to Render

I created a Render web service for my Flask backend and connected it to my GitHub submission repository.

I configured the backend root directory, dependency installation command, Gunicorn start command, and environment variables.

After resolving an initial deployment error, Render successfully started my Flask application.

My deployed backend is available at:

https://level4-task-manager-api.onrender.com

I verified the health endpoint:

https://level4-task-manager-api.onrender.com/api/health

The endpoint returned a successful response with the message "Hello from Flask" and a status of "ok."

### 4. Connecting to Hosted Supabase PostgreSQL

I configured my deployed backend to use the hosted PostgreSQL database in Supabase.

During deployment, I encountered an error because SQLAlchemy could not parse the database connection URL.

I reviewed the Supabase connection settings and corrected the database URL using the Session Pooler connection information.

After updating the environment variable and redeploying the service, the application started successfully.

I also verified that the hosted database contained the tasks and categories tables and the Alembic migration version table.

### 5. Connecting React to the Deployed Backend

I updated my local React environment configuration to use the Render backend instead of my local Flask server.

At first, I discovered that Vite was still using an environment variable from `.env.day-05.local`.

After correcting that file and restarting Vite, my React application successfully communicated with the deployed backend over HTTPS.

The application displayed the successful backend health response.

### 6. Testing Task Management

I signed in to my React application and tested creating, viewing, completing, and deleting tasks.

I refreshed Safari to confirm that created tasks and completion changes remained saved.

I also verified that deleted tasks did not return after refreshing the page.

These tests helped me confirm that the frontend and deployed backend were communicating correctly and that task changes persisted across page refreshes.

### 7. Testing Authentication and User Ownership

I tested account isolation using two separate Supabase accounts.

I created a task while signed in with my primary account.

I then logged out and signed in with my second test account. The task created by my primary account was not visible.

I also attempted to open the original task directly using its URL while signed in with the second account.

The application displayed "Task unavailable" and "Task not found."

After signing back in with my primary account, I confirmed that the original task was still available.

This helped me verify that the deployed application was enforcing task ownership during the scenarios I tested.

### 8. Automated Tests and Code Quality

After deployment, I ran my backend automated tests using pytest.

Result:

```text
25 passed in 3.58s
```

I also ran my React frontend automated tests using Vitest.

Result:

```text
5 test files passed
18 tests passed
```

I ran the frontend linting checks using ESLint, Stylelint, and HTMLHint. All checks passed.

I also ran the React production build using Vite.

Result:

```text
162 modules transformed
Built successfully in 3.59s
```

Vite displayed a warning about a JavaScript chunk exceeding 500 kB. However, the build completed successfully.

### 9. Environment Variable and Git Verification

I verified that my local React environment files were excluded by `.gitignore` and were not tracked by Git.

I also confirmed that my Day 10 deployment branch was synchronized with its remote tracking branch and that my working directory was clean before creating this documentation.

I learned that environment variables allow applications to use different settings locally and in deployment without placing credentials directly into the source code.

## Files Updated

- `backend/app.py` — Added SQLAlchemy connection pooling settings for deployment.
- `backend/requirements.txt` — Added Gunicorn as a backend dependency.
- `notes/day-10.md` — Documented deployment configuration, troubleshooting, testing, and reflection.

I also updated local React environment configuration files to point to the deployed backend. These files are intentionally excluded from Git.

## Challenges and What I Learned

### Database Connection URL

My first Render deployment failed because SQLAlchemy could not parse the database URL.

I learned that database connection strings must use the correct format and contain the appropriate host, port, username, password, and connection parameters.

Using the Supabase Session Pooler configuration helped me correct the connection settings.

### Understanding Vite Environment Variables

Another challenge was understanding why React continued connecting to my local Flask server even after I updated an environment file.

I discovered that my application was running in `day-05` mode and that `.env.day-05.local` contained a different API URL.

After updating the correct file and restarting Vite, React connected to Render successfully.

This taught me that environment variable files can behave differently depending on the mode used to start a Vite application.

### Deployment Versus Local Development

I learned that running an application locally and deploying it to a hosting service involve different configurations.

Locally, I can start Flask directly for development. On Render, I needed a production server, environment variables, and a hosted database connection.

I also learned why database connection pooling matters when application and database resources are limited.

### Testing After Deployment

One important lesson was that a successful deployment message does not automatically prove every application feature works.

I needed to test authentication, task creation, updates, deletion, persistence, and account isolation through the deployed backend.

I also learned the importance of rerunning automated tests, lint checks, and the production build after making deployment changes.

### Render Free-Tier Considerations

I learned that Render's free hosting tier has resource limitations and may put an inactive service to sleep.

This means the first request after a period of inactivity may take longer than usual.

A separate sleep-and-wake verification and persistence check after a redeployment remain useful final checks.

## Reflection

Day 10 helped me understand how the different parts of my full-stack application work together outside my local development environment.

I gained experience configuring Render, using Gunicorn, connecting to hosted PostgreSQL, managing environment variables, and troubleshooting deployment errors.

One of the most important things I learned was that deployment is more than getting an application online. I also needed to verify that users could sign in, manage their tasks, and access only their own records.

The database connection error and Vite environment variable issue were challenging, but resolving them helped me become more comfortable investigating problems step by step.

Completing 25 backend tests, 18 frontend tests, all frontend lint checks, and a successful production build gave me more confidence in the application.

Overall, Day 10 helped me better understand the responsibilities involved in deploying, testing, and maintaining a full-stack React, Flask, and PostgreSQL application.

## Next Steps

Before final submission, I will finish any remaining deployment checks, including verifying persistence after a Render redeployment and checking free-tier sleep-and-wake behavior.

I will then finalize my documentation, commit my Day 10 changes, and prepare my Week 2 submission.
