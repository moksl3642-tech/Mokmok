DROP TABLE IF EXISTS algorithm_configs_backup_hotfix_20260307103000;
CREATE TABLE algorithm_configs_backup_hotfix_20260307103000 AS
SELECT id, key, value, is_active, created_at
FROM algorithm_configs;

UPDATE algorithm_configs
SET key = lower(trim(key));

DELETE FROM algorithm_configs
WHERE id NOT IN (
  SELECT MAX(id)
  FROM algorithm_configs
  GROUP BY key
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_algorithm_configs_key ON algorithm_configs(key);
