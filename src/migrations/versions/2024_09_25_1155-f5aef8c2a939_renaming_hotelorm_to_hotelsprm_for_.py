"""renaming HotelOrm to HotelsPrm for hotels.py

Revision ID: f5aef8c2a939
Revises: b52399b60552
Create Date: 2024-09-25 11:55:10.674098

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "f5aef8c2a939"
down_revision: Union[str, None] = "b52399b60552"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
