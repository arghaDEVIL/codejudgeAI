"""
Script to update the Print Hello problem with proper description
"""

from app.db.database import SessionLocal
from app.models.problem import Problem


def update_print_hello():
    db = SessionLocal()

    try:
        # Find Print Hello problem
        problem = db.query(Problem).filter(Problem.title == "Print Hello").first()

        if not problem:
            print("❌ Print Hello problem not found!")
            return

        # Update with proper statement
        problem.statement = """Write a program that prints "Hello" to the console.

This is a simple introductory problem to test your setup.

Input: None
Output: Print the word "Hello" (without quotes)

Example:
Output: Hello

Note: Make sure to print exactly "Hello" with no extra spaces or characters."""

        problem.difficulty = "Easy"

        db.commit()
        print("✅ Print Hello problem updated successfully!")
        print(f"\nTitle: {problem.title}")
        print(f"Difficulty: {problem.difficulty}")
        print(f"Statement:\n{problem.statement}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Updating Print Hello problem...\n")
    update_print_hello()
