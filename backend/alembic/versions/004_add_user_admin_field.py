"""Add admin field to users

Revision ID: 004
Revises: 003
Create Date: 2026-04-15 22:05:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade():
    """Add admin field to users table"""
    # Add is_admin column (default False)
    op.add_column(
        "users", sa.Column("is_admin", sa.Boolean, default=False, nullable=False)
    )


def downgrade():
    """Remove admin field from users table"""
    op.drop_column("users", "is_admin")
