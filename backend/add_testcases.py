"""
Script to add sample testcases to existing problems
Run this once to populate testcases for testing
"""

from app.db.database import SessionLocal
from app.models.problem import Problem
from app.models.testcase import Testcase


def add_testcases():
    db = SessionLocal()

    try:
        # Get all problems
        problems = db.query(Problem).all()

        if not problems:
            print("❌ No problems found. Please add problems first.")
            return

        for problem in problems:
            # Check if testcases already exist
            existing = (
                db.query(Testcase).filter(Testcase.problem_id == problem.id).first()
            )
            if existing:
                print(
                    f"⏭️  Problem '{problem.title}' already has testcases, skipping..."
                )
                continue

            print(f"➕ Adding testcases for: {problem.title}")

            # Add sample testcases based on problem type
            if "sum" in problem.title.lower() or "add" in problem.title.lower():
                # Two Sum / Add Numbers problem
                testcases_data = [
                    {
                        "stdin": "5 3",
                        "expected_output": "8",
                        "is_sample": True,
                        "weight": 10,
                        "description": "Sample 1: Basic addition",
                    },
                    {
                        "stdin": "10 20",
                        "expected_output": "30",
                        "is_sample": True,
                        "weight": 10,
                        "description": "Sample 2: Larger numbers",
                    },
                    {
                        "stdin": "0 0",
                        "expected_output": "0",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: Edge case - zeros",
                    },
                    {
                        "stdin": "-5 5",
                        "expected_output": "0",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: Negative numbers",
                    },
                    {
                        "stdin": "100 200",
                        "expected_output": "300",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: Large numbers",
                    },
                    {
                        "stdin": "-10 -20",
                        "expected_output": "-30",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: Both negative",
                    },
                ]

            elif "hello" in problem.title.lower():
                # Hello World problem
                testcases_data = [
                    {
                        "stdin": "",
                        "expected_output": "Hello, World!",
                        "is_sample": True,
                        "weight": 100,
                        "description": "Sample 1: Print Hello World",
                    },
                ]

            elif "factorial" in problem.title.lower():
                # Factorial problem
                testcases_data = [
                    {
                        "stdin": "5",
                        "expected_output": "120",
                        "is_sample": True,
                        "weight": 15,
                        "description": "Sample 1: Factorial of 5",
                    },
                    {
                        "stdin": "3",
                        "expected_output": "6",
                        "is_sample": True,
                        "weight": 15,
                        "description": "Sample 2: Factorial of 3",
                    },
                    {
                        "stdin": "0",
                        "expected_output": "1",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: Edge case - zero",
                    },
                    {
                        "stdin": "1",
                        "expected_output": "1",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: Edge case - one",
                    },
                    {
                        "stdin": "10",
                        "expected_output": "3628800",
                        "is_sample": False,
                        "weight": 30,
                        "description": "Hidden: Larger number",
                    },
                ]

            elif "fibonacci" in problem.title.lower():
                # Fibonacci problem
                testcases_data = [
                    {
                        "stdin": "5",
                        "expected_output": "5",
                        "is_sample": True,
                        "weight": 15,
                        "description": "Sample 1: 5th Fibonacci",
                    },
                    {
                        "stdin": "10",
                        "expected_output": "55",
                        "is_sample": True,
                        "weight": 15,
                        "description": "Sample 2: 10th Fibonacci",
                    },
                    {
                        "stdin": "1",
                        "expected_output": "1",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: First Fibonacci",
                    },
                    {
                        "stdin": "2",
                        "expected_output": "1",
                        "is_sample": False,
                        "weight": 20,
                        "description": "Hidden: Second Fibonacci",
                    },
                    {
                        "stdin": "15",
                        "expected_output": "610",
                        "is_sample": False,
                        "weight": 30,
                        "description": "Hidden: 15th Fibonacci",
                    },
                ]

            else:
                # Generic problem - assume it takes two numbers and adds them
                testcases_data = [
                    {
                        "stdin": "5 3",
                        "expected_output": "8",
                        "is_sample": True,
                        "weight": 20,
                        "description": "Sample 1",
                    },
                    {
                        "stdin": "10 20",
                        "expected_output": "30",
                        "is_sample": True,
                        "weight": 20,
                        "description": "Sample 2",
                    },
                    {
                        "stdin": "0 0",
                        "expected_output": "0",
                        "is_sample": False,
                        "weight": 30,
                        "description": "Hidden testcase 1",
                    },
                    {
                        "stdin": "100 100",
                        "expected_output": "200",
                        "is_sample": False,
                        "weight": 30,
                        "description": "Hidden testcase 2",
                    },
                ]

            # Create testcases
            for tc_data in testcases_data:
                testcase = Testcase(
                    problem_id=problem.id,
                    stdin=tc_data["stdin"],
                    expected_output=tc_data["expected_output"],
                    is_sample=tc_data["is_sample"],
                    description=tc_data["description"],
                    time_limit=2000,  # 2 seconds
                    memory_limit=256,  # 256 MB
                    weight=tc_data["weight"],
                )
                db.add(testcase)

            db.commit()
            print(f"✅ Added {len(testcases_data)} testcases for '{problem.title}'")

        print("\n🎉 All testcases added successfully!")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Adding testcases to problems...\n")
    add_testcases()
