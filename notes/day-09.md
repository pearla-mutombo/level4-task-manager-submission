# Day 09 — Supabase Authentication and User Ownership

## Objective

The goal for Day 09 was to add user authentication to my Task Manager application using Supabase. I also needed to make sure each signed-in user could only view and manage their own tasks and categories.

## What I Completed

### 1. Supabase Authentication

I connected my React frontend and Flask backend to Supabase Authentication and added registration, login, logout, and session management. Users can sign in with their email and password to access their tasks.

### 2. Protected React Routes

I created a `ProtectedRoute` component to prevent users who are not signed in from opening protected task pages. I also added an authentication context and a custom `useAuth` hook to share authentication information throughout the React application.

### 3. Backend Authentication and Authorization

I updated Flask to verify the Supabase access token sent with protected API requests.

I learned that protecting a page in React is not enough by itself. The backend must also verify the user's identity and check which records they are allowed to access before returning or changing private information.

### 4. User Ownership of Tasks and Categories

I added a `user_id` field to tasks and categories and updated the backend queries to restrict access to records owned by the signed-in user.

This means users should not be able to view, edit, or delete another user's tasks through the application.

### 5. PostgreSQL Database Migration

I created an Alembic migration to add user ownership to the existing database tables.

Before applying the migration to my local PostgreSQL database, I backed up my existing records. I then assigned my two original tasks and category to my primary Supabase account so I could preserve the work I had completed during earlier assignments.

I also updated `.gitignore` to prevent my local database backup from being accidentally uploaded to GitHub.

### 6. Authentication and Ownership Testing

I tested the application using three separate Supabase accounts.

My primary account could access its existing tasks and category, while the other two accounts could sign in but could not view those tasks.

I also tested navigating directly to a task belonging to my primary account while signed in with the other accounts. The application displayed a message indicating that the task was unavailable or could not be found.

This helped me verify that the application was restricting access based on user ownership.

While signed in with my primary account, I also tested creating, editing, completing, and deleting a task.

I ran the backend automated tests:

```bash
python -m pytest -q
```

Result:

```text
25 passed in 3.39s
```

I also ran the frontend automated tests using Vitest.

Result:

```text
18 tests passed
```

During Day 09 development, I also ran the frontend linting and production build commands successfully.

### 7. Environment Configuration

I updated `backend/.env.example` and `frontend/.env.example` to document the PostgreSQL, Flask API, and Supabase configuration variables.

The example files use placeholders instead of real credentials, and my actual local environment files remain separate from the files intended for GitHub.

## Files Updated

- `backend/app.py` — Added authentication checks and user-specific API access.
- `backend/auth.py` — Added Supabase access-token verification.
- `backend/config.py` — Updated backend configuration for Supabase.
- `backend/models.py` — Added user ownership fields and relationships.
- `backend/requirements.txt` — Updated backend dependencies.
- `backend/tests/test_tasks.py` — Expanded backend automated tests.
- `backend/migrations/versions/29dcc638dbc8_add_user_ownership_to_tasks_and_.py` — Added the database migration for user ownership.
- `backend/.env.example` — Documented backend environment configuration.
- `frontend/.env.example` — Documented frontend environment configuration.
- `frontend/src/components/ProtectedRoute.jsx` — Added protected routing.
- `frontend/src/context/AuthContext.jsx` and `frontend/src/context/authContext.js` — Added authentication context.
- `frontend/src/hooks/useAuth.js` — Added a custom authentication hook.
- `frontend/src/lib/supabaseClient.js` — Configured the Supabase client.
- `frontend/src/lib/apiClient.js` — Added authentication tokens to API requests.
- `frontend/src/pages/LoginPage.jsx` — Added the login page.
- `frontend/src/pages/RegisterPage.jsx` — Added the registration page.
- `frontend/src/App.jsx` — Updated application routes for authentication.
- `frontend/src/App.test.jsx` — Updated frontend tests.
- `frontend/src/layouts/AppLayout.jsx` — Updated the application layout.
- `frontend/src/main.jsx` — Updated application setup.
- `frontend/package.json` and `frontend/package-lock.json` — Updated frontend dependencies.
- `.gitignore` — Excluded local database backup files from Git.

## Challenges and What I Learned

### Supabase Email Confirmation

One of the challenges I encountered was understanding why newly created Supabase accounts could not always sign in immediately.

At first, I did not realize that creating an account and confirming its email address were two separate steps.

While testing my application, I discovered that Supabase's email confirmation process could prevent a newly created account from signing in until the email address was confirmed.

To resolve this issue during development, I recreated my three test accounts through the Supabase dashboard using the **Auto Confirm User** option.

After the accounts were confirmed, I was able to sign in with each account and continue testing authentication and user ownership.

This experience helped me understand how email confirmation works in Supabase and why authentication settings are important.

I also learned that automatically confirming accounts through the dashboard can be useful for controlled development testing, but a production application should use an appropriate email verification process to protect real users.

### CORS and Authentication Requests

Another challenge was a CORS issue caused by the backend authentication check blocking the browser's preflight `OPTIONS` request.

I learned that the preflight request needs to be handled correctly before the browser can send the protected API request.

After adjusting the Flask authentication handling, the frontend and backend were able to communicate correctly.

### Applying the Database Migration

After adding `user_id` to my SQLAlchemy models, I encountered another issue because my local PostgreSQL database still needed the Alembic migration.

I learned that changing Python models does not automatically update existing database tables.

After applying the migration, I was able to verify that my original records were preserved and associated with my primary account.

### Authentication Versus Authorization

Another important lesson was understanding the difference between authentication and authorization.

Authentication confirms who a user is, while authorization determines which records that user is allowed to access.

I learned that both are necessary because signing in successfully should not automatically give a user permission to access another person's private information.

### Protecting Existing Data

Before making changes to my local database, I created a backup of my original tasks and category.

I also made sure the backup would not be committed to GitHub.

This taught me the importance of protecting existing data before applying database migrations and keeping local backup files separate from the source code.

## Reflection

Day 09 helped me understand that creating a login page is only one part of securing a full-stack application.

I also needed to manage user sessions, verify access tokens in Flask, connect database records to their owners, and test the application using different accounts.

The Supabase email confirmation issue, CORS error, and database migration challenges taught me to troubleshoot each part of the application carefully instead of assuming the problem was only in the frontend.

I also learned the importance of protecting existing records and making sure users can only access information that belongs to them.

Completing this assignment gave me more confidence working with Supabase Authentication, React Context, Flask, PostgreSQL, database migrations, and automated testing.

## Next Steps

On Day 10, I will prepare my Task Manager application for deployment, review the production environment settings, and test that the frontend and backend work together after deployment.
