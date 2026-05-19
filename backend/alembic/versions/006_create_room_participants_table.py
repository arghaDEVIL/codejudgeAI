"""Create room_participants table

Revision ID: 006
Revises: 005
Create Date: 2026-04-21 03:01:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade():
    """Create room_participants table"""

    # Create enum type if it doesn't exist
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE participant_role AS ENUM ('host', 'interviewer', 'candidate', 'viewer');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create room_participants table
    op.create_table(
        "room_participants",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "role",
            sa.Enum(
                "host", "interviewer", "candidate", "viewer", name="participant_role"
            ),
            nullable=False,
            server_default="viewer",
        ),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("cursor_color", sa.String(length=7), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "joined_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("left_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index(
        op.f("ix_room_participants_id"), "room_participants", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_room_participants_room_id"),
        "room_participants",
        ["room_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_room_participants_user_id"),
        "room_participants",
        ["user_id"],
        unique=False,
    )


def downgrade():
    """Drop room_participants table"""
    op.drop_index(op.f("ix_room_participants_user_id"), table_name="room_participants")
    op.drop_index(op.f("ix_room_participants_room_id"), table_name="room_participants")
    op.drop_index(op.f("ix_room_participants_id"), table_name="room_participants")
    op.drop_table("room_participants")

    # Drop enum type
    op.execute("DROP TYPE participant_role;")
