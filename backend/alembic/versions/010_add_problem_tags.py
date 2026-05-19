"""Add tags column to problems table

Revision ID: 010_add_problem_tags
Revises: 009_create_room_code_snapshots_table
Create Date: 2024-04-24 12:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "010"
down_revision = "009"
branch_labels = None
depends_on = None


def upgrade():
    # Add tags column to problems table
    op.add_column("problems", sa.Column("tags", sa.JSON(), nullable=True))

    # Add index on difficulty for better filtering performance
    op.create_index("ix_problems_difficulty", "problems", ["difficulty"])


def downgrade():
    # Remove index and column
    op.drop_index("ix_problems_difficulty", table_name="problems")
    op.drop_column("problems", "tags")
