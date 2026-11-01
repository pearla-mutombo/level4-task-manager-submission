DO $$
BEGIN
  IF current_database() <> 'level4_sql_sandbox' THEN
    RAISE EXCEPTION 'Use the level4_sql_sandbox database for this exercise.';
  END IF;
END $$;

BEGIN;
INSERT INTO sql_categories (name) VALUES ('Learning'), ('Personal')
ON CONFLICT (name) DO NOTHING;

INSERT INTO sql_tasks (title, category_id)
SELECT 'Practice SQL', id FROM sql_categories
WHERE name = 'Learning'
  AND NOT EXISTS (SELECT 1 FROM sql_tasks WHERE title = 'Practice SQL');

INSERT INTO sql_tasks (title, is_complete, category_id)
SELECT 'Explain a foreign key', TRUE, id FROM sql_categories
WHERE name = 'Learning'
  AND NOT EXISTS (SELECT 1 FROM sql_tasks WHERE title = 'Explain a foreign key');

INSERT INTO sql_tasks (title)
SELECT 'Plan tomorrow'
WHERE NOT EXISTS (SELECT 1 FROM sql_tasks WHERE title = 'Plan tomorrow');
COMMIT;
