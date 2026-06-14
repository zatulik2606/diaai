"""full data layer

Revision ID: 002
Revises: 001
Create Date: 2026-06-14

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("users", "telegram_id", existing_type=sa.BigInteger(), nullable=True)
    op.add_column("users", sa.Column("display_name", sa.Text(), nullable=True))
    op.add_column("users", sa.Column("email", sa.Text(), nullable=True))
    op.drop_constraint("users_telegram_id_key", "users", type_="unique")
    op.drop_index("ix_users_telegram_id", table_name="users")
    op.create_index(
        "ix_users_telegram_id",
        "users",
        ["telegram_id"],
        unique=True,
        postgresql_where=sa.text("telegram_id IS NOT NULL"),
    )
    op.create_check_constraint(
        "ck_users_role",
        "users",
        "role IN ('diabetic', 'doctor')",
    )
    op.create_index("ix_users_role", "users", ["role"], unique=False)

    op.create_table(
        "photo_analyses",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("request_id", sa.Uuid(), nullable=False),
        sa.Column("food_event_id", sa.Uuid(), nullable=True),
        sa.Column("object_type", sa.Text(), nullable=False),
        sa.Column("xe", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("bje", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("proteins", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("fats", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("carbs", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("confidence", sa.Numeric(precision=3, scale=2), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("object_type IN ('dish', 'product', 'label')"),
        sa.CheckConstraint(
            "confidence IS NULL OR (confidence >= 0 AND confidence <= 1)",
            name="ck_photo_analyses_confidence",
        ),
        sa.ForeignKeyConstraint(["food_event_id"], ["food_events.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["request_id"], ["dialog_requests.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_photo_analyses_user_id", "photo_analyses", ["user_id"], unique=False)
    op.create_index(
        "ix_photo_analyses_request_id", "photo_analyses", ["request_id"], unique=False
    )
    op.create_index(
        "ix_photo_analyses_food_event_id",
        "photo_analyses",
        ["food_event_id"],
        unique=False,
        postgresql_where=sa.text("food_event_id IS NOT NULL"),
    )

    op.create_table(
        "progress_snapshots",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("period", sa.Text(), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("sum_xe", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("sum_bje", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("sum_insulin", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("sum_proteins", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("sum_fats", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("sum_carbs", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("trend", sa.Text(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("period IN ('day', 'week', 'month')"),
        sa.CheckConstraint("trend IN ('improving', 'stable', 'worsening')"),
        sa.CheckConstraint("period_start <= period_end"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "period", "period_start"),
    )
    op.create_index(
        "ix_progress_snapshots_user_period",
        "progress_snapshots",
        ["user_id", "period", sa.text("period_start DESC")],
        unique=False,
    )

    op.create_table(
        "recommendations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("request_id", sa.Uuid(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("type", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("type IN ('nutrition', 'insulin', 'dynamics', 'forecast')"),
        sa.ForeignKeyConstraint(["request_id"], ["dialog_requests.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_recommendations_user_id", "recommendations", ["user_id"], unique=False)
    op.create_index(
        "ix_recommendations_request_id",
        "recommendations",
        ["request_id"],
        unique=False,
        postgresql_where=sa.text("request_id IS NOT NULL"),
    )

    op.create_table(
        "consultations",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("diabetic_id", sa.Uuid(), nullable=False),
        sa.Column("doctor_id", sa.Uuid(), nullable=False),
        sa.Column("format", sa.Text(), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("status", sa.Text(), nullable=False),
        sa.Column("doctor_comment", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("format IN ('online', 'offline')"),
        sa.CheckConstraint("status IN ('scheduled', 'completed', 'cancelled')"),
        sa.CheckConstraint("diabetic_id != doctor_id"),
        sa.ForeignKeyConstraint(["diabetic_id"], ["users.id"], ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["doctor_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_consultations_diabetic_id", "consultations", ["diabetic_id"], unique=False)
    op.create_index("ix_consultations_doctor_id", "consultations", ["doctor_id"], unique=False)
    op.create_index(
        "ix_consultations_doctor_scheduled",
        "consultations",
        ["doctor_id", "scheduled_at"],
        unique=False,
    )

    op.create_index(
        "ix_food_events_user_recorded_at",
        "food_events",
        ["user_id", sa.text("recorded_at DESC")],
        unique=False,
    )
    op.create_index(
        "ix_food_events_request_id",
        "food_events",
        ["request_id"],
        unique=False,
        postgresql_where=sa.text("request_id IS NOT NULL"),
    )
    op.create_index(
        "ix_insulin_events_user_injected_at",
        "insulin_events",
        ["user_id", sa.text("injected_at DESC")],
        unique=False,
    )
    op.create_index(
        "ix_insulin_events_food_event_id",
        "insulin_events",
        ["food_event_id"],
        unique=False,
        postgresql_where=sa.text("food_event_id IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index(
        "ix_insulin_events_food_event_id",
        table_name="insulin_events",
        postgresql_where=sa.text("food_event_id IS NOT NULL"),
    )
    op.drop_index("ix_insulin_events_user_injected_at", table_name="insulin_events")
    op.drop_index(
        "ix_food_events_request_id",
        table_name="food_events",
        postgresql_where=sa.text("request_id IS NOT NULL"),
    )
    op.drop_index("ix_food_events_user_recorded_at", table_name="food_events")

    op.drop_index("ix_consultations_doctor_scheduled", table_name="consultations")
    op.drop_index("ix_consultations_doctor_id", table_name="consultations")
    op.drop_index("ix_consultations_diabetic_id", table_name="consultations")
    op.drop_table("consultations")

    op.drop_index(
        "ix_recommendations_request_id",
        table_name="recommendations",
        postgresql_where=sa.text("request_id IS NOT NULL"),
    )
    op.drop_index("ix_recommendations_user_id", table_name="recommendations")
    op.drop_table("recommendations")

    op.drop_index("ix_progress_snapshots_user_period", table_name="progress_snapshots")
    op.drop_table("progress_snapshots")

    op.drop_index(
        "ix_photo_analyses_food_event_id",
        table_name="photo_analyses",
        postgresql_where=sa.text("food_event_id IS NOT NULL"),
    )
    op.drop_index("ix_photo_analyses_request_id", table_name="photo_analyses")
    op.drop_index("ix_photo_analyses_user_id", table_name="photo_analyses")
    op.drop_table("photo_analyses")

    op.drop_index("ix_users_role", table_name="users")
    op.drop_constraint("ck_users_role", "users", type_="check")
    op.drop_index(
        "ix_users_telegram_id",
        table_name="users",
        postgresql_where=sa.text("telegram_id IS NOT NULL"),
    )
    op.drop_column("users", "email")
    op.drop_column("users", "display_name")
    op.create_unique_constraint("users_telegram_id_key", "users", ["telegram_id"])
    op.create_index("ix_users_telegram_id", "users", ["telegram_id"], unique=False)
    op.alter_column("users", "telegram_id", existing_type=sa.BigInteger(), nullable=False)
