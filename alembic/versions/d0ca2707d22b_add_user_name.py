"""add user name

Revision ID: d0ca2707d22b
Revises: 4f77524d45ad
Create Date: 2026-03-07 08:07:13.501306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0ca2707d22b'
down_revision: Union[str, Sequence[str], None] = '4f77524d45ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
