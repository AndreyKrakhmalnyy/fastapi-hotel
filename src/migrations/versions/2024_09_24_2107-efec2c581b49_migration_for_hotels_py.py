"""migration for hotels.py

Revision ID: efec2c581b49
Revises: 051f86b8c20d
Create Date: 2024-09-24 21:07:44.342825

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "efec2c581b49"
down_revision: Union[str, None] = "051f86b8c20d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
