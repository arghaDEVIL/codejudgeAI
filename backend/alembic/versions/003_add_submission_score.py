"""Add score field to submissions

Revision ID: 003
Revises: 002
Create Date: 2026-04-15 22:00:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade():
    """Add score field to submissions table"""
    # Add score column (0-100 weighted score)
    op.add_column(
        "submissions", sa.Column("score", sa.Float, default=0.0, nullable=False)
    )


def downgrade():
    """Remove score field from submissions table"""
    op.drop_column("submissions", "score")
