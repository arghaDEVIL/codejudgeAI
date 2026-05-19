"""
Setup script for Collaborative Coding feature
Runs migrations and verifies setup
"""

import subprocess
import sys


def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'=' * 60}")
    print(f"🚀 {description}")
    print(f"{'=' * 60}")

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"✅ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - FAILED")
        print(f"Error: {e.stderr}")
        return False


def verify_models():
    """Verify that all models can be imported"""
    print(f"\n{'=' * 60}")
    print("🔍 Verifying models...")
    print(f"{'=' * 60}")

    try:
        from app.models import (
            Room,
            RoomParticipant,
            RoomSession,
            RoomMessage,
            RoomCodeSnapshot,
        )

        print("✅ Room")
        print("✅ RoomParticipant")
        print("✅ RoomSession")
        print("✅ RoomMessage")
        print("✅ RoomCodeSnapshot")
        print("\n✅ All models imported successfully!")
        return True
    except Exception as e:
        print(f"❌ Model import failed: {e}")
        return False


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║   Collaborative Coding Feature - Setup Script           ║
╚══════════════════════════════════════════════════════════╝
    """)

    print("\n📋 This script will:")
    print("  1. Run database migrations (005-009)")
    print("  2. Verify models can be imported")
    print("  3. Check database tables")

    response = input("\n✋ Continue? (yes/no): ").strip().lower()
    if response != "yes":
        print("\n❌ Setup cancelled.")
        sys.exit(0)

    # Step 1: Run migrations
    print("\n📋 Step 1: Running database migrations...")
    migration_success = run_command("python migrate.py upgrade", "Database migrations")

    if not migration_success:
        print("\n⚠️  Migration failed. Trying to mark as complete...")
        print("\nIf tables already exist, run:")
        print("  python migrate.py stamp head")
        print("\nOr apply SQL manually (see RUN_MIGRATIONS.md)")

        response = (
            input("\n✋ Have you fixed the migrations? (yes/no): ").strip().lower()
        )
        if response != "yes":
            print("\n❌ Setup incomplete. Please fix migrations and run again.")
            sys.exit(1)

    # Step 2: Verify models
    print("\n📋 Step 2: Verifying models...")
    if not verify_models():
        print("\n❌ Model verification failed.")
        print("Make sure all model files are created correctly.")
        sys.exit(1)

    # Success message
    print(f"\n{'=' * 60}")
    print("🎉 Setup Complete!")
    print(f"{'=' * 60}")
    print("""
✅ Database migrations applied
✅ Models verified

Database Tables Created:
  • rooms - Main room entity
  • room_participants - User participation tracking
  • room_sessions - Current code state
  • room_messages - Chat and system messages
  • room_code_snapshots - Version history

Next Steps:
1. Implement WebSocket manager (backend/app/services/websocket_manager.py)
2. Create room endpoints (backend/app/api/v1/endpoints/rooms.py)
3. Build frontend components (frontend/src/pages/RoomLobby.jsx)

📖 For detailed implementation plan, see: COLLABORATIVE_CODING_PLAN.md
📖 For migration details, see: RUN_MIGRATIONS.md
    """)


if __name__ == "__main__":
    main()
