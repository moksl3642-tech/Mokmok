CREATE SCHEMA IF NOT EXISTS system;

CREATE TABLE IF NOT EXISTS system.background_jobs (
    id BIGSERIAL PRIMARY KEY,
    job_id VARCHAR(64) NOT NULL UNIQUE,
    task_name VARCHAR(128) NOT NULL,
    status VARCHAR(20) NOT NULL,
    idempotency_key VARCHAR(128),
    payload JSONB,
    result JSONB,
    error_message TEXT,
    retry_count INT NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_background_jobs_task_name ON system.background_jobs(task_name);
CREATE INDEX IF NOT EXISTS idx_background_jobs_status ON system.background_jobs(status);
CREATE UNIQUE INDEX IF NOT EXISTS idx_background_jobs_task_idempotency
    ON system.background_jobs(task_name, idempotency_key)
    WHERE idempotency_key IS NOT NULL;
