-- Run once in the dedicated Monday sandbox. Never run in an application database.
DO $$
BEGIN
  IF current_database() <> 'level4_sql_sandbox' THEN
    RAISE EXCEPTION 'Use the level4_sql_sandbox database for this exercise.';
  END IF;
END $$;

BEGIN;
CREATE TABLE sql_categories (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  name VARCHAR(40) NOT NULL UNIQUE,
  CONSTRAINT sql_categories_name_length CHECK (char_length(btrim(name)) BETWEEN 1 AND 40)
);

CREATE TABLE sql_tasks (
  id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  title VARCHAR(80) NOT NULL,
  is_complete BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  category_id INTEGER REFERENCES sql_categories(id) ON DELETE SET NULL,
  CONSTRAINT sql_tasks_title_length CHECK (char_length(btrim(title)) BETWEEN 1 AND 80)
);
CREATE INDEX ix_sql_tasks_category_id ON sql_tasks(category_id);
COMMIT;
