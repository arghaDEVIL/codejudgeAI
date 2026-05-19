"""
Test database connection for Render deployment
"""

import os
import sys
from sqlalchemy import create_engine, text

print("=" * 60)
print("DATABASE CONNECTION TEST")
print("=" * 60)

# Get database URL
database_url = os.getenv("DATABASE_URL", "")
print(f"\n1. Original DATABASE_URL: {database_url[:30]}...")

# Convert postgres:// to postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
    print(f"2. Converted to: {database_url[:30]}...")
else:
    print(f"2. No conversion needed")

try:
    print("\n3. Creating engine...")
    engine = create_engine(database_url, echo=True)

    print("\n4. Testing connection...")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version()"))
        version = result.fetchone()[0]
        print(f"\n✅ Connection successful!")
        print(f"PostgreSQL version: {version}")

        # Check existing tables
        print("\n5. Checking existing tables...")
        result = conn.execute(
            text("""
            SELECT tablename FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        )
        tables = [row[0] for row in result.fetchall()]
        if tables:
            print(f"Found {len(tables)} tables:")
            for table in tables:
                print(f"  - {table}")
        else:
            print("No tables found (fresh database)")

        # Check existing ENUM types
        print("\n6. Checking existing ENUM types...")
        result = conn.execute(
            text("""
            SELECT typname FROM pg_type 
            WHERE typtype = 'e'
            ORDER BY typname
        """)
        )
        enums = [row[0] for row in result.fetchall()]
        if enums:
            print(f"Found {len(enums)} ENUM types:")
            for enum in enums:
                print(f"  - {enum}")
        else:
            print("No ENUM types found")

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED")
        print("=" * 60)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print(f"\nFull error details:")
    import traceback

    traceback.print_exc()
    sys.exit(1)
