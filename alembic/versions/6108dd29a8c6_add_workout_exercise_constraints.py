"""add workout exercise constraints

Revision ID: 6108dd29a8c6
Revises: 3d4bbb889c8f
Create Date: 2026-11-11 16:53:33.101920

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6108dd29a8c6'
down_revision: Union[str, Sequence[str], None] = '3d4bbb889c8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
