"""migration for users.py

Revision ID: 5adf63d91a30
Revises: f5aef8c2a939
Create Date: 2024-09-30 21:14:56.232397

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5adf63d91a30"
down_revision: Union[str, None] = "f5aef8c2a939"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_password", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
