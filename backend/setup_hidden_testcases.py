"""
Quick setup script for Hidden Testcase System
Adds database columns and populates testcases
"""

import subprocess
import sys


def run_sql_script():
    """Run SQL script to add columns"""
    print("\n📝 Running SQL script to add columns...")
    print("\nPlease run this SQL in pgAdmin or psql:")
    print("=" * 60)
    with open("add_hidden_testcase_columns.sql", "r") as f:
        print(f.read())
    print("=" * 60)


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║     Hidden Testcase System - Quick Setup Script         ║
╚══════════════════════════════════════════════════════════╝
    """)

    print("\n📋 Step 1: Add database columns")
    print("\nRun this SQL in pgAdmin:")
    print("-" * 60)
    print(
        "ALTER TABLE submissions ADD COLUMN IF NOT EXISTS score FLOAT DEFAULT 0.0 NOT NULL;"
    )
    print(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE NOT NULL;"
    )
    print("-" * 60)

    response = input("\n✋ Have you added the columns? (yes/no): ").strip().lower()
    if response != "yes":
        print("\n❌ Setup cancelled. Please add the columns and run this script again.")
        print("\n📄 You can also run the SQL file: add_hidden_testcase_columns.sql")
        sys.exit(1)

    # Step 2: Populate testcases
    print("\n📋 Step 2: Populating testcases with weights...")
    try:
        result = subprocess.run(
            "python add_testcases.py",
            shell=True,
            check=True,
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        print("✅ Testcases populated successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Testcase population failed: {e.stderr}")
        print("\nYou can run 'python add_testcases.py' manually later.")

    # Success message
    print(f"\n{'=' * 60}")
    print("🎉 Setup Complete!")
    print(f"{'=' * 60}")
    print("""
✅ Database schema updated
✅ Testcases populated with weighted scoring

Next Steps:
1. Create an admin user (optional):
   UPDATE users SET is_admin = true WHERE email = 'your@email.com';

2. Start the backend server:
   python run.py

3. Test the system:
   - Login and submit code
   - Check scores in submission results
   - View submission history with scores

📖 For more details, see: HIDDEN_TESTCASE_SYSTEM.md
    """)


if __name__ == "__main__":
    main()
