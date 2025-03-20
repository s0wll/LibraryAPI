"""add borrows and refactor users

Revision ID: 3cad4b33cb0f
Revises: 81565c3be76d
Create Date: 2025-03-11 20:02:16.771072

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "3cad4b33cb0f"
down_revision: Union[str, None] = "81565c3be76d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "borrows",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("book_id", sa.Integer(), nullable=False),
        sa.Column("date_from", sa.Date(), nullable=False),
        sa.Column("date_to", sa.Date(), nullable=False),
        sa.Column("is_returned", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["book_id"],
            ["books.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column("users", sa.Column("borrowed_books_count", sa.Integer(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "borrowed_books_count")
    op.drop_table("borrows")
