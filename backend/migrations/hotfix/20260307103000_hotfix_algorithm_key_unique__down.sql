DROP INDEX IF EXISTS ux_algorithm_configs_key;
DELETE FROM algorithm_configs;

INSERT INTO algorithm_configs (id, key, value, is_active, created_at)
SELECT id, key, value, is_active, created_at
FROM algorithm_configs_backup_hotfix_20260307103000
ORDER BY id;

DROP TABLE IF EXISTS algorithm_configs_backup_hotfix_20260307103000;
