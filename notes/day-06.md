# Day 06 — SQL Foundations

## Project Description

For Day 06 of my Level 4 Task Manager project, I focused on learning the fundamentals of PostgreSQL and practicing SQL queries using pgAdmin 4.

I created a separate practice database named `level4_sql_sandbox` so I could work with SQL without affecting my Task Manager application's existing data.

During this exercise, I practiced creating database tables, inserting and retrieving records, filtering and sorting results, connecting tables using foreign keys, and using SQL transactions.

I also learned how `ROLLBACK` works by making temporary changes to records and verifying that those changes were reversed successfully.

This exercise helped me better understand how relational databases store and manage information and prepared me for connecting PostgreSQL to my Flask application in the next stage of the project.

## Files Used

- `sql/day-06/01-schema.sql` — Reference SQL script used to create the `sql_categories` and `sql_tasks` tables in my PostgreSQL practice database.
- `exercises/day-06/practice.sql` — My SQL practice file containing exercises for retrieving, filtering, updating, and working with database records.
- `notes/day-06/README.md` — Documentation of the exercises I completed, the results I verified, and the concepts I learned.

### Database and Tools

- **PostgreSQL 18:** The relational database management system used for the exercises.
- **pgAdmin 4:** The graphical interface I used to create my database, execute SQL queries, and review results.
- **Visual Studio Code:** The code editor I used to write and save my SQL exercises and documentation.
- **Git:** The version control tool used to track my Day 06 work on the `day-06-sql-foundations` branch.

### Practice Database

- **Database name:** `level4_sql_sandbox`
- **Tables:** `sql_categories` and `sql_tasks`
- **Purpose:** A separate learning environment for practicing SQL without changing the Task Manager application's existing data.

## How to Run the Exercises

For this assignment, I used PostgreSQL 18 and pgAdmin 4 to practice SQL in a separate database.

1. Open pgAdmin 4 and connect to the local PostgreSQL 18 server.
2. Create a practice database named `level4_sql_sandbox` if it does not already exist.
3. Open the Query Tool for the `level4_sql_sandbox` database.
4. Run `sql/day-06/01-schema.sql` once to create the `sql_categories` and `sql_tasks` tables.
5. Run `sql/day-06/02-seed.sql` to insert sample categories and tasks.
6. Open `exercises/day-06/practice.sql` to review the SQL queries I practiced.
7. Run individual queries in pgAdmin 4 and check the **Data Output** or **Messages** panel to verify the results.

**Important:** The schema script is intended for a new sandbox database. I should not rerun it against tables that already exist without first checking the database.

For the transaction exercises, I used `BEGIN` and `ROLLBACK` to test changes without permanently modifying my practice records.

I kept this database separate from my Flask application's database so I could learn and experiment safely.

## SQL Practice Results

I completed the following SQL exercises using PostgreSQL 18 and pgAdmin 4. I checked the results in the Data Output and Messages panels to confirm that my queries worked.

| Exercise                     | SQL Concepts                               | Verified Result                                            |
| ---------------------------- | ------------------------------------------ | ---------------------------------------------------------- |
| Create tables                | `CREATE TABLE`, primary keys, foreign keys | Successfully created `sql_categories` and `sql_tasks`.     |
| Insert sample data           | `INSERT INTO`                              | Added 2 categories and 3 tasks.                            |
| Retrieve tasks               | `SELECT`                                   | Returned all 3 tasks.                                      |
| Filter incomplete tasks      | `WHERE`                                    | Returned 2 incomplete tasks.                               |
| Sort tasks                   | `ORDER BY ASC`                             | Displayed incomplete tasks alphabetically.                 |
| Connect tasks and categories | `LEFT JOIN`                                | Returned all 3 tasks, including one without a category.    |
| Count tasks by category      | `COUNT()`, `GROUP BY`                      | Learning: 2 tasks; Personal: 0 tasks.                      |
| Undo a task insertion        | `BEGIN`, `INSERT`, `ROLLBACK`              | Verified that 0 temporary tasks remained.                  |
| Undo a category deletion     | `DELETE`, `ROLLBACK`                       | Restored the Learning category and its task relationships. |
| Undo a task update           | `UPDATE`, `ROLLBACK`                       | Verified that Practice SQL remained incomplete (`false`).  |

I tested the task title constraint by attempting to insert a task with an empty title. PostgreSQL rejected the insert with SQL state 23514 because it violated the sql_tasks_title_length check constraint. This confirmed that the database prevents tasks from being created without a valid title.

### Transaction Verification

One of the most important lessons I learned was how to use transactions to protect database records.

I practiced inserting a temporary task and then using `ROLLBACK` to undo the insertion. When I checked the database afterward, the query returned:

```text
temporary_tasks_after_rollback = 0
```

I also practiced temporarily deleting the Learning category. After executing `ROLLBACK`, I verified that both Practice SQL and Explain a foreign key were still assigned to Learning.

Finally, I tested an `UPDATE` statement by temporarily marking Practice SQL as completed. After rolling back the transaction, I confirmed that its `is_complete` value was still `false`.

These results helped me understand how PostgreSQL can reverse changes made within a transaction.

## Concepts Practiced

During Day 06, I practiced several important PostgreSQL and SQL concepts.

- **Relational databases:** I learned how PostgreSQL stores information in tables and how related tables can work together.
- **Primary keys:** I learned that a primary key uniquely identifies each record in a table.
- **Foreign keys:** I practiced connecting tasks to categories using `category_id`.
- **SELECT:** I used SQL queries to retrieve records from my database.
- **WHERE:** I filtered tasks based on whether they were completed.
- **ORDER BY:** I sorted task records alphabetically.
- **LEFT JOIN:** I connected tasks with their category names while keeping tasks that had no category.
- **COUNT and GROUP BY:** I counted how many tasks belonged to each category.
- **INSERT:** I added sample records to my practice database.
- **UPDATE:** I practiced changing a task's completion status.
- **DELETE:** I practiced temporarily deleting a category.
- **Transactions:** I used `BEGIN` to group database operations together.
- **ROLLBACK:** I learned how to undo changes made during a transaction.
- **ON DELETE SET NULL:** I observed how deleting a category can affect related tasks without deleting the tasks themselves.

These exercises helped me understand how SQL can be used to create, retrieve, update, and manage information in a relational database.

I also learned why it is important to test database operations carefully, especially when working with related records.

## What I Learned

During Day 06, I learned more about how PostgreSQL works and how SQL is used to manage information in a database.

Before completing these exercises, I was still getting familiar with writing SQL queries and understanding how tables connect to one another. Practicing each query in pgAdmin 4 helped me understand what the commands actually do instead of just reading about them.

One of the things I found helpful was learning how to use `LEFT JOIN` to connect my tasks with their categories. I also learned that a task can still appear in the results even when it does not have a category assigned to it.

Another important lesson was understanding the difference between `COMMIT` and `ROLLBACK`. I practiced making temporary changes to my database and then undoing those changes. Being able to check the results afterward helped me understand why transactions are important when working with database records.

I also became more comfortable using pgAdmin 4 to execute queries, review the Data Output, and check for errors.

Overall, this assignment helped me build a better understanding of SQL and relational databases. I know I still need more practice, but I feel more confident working with PostgreSQL than I did when I first started these exercises.

## Challenges and How I Resolved Them

During Day 06, I encountered a few challenges while learning PostgreSQL and working with SQL queries.

**1. Getting familiar with pgAdmin 4**

At first, I needed some guidance navigating pgAdmin 4, especially when opening SQL files and using the Query Tool. I worked through the steps carefully and learned how to select the correct database, open my SQL scripts, and execute them.

**2. Understanding how related tables work**

I was still learning how foreign keys connect information between tables. Practicing `LEFT JOIN` helped me understand how the tasks table connects to the categories table and why a task can still exist without an assigned category.

**3. Understanding transactions and ROLLBACK**

I wanted to make sure I understood how to undo database changes safely. I practiced inserting, updating, and deleting records inside transactions and then using `ROLLBACK` to reverse those changes. I also ran verification queries afterward to confirm that the original records were preserved.

**4. Opening files in Visual Studio Code from Terminal**

When I tried using the `code` command, Terminal displayed a `command not found` error. I resolved this by using the macOS `open -a "Visual Studio Code"` command, which allowed me to open my SQL practice file and README successfully.

These challenges gave me an opportunity to become more familiar with PostgreSQL, pgAdmin 4, SQL commands, and my development environment. Working through each issue step by step helped me better understand the tools and become more comfortable using them.
