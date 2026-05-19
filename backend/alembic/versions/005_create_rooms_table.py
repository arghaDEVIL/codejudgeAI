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

    # Check and create enum types only if they don't exist
    connection = op.get_bind()

    # Check if room_mode exists
    result = connection.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'room_mode'")
    )
    if not result.fetchone():
        connection.execute(
            sa.text(
                "CREATE TYPE room_mode AS ENUM ('collaborative', 'interview', 'practice')"
            )
        )
        connection.commit()

    # Check if room_status exists
    result = connection.execute(
        sa.text("SELECT 1 FROM pg_type WHERE typname = 'room_status'")
    )
    if not result.fetchone():
        connection.execute(
            sa.text("CREATE TYPE room_status AS ENUM ('active', 'ended', 'archived')")
        )
        connection.commit()

    # Create rooms table using raw SQL to avoid SQLAlchemy's automatic ENUM creation
    connection.execute(
        sa.text("""
        CREATE TABLE IF NOT EXISTS rooms (
            id SERIAL PRIMARY KEY,
            room_code VARCHAR(8) NOT NULL UNIQUE,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            host_user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            problem_id INTEGER REFERENCES problems(id) ON DELETE SET NULL,
            mode room_mode NOT NULL DEFAULT 'collaborative',
            status room_status NOT NULL DEFAULT 'active',
            max_participants INTEGER NOT NULL DEFAULT 10,
            settings JSON NOT NULL DEFAULT '{}',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
            updated_at TIMESTAMP WITH TIME ZONE,
            ended_at TIMESTAMP WITH TIME ZONE
        )
    """)
    )
    connection.commit()

    # Create indexes
    connection.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_rooms_id ON rooms(id)"))
    connection.execute(
        sa.text("CREATE INDEX IF NOT EXISTS ix_rooms_room_code ON rooms(room_code)")
    )
    connection.execute(
        sa.text(
            "CREATE INDEX IF NOT EXISTS ix_rooms_host_user_id ON rooms(host_user_id)"
        )
    )
    connection.execute(
        sa.text("CREATE INDEX IF NOT EXISTS ix_rooms_problem_id ON rooms(problem_id)")
    )
    connection.commit()


def downgrade():
    """Drop rooms table"""
    connection = op.get_bind()
    connection.execute(sa.text("DROP TABLE IF EXISTS rooms CASCADE"))
    connection.execute(sa.text("DROP TYPE IF EXISTS room_mode"))
    connection.execute(sa.text("DROP TYPE IF EXISTS room_status"))
    connection.commit()
