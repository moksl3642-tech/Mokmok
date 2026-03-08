BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS app;
CREATE SCHEMA IF NOT EXISTS auth;
CREATE SCHEMA IF NOT EXISTS system;

-- =========================
-- auth schema
-- =========================
CREATE TABLE IF NOT EXISTS auth.users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL,
  username TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'player',
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT users_email_format_chk CHECK (position('@' IN email) > 1),
  CONSTRAINT users_role_chk CHECK (role IN ('player', 'coach', 'admin')),
  CONSTRAINT users_status_chk CHECK (status IN ('active', 'inactive', 'suspended')),
  CONSTRAINT users_email_uq UNIQUE (email),
  CONSTRAINT users_username_uq UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS auth.admin_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  access_level TEXT NOT NULL DEFAULT 'viewer',
  status TEXT NOT NULL DEFAULT 'active',
  mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT admin_accounts_user_fk
    FOREIGN KEY (user_id)
    REFERENCES auth.users(id)
    ON DELETE CASCADE,
  CONSTRAINT admin_accounts_access_level_chk CHECK (access_level IN ('viewer', 'editor', 'super_admin')),
  CONSTRAINT admin_accounts_status_chk CHECK (status IN ('active', 'inactive', 'revoked')),
  CONSTRAINT admin_accounts_user_uq UNIQUE (user_id)
);

-- =========================
-- app schema
-- =========================
CREATE TABLE IF NOT EXISTS app.sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT sessions_user_fk
    FOREIGN KEY (user_id)
    REFERENCES auth.users(id)
    ON DELETE CASCADE,
  CONSTRAINT sessions_status_chk CHECK (status IN ('active', 'completed', 'cancelled')),
  CONSTRAINT sessions_time_window_chk CHECK (ended_at IS NULL OR ended_at >= started_at)
);

CREATE TABLE IF NOT EXISTS app.shoes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL,
  shoe_no SMALLINT NOT NULL,
  status TEXT NOT NULL DEFAULT 'open',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  closed_at TIMESTAMPTZ,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT shoes_session_fk
    FOREIGN KEY (session_id)
    REFERENCES app.sessions(id)
    ON DELETE CASCADE,
  CONSTRAINT shoes_status_chk CHECK (status IN ('open', 'closed', 'void')),
  CONSTRAINT shoes_no_range_chk CHECK (shoe_no BETWEEN 1 AND 12),
  CONSTRAINT shoes_unique_per_session_uq UNIQUE (session_id, shoe_no)
);

CREATE TABLE IF NOT EXISTS app.hands (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL,
  shoe_id UUID,
  hand_no INTEGER NOT NULL,
  result TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT hands_session_fk
    FOREIGN KEY (session_id)
    REFERENCES app.sessions(id)
    ON DELETE CASCADE,
  CONSTRAINT hands_shoe_fk
    FOREIGN KEY (shoe_id)
    REFERENCES app.shoes(id)
    ON DELETE SET NULL,
  CONSTRAINT hands_result_chk CHECK (result IN ('player', 'banker', 'tie', 'void')),
  CONSTRAINT hands_no_positive_chk CHECK (hand_no > 0),
  CONSTRAINT hands_unique_no_in_session_uq UNIQUE (session_id, hand_no)
);

CREATE TABLE IF NOT EXISTS app.patterns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  session_id UUID NOT NULL,
  hand_id UUID,
  pattern_type TEXT NOT NULL,
  confidence NUMERIC(5,4) NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  details JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT patterns_session_fk
    FOREIGN KEY (session_id)
    REFERENCES app.sessions(id)
    ON DELETE CASCADE,
  CONSTRAINT patterns_hand_fk
    FOREIGN KEY (hand_id)
    REFERENCES app.hands(id)
    ON DELETE SET NULL,
  CONSTRAINT patterns_type_chk CHECK (pattern_type IN ('streak', 'zigzag', 'cluster', 'custom')),
  CONSTRAINT patterns_confidence_chk CHECK (confidence >= 0 AND confidence <= 1),
  CONSTRAINT patterns_status_chk CHECK (status IN ('active', 'inactive', 'archived')),
  CONSTRAINT patterns_unique_session_hand_type_uq UNIQUE (session_id, hand_id, pattern_type)
);

CREATE TABLE IF NOT EXISTS app.user_settings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  setting_scope TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  preferences JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT user_settings_user_fk
    FOREIGN KEY (user_id)
    REFERENCES auth.users(id)
    ON DELETE CASCADE,
  CONSTRAINT user_settings_scope_chk CHECK (setting_scope IN ('global', 'session', 'notification', 'display')),
  CONSTRAINT user_settings_status_chk CHECK (status IN ('active', 'inactive')),
  CONSTRAINT user_settings_unique_scope_uq UNIQUE (user_id, setting_scope)
);

-- =========================
-- system schema
-- =========================
CREATE TABLE IF NOT EXISTS system.algorithm_config (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  config_key TEXT NOT NULL,
  version INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'active',
  config JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_by UUID,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT algorithm_config_updated_by_fk
    FOREIGN KEY (updated_by)
    REFERENCES auth.users(id)
    ON DELETE SET NULL,
  CONSTRAINT algorithm_config_status_chk CHECK (status IN ('active', 'inactive', 'deprecated')),
  CONSTRAINT algorithm_config_version_chk CHECK (version > 0),
  CONSTRAINT algorithm_config_key_version_uq UNIQUE (config_key, version)
);

CREATE TABLE IF NOT EXISTS system.audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  actor_user_id UUID,
  entity_schema TEXT NOT NULL,
  entity_table TEXT NOT NULL,
  entity_id UUID,
  action TEXT NOT NULL,
  severity TEXT NOT NULL DEFAULT 'info',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  CONSTRAINT audit_logs_actor_fk
    FOREIGN KEY (actor_user_id)
    REFERENCES auth.users(id)
    ON DELETE SET NULL,
  CONSTRAINT audit_logs_action_chk CHECK (action IN ('create', 'update', 'delete', 'login', 'logout', 'config_change')),
  CONSTRAINT audit_logs_severity_chk CHECK (severity IN ('info', 'warning', 'critical')),
  CONSTRAINT audit_logs_entity_schema_chk CHECK (entity_schema IN ('app', 'auth', 'system'))
);

CREATE TABLE IF NOT EXISTS system.education_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  slug TEXT NOT NULL,
  title TEXT NOT NULL,
  content_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'draft',
  language_code TEXT NOT NULL DEFAULT 'vi',
  body JSONB NOT NULL,
  published_at TIMESTAMPTZ,
  created_by UUID,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT education_content_created_by_fk
    FOREIGN KEY (created_by)
    REFERENCES auth.users(id)
    ON DELETE SET NULL,
  CONSTRAINT education_content_type_chk CHECK (content_type IN ('article', 'video', 'faq', 'guide')),
  CONSTRAINT education_content_status_chk CHECK (status IN ('draft', 'review', 'published', 'archived')),
  CONSTRAINT education_content_lang_chk CHECK (language_code IN ('vi', 'en')),
  CONSTRAINT education_content_publish_time_chk CHECK (published_at IS NULL OR published_at >= created_at),
  CONSTRAINT education_content_slug_lang_uq UNIQUE (slug, language_code)
);

-- =========================
-- Index strategy
-- =========================

-- Timeline query indexes (session_id + created_at)
CREATE INDEX IF NOT EXISTS idx_hands_session_created_at
  ON app.hands (session_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_patterns_session_created_at
  ON app.patterns (session_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_shoes_session_created_at
  ON app.shoes (session_id, created_at DESC);

-- Partial index for active/inactive workloads
CREATE INDEX IF NOT EXISTS idx_users_active_email
  ON auth.users (email)
  WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_admin_accounts_active_level
  ON auth.admin_accounts (access_level)
  WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_sessions_active_user_started
  ON app.sessions (user_id, started_at DESC)
  WHERE status = 'active';

CREATE INDEX IF NOT EXISTS idx_patterns_active_session_created
  ON app.patterns (session_id, created_at DESC)
  WHERE status = 'active';

-- GIN indexes on JSONB filterable columns
CREATE INDEX IF NOT EXISTS idx_user_settings_preferences_gin
  ON app.user_settings USING GIN (preferences jsonb_path_ops);

CREATE INDEX IF NOT EXISTS idx_algorithm_config_gin
  ON system.algorithm_config USING GIN (config jsonb_path_ops);

CREATE INDEX IF NOT EXISTS idx_audit_logs_metadata_gin
  ON system.audit_logs USING GIN (metadata jsonb_path_ops);

COMMIT;
