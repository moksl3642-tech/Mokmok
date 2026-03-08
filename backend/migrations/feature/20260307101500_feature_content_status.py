"""feature add content status

Revision ID: 20260307101500
Revises: 20260307100000
Create Date: 2026-03-07 10:15:00
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "20260307101500"
down_revision = "20260307100000"
branch_labels = ("feature",)
depends_on = None


def upgrade() -> None:
    op.add_column(
        "educational_contents",
        sa.Column("status", sa.String(length=30), server_default="draft", nullable=False),
    )
    op.create_index("ix_educational_contents_status", "educational_contents", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_educational_contents_status", table_name="educational_contents")
    op.drop_column("educational_contents", "status")
