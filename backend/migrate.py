"""
Database migration helper script
Run migrations easily without alembic commands
"""

import subprocess
import sys


def run_migrations():
    """Run all pending migrations"""
    print("🔄 Running database migrations...")
    result = subprocess.run(
        ["alembic", "upgrade", "head"], capture_output=True, text=True
    )

    if result.returncode == 0:
        print("✅ Migrations completed successfully!")
        print(result.stdout)
    else:
        print("❌ Migration failed!")
        print(result.stderr)
        sys.exit(1)


def create_migration(message: str):
    """Create a new migration"""
    print(f"📝 Creating migration: {message}")
    result = subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        print("✅ Migration created!")
        print(result.stdout)
    else:
        print("❌ Failed to create migration!")
        print(result.stderr)
        sys.exit(1)


def show_current():
    """Show current migration version"""
    result = subprocess.run(["alembic", "current"], capture_output=True, text=True)
    print("📍 Current migration:")
    print(result.stdout)


def show_history():
    """Show migration history"""
    result = subprocess.run(["alembic", "history"], capture_output=True, text=True)
    print("📜 Migration history:")
    print(result.stdout)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python migrate.py upgrade    - Run migrations")
        print("  python migrate.py create 'message' - Create new migration")
        print("  python migrate.py current    - Show current version")
        print("  python migrate.py history    - Show history")
        sys.exit(1)

    command = sys.argv[1]

    if command == "upgrade":
        run_migrations()
    elif command == "create" and len(sys.argv) > 2:
        create_migration(sys.argv[2])
    elif command == "current":
        show_current()
    elif command == "history":
        show_history()
    else:
        print("❌ Invalid command!")
        sys.exit(1)
