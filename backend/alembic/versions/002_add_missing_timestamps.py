"""Add missing timestamp columns to existing tables

Revision ID: 002
Revises: 001
Create Date: 2024-01-01 00:00:01.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "002"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add created_at and updated_at to users if missing
    try:
        op.add_column(
            "users",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
        )
    except Exception:
        pass  # Column already exists

    try:
        op.add_column(
            "users", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True)
        )
    except Exception:
        pass

    # Add created_at and updated_at to problems if missing
    try:
        op.add_column(
            "problems",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
        )
    except Exception:
        pass

    try:
        op.add_column(
            "problems",
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        )
    except Exception:
        pass

    # Add created_at to submissions if missing
    try:
        op.add_column(
            "submissions",
            sa.Column(
                "created_at",
                sa.DateTime(timezone=True),
                server_default=sa.text("now()"),
                nullable=True,
            ),
        )
    except Exception:
        pass

    # Add execution_time and memory_used to submissions if missing
    try:
        op.add_column(
            "submissions", sa.Column("execution_time", sa.Integer(), nullable=True)
        )
    except Exception:
        pass

    try:
        op.add_column(
            "submissions", sa.Column("memory_used", sa.Float(), nullable=True)
        )
    except Exception:
        pass


def downgrade() -> None:
    # Remove added columns
    op.drop_column("submissions", "memory_used")
    op.drop_column("submissions", "execution_time")
    op.drop_column("submissions", "created_at")
    op.drop_column("problems", "updated_at")
    op.drop_column("problems", "created_at")
    op.drop_column("users", "updated_at")
    op.drop_column("users", "created_at")
