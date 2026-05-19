"""
Quick fix for database schema drift
Adds missing columns to existing tables
"""

from sqlalchemy import text
from app.db.database import engine


def fix_schema():
    """Add missing columns to database tables"""

    sql_commands = [
        # Fix submissions table
        """
        ALTER TABLE submissions 
        ADD COLUMN IF NOT EXISTS execution_time INTEGER,
        ADD COLUMN IF NOT EXISTS memory_used FLOAT;
        """,
        # Fix users table
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW(),
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();
        """,
        # Fix problems table
        """
        ALTER TABLE problems 
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW(),
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();
        """,
        # Fix testcases table
        """
        ALTER TABLE testcases 
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW(),
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW();
        """,
        # Fix testcase_results table
        """
        ALTER TABLE testcase_results 
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();
        """,
        # Fix ai_feedback table
        """
        ALTER TABLE ai_feedback 
        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();
        """,
    ]

    try:
        with engine.connect() as conn:
            print("🔧 Fixing database schema...\n")

            for i, sql in enumerate(sql_commands, 1):
                try:
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"✅ Step {i}/{len(sql_commands)} completed")
                except Exception as e:
                    print(f"⚠️  Step {i}/{len(sql_commands)} - {str(e)}")

            print("\n🎉 Database schema fixed successfully!")
            print("\n📋 Verifying submissions table columns:")

            # Verify submissions table
            result = conn.execute(
                text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'submissions' 
                ORDER BY ordinal_position;
            """)
            )

            for row in result:
                print(f"   - {row[0]}: {row[1]}")

            print("\n✅ All done! Restart your backend with: python run.py")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check your DATABASE_URL in .env file")
        print("3. Verify database credentials")


if __name__ == "__main__":
    fix_schema()
