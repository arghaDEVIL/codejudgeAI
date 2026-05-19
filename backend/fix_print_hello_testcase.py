"""
Script to fix the Print Hello test case to match the problem description
"""

from app.db.database import SessionLocal
from app.models.problem import Problem
from app.models.testcase import Testcase


def fix_print_hello_testcase():
    db = SessionLocal()

    try:
        # Find Print Hello problem
        problem = db.query(Problem).filter(Problem.title == "Print Hello").first()

        if not problem:
            print("❌ Print Hello problem not found!")
            return

        # Find its test case
        testcase = db.query(Testcase).filter(Testcase.problem_id == problem.id).first()

        if not testcase:
            print("❌ No test case found for Print Hello!")
            return

        print(f"Current test case:")
        print(f"  Input: '{testcase.stdin}'")
        print(f"  Expected: '{testcase.expected_output}'")
        print()

        # Update test case to match problem description
        testcase.stdin = ""  # No input needed
        testcase.expected_output = "Hello"  # Just "Hello", not "Hello, World!"
        testcase.is_sample = True  # Make it a sample test

        db.commit()

        print("✅ Test case updated successfully!")
        print(f"\nNew test case:")
        print(f"  Input: '{testcase.stdin}'")
        print(f"  Expected: '{testcase.expected_output}'")
        print(f"  Is Sample: {testcase.is_sample}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Fixing Print Hello test case...\n")
    fix_print_hello_testcase()
