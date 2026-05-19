"""Create rooms table

Revision ID: 005
Revises: 004
Create Date: 2026-04-21 03:00:00.000000

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = "005"
down_revision = "001"
branch_labels = None
depends_on = None


def upgrade():
    """Create rooms table"""

    # Create enum types
    op.execute("""
        CREATE TYPE room_mode AS ENUM ('collaborative', 'interview', 'practice');
        CREATE TYPE room_status AS ENUM ('active', 'ended', 'archived');
    """)

    # Create rooms table
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_code", sa.String(length=8), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("host_user_id", sa.Integer(), nullable=False),
        sa.Column("problem_id", sa.Integer(), nullable=True),
        sa.Column(
            "mode",
            sa.Enum("collaborative", "interview", "practice", name="room_mode"),
            nullable=False,
            server_default="collaborative",
        ),
        sa.Column(
            "status",
            sa.Enum("active", "ended", "archived", name="room_status"),
            nullable=False,
            server_default="active",
        ),
        sa.Column(
            "max_participants", sa.Integer(), nullable=False, server_default="10"
        ),
        sa.Column("settings", JSON, nullable=False, server_default="{}"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ended_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["host_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["problem_id"], ["problems.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index(op.f("ix_rooms_id"), "rooms", ["id"], unique=False)
    op.create_index(op.f("ix_rooms_room_code"), "rooms", ["room_code"], unique=True)
    op.create_index(
        op.f("ix_rooms_host_user_id"), "rooms", ["host_user_id"], unique=False
    )
    op.create_index(op.f("ix_rooms_problem_id"), "rooms", ["problem_id"], unique=False)


def downgrade():
    """Drop rooms table"""
    op.drop_index(op.f("ix_rooms_problem_id"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_host_user_id"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_room_code"), table_name="rooms")
    op.drop_index(op.f("ix_rooms_id"), table_name="rooms")
    op.drop_table("rooms")

    # Drop enum types
    op.execute("DROP TYPE room_mode;")
    op.execute("DROP TYPE room_status;")
