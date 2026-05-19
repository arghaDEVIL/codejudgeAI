"""Create room_sessions table

Revision ID: 007
Revises: 006
Create Date: 2026-04-21 03:02:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade():
    """Create room_sessions table"""
    op.create_table(
        "room_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False, server_default=""),
        sa.Column(
            "language", sa.String(length=20), nullable=False, server_default="python"
        ),
        sa.Column("version", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_edited_by", sa.Integer(), nullable=True),
        sa.Column("last_edited_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["last_edited_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("room_id"),
    )

    # Create indexes
    op.create_index(op.f("ix_room_sessions_id"), "room_sessions", ["id"], unique=False)
    op.create_index(
        op.f("ix_room_sessions_room_id"), "room_sessions", ["room_id"], unique=True
    )


def downgrade():
    """Drop room_sessions table"""
    op.drop_index(op.f("ix_room_sessions_room_id"), table_name="room_sessions")
    op.drop_index(op.f("ix_room_sessions_id"), table_name="room_sessions")
    op.drop_table("room_sessions")
