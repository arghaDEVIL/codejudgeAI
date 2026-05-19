"""
Script to add sample problems for testing the hidden testcase system
"""

from app.db.database import SessionLocal
from app.models.problem import Problem


def add_sample_problems():
    db = SessionLocal()

    try:
        # Check if problems already exist
        existing_count = db.query(Problem).count()

        if existing_count > 1:
            print(f"⏭️  Already have {existing_count} problems. Skipping...")
            return

        problems_data = [
            {
                "title": "Two Sum",
                "statement": "Write a program that reads two integers from input and prints their sum.\n\nInput: Two space-separated integers\nOutput: Their sum",
                "difficulty": "Easy",
                "expected_output": "Sample output based on input",
            },
            {
                "title": "Factorial",
                "statement": "Write a program that calculates the factorial of a given number.\n\nInput: A single integer n (0 ≤ n ≤ 10)\nOutput: The factorial of n",
                "difficulty": "Easy",
                "expected_output": "Factorial of the input number",
            },
            {
                "title": "Fibonacci Number",
                "statement": "Write a program that finds the nth Fibonacci number.\n\nInput: A single integer n (1 ≤ n ≤ 20)\nOutput: The nth Fibonacci number",
                "difficulty": "Medium",
                "expected_output": "The nth Fibonacci number",
            },
        ]

        for prob_data in problems_data:
            # Check if problem already exists
            existing = (
                db.query(Problem).filter(Problem.title == prob_data["title"]).first()
            )
            if existing:
                print(f"⏭️  Problem '{prob_data['title']}' already exists, skipping...")
                continue

            problem = Problem(
                title=prob_data["title"],
                statement=prob_data["statement"],
                difficulty=prob_data["difficulty"],
                expected_output=prob_data["expected_output"],
            )
            db.add(problem)
            print(f"✅ Added problem: {prob_data['title']}")

        db.commit()
        print("\n🎉 Sample problems added successfully!")
        print("\nNow run: python update_testcases.py")
        print("This will add multiple testcases (sample + hidden) to each problem.")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Adding sample problems...\n")
    add_sample_problems()
