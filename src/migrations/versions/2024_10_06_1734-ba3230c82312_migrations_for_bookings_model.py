"""migrations for bookings model

Revision ID: ba3230c82312
Revises: 5fc9e3858228
Create Date: 2024-10-06 17:34:47.055067

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "ba3230c82312"
down_revision: Union[str, None] = "5fc9e3858228"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
