#!/usr/bin/env python3
"""
Enhanced Problem Importer - Fetch full problem descriptions from web pages
"""

import requests
import time
import json
import re
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.models.problem import Problem
from app.db.database import SessionLocal
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EnhancedProblemImporter:
    """Enhanced service to import problems with full descriptions"""

    def __init__(self):
        self.session = SessionLocal()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def __del__(self):
        if hasattr(self, "session"):
            self.session.close()

    def import_from_codeforces_with_descriptions(
        self, limit: int = 20, min_rating: int = 800, max_rating: int = 1600
    ) -> int:
        """
        Import problems from Codeforces with full problem descriptions
        """
        try:
            logger.info(
                f"Fetching problems from Codeforces with full descriptions (rating {min_rating}-{max_rating})"
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

                # Fetch full problem description
                full_description = self._fetch_codeforces_problem_description(
                    problem_data
                )
                if not full_description:
                    logger.warning(
                        f"Could not fetch description for {problem_data['name']}, skipping"
                    )
                    continue

                # Convert to our format with full description
                converted_problem = self._convert_codeforces_problem_with_description(
                    problem_data, full_description
                )
                if converted_problem:
                    try:
                        new_problem = Problem(**converted_problem)
                        self.session.add(new_problem)
                        self.session.commit()
                        imported_count += 1
                        logger.info(
                            f"Imported with full description: {problem_data['name']} (Rating: {rating})"
                        )

                        # Rate limiting - Be respectful to Codeforces
                        time.sleep(2)

                    except Exception as e:
                        logger.error(
                            f"Failed to save problem {problem_data['name']}: {e}"
                        )
                        self.session.rollback()

            logger.info(
                f"Successfully imported {imported_count} problems with full descriptions"
            )
            return imported_count

        except Exception as e:
            logger.error(f"Error importing from Codeforces: {e}")
            return 0

    def _fetch_codeforces_problem_description(self, cf_problem: Dict) -> Optional[str]:
        """Fetch full problem description from Codeforces problem page"""
        try:
            contest_id = cf_problem.get("contestId")
            index = cf_problem.get("index")

            if not contest_id or not index:
                return None

            # Construct problem URL
            problem_url = (
                f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
            )

            logger.info(f"Fetching description from: {problem_url}")

            # Fetch the problem page
            response = requests.get(problem_url, headers=self.headers, timeout=30)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract problem statement
            problem_statement = self._extract_problem_statement(soup, cf_problem)

            return problem_statement

        except Exception as e:
            logger.error(f"Error fetching problem description: {e}")
            return None

    def _extract_problem_statement(self, soup: BeautifulSoup, cf_problem: Dict) -> str:
        """Extract and format problem statement from Codeforces HTML"""
        try:
            # Find the problem statement div
            problem_div = soup.find("div", class_="problem-statement")
            if not problem_div:
                return None

            # Extract title
            title = cf_problem.get("name", "Problem")

            # Extract problem description
            description_div = problem_div.find("div", class_="header")
            time_limit = ""
            memory_limit = ""

            if description_div:
                time_div = description_div.find("div", class_="time-limit")
                memory_div = description_div.find("div", class_="memory-limit")

                if time_div:
                    time_limit = time_div.get_text().strip()
                if memory_div:
                    memory_limit = memory_div.get_text().strip()

            # Extract problem statement text
            statement_parts = []

            # Problem description
            desc_div = problem_div.find("div", class_="problem-statement")
            if desc_div:
                # Find all paragraphs and divs with problem content
                for element in desc_div.find_all(["p", "div"], recursive=True):
                    if element.get("class") and any(
                        cls
                        in [
                            "header",
                            "input-specification",
                            "output-specification",
                            "sample-tests",
                        ]
                        for cls in element.get("class")
                    ):
                        continue

                    text = element.get_text().strip()
                    if text and len(text) > 10:  # Filter out short/empty elements
                        statement_parts.append(text)

            # Extract input specification
            input_spec = ""
            input_div = problem_div.find("div", class_="input-specification")
            if input_div:
                input_spec = self._clean_text(input_div.get_text())

            # Extract output specification
            output_spec = ""
            output_div = problem_div.find("div", class_="output-specification")
            if output_div:
                output_spec = self._clean_text(output_div.get_text())

            # Extract sample tests
            samples = []
            sample_tests = problem_div.find("div", class_="sample-tests")
            if sample_tests:
                inputs = sample_tests.find_all("div", class_="input")
                outputs = sample_tests.find_all("div", class_="output")

                for i, (inp, out) in enumerate(zip(inputs, outputs)):
                    input_text = self._extract_sample_text(inp)
                    output_text = self._extract_sample_text(out)

                    if input_text is not None and output_text is not None:
                        samples.append(
                            {
                                "input": input_text,
                                "output": output_text,
                                "number": i + 1,
                            }
                        )

            # Format the complete problem statement
            formatted_statement = self._format_problem_statement(
                title,
                statement_parts,
                input_spec,
                output_spec,
                samples,
                time_limit,
                memory_limit,
                cf_problem,
            )

            return formatted_statement

        except Exception as e:
            logger.error(f"Error extracting problem statement: {e}")
            return None

    def _clean_text(self, text: str) -> str:
        """Clean and format text content"""
        if not text:
            return ""

        # Remove extra whitespace and normalize
        text = re.sub(r"\s+", " ", text.strip())

        # Remove common prefixes
        text = re.sub(r"^(Input|Output|Note):\s*", "", text)

        return text

    def _extract_sample_text(self, element) -> Optional[str]:
        """Extract sample input/output text"""
        try:
            pre_tag = element.find("pre")
            if pre_tag:
                return pre_tag.get_text().strip()
            return element.get_text().strip()
        except:
            return None

    def _format_problem_statement(
        self,
        title: str,
        statement_parts: List[str],
        input_spec: str,
        output_spec: str,
        samples: List[Dict],
        time_limit: str,
        memory_limit: str,
        cf_problem: Dict,
    ) -> str:
        """Format the complete problem statement in markdown"""

        contest_id = cf_problem.get("contestId", "")
        index = cf_problem.get("index", "")
        rating = cf_problem.get("rating", "Unrated")
        tags = ", ".join(cf_problem.get("tags", []))

        # Build the formatted statement
        statement = f"""# {title}

**Source:** Codeforces Contest {contest_id}, Problem {index}  
**Difficulty Rating:** {rating}  
**Topics:** {tags}  
"""

        if time_limit or memory_limit:
            statement += f"**Constraints:** {time_limit}, {memory_limit}\n"

        statement += "\n## Problem Description\n\n"

        # Add main problem description
        if statement_parts:
            # Take the most substantial part as the main description
            main_desc = max(statement_parts, key=len) if statement_parts else ""
            if main_desc:
                statement += f"{main_desc}\n\n"

        # Add input specification
        if input_spec:
            statement += f"## Input\n\n{input_spec}\n\n"

        # Add output specification
        if output_spec:
            statement += f"## Output\n\n{output_spec}\n\n"

        # Add sample test cases
        if samples:
            statement += "## Examples\n\n"
            for sample in samples:
                statement += f"**Example {sample['number']}:**\n\n"
                statement += f"```\nInput:\n{sample['input']}\n\nOutput:\n{sample['output']}\n```\n\n"

        # Add approach hints
        if tags:
            statement += f"## Approach Hints\n\nThis problem involves: **{tags}**\n\n"
            statement += "Consider which algorithms or data structures from these topics might be useful.\n\n"

        statement += f"## Original Problem\n\nView the original problem at: https://codeforces.com/problemset/problem/{contest_id}/{index}\n"

        return statement

    def _convert_codeforces_problem_with_description(
        self, cf_problem: Dict, description: str
    ) -> Optional[Dict]:
        """Convert Codeforces problem with full description to our database format"""
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

            return {
                "title": cf_problem["name"],
                "statement": description,
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
        }

        mapped = []
        for tag in cf_tags:
            mapped_tag = tag_mapping.get(tag.lower(), tag.lower().replace(" ", "-"))
            if mapped_tag not in mapped:
                mapped.append(mapped_tag)

        return mapped

    def import_sample_problems_with_full_descriptions(self) -> int:
        """Import enhanced sample problems with detailed descriptions"""
        sample_problems = [
            {
                "title": "Two Sum",
                "statement": """# Two Sum

**Difficulty:** Easy  
**Topics:** arrays, hash-table, algorithms  

## Problem Description

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

## Input

- An array of integers `nums` where `2 ≤ nums.length ≤ 10⁴`
- An integer `target` where `-10⁹ ≤ target ≤ 10⁹`
- `-10⁹ ≤ nums[i] ≤ 10⁹`

## Output

Return an array of two integers representing the indices of the two numbers that add up to the target.

## Examples

**Example 1:**
```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

**Example 2:**
```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

**Example 3:**
```
Input: nums = [3,3], target = 6
Output: [0,1]
```

## Approach Hints

This problem involves: **arrays, hash-table**

Consider using a hash map to store numbers you've seen and their indices. For each number, check if `target - current_number` exists in your hash map.

## Constraints

- Only one valid answer exists.
- You cannot use the same element twice.
""",
                "difficulty": "Easy",
                "tags": ["arrays", "hash-table", "algorithms"],
            },
            {
                "title": "Valid Parentheses",
                "statement": """# Valid Parentheses

**Difficulty:** Easy  
**Topics:** strings, stack, algorithms  

## Problem Description

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

## Input

A string `s` consisting only of characters `'()[]{}'` where `1 ≤ s.length ≤ 10⁴`.

## Output

Return `true` if the string is valid, `false` otherwise.

## Examples

**Example 1:**
```
Input: s = "()"
Output: true
```

**Example 2:**
```
Input: s = "()[]{}"
Output: true
```

**Example 3:**
```
Input: s = "(]"
Output: false
```

**Example 4:**
```
Input: s = "([)]"
Output: false
```

## Approach Hints

This problem involves: **strings, stack**

Use a stack data structure:
1. Push opening brackets onto the stack
2. When you encounter a closing bracket, check if it matches the most recent opening bracket
3. The string is valid if the stack is empty at the end

## Algorithm

1. Create an empty stack
2. Iterate through each character in the string
3. If it's an opening bracket, push it onto the stack
4. If it's a closing bracket, check if the stack is empty or if the top doesn't match
5. Return true if stack is empty at the end
""",
                "difficulty": "Easy",
                "tags": ["strings", "stack", "algorithms"],
            },
            {
                "title": "Maximum Subarray",
                "statement": """# Maximum Subarray (Kadane's Algorithm)

**Difficulty:** Medium  
**Topics:** arrays, dynamic-programming, algorithms  

## Problem Description

Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

## Input

An integer array `nums` where:
- `1 ≤ nums.length ≤ 10⁵`
- `-10⁴ ≤ nums[i] ≤ 10⁴`

## Output

Return the maximum sum of any contiguous subarray.

## Examples

**Example 1:**
```
Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.
```

**Example 2:**
```
Input: nums = [1]
Output: 1
```

**Example 3:**
```
Input: nums = [5,4,-1,7,8]
Output: 23
```

## Approach Hints

This problem involves: **arrays, dynamic-programming**

**Kadane's Algorithm** is the optimal solution:
1. Keep track of the maximum sum ending at the current position
2. At each step, decide whether to extend the existing subarray or start a new one
3. Update the global maximum as you go

## Algorithm (Kadane's Algorithm)

```
max_so_far = nums[0]
max_ending_here = nums[0]

for i from 1 to n-1:
    max_ending_here = max(nums[i], max_ending_here + nums[i])
    max_so_far = max(max_so_far, max_ending_here)

return max_so_far
```

## Time Complexity

- **Time:** O(n) - single pass through the array
- **Space:** O(1) - only using constant extra space

## Follow-up

If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
""",
                "difficulty": "Medium",
                "tags": ["arrays", "dynamic-programming", "algorithms"],
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
                logger.info(
                    f"Imported enhanced sample problem: {problem_data['title']}"
                )

            except Exception as e:
                logger.error(
                    f"Failed to save sample problem {problem_data['title']}: {e}"
                )
                self.session.rollback()

        logger.info(f"Successfully imported {imported_count} enhanced sample problems")
        return imported_count


def main():
    """CLI interface for the enhanced problem importer"""
    print("🚀 Enhanced Problem Importer - Full Descriptions")
    print("=" * 50)

    importer = EnhancedProblemImporter()

    print("\n📊 Available Options:")
    print("1. Import Enhanced Sample Problems (3 with full descriptions)")
    print("2. Import Codeforces Easy Problems (with full descriptions)")
    print("3. Import Codeforces Medium Problems (with full descriptions)")
    print("0. Exit")

    while True:
        try:
            choice = input("\n🔥 Select an option (0-3): ").strip()

            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                print("\n📥 Importing enhanced sample problems...")
                count = importer.import_sample_problems_with_full_descriptions()
                print(f"✅ Successfully imported {count} enhanced sample problems!")

            elif choice == "2":
                print(
                    "\n📥 Importing Easy problems from Codeforces with full descriptions..."
                )
                print(
                    "⚠️  This will take longer as we fetch full problem descriptions..."
                )
                count = importer.import_from_codeforces_with_descriptions(
                    limit=5, min_rating=800, max_rating=1000
                )
                print(
                    f"✅ Successfully imported {count} Easy problems with full descriptions!"
                )

            elif choice == "3":
                print(
                    "\n📥 Importing Medium problems from Codeforces with full descriptions..."
                )
                print(
                    "⚠️  This will take longer as we fetch full problem descriptions..."
                )
                count = importer.import_from_codeforces_with_descriptions(
                    limit=5, min_rating=1000, max_rating=1500
                )
                print(
                    f"✅ Successfully imported {count} Medium problems with full descriptions!"
                )

            else:
                print("❌ Invalid choice. Please select 0-3.")

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
