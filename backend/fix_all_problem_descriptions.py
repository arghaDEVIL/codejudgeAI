#!/usr/bin/env python3
"""
Fix ALL problem descriptions - update existing problems with detailed, well-formatted descriptions
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.problem import Problem


def fix_all_problems():
    """Update all problems with enhanced descriptions"""

    db = SessionLocal()

    # Map of problem titles to enhanced descriptions
    enhanced_descriptions = {
        "Two Sum": {
            "statement": """# Two Sum

Given an array of integers `nums` and an integer `target`, return **indices** of the two numbers such that they add up to `target`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

## Input Format
- **Line 1:** An integer `n` (2 ≤ n ≤ 10⁴) - the length of the array
- **Line 2:** `n` space-separated integers representing the array
- **Line 3:** An integer `target`

## Output Format
Two space-separated integers representing the indices (0-indexed) of the two numbers.

## Examples

### Example 1
```
Input:
4
2 7 11 15
9

Output:
0 1

Explanation: nums[0] + nums[1] = 2 + 7 = 9
```

### Example 2
```
Input:
3
3 2 4
6

Output:
1 2

Explanation: nums[1] + nums[2] = 2 + 4 = 6
```

### Example 3
```
Input:
2
3 3
6

Output:
0 1

Explanation: Two different elements with same value
```

## Approach

**Optimal Solution (O(n)):**
1. Use a hash map to store numbers and their indices
2. For each number, check if `target - number` exists in the map
3. If found, return the indices

**Time Complexity:** O(n)  
**Space Complexity:** O(n)
""",
            "tags": ["arrays", "hash-table", "algorithms"],
        },
        "Factorial": {
            "statement": """# Factorial

Calculate the factorial of a given number.

The factorial of n (written as n!) is the product of all positive integers less than or equal to n.

## Definition
- 0! = 1
- n! = n × (n-1) × (n-2) × ... × 2 × 1

## Input Format
- **Line 1:** A single integer `n` (0 ≤ n ≤ 10)

## Output Format
The factorial of n

## Examples

### Example 1
```
Input:
5

Output:
120

Explanation: 5! = 5 × 4 × 3 × 2 × 1 = 120
```

### Example 2
```
Input:
0

Output:
1

Explanation: By definition, 0! = 1
```

### Example 3
```
Input:
3

Output:
6

Explanation: 3! = 3 × 2 × 1 = 6
```

### Example 4
```
Input:
1

Output:
1

Explanation: 1! = 1
```

## Approach

**Iterative Solution:**
```python
result = 1
for i in range(1, n + 1):
    result *= i
return result
```

**Recursive Solution:**
```python
if n == 0 or n == 1:
    return 1
return n * factorial(n - 1)
```

**Time Complexity:** O(n)  
**Space Complexity:** O(1) for iterative, O(n) for recursive
""",
            "tags": ["math", "recursion", "algorithms"],
        },
        "Fibonacci Number": {
            "statement": """# Fibonacci Number

Find the nth number in the Fibonacci sequence.

The Fibonacci sequence is: 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

Each number is the sum of the two preceding ones.

## Definition
- F(1) = 1
- F(2) = 1
- F(n) = F(n-1) + F(n-2) for n > 2

## Input Format
- **Line 1:** A single integer `n` (1 ≤ n ≤ 20)

## Output Format
The nth Fibonacci number

## Examples

### Example 1
```
Input:
1

Output:
1

Explanation: The 1st Fibonacci number is 1
```

### Example 2
```
Input:
5

Output:
5

Explanation: 
Sequence: 1, 1, 2, 3, 5
The 5th number is 5
```

### Example 3
```
Input:
10

Output:
55

Explanation:
Sequence: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55
The 10th number is 55
```

### Example 4
```
Input:
2

Output:
1

Explanation: The 2nd Fibonacci number is 1
```

## Approach

**Iterative Solution (Optimal):**
```python
if n <= 2:
    return 1
a, b = 1, 1
for i in range(3, n + 1):
    a, b = b, a + b
return b
```

**Recursive Solution:**
```python
if n <= 2:
    return 1
return fib(n-1) + fib(n-2)
```

**Time Complexity:** O(n) for iterative, O(2^n) for naive recursive  
**Space Complexity:** O(1) for iterative, O(n) for recursive
""",
            "tags": ["math", "dynamic-programming", "recursion"],
        },
        "Valid Parentheses": {
            "statement": """# Valid Parentheses

Given a string containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the **same type** of brackets
2. Open brackets must be closed in the **correct order**
3. Every close bracket has a corresponding open bracket

## Input Format
- **Line 1:** A string `s` consisting only of characters `'()[]{}'`

## Output Format
Print `true` if valid, `false` otherwise

## Examples

### Example 1
```
Input:
()

Output:
true

Explanation: One pair of parentheses, properly closed
```

### Example 2
```
Input:
()[]{}

Output:
true

Explanation: Three pairs, all properly closed
```

### Example 3
```
Input:
(]

Output:
false

Explanation: Wrong closing bracket type
```

### Example 4
```
Input:
([)]

Output:
false

Explanation: Wrong order - should be ([])
```

### Example 5
```
Input:
{[]}

Output:
true

Explanation: Properly nested brackets
```

## Approach

**Stack-Based Solution:**
1. Create an empty stack
2. For each character:
   - If opening bracket: push to stack
   - If closing bracket: check if it matches stack top
3. Return true if stack is empty at the end

**Time Complexity:** O(n)  
**Space Complexity:** O(n)
""",
            "tags": ["strings", "stack", "algorithms"],
        },
        "Maximum Subarray": {
            "statement": """# Maximum Subarray

Find the contiguous subarray with the largest sum.

A subarray is a contiguous part of an array.

## Input Format
- **Line 1:** An integer `n` (1 ≤ n ≤ 10⁵)
- **Line 2:** `n` space-separated integers

## Output Format
The maximum sum of any contiguous subarray

## Examples

### Example 1
```
Input:
9
-2 1 -3 4 -1 2 1 -5 4

Output:
6

Explanation: [4, -1, 2, 1] has the largest sum = 6
```

### Example 2
```
Input:
1
1

Output:
1

Explanation: Only one element
```

### Example 3
```
Input:
5
5 4 -1 7 8

Output:
23

Explanation: The entire array gives maximum sum
```

### Example 4
```
Input:
3
-2 -3 -1

Output:
-1

Explanation: All negative, pick the least negative
```

## Approach

**Kadane's Algorithm (Optimal):**
```python
max_so_far = nums[0]
max_ending_here = nums[0]

for i in range(1, len(nums)):
    max_ending_here = max(nums[i], max_ending_here + nums[i])
    max_so_far = max(max_so_far, max_ending_here)

return max_so_far
```

**Key Insight:** At each position, decide whether to extend the previous subarray or start fresh.

**Time Complexity:** O(n)  
**Space Complexity:** O(1)
""",
            "tags": ["arrays", "dynamic-programming", "algorithms"],
        },
    }

    updated_count = 0
    not_found = []

    try:
        # Get all problems
        problems = db.query(Problem).all()

        print(f"\n📊 Found {len(problems)} problems in database\n")
        print("=" * 80)

        for problem in problems:
            if problem.title in enhanced_descriptions:
                enhanced = enhanced_descriptions[problem.title]
                problem.statement = enhanced["statement"]
                problem.tags = enhanced["tags"]
                updated_count += 1
                print(f"✅ Updated: {problem.title}")
            else:
                not_found.append(problem.title)
                print(f"⚠️  No enhanced description for: {problem.title}")

        db.commit()

        print("\n" + "=" * 80)
        print(f"\n🎉 Successfully updated {updated_count} problem descriptions!")

        if not_found:
            print(f"\n⚠️  Problems without enhanced descriptions ({len(not_found)}):")
            for title in not_found:
                print(f"   - {title}")

        # Show final stats
        total = db.query(Problem).count()
        easy = db.query(Problem).filter(Problem.difficulty == "Easy").count()
        medium = db.query(Problem).filter(Problem.difficulty == "Medium").count()
        hard = db.query(Problem).filter(Problem.difficulty == "Hard").count()

        print(f"\n📊 Final Database Stats:")
        print(f"   Total Problems: {total}")
        print(f"   Easy: {easy}")
        print(f"   Medium: {medium}")
        print(f"   Hard: {hard}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Fixing All Problem Descriptions...")
    print("=" * 80)
    fix_all_problems()
