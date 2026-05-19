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

    # Check and create enum type only if it doesn't exist
    connection = op.get_bind()
    result = connection.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'message_type'")
    )
    if not result.fetchone():
        connection.execute(
            sa.text("CREATE TYPE message_type AS ENUM ('chat', 'system', 'code_run')")
        )
        connection.commit()

    # Create room_messages table using raw SQL
    connection.execute(
        sa.text("""
        CREATE TABLE IF NOT EXISTS room_messages (
            id SERIAL PRIMARY KEY,
            room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
            message_type message_type NOT NULL DEFAULT 'chat',
            content TEXT NOT NULL,
            message_data JSON DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        )
    """)
    )
    connection.commit()

    # Create indexes
    connection.execute(
        sa.text("CREATE INDEX IF NOT EXISTS ix_room_messages_id ON room_messages(id)")
    )
    connection.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS ix_room_messages_room_id ON room_messages(room_id)"
        )
    )
    connection.commit()


def downgrade():
    """Drop room_messages table"""
    connection = op.get_bind()
    connection.execute(sa.text("DROP TABLE IF EXISTS room_messages CASCADE"))
    connection.execute(sa.text("DROP TYPE IF EXISTS message_type"))
    connection.commit()
