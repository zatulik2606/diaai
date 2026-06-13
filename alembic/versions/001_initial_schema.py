"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-07

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"], unique=False)

    op.create_table(
        "dialogs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("channel", sa.String(length=32), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_dialogs_user_id", "dialogs", ["user_id"], unique=False)

    op.create_table(
        "dialog_requests",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("dialog_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("reply", sa.Text(), nullable=False),
        sa.Column("media", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["dialog_id"], ["dialogs.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_dialog_requests_dialog_id", "dialog_requests", ["dialog_id"], unique=False)
    op.create_index("ix_dialog_requests_user_id", "dialog_requests", ["user_id"], unique=False)

    op.create_table(
        "food_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("request_id", sa.Uuid(), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("xe", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("bje", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("proteins", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("fats", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("carbs", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["request_id"], ["dialog_requests.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_food_events_user_id", "food_events", ["user_id"], unique=False)

    op.create_table(
        "insulin_events",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("food_event_id", sa.Uuid(), nullable=True),
        sa.Column("dose", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("injected_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["food_event_id"], ["food_events.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_insulin_events_user_id", "insulin_events", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_insulin_events_user_id", table_name="insulin_events")
    op.drop_table("insulin_events")
    op.drop_index("ix_food_events_user_id", table_name="food_events")
    op.drop_table("food_events")
    op.drop_index("ix_dialog_requests_user_id", table_name="dialog_requests")
    op.drop_index("ix_dialog_requests_dialog_id", table_name="dialog_requests")
    op.drop_table("dialog_requests")
    op.drop_index("ix_dialogs_user_id", table_name="dialogs")
    op.drop_table("dialogs")
    op.drop_index("ix_users_telegram_id", table_name="users")
    op.drop_table("users")
