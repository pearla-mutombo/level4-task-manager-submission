# Day 08 — PostgreSQL CRUD and Category Management

## Objective

The goal for Day 08 was to expand my Flask Task Manager API by implementing full CRUD operations using PostgreSQL and SQLAlchemy. I also needed to add categories so tasks could be organized and filtered.

## What I Completed

### 1. PostgreSQL Task CRUD

I implemented the following API endpoints:

| Method | Endpoint          | Purpose                  |
| ------ | ----------------- | ------------------------ |
| GET    | `/api/tasks`      | Retrieve all tasks       |
| GET    | `/api/tasks/<id>` | Retrieve a specific task |
| POST   | `/api/tasks`      | Create a new task        |
| PATCH  | `/api/tasks/<id>` | Update an existing task  |
| DELETE | `/api/tasks/<id>` | Delete a task            |

Tasks are stored in PostgreSQL, so changes remain saved after the Flask application restarts.

### 2. Category Management

I created a `Category` model and added endpoints for managing categories.

| Method | Endpoint               | Purpose           |
| ------ | ---------------------- | ----------------- |
| GET    | `/api/categories`      | List categories   |
| POST   | `/api/categories`      | Create a category |
| PATCH  | `/api/categories/<id>` | Rename a category |
| DELETE | `/api/categories/<id>` | Delete a category |

Category names are validated to prevent blank names and names longer than 40 characters. Duplicate category names are also rejected.

### 3. Database Relationships and Migration

I created an Alembic migration that:

- Adds the `categories` table.
- Adds an optional `category_id` column to the `tasks` table.
- Establishes a foreign-key relationship between tasks and categories.
- Uses `ON DELETE SET NULL` so deleting a category does not delete its tasks.

I applied and verified the migration in both my development and testing PostgreSQL databases.

### 4. Task Filtering

I added support for filtering tasks by category and completion status.

Examples:

```text
GET /api/tasks?category_id=2
GET /api/tasks?status=active
GET /api/tasks?status=completed&category_id=2
```

This allows users to retrieve tasks that match a specific category, completion status, or both.

### 5. Validation and Error Handling

I added validation for task titles, category names, category IDs, and completion status values.

The API returns appropriate HTTP responses, including:

- `200 OK` for successful retrieval and updates.
- `201 Created` when a task or category is created.
- `204 No Content` after successful deletion.
- `400 Bad Request` for invalid input.
- `404 Not Found` when a requested resource does not exist.
- `409 Conflict` for duplicate category names.

### 6. Automated Testing

I expanded the backend test suite to cover task CRUD operations, category management, category assignments, and filtering.

I ran:

```bash
python -m pytest -q
```

Result:

```text
11 passed in 2.16s
```

The tests use a separate PostgreSQL testing database to protect my development data.

I also ran:

```bash
git diff --check
```

No whitespace errors were reported.

## Files Updated

- `backend/app.py` — Added task CRUD, category endpoints, validation, and filtering.
- `backend/models.py` — Added the Category model and task-category relationship.
- `backend/tests/test_tasks.py` — Expanded automated tests.
- `backend/migrations/versions/fa130ea5e2c6_add_categories_and_task_category_.py` — Added the database migration.

## Challenges and What I Learned

One challenge was understanding how to connect tasks to categories without accidentally deleting tasks when a category is removed. I learned how a foreign key with `ON DELETE SET NULL` can preserve the task while removing its category assignment.

I also gained more experience with Flask routes, SQLAlchemy queries, database migrations, and API validation.

Another important lesson was keeping my testing database separate from my development database. This allowed me to run automated tests without deleting the tasks I had already saved.

## Reflection

Day 08 helped me better understand how a backend application manages information in a relational database.

I learned that CRUD operations involve more than simply creating and deleting records. It is also important to validate incoming data, return meaningful error messages, protect existing records, and test the application carefully.

Completing this assignment gave me more confidence working with Flask, PostgreSQL, SQLAlchemy, and automated tests.

## Next Steps

On Day 09, I will begin implementing authentication and user ownership so that each signed-in user can access and manage only their own tasks.
