#!/usr/bin/env python3
"""
List all problems in the database
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.problem import Problem


def list_problems():
    """List all problems in the database"""
    db = SessionLocal()

    try:
        problems = db.query(Problem).all()

        print(f"\n📊 Total Problems: {len(problems)}\n")
        print("=" * 80)

        for i, problem in enumerate(problems, 1):
            print(f"\n{i}. {problem.title}")
            print(f"   Difficulty: {problem.difficulty}")
            print(f"   Tags: {problem.tags if problem.tags else 'None'}")
            print(f"   Description Length: {len(problem.statement)} characters")
            print(f"   First 100 chars: {problem.statement[:100]}...")
            print("-" * 80)

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("🔍 Listing all problems in database...")
    list_problems()
