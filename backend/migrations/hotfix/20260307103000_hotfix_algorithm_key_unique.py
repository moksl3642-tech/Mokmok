"""hotfix enforce unique algorithm key with rollback snapshot

Revision ID: 20260307103000
Revises: 20260307101500
Create Date: 2026-03-07 10:30:00
"""
from __future__ import annotations

from alembic import op

revision = "20260307103000"
down_revision = "20260307101500"
branch_labels = ("hotfix",)
depends_on = None

BACKUP_TABLE = "algorithm_configs_backup_hotfix_20260307103000"


def upgrade() -> None:
    # High-risk path: snapshot old data before normalization/dedup.
    op.execute(f"DROP TABLE IF EXISTS {BACKUP_TABLE}")
    op.execute(
        f"""
        CREATE TABLE {BACKUP_TABLE} AS
        SELECT id, key, value, is_active, created_at
        FROM algorithm_configs
        """
    )

    op.execute("UPDATE algorithm_configs SET key = lower(trim(key))")
    op.execute(
        """
        DELETE FROM algorithm_configs
        WHERE id NOT IN (
            SELECT MAX(id)
            FROM algorithm_configs
            GROUP BY key
        )
        """
    )
    op.create_index("ux_algorithm_configs_key", "algorithm_configs", ["key"], unique=True)


def downgrade() -> None:
    # Rollback path: recover exact pre-hotfix rows from snapshot.
    op.drop_index("ux_algorithm_configs_key", table_name="algorithm_configs")
    op.execute("DELETE FROM algorithm_configs")
    op.execute(
        f"""
        INSERT INTO algorithm_configs (id, key, value, is_active, created_at)
        SELECT id, key, value, is_active, created_at
        FROM {BACKUP_TABLE}
        ORDER BY id
        """
    )
    op.execute(f"DROP TABLE IF EXISTS {BACKUP_TABLE}")
