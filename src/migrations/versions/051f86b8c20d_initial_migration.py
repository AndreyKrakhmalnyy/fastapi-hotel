"""initial migration

Revision ID: 051f86b8c20d
Revises: 
Create Date: 2024-09-24 19:51:17.225981

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "051f86b8c20d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:  
    op.drop_table("hotels")
