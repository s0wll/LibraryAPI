"""add user roles

Revision ID: 81565c3be76d
Revises: b997c4960a54
Create Date: 2025-03-11 14:26:05.860648

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "81565c3be76d"
down_revision: Union[str, None] = "b997c4960a54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("users", sa.Column("is_admin", sa.Boolean(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "is_admin")
