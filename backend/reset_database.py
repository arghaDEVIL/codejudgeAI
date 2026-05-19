"""
Database reset script for Render deployment
Run this from Render shell if migrations are stuck
"""

import os
from sqlalchemy import create_engine, text

# Get database URL from environment
database_url = os.getenv("DATABASE_URL", "")

# Convert postgres:// to postgresql:// for SQLAlchemy 1.4+
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

print(f"Connecting to database...")
engine = create_engine(database_url)

with engine.connect() as conn:
    print("Dropping all ENUM types...")

    # Drop all custom ENUM types
    enum_types = [
        "room_mode",
        "room_status",
        "participant_role",
        "message_type",
        "snapshot_type",
    ]

    for enum_type in enum_types:
        try:
            conn.execute(text(f"DROP TYPE IF EXISTS {enum_type} CASCADE"))
            conn.commit()
            print(f"  ✓ Dropped {enum_type}")
        except Exception as e:
            print(f"  ✗ Error dropping {enum_type}: {e}")

    print("\nDropping all tables...")

    # Drop all tables in correct order (respecting foreign keys)
    tables = [
        "alembic_version",
        "room_code_snapshots",
        "room_messages",
        "room_sessions",
        "room_participants",
        "rooms",
        "ai_feedback",
        "testcase_results",
        "testcases",
        "submissions",
        "problems",
        "users",
    ]

    for table in tables:
        try:
            conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
            conn.commit()
            print(f"  ✓ Dropped {table}")
        except Exception as e:
            print(f"  ✗ Error dropping {table}: {e}")

    print("\n✅ Database reset complete!")
    print("Now run: alembic upgrade head")

print("\nDone!")
