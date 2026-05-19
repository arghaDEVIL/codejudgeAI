#!/usr/bin/env python3
"""
Script to add sample tags to existing problems for demonstration
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.problem import Problem

# Sample tags for different types of problems
SAMPLE_TAGS = {
    "Hello World": ["basics", "output"],
    "Print Hello": ["basics", "output"],
    "Add Two Numbers": ["math", "arithmetic", "basics"],
    "Sum of Two Numbers": ["math", "arithmetic", "basics"],
    "Maximum of Two Numbers": ["math", "conditionals", "basics"],
    "Factorial": ["math", "recursion", "loops"],
    "Fibonacci": ["math", "recursion", "dynamic-programming"],
    "Prime Number": ["math", "number-theory", "loops"],
    "Palindrome": ["strings", "algorithms"],
    "Reverse String": ["strings", "algorithms"],
    "Array Sum": ["arrays", "loops", "math"],
    "Binary Search": ["arrays", "search", "algorithms"],
    "Sorting": ["arrays", "sorting", "algorithms"],
    "Two Sum": ["arrays", "hash-table", "algorithms"],
    "Valid Parentheses": ["strings", "stack", "algorithms"],
    "Linked List": ["linked-list", "data-structures"],
    "Binary Tree": ["trees", "data-structures", "recursion"],
    "Graph Traversal": ["graphs", "dfs", "bfs", "algorithms"],
    "Dynamic Programming": ["dynamic-programming", "algorithms"],
    "Greedy": ["greedy", "algorithms"],
}


def add_tags_to_problems():
    """Add sample tags to existing problems based on their titles"""

    db = SessionLocal()

    try:
        problems = db.query(Problem).all()

        print(f"Found {len(problems)} problems")

        for problem in problems:
            # Find matching tags based on title keywords
            tags = []
            title_lower = problem.title.lower()

            # Check for exact matches first
            if problem.title in SAMPLE_TAGS:
                tags = SAMPLE_TAGS[problem.title]
            else:
                # Check for keyword matches
                for keyword, keyword_tags in SAMPLE_TAGS.items():
                    if keyword.lower() in title_lower:
                        tags.extend(keyword_tags)
                        break

                # If no specific match, add general tags based on common patterns
                if not tags:
                    if any(
                        word in title_lower for word in ["hello", "print", "output"]
                    ):
                        tags = ["basics", "output"]
                    elif any(
                        word in title_lower for word in ["add", "sum", "math", "number"]
                    ):
                        tags = ["math", "arithmetic"]
                    elif any(word in title_lower for word in ["string", "text"]):
                        tags = ["strings", "algorithms"]
                    elif any(word in title_lower for word in ["array", "list"]):
                        tags = ["arrays", "data-structures"]
                    elif any(word in title_lower for word in ["sort", "search"]):
                        tags = ["algorithms", "sorting"]
                    else:
                        tags = ["algorithms"]  # Default tag

            # Remove duplicates and limit to 4 tags
            tags = list(set(tags))[:4]

            # Update the problem
            problem.tags = tags
            print(f"Updated '{problem.title}' with tags: {tags}")

        db.commit()
        print(f"\nSuccessfully updated {len(problems)} problems with tags!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_tags_to_problems()
