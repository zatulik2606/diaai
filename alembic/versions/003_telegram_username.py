"""telegram username

Revision ID: 003
Revises: 002
Create Date: 2026-06-07

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("telegram_username", sa.Text(), nullable=True))
    op.create_index(
        "users_telegram_username_key",
        "users",
        ["telegram_username"],
        unique=True,
        postgresql_where=sa.text("telegram_username IS NOT NULL"),
    )


def downgrade() -> None:
    op.drop_index("users_telegram_username_key", table_name="users")
    op.drop_column("users", "telegram_username")
