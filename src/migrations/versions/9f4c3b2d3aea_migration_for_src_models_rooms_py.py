"""migration for src/models/rooms.py

Revision ID: 9f4c3b2d3aea
Revises: 051f86b8c20d
Create Date: 2024-09-24 20:33:47.446240

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "9f4c3b2d3aea"
down_revision: Union[str, None] = "051f86b8c20d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
