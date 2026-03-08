-- Run after applying backend/db/schema.sql
-- Example:
--   psql "$DATABASE_URL" -f backend/db/schema.sql
--   psql "$DATABASE_URL" -f backend/db/explain-plans.sql

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, hand_no, result, created_at
FROM app.hands
WHERE session_id = '00000000-0000-0000-0000-000000000001'
ORDER BY created_at DESC
LIMIT 100;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, pattern_type, confidence, created_at
FROM app.patterns
WHERE session_id = '00000000-0000-0000-0000-000000000001'
ORDER BY created_at DESC
LIMIT 100;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, shoe_no, status, created_at
FROM app.shoes
WHERE session_id = '00000000-0000-0000-0000-000000000001'
ORDER BY created_at DESC;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, email, username
FROM auth.users
WHERE status = 'active'
  AND email = 'active.user@example.com';

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, started_at
FROM app.sessions
WHERE user_id = '00000000-0000-0000-0000-000000000001'
  AND status = 'active'
ORDER BY started_at DESC
LIMIT 20;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, pattern_type, created_at
FROM app.patterns
WHERE session_id = '00000000-0000-0000-0000-000000000001'
  AND status = 'active'
ORDER BY created_at DESC;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, user_id, preferences
FROM app.user_settings
WHERE preferences @> '{"theme": "dark"}'::jsonb;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, config_key, version
FROM system.algorithm_config
WHERE config @> '{"mode": "aggressive"}'::jsonb;

EXPLAIN (ANALYZE, BUFFERS)
SELECT id, action, created_at
FROM system.audit_logs
WHERE metadata @> '{"ip": "10.0.0.1"}'::jsonb
ORDER BY created_at DESC;
