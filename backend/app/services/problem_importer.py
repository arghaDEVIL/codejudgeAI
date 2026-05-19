#!/usr/bin/env python3
"""
Problem Importer Service - Fetch problems from various coding platforms
"""

import requests
import time
import json
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.problem import Problem
from app.db.database import SessionLocal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProblemImporter:
    """Service to import problems from various coding platforms"""

    def __init__(self):
        self.session = SessionLocal()

    def __del__(self):
        if hasattr(self, "session"):
            self.session.close()

    def import_from_codeforces(
        self, limit: int = 50, min_rating: int = 800, max_rating: int = 1600
    ) -> int:
        """
        Import problems from Codeforces API

        Args:
            limit: Maximum number of problems to import
            min_rating: Minimum problem rating (difficulty)
            max_rating: Maximum problem rating (difficulty)

        Returns:
            Number of problems successfully imported
        """
        try:
            logger.info(
                f"Fetching problems from Codeforces API (rating {min_rating}-{max_rating})"
            )

            # Fetch problems from Codeforces API
            response = requests.get(
                "https://codeforces.com/api/problemset.problems", timeout=30
            )
            response.raise_for_status()

            data = response.json()
            if data["status"] != "OK":
                logger.error(
                    f"Codeforces API error: {data.get('comment', 'Unknown error')}"
                )
                return 0

            problems = data["result"]["problems"]
            imported_count = 0

            for problem_data in problems:
                if imported_count >= limit:
                    break

                # Filter by rating (difficulty)
                rating = problem_data.get("rating")
                if not rating or rating < min_rating or rating > max_rating:
                    continue

                # Skip if problem already exists
                existing = (
                    self.session.query(Problem)
                    .filter(Problem.title == problem_data["name"])
                    .first()
                )
                if existing:
                    continue

                # Convert Codeforces problem to our format
                converted_problem = self._convert_codeforces_problem(problem_data)
                if converted_problem:
                    try:
                        new_problem = Problem(**converted_problem)
                        self.session.add(new_problem)
                        self.session.commit()
                        imported_count += 1
                        logger.info(
                            f"Imported: {problem_data['name']} (Rating: {rating})"
                        )

                        # Rate limiting - Codeforces allows 1 request per 2 seconds
                        time.sleep(0.1)

                    except Exception as e:
                        logger.error(
                            f"Failed to save problem {problem_data['name']}: {e}"
                        )
                        self.session.rollback()

            logger.info(
                f"Successfully imported {imported_count} problems from Codeforces"
            )
            return imported_count

        except Exception as e:
            logger.error(f"Error importing from Codeforces: {e}")
            return 0

    def _convert_codeforces_problem(self, cf_problem: Dict) -> Optional[Dict]:
        """Convert Codeforces problem format to our database format"""
        try:
            # Map Codeforces rating to our difficulty levels
            rating = cf_problem.get("rating", 1000)
            if rating <= 1000:
                difficulty = "Easy"
            elif rating <= 1500:
                difficulty = "Medium"
            else:
                difficulty = "Hard"

            # Clean and map tags
            cf_tags = cf_problem.get("tags", [])
            mapped_tags = self._map_codeforces_tags(cf_tags)

            # Generate problem statement (since CF API doesn't provide full statements)
            statement = self._generate_problem_statement(cf_problem)

            return {
                "title": cf_problem["name"],
                "statement": statement,
                "difficulty": difficulty,
                "tags": mapped_tags[:6],  # Limit to 6 tags
                "expected_output": None,  # Will be handled by testcases
            }

        except Exception as e:
            logger.error(f"Error converting Codeforces problem: {e}")
            return None

    def _map_codeforces_tags(self, cf_tags: List[str]) -> List[str]:
        """Map Codeforces tags to our standardized tag system"""
        tag_mapping = {
            # Data Structures
            "data structures": "data-structures",
            "trees": "trees",
            "graphs": "graphs",
            "dsu": "union-find",
            "binary indexed tree": "bit",
            "segment tree": "segment-tree",
            # Algorithms
            "dp": "dynamic-programming",
            "greedy": "greedy",
            "binary search": "binary-search",
            "two pointers": "two-pointers",
            "sortings": "sorting",
            "dfs and similar": "dfs",
            "bfs": "bfs",
            # Math & Number Theory
            "math": "math",
            "number theory": "number-theory",
            "combinatorics": "combinatorics",
            "geometry": "geometry",
            "probabilities": "probability",
            # String Processing
            "strings": "strings",
            "string suffix structures": "string-algorithms",
            "hashing": "hashing",
            # Implementation & Logic
            "implementation": "implementation",
            "brute force": "brute-force",
            "constructive algorithms": "constructive",
            "bitmasks": "bitmasks",
            # Game Theory & Interactive
            "games": "game-theory",
            "interactive": "interactive",
            # Basic Categories
            "expression parsing": "parsing",
            "shortest paths": "shortest-path",
            "flows": "max-flow",
        }

        mapped = []
        for tag in cf_tags:
            mapped_tag = tag_mapping.get(tag.lower(), tag.lower().replace(" ", "-"))
            if mapped_tag not in mapped:
                mapped.append(mapped_tag)

        return mapped

    def _generate_problem_statement(self, cf_problem: Dict) -> str:
        """Generate a problem statement since Codeforces API doesn't provide full statements"""
        name = cf_problem["name"]
        contest_id = cf_problem.get("contestId", "")
        index = cf_problem.get("index", "")
        rating = cf_problem.get("rating", "Unrated")
        tags = ", ".join(cf_problem.get("tags", []))

        statement = f"""# {name}

**Source:** Codeforces Contest {contest_id}, Problem {index}
**Difficulty Rating:** {rating}
**Topics:** {tags}

## Problem Description

This is a competitive programming problem from Codeforces. 

**Note:** This problem was imported automatically from Codeforces. The full problem statement, input/output format, and sample test cases can be found at:
https://codeforces.com/problemset/problem/{contest_id}/{index}

## Your Task

Solve this problem by implementing an efficient algorithm that handles the given constraints.

## Approach

Consider the problem tags: {tags}

These tags give you hints about which algorithms or data structures might be useful for solving this problem.

## Implementation

Write your solution in the code editor and test it against the provided test cases.
"""
        return statement

    def import_sample_problems(self) -> int:
        """Import a curated set of sample problems for demonstration"""
        sample_problems = [
            {
                "title": "Two Sum",
                "statement": """# Two Sum

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

## Example

**Input:** nums = [2,7,11,15], target = 9
**Output:** [0,1]
**Explanation:** Because nums[0] + nums[1] == 9, we return [0, 1].

## Constraints

- 2 ≤ nums.length ≤ 10⁴
- -10⁹ ≤ nums[i] ≤ 10⁹
- -10⁹ ≤ target ≤ 10⁹
- Only one valid answer exists.
""",
                "difficulty": "Easy",
                "tags": ["arrays", "hash-table", "algorithms"],
            },
            {
                "title": "Valid Parentheses",
                "statement": """# Valid Parentheses

Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

## Example

**Input:** s = "()[]{}"
**Output:** true

**Input:** s = "([)]"
**Output:** false

## Constraints

- 1 ≤ s.length ≤ 10⁴
- s consists of parentheses only '()[]{}'.
""",
                "difficulty": "Easy",
                "tags": ["strings", "stack", "algorithms"],
            },
            {
                "title": "Binary Tree Inorder Traversal",
                "statement": """# Binary Tree Inorder Traversal

Given the root of a binary tree, return the inorder traversal of its nodes' values.

## Example

**Input:** root = [1,null,2,3]
**Output:** [1,3,2]

## Constraints

- The number of nodes in the tree is in the range [0, 100].
- -100 ≤ Node.val ≤ 100

## Follow up

Recursive solution is trivial, could you do it iteratively?
""",
                "difficulty": "Easy",
                "tags": ["trees", "dfs", "data-structures", "recursion"],
            },
            {
                "title": "Longest Substring Without Repeating Characters",
                "statement": """# Longest Substring Without Repeating Characters

Given a string s, find the length of the longest substring without repeating characters.

## Example

**Input:** s = "abcabcbb"
**Output:** 3
**Explanation:** The answer is "abc", with the length of 3.

**Input:** s = "pwwkew"
**Output:** 3
**Explanation:** The answer is "wke", with the length of 3.

## Constraints

- 0 ≤ s.length ≤ 5 * 10⁴
- s consists of English letters, digits, symbols and spaces.
""",
                "difficulty": "Medium",
                "tags": ["strings", "sliding-window", "hash-table", "algorithms"],
            },
            {
                "title": "Maximum Subarray",
                "statement": """# Maximum Subarray

Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

## Example

**Input:** nums = [-2,1,-3,4,-1,2,1,-5,4]
**Output:** 6
**Explanation:** [4,-1,2,1] has the largest sum = 6.

## Constraints

- 1 ≤ nums.length ≤ 10⁵
- -10⁴ ≤ nums[i] ≤ 10⁴

## Follow up

If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach.
""",
                "difficulty": "Medium",
                "tags": ["arrays", "dynamic-programming", "algorithms"],
            },
            {
                "title": "Merge k Sorted Lists",
                "statement": """# Merge k Sorted Lists

You are given an array of k linked-lists lists, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

## Example

**Input:** lists = [[1,4,5],[1,3,4],[2,6]]
**Output:** [1,1,2,3,4,4,5,6]

## Constraints

- k == lists.length
- 0 ≤ k ≤ 10⁴
- 0 ≤ lists[i].length ≤ 500
- -10⁴ ≤ lists[i][j] ≤ 10⁴
- lists[i] is sorted in ascending order.
- The sum of lists[i].length will not exceed 10⁴.
""",
                "difficulty": "Hard",
                "tags": ["linked-list", "divide-and-conquer", "heap", "algorithms"],
            },
        ]

        imported_count = 0

        for problem_data in sample_problems:
            # Skip if problem already exists
            existing = (
                self.session.query(Problem)
                .filter(Problem.title == problem_data["title"])
                .first()
            )
            if existing:
                continue

            try:
                new_problem = Problem(**problem_data)
                self.session.add(new_problem)
                self.session.commit()
                imported_count += 1
                logger.info(f"Imported sample problem: {problem_data['title']}")

            except Exception as e:
                logger.error(
                    f"Failed to save sample problem {problem_data['title']}: {e}"
                )
                self.session.rollback()

        logger.info(f"Successfully imported {imported_count} sample problems")
        return imported_count

    def get_import_stats(self) -> Dict:
        """Get statistics about imported problems"""
        try:
            total_problems = self.session.query(Problem).count()

            # Count by difficulty
            easy_count = (
                self.session.query(Problem).filter(Problem.difficulty == "Easy").count()
            )
            medium_count = (
                self.session.query(Problem)
                .filter(Problem.difficulty == "Medium")
                .count()
            )
            hard_count = (
                self.session.query(Problem).filter(Problem.difficulty == "Hard").count()
            )

            # Get tag distribution
            problems = self.session.query(Problem).all()
            tag_counts = {}

            for problem in problems:
                if problem.tags:
                    for tag in problem.tags:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1

            return {
                "total_problems": total_problems,
                "difficulty_distribution": {
                    "Easy": easy_count,
                    "Medium": medium_count,
                    "Hard": hard_count,
                },
                "top_tags": sorted(
                    tag_counts.items(), key=lambda x: x[1], reverse=True
                )[:10],
                "total_tags": len(tag_counts),
            }

        except Exception as e:
            logger.error(f"Error getting import stats: {e}")
            return {}


def main():
    """CLI interface for the problem importer"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Import coding problems from various platforms"
    )
    parser.add_argument(
        "--source",
        choices=["codeforces", "sample", "all"],
        default="sample",
        help="Source to import from",
    )
    parser.add_argument(
        "--limit", type=int, default=20, help="Maximum number of problems to import"
    )
    parser.add_argument(
        "--min-rating",
        type=int,
        default=800,
        help="Minimum problem rating (Codeforces only)",
    )
    parser.add_argument(
        "--max-rating",
        type=int,
        default=1600,
        help="Maximum problem rating (Codeforces only)",
    )
    parser.add_argument("--stats", action="store_true", help="Show import statistics")

    args = parser.parse_args()

    importer = ProblemImporter()

    if args.stats:
        stats = importer.get_import_stats()
        print("\n=== Problem Import Statistics ===")
        print(f"Total Problems: {stats.get('total_problems', 0)}")
        print(f"Easy: {stats.get('difficulty_distribution', {}).get('Easy', 0)}")
        print(f"Medium: {stats.get('difficulty_distribution', {}).get('Medium', 0)}")
        print(f"Hard: {stats.get('difficulty_distribution', {}).get('Hard', 0)}")
        print(f"Total Tags: {stats.get('total_tags', 0)}")
        print("\nTop Tags:")
        for tag, count in stats.get("top_tags", []):
            print(f"  {tag}: {count}")
        return

    total_imported = 0

    if args.source in ["sample", "all"]:
        print("Importing sample problems...")
        count = importer.import_sample_problems()
        total_imported += count
        print(f"Imported {count} sample problems")

    if args.source in ["codeforces", "all"]:
        print(
            f"Importing from Codeforces (rating {args.min_rating}-{args.max_rating})..."
        )
        count = importer.import_from_codeforces(
            limit=args.limit, min_rating=args.min_rating, max_rating=args.max_rating
        )
        total_imported += count
        print(f"Imported {count} problems from Codeforces")

    print(f"\nTotal problems imported: {total_imported}")


if __name__ == "__main__":
    main()
