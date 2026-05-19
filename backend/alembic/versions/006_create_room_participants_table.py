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

    # Check and create enum type only if it doesn't exist
    connection = op.get_bind()
    result = connection.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'participant_role'")
    )
    if not result.fetchone():
        connection.execute(
            sa.text(
                "CREATE TYPE participant_role AS ENUM ('host', 'interviewer', 'candidate', 'viewer')"
            )
        )
        connection.commit()

    # Create room_participants table using raw SQL
    connection.execute(
        sa.text("""
        CREATE TABLE IF NOT EXISTS room_participants (
            id SERIAL PRIMARY KEY,
            room_id INTEGER NOT NULL REFERENCES rooms(id) ON DELETE CASCADE,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role participant_role NOT NULL DEFAULT 'viewer',
            display_name VARCHAR(100) NOT NULL,
            cursor_color VARCHAR(7) NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT true,
            joined_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            left_at TIMESTAMP WITH TIME ZONE
        )
    """)
    )
    connection.commit()

    # Create indexes
    connection.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS ix_room_participants_id ON room_participants(id)"
        )
    )
    connection.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS ix_room_participants_room_id ON room_participants(room_id)"
        )
    )
    connection.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS ix_room_participants_user_id ON room_participants(user_id)"
        )
    )
    connection.commit()


def downgrade():
    """Drop room_participants table"""
    connection = op.get_bind()
    connection.execute(sa.text("DROP TABLE IF EXISTS room_participants CASCADE"))
    connection.execute(sa.text("DROP TYPE IF EXISTS participant_role"))
    connection.commit()
