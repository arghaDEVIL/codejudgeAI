"""Create room_messages table

Revision ID: 008
Revises: 007
Create Date: 2026-04-21 03:03:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None


def upgrade():
    """Create room_messages table"""

    # Create enum type
    op.execute("""
        CREATE TYPE message_type AS ENUM ('chat', 'system', 'code_run');
    """)

    # Create room_messages table
    op.create_table(
        "room_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column(
            "message_type",
            sa.Enum("chat", "system", "code_run", name="message_type"),
            nullable=False,
            server_default="chat",
        ),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("message_data", JSON, nullable=True, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index(op.f("ix_room_messages_id"), "room_messages", ["id"], unique=False)
    op.create_index(
        op.f("ix_room_messages_room_id"), "room_messages", ["room_id"], unique=False
    )


def downgrade():
    """Drop room_messages table"""
    op.drop_index(op.f("ix_room_messages_room_id"), table_name="room_messages")
    op.drop_index(op.f("ix_room_messages_id"), table_name="room_messages")
    op.drop_table("room_messages")

    # Drop enum type
    op.execute("DROP TYPE message_type;")
