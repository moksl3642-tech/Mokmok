from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def apply_seed(conn: sqlite3.Connection, sql_file: Path) -> None:
    sql = sql_file.read_text(encoding="utf-8")
    conn.executescript(sql)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply database seed scripts.")
    parser.add_argument("--db", default="backend/dev.db", help="SQLite DB path")
    args = parser.parse_args()

    seed_dir = Path(__file__).parent
    seed_files = sorted(seed_dir.glob("[0-9][0-9][0-9]_*.sql"))

    conn = sqlite3.connect(args.db)
    try:
        for seed_file in seed_files:
            apply_seed(conn, seed_file)
        conn.commit()
    finally:
        conn.close()


if __name__ == "__main__":
    main()
