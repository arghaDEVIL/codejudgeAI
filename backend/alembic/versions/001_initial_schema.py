"""Initial schema with timestamps

Revision ID: 001
Revises:
Create Date: 2024-01-01 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add missing timestamp columns safely

    tables = [
        "users",
        "problems",
        "submissions",
        "testcases",
        "testcase_results",
        "ai_feedback",
    ]

    for table in tables:
        op.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """)

        op.execute(f"""
        ALTER TABLE {table}
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
        """)


def downgrade() -> None:
    # Optional rollback (safe)
    tables = [
        "users",
        "problems",
        "submissions",
        "testcases",
        "testcase_results",
        "ai_feedback",
    ]

    for table in tables:
        op.execute(f"""
        ALTER TABLE {table}
        DROP COLUMN IF EXISTS created_at;
        """)

        op.execute(f"""
        ALTER TABLE {table}
        DROP COLUMN IF EXISTS updated_at;
        """)