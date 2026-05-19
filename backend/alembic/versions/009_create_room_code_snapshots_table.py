"""Create room_code_snapshots table

Revision ID: 009
Revises: 008
Create Date: 2026-04-21 03:04:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade():
    """Create room_code_snapshots table"""

    # Create enum type if it doesn't exist
    op.execute("""
        DO $$ BEGIN
            CREATE TYPE snapshot_type AS ENUM ('auto', 'manual', 'submission');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
    """)

    # Create room_code_snapshots table
    op.create_table(
        "room_code_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=20), nullable=False),
        sa.Column(
            "snapshot_type",
            sa.Enum("auto", "manual", "submission", name="snapshot_type"),
            nullable=False,
            server_default="auto",
        ),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # Create indexes
    op.create_index(
        op.f("ix_room_code_snapshots_id"), "room_code_snapshots", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_room_code_snapshots_room_id"),
        "room_code_snapshots",
        ["room_id"],
        unique=False,
    )


def downgrade():
    """Drop room_code_snapshots table"""
    op.drop_index(
        op.f("ix_room_code_snapshots_room_id"), table_name="room_code_snapshots"
    )
    op.drop_index(op.f("ix_room_code_snapshots_id"), table_name="room_code_snapshots")
    op.drop_table("room_code_snapshots")

    # Drop enum type
    op.execute("DROP TYPE snapshot_type;")
