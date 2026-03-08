from __future__ import annotations

import argparse
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

GROUP_ORDER = {"baseline": 0, "feature": 1, "hotfix": 2}
PATTERN = re.compile(r"^(\d{14})_(baseline|feature|hotfix)_(.+)__up\.sql$")


@dataclass(frozen=True)
class Migration:
    version: str
    group: str
    name: str
    up_path: Path
    down_path: Path

    @property
    def key(self) -> tuple[str, int, str]:
        return (self.version, GROUP_ORDER[self.group], self.name)


def load_migrations(root: Path) -> list[Migration]:
    migrations: list[Migration] = []
    for up_file in root.glob("*/*__up.sql"):
        match = PATTERN.match(up_file.name)
        if not match:
            continue
        version, group, name = match.groups()
        down_file = up_file.with_name(up_file.name.replace("__up.sql", "__down.sql"))
        if not down_file.exists():
            raise FileNotFoundError(f"Missing down migration for {up_file}")
        migrations.append(Migration(version, group, name, up_file, down_file))
    return sorted(migrations, key=lambda m: m.key)


def ensure_meta(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
          version TEXT PRIMARY KEY,
          group_name TEXT NOT NULL,
          name TEXT NOT NULL,
          applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def applied_versions(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("SELECT version FROM schema_migrations ORDER BY version").fetchall()
    return [r[0] for r in rows]


def apply_migration(conn: sqlite3.Connection, m: Migration) -> None:
    conn.executescript(m.up_path.read_text(encoding="utf-8"))
    conn.execute(
        "INSERT INTO schema_migrations(version, group_name, name) VALUES (?, ?, ?)",
        (m.version, m.group, m.name),
    )


def rollback_migration(conn: sqlite3.Connection, m: Migration) -> None:
    conn.executescript(m.down_path.read_text(encoding="utf-8"))
    conn.execute("DELETE FROM schema_migrations WHERE version = ?", (m.version,))


def upgrade(conn: sqlite3.Connection, migrations: list[Migration]) -> None:
    applied = set(applied_versions(conn))
    for migration in migrations:
        if migration.version in applied:
            continue
        apply_migration(conn, migration)


def downgrade_steps(conn: sqlite3.Connection, migrations: list[Migration], steps: int) -> None:
    applied = applied_versions(conn)
    migration_map = {m.version: m for m in migrations}
    for version in reversed(applied[-steps:]):
        rollback_migration(conn, migration_map[version])


def downgrade_base(conn: sqlite3.Connection, migrations: list[Migration]) -> None:
    applied = applied_versions(conn)
    migration_map = {m.version: m for m in migrations}
    for version in reversed(applied):
        rollback_migration(conn, migration_map[version])


def main() -> None:
    parser = argparse.ArgumentParser(description="Simple SQL migration runner")
    parser.add_argument("action", choices=["upgrade", "downgrade"])
    parser.add_argument("target", help="head | base | -1 | -N")
    parser.add_argument("--db", default="backend/dev.db", help="SQLite DB path")
    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    try:
        ensure_meta(conn)
        migrations = load_migrations(Path(__file__).parent)

        if args.action == "upgrade":
            if args.target != "head":
                raise ValueError("Only upgrade head is supported")
            upgrade(conn, migrations)

        if args.action == "downgrade":
            if args.target == "base":
                downgrade_base(conn, migrations)
            elif args.target.startswith("-"):
                steps = int(args.target[1:])
                downgrade_steps(conn, migrations, steps)
            else:
                raise ValueError("Downgrade target must be base or -N")

        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
