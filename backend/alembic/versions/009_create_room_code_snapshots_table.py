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

    # Check and create enum type only if it doesn't exist
    connection = op.get_bind()
    result = connection.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'snapshot_type'")
    )
    if not result.fetchone():
        connection.execute(
            sa.text(
                "CREATE TYPE snapshot_type AS ENUM ('auto', 'manual', 'submission')"
            )
        )
        connection.commit()

    # Create room_code_snapshots table using raw SQL
    connection.execute(
        sa.text("""
        CREATE TABLE IF NOT EXISTS room_code_snapshots (
            id SERIAL PRIMARY KEY,
            room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
            code TEXT NOT NULL,
            language VARCHAR(20) NOT NULL,
            snapshot_type snapshot_type NOT NULL DEFAULT 'auto',
            created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        )
    """)
    )
    connection.commit()

    # Create indexes
    connection.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS ix_room_code_snapshots_id ON room_code_snapshots(id)"
        )
    )
    connection.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS ix_room_code_snapshots_room_id ON room_code_snapshots(room_id)"
        )
    )
    connection.commit()


def downgrade():
    """Drop room_code_snapshots table"""
    connection = op.get_bind()
    connection.execute(sa.text("DROP TABLE IF EXISTS room_code_snapshots CASCADE"))
    connection.execute(sa.text("DROP TYPE IF EXISTS snapshot_type"))
    connection.commit()
