# Day 07 — PostgreSQL Models and Migrations

## Project Description

For Day 07 of my Level 4 Task Manager project, I focused on connecting my Flask backend to PostgreSQL so that tasks could be saved permanently instead of being stored only in memory.

During this assignment, I learned how to use Flask-SQLAlchemy to create a Python model representing a database table. I also worked with Flask-Migrate and Alembic to create and apply database migrations.

I created separate development and testing databases so that I could run automated tests without affecting the tasks saved in my development environment.

This assignment helped me understand how Flask communicates with PostgreSQL and why database models, migrations, and testing are important when building a full-stack application.

## Files Used

- `backend/app.py` — Updated Flask API endpoints to create and retrieve tasks using PostgreSQL.
- `backend/models.py` — SQLAlchemy model defining the Task Manager's database table.
- `backend/config.py` — Configuration functions for development and testing database connections.
- `backend/requirements.txt` — Python dependencies for PostgreSQL, SQLAlchemy, and Flask-Migrate.
- `backend/migrations/` — Alembic migration configuration and migration history.
- `backend/tests/test_tasks.py` — Automated tests updated for PostgreSQL.
- `notes/day-07.md` — Documentation of my Day 07 work, testing results, challenges, and reflection.

### Database and Tools

- **PostgreSQL 18:** Used to store task records permanently.
- **Flask:** Python framework used to build the backend API.
- **Flask-SQLAlchemy:** Used to connect Python models to PostgreSQL.
- **Flask-Migrate and Alembic:** Used to manage changes to the database structure.
- **psycopg:** PostgreSQL database driver used by the Flask application.
- **pytest:** Used to test the Flask API.
- **Visual Studio Code:** Used to edit and test my project files.
- **Git:** Used to track changes on the `day-07-models-migrations` branch.

### PostgreSQL Databases

I created two separate databases:

- `level4_task_manager_dev` — Used for development and manually created tasks.
- `level4_task_manager_test` — Used for automated testing.

I kept my Day 06 database, `level4_sql_sandbox`, separate from both databases.

I also configured my database connections using environment variables and confirmed that Git ignores my private `.env` file and Python virtual environment.

## How to Run the Application and Migrations

I worked from the `backend` folder with my Python virtual environment activated.

I installed the required dependencies and updated `requirements.txt` to include:

- Flask-SQLAlchemy 3.1.1
- Flask-Migrate 4.1.0
- psycopg 3.3.6

I initialized Flask-Migrate and generated my first migration using:

```bash
python -m flask --app app db init
python -m flask --app app db migrate -m "Create tasks table"
```

I applied the migration to my development database using:

```bash
python -m flask --app app db upgrade
```

I also applied the same migration to my separate testing database.

The migration created the `tasks` table, and Alembic created the `alembic_version` table to track the migration history.

**Important:** The development and testing databases use separate connection addresses. I should always verify the selected database before running migrations or tests.

## PostgreSQL Model and API Changes

I created a `Task` model in `backend/models.py`.

The model contains the following fields:

| Field         | Purpose                                       |
| ------------- | --------------------------------------------- |
| `id`          | Unique identifier for each task               |
| `title`       | Required task title, limited to 80 characters |
| `is_complete` | Boolean showing whether a task is completed   |
| `created_at`  | Date and time when the task was created       |

I updated the Flask API so that the following endpoints use PostgreSQL:

- `GET /api/tasks` — Retrieves tasks and supports completion-status filtering.
- `GET /api/tasks/<id>` — Retrieves an individual task.
- `POST /api/tasks` — Creates and saves a new task.

I kept the existing title validation so that invalid task titles would still be rejected.

For Day 07, I temporarily disabled the PATCH and DELETE endpoints. I will implement PostgreSQL-backed editing and deletion during Day 08.

## Persistence Verification

One of the most important parts of Day 07 was verifying that PostgreSQL actually saved my task.

I created a task through the Flask API with the following information:

- **Task ID:** 1
- **Title:** Practice PostgreSQL persistence
- **Completion status:** False

Flask returned HTTP `201 Created`, confirming that the request succeeded.

I then started a separate Python process and retrieved the task through `GET /api/tasks`.

The API returned HTTP `200 OK` and displayed the same saved task.

To verify the record independently of Flask, I also queried the PostgreSQL `tasks` table directly using `psql`.

The database returned the saved record with ID `1` and the correct title and completion status.

This confirmed that my task was stored in PostgreSQL rather than only in Python memory.

## Automated Testing Results

I updated my pytest tests to work with the separate PostgreSQL testing database.

I also changed the task creation test so that it no longer expected a specific ID. PostgreSQL assigns task IDs automatically, so the test now verifies that the returned ID is a positive integer.

I tested the following behaviors:

| Test                             | Expected Result       | Verified Result |
| -------------------------------- | --------------------- | --------------- |
| Create and retrieve a task       | HTTP 201 and HTTP 200 | PASS            |
| Reject a blank task title        | HTTP 400              | PASS            |
| Retrieve a nonexistent task      | HTTP 404              | PASS            |
| Temporarily reject task editing  | HTTP 405              | PASS            |
| Temporarily reject task deletion | HTTP 405              | PASS            |

I ran the automated tests using:

```bash
python -m pytest -q
```

My final Terminal result was:

```text
5 passed in 2.03s
```

After running pytest, I checked my development database again and confirmed that the task I had created earlier was still there.

This helped verify that my automated tests were using the separate testing database rather than deleting records from my development database.

## Concepts Practiced

During Day 07, I practiced several important backend and database concepts.

- **Database persistence:** Understanding how PostgreSQL keeps records after a Python process ends.
- **SQLAlchemy models:** Defining database tables using Python classes.
- **Primary keys:** Allowing PostgreSQL to assign unique task IDs.
- **Database sessions:** Using `db.session.add()` and `db.session.commit()` to save records.
- **Database migrations:** Recording and applying changes to the database structure.
- **Alembic migration history:** Tracking which migrations have been applied.
- **Environment variables:** Keeping database connection information outside my source code.
- **Test isolation:** Using a separate database for automated tests.
- **API validation:** Rejecting invalid task titles before saving records.
- **HTTP status codes:** Understanding responses such as 200, 201, 400, 404, and 405.

## What I Learned

During Day 07, I learned how Flask can communicate with PostgreSQL through SQLAlchemy.

Before this assignment, my Task Manager stored tasks in a Python list. That allowed me to practice API operations, but the information was lost when the application restarted.

Using PostgreSQL helped me understand the difference between temporary storage and permanent database storage.

I also learned why migrations are important. Instead of manually recreating database tables every time the application changes, Flask-Migrate and Alembic allow me to keep track of the database structure.

Another important lesson was understanding why development and testing databases should be separate. I was able to run my automated tests and then confirm that my original development task had not been deleted.

## Challenges and How I Resolved Them

During Day 07, I experienced several challenges while connecting Flask to PostgreSQL.

**1. Duplicate Flask routes**

When I first updated my task creation endpoint, I accidentally left the original `create_task()` function in `app.py`.

Flask displayed an error because two functions were registered with the same endpoint name.

I reviewed the file, identified the duplicate, and corrected the application so that the task creation route used PostgreSQL.

**2. Python indentation error**

After updating the database configuration, Python reported an indentation error in `app.py`.

I corrected the spacing and used `python -m py_compile app.py` to verify that the file compiled successfully.

**3. PostgreSQL command not found**

When I tried running `psql` directly from Terminal, the command was not recognized.

I resolved this by using the full PostgreSQL 18 installation path on my Mac.

**4. Updating tests for PostgreSQL**

Some of my original tests were written for the in-memory version of the application.

I needed to update the tests so that they worked with PostgreSQL-generated IDs and the temporary Day 07 restrictions on editing and deleting tasks.

At one point, four tests passed and one failed because the remaining test still expected the old PATCH behavior.

After correcting that test and restoring the blank-title validation test, all five tests passed.

These challenges helped me become more comfortable reading error messages, reviewing my code, and making corrections one step at a time.

## My Reflection

Day 07 helped me better understand how a Flask backend works with a relational database.

I was especially happy to see that the task I created was still available when I started a new Python process and checked PostgreSQL directly.

That made the concept of database persistence much easier for me to understand.

I also learned that setting up a database involves more than creating tables. I need to think about configuration, migrations, validation, and protecting my development data while running tests.

Although I encountered a few errors along the way, working through them helped me gain more confidence in debugging Python and Flask applications.

My biggest takeaway from Day 07 was learning that reliable applications need both permanent data storage and careful testing.

I am looking forward to continuing with Day 08, where I will work on PostgreSQL-backed task editing, deletion, and categories.
