-- Day 06: SQL Foundations
-- Practice Exercise 1: Reading records from a table
-- Database: level4_sql_sandbox

-- SELECT retrieves information from a database table.
-- The * symbol means to display all columns.
SELECT * FROM sql_tasks;

-- Expected result:
-- 3 tasks: Practice SQL, Explain a foreign key, Plan tomorrow.

-- Practice Exercise 2: Filtering incomplete tasks
-- WHERE allows us to retrieve records that meet a condition.

SELECT * FROM sql_tasks
WHERE is_complete = FALSE;

-- Expected result:
-- 2 incomplete tasks:
-- Practice SQL
-- Plan tomorrow

-- Practice Exercise 3: Sorting incomplete tasks alphabetically
-- ORDER BY arranges query results in a specific order.
-- ASC means ascending order (A to Z).

SELECT * FROM sql_tasks
WHERE is_complete = FALSE
ORDER BY title ASC;

-- Actual result verified in pgAdmin 4:
-- 2 incomplete tasks, sorted alphabetically:
-- 1. Plan tomorrow
-- 2. Practice SQL

-- Practice Exercise 4: Connecting tasks with categories
-- LEFT JOIN combines records from two related tables.
-- It also includes tasks that do not have a category.

SELECT t.title, c.name AS category_name
FROM sql_tasks AS t
LEFT JOIN sql_categories AS c
ON t.category_id = c.id
ORDER BY t.title ASC;

-- Actual results verified in pgAdmin 4:
-- Explain a foreign key | Learning
-- Plan tomorrow         | NULL
-- Practice SQL          | Learning

-- Practice Exercise 5: Counting tasks in each category
-- COUNT() counts the number of matching records.
-- GROUP BY organizes records into groups.
-- LEFT JOIN includes categories that have no tasks.

SELECT c.name AS category_name,
       COUNT(t.id) AS task_count
FROM sql_categories AS c
LEFT JOIN sql_tasks AS t
ON t.category_id = c.id
GROUP BY c.id, c.name
ORDER BY c.name ASC;

-- Actual results verified in pgAdmin 4:
-- Learning | 2
-- Personal | 0

-- Practice Exercise 6: Using transactions and ROLLBACK
-- BEGIN starts a transaction.
-- INSERT adds a temporary task.
-- ROLLBACK undoes the insertion.

BEGIN;

INSERT INTO sql_tasks (title)
VALUES ('My rollback practice task');

SELECT id, title, is_complete
FROM sql_tasks
WHERE title = 'My rollback practice task';

ROLLBACK;

-- Verify that the temporary task was not saved.
SELECT COUNT(*) AS temporary_tasks_after_rollback
FROM sql_tasks
WHERE title = 'My rollback practice task';

-- Actual result verified in pgAdmin 4:
-- temporary_tasks_after_rollback = 0

-- Practice Exercise 7: Rolling back a category deletion
-- DELETE temporarily removes the Learning category.
-- ON DELETE SET NULL temporarily removes its task assignments.
-- ROLLBACK restores the category and its relationships.

BEGIN;

DELETE FROM sql_categories
WHERE name = 'Learning';

SELECT id, title, category_id
FROM sql_tasks
ORDER BY id;

ROLLBACK;

-- Verify that the category and task relationships were restored.
SELECT t.title, c.name AS category_name
FROM sql_tasks AS t
LEFT JOIN sql_categories AS c
ON t.category_id = c.id
ORDER BY t.id;

-- Actual results verified in pgAdmin 4:
-- Practice SQL          | Learning
-- Explain a foreign key | Learning
-- Plan tomorrow         | NULL

-- Practice Exercise 8: Updating a task and using ROLLBACK
-- UPDATE changes an existing record.
-- ROLLBACK reverses the change made during the transaction.

BEGIN;

UPDATE sql_tasks
SET is_complete = TRUE
WHERE title = 'Practice SQL';

SELECT id, title, is_complete
FROM sql_tasks
WHERE title = 'Practice SQL';

ROLLBACK;

-- Verify that the original completion status was restored.
SELECT id, title, is_complete
FROM sql_tasks
WHERE title = 'Practice SQL';

-- Actual result verified in pgAdmin 4:
-- 1 | Practice SQL | false

-- Practice Exercise 9: Testing a CHECK constraint
-- A CHECK constraint prevents invalid data from being saved.
-- The task title must contain between 1 and 80 characters
-- after leading and trailing spaces are removed.

-- The following INSERT was tested separately in pgAdmin 4.
-- It is commented out because PostgreSQL correctly rejects it.

-- INSERT INTO sql_tasks (title)
-- VALUES ('');

-- Actual result verified in pgAdmin 4:
-- ERROR: new row for relation "sql_tasks" violates
-- check constraint "sql_tasks_title_length"
-- SQL state: 23514

-- This confirms that PostgreSQL rejects empty task titles.