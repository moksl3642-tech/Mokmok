DROP INDEX IF EXISTS ix_educational_contents_status;

CREATE TABLE educational_contents__rollback AS
SELECT id, slug, title, body, created_at
FROM educational_contents;

DROP TABLE educational_contents;

CREATE TABLE educational_contents (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL UNIQUE,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO educational_contents (id, slug, title, body, created_at)
SELECT id, slug, title, body, created_at
FROM educational_contents__rollback;

DROP TABLE educational_contents__rollback;
