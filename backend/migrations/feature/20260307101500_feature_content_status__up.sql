ALTER TABLE educational_contents ADD COLUMN status TEXT NOT NULL DEFAULT 'draft';
CREATE INDEX IF NOT EXISTS ix_educational_contents_status ON educational_contents(status);
