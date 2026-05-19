#!/usr/bin/env python3
"""
Curated Problem Importer - High-quality problems with full descriptions
"""

import time
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from app.models.problem import Problem
from app.db.database import SessionLocal
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CuratedProblemImporter:
    """Service to import curated high-quality problems with full descriptions"""

    def __init__(self):
        self.session = SessionLocal()

    def __del__(self):
        if hasattr(self, "session"):
            self.session.close()

    def import_curated_problems(self) -> int:
        """Import a comprehensive set of curated problems with full descriptions"""

        curated_problems = [
            # EASY PROBLEMS
            {
                "title": "Two Sum",
                "statement": """# Two Sum

**Difficulty:** Easy  
**Topics:** arrays, hash-table, algorithms  

## Problem Description

Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

## Input Format

- Line 1: An integer `n` (2 ≤ n ≤ 10⁴) - the length of the array
- Line 2: `n` space-separated integers representing the array `nums` (-10⁹ ≤ nums[i] ≤ 10⁹)
- Line 3: An integer `target` (-10⁹ ≤ target ≤ 10⁹)

## Output Format

Two space-separated integers representing the indices (0-indexed) of the two numbers that add up to the target.

## Examples

**Example 1:**
```
Input:
4
2 7 11 15
9

Output:
0 1
```

**Example 2:**
```
Input:
3
3 2 4
6

Output:
1 2
```

## Approach Hints

This problem involves: **arrays, hash-table**

**Optimal Solution (O(n) time):**
1. Use a hash map to store numbers you've seen and their indices
2. For each number, check if `target - current_number` exists in your hash map
3. If found, return the indices; otherwise, add current number to hash map

**Brute Force (O(n²) time):**
1. Try all pairs of numbers using nested loops
2. Check if their sum equals the target

## Constraints

- Only one valid answer exists
- You cannot use the same element twice
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
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type

## Input Format

- Line 1: A string `s` consisting only of characters `'()[]{}'` (1 ≤ |s| ≤ 10⁴)

## Output Format

Print `true` if the string is valid, `false` otherwise.

## Examples

**Example 1:**
```
Input:
()

Output:
true
```

**Example 2:**
```
Input:
()[]{} 

Output:
true
```

**Example 3:**
```
Input:
(]

Output:
false
```

**Example 4:**
```
Input:
([)]

Output:
false
```

## Approach Hints

This problem involves: **strings, stack**

**Stack-based Solution:**
1. Create an empty stack
2. Iterate through each character in the string
3. If it's an opening bracket `([{`, push it onto the stack
4. If it's a closing bracket `)]}`, check if the stack is empty or if the top doesn't match
5. Return true if stack is empty at the end

**Matching Rules:**
- `(` matches `)`
- `[` matches `]`  
- `{` matches `}`

## Time Complexity

- **Time:** O(n) - single pass through the string
- **Space:** O(n) - worst case all opening brackets
""",
                "difficulty": "Easy",
                "tags": ["strings", "stack", "algorithms"],
            },
            {
                "title": "Palindrome Number",
                "statement": """# Palindrome Number

**Difficulty:** Easy  
**Topics:** math, algorithms  

## Problem Description

Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.

A palindrome number reads the same backward as forward. For example, `121` is a palindrome while `123` is not.

## Input Format

- Line 1: An integer `x` (-2³¹ ≤ x ≤ 2³¹ - 1)

## Output Format

Print `true` if the number is a palindrome, `false` otherwise.

## Examples

**Example 1:**
```
Input:
121

Output:
true
```

**Example 2:**
```
Input:
-121

Output:
false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
```

**Example 3:**
```
Input:
10

Output:
false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
```

## Approach Hints

This problem involves: **math**

**Method 1 - String Conversion:**
1. Convert number to string
2. Compare string with its reverse
3. Handle negative numbers (always false)

**Method 2 - Mathematical (No extra space):**
1. Reverse only half the number
2. Compare first half with reversed second half
3. Handle odd-length numbers specially

**Edge Cases:**
- Negative numbers are not palindromes
- Single digit numbers are palindromes
- Numbers ending in 0 (except 0 itself) are not palindromes

## Follow-up

Could you solve it without converting the integer to a string?
""",
                "difficulty": "Easy",
                "tags": ["math", "algorithms"],
            },
            # MEDIUM PROBLEMS
            {
                "title": "Longest Substring Without Repeating Characters",
                "statement": """# Longest Substring Without Repeating Characters

**Difficulty:** Medium  
**Topics:** strings, sliding-window, hash-table, algorithms  

## Problem Description

Given a string `s`, find the length of the longest substring without repeating characters.

A substring is a contiguous sequence of characters within a string.

## Input Format

- Line 1: A string `s` consisting of English letters, digits, symbols and spaces (0 ≤ |s| ≤ 5 × 10⁴)

## Output Format

An integer representing the length of the longest substring without repeating characters.

## Examples

**Example 1:**
```
Input:
abcabcbb

Output:
3
Explanation: The answer is "abc", with the length of 3.
```

**Example 2:**
```
Input:
bbbbb

Output:
1
Explanation: The answer is "b", with the length of 1.
```

**Example 3:**
```
Input:
pwwkew

Output:
3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
```

## Approach Hints

This problem involves: **strings, sliding-window, hash-table**

**Sliding Window Technique:**
1. Use two pointers (left and right) to maintain a window
2. Expand the window by moving right pointer
3. When a duplicate is found, shrink window from left
4. Keep track of maximum window size seen

**Implementation Steps:**
1. Use a hash set to track characters in current window
2. Expand window: add character to set, update max length
3. Shrink window: remove characters from left until no duplicates
4. Return maximum length found

## Time Complexity

- **Time:** O(n) - each character visited at most twice
- **Space:** O(min(m,n)) - where m is charset size

## Optimization

Use hash map to store character indices for faster window adjustment.
""",
                "difficulty": "Medium",
                "tags": ["strings", "sliding-window", "hash-table", "algorithms"],
            },
            {
                "title": "Add Two Numbers",
                "statement": """# Add Two Numbers

**Difficulty:** Medium  
**Topics:** linked-list, math, recursion  

## Problem Description

You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

## Input Format

- Line 1: Space-separated digits of first number (in reverse order)
- Line 2: Space-separated digits of second number (in reverse order)

## Output Format

Space-separated digits of the sum (in reverse order)

## Examples

**Example 1:**
```
Input:
2 4 3
5 6 4

Output:
7 0 8
Explanation: 342 + 465 = 807
```

**Example 2:**
```
Input:
0

9 9 9 9 9 9 9

Output:
9 9 9 9 9 9 9
```

**Example 3:**
```
Input:
9 9 9 9 9 9 9
9 9 9 9

Output:
8 9 9 9 0 0 0 1
```

## Approach Hints

This problem involves: **linked-list, math, recursion**

**Algorithm:**
1. Initialize carry = 0
2. Traverse both lists simultaneously
3. At each step: sum = digit1 + digit2 + carry
4. New digit = sum % 10, carry = sum // 10
5. Create new node with the digit
6. Continue until both lists are processed and carry = 0

**Edge Cases:**
- Lists of different lengths
- Final carry after processing both lists
- One or both lists are empty

## Implementation Notes

```
def addTwoNumbers(l1, l2):
    dummy = ListNode(0)
    current = dummy
    carry = 0
    
    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        
        total = val1 + val2 + carry
        carry = total // 10
        digit = total % 10
        
        current.next = ListNode(digit)
        current = current.next
        
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None
    
    return dummy.next
```

## Time Complexity

- **Time:** O(max(m,n)) - where m and n are lengths of the lists
- **Space:** O(max(m,n)) - for the result list
""",
                "difficulty": "Medium",
                "tags": ["linked-list", "math", "recursion"],
            },
            {
                "title": "Maximum Subarray",
                "statement": """# Maximum Subarray (Kadane's Algorithm)

**Difficulty:** Medium  
**Topics:** arrays, dynamic-programming, algorithms  

## Problem Description

Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

A subarray is a contiguous part of an array.

## Input Format

- Line 1: An integer `n` (1 ≤ n ≤ 10⁵) - the length of the array
- Line 2: `n` space-separated integers (-10⁴ ≤ nums[i] ≤ 10⁴)

## Output Format

An integer representing the maximum sum of any contiguous subarray.

## Examples

**Example 1:**
```
Input:
9
-2 1 -3 4 -1 2 1 -5 4

Output:
6
Explanation: [4,-1,2,1] has the largest sum = 6.
```

**Example 2:**
```
Input:
1
1

Output:
1
```

**Example 3:**
```
Input:
5
5 4 -1 7 8

Output:
23
```

## Approach Hints

This problem involves: **arrays, dynamic-programming**

**Kadane's Algorithm (Optimal):**
1. Keep track of maximum sum ending at current position
2. At each step, decide: extend existing subarray or start new one
3. Update global maximum as you go

**Algorithm:**
```
max_so_far = nums[0]
max_ending_here = nums[0]

for i from 1 to n-1:
    max_ending_here = max(nums[i], max_ending_here + nums[i])
    max_so_far = max(max_so_far, max_ending_here)

return max_so_far
```

**Intuition:**
- If current sum becomes negative, start fresh from current element
- Always keep track of the best sum seen so far

## Time Complexity

- **Time:** O(n) - single pass through the array
- **Space:** O(1) - only using constant extra space

## Follow-up

If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
""",
                "difficulty": "Medium",
                "tags": ["arrays", "dynamic-programming", "algorithms"],
            },
            # HARD PROBLEMS
            {
                "title": "Merge k Sorted Lists",
                "statement": """# Merge k Sorted Lists

**Difficulty:** Hard  
**Topics:** linked-list, divide-and-conquer, heap, algorithms  

## Problem Description

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

Merge all the linked-lists into one sorted linked-list and return it.

## Input Format

- Line 1: An integer `k` (0 ≤ k ≤ 10⁴) - number of linked lists
- Next k lines: Each line contains space-separated integers representing a sorted linked list

## Output Format

Space-separated integers representing the merged sorted linked list.

## Examples

**Example 1:**
```
Input:
3
1 4 5
1 3 4
2 6

Output:
1 1 2 3 4 4 5 6
```

**Example 2:**
```
Input:
0

Output:
(empty)
```

**Example 3:**
```
Input:
1

Output:
(empty)
```

## Approach Hints

This problem involves: **linked-list, divide-and-conquer, heap**

**Method 1 - Priority Queue/Heap:**
1. Add first node of each list to min-heap
2. Extract minimum, add to result
3. Add next node from same list to heap
4. Repeat until heap is empty

**Method 2 - Divide and Conquer:**
1. Pair up lists and merge each pair
2. Repeat until only one list remains
3. Use merge function from "Merge Two Sorted Lists"

**Method 3 - Sequential Merging:**
1. Start with first list
2. Merge with second list
3. Merge result with third list, and so on

## Implementation (Divide and Conquer)

```python
def mergeKLists(lists):
    if not lists:
        return None
    
    while len(lists) > 1:
        merged_lists = []
        
        for i in range(0, len(lists), 2):
            l1 = lists[i]
            l2 = lists[i + 1] if i + 1 < len(lists) else None
            merged_lists.append(mergeTwoLists(l1, l2))
        
        lists = merged_lists
    
    return lists[0]
```

## Time Complexity

- **Divide & Conquer:** O(N log k) where N is total number of nodes
- **Priority Queue:** O(N log k)
- **Sequential:** O(kN)

## Space Complexity

- **Divide & Conquer:** O(log k) for recursion stack
- **Priority Queue:** O(k) for heap
""",
                "difficulty": "Hard",
                "tags": ["linked-list", "divide-and-conquer", "heap", "algorithms"],
            },
            {
                "title": "Trapping Rain Water",
                "statement": """# Trapping Rain Water

**Difficulty:** Hard  
**Topics:** arrays, two-pointers, dynamic-programming, stack  

## Problem Description

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

## Input Format

- Line 1: An integer `n` (1 ≤ n ≤ 2 × 10⁴) - the length of the array
- Line 2: `n` space-separated non-negative integers (0 ≤ height[i] ≤ 3 × 10⁴)

## Output Format

An integer representing the total amount of trapped rainwater.

## Examples

**Example 1:**
```
Input:
12
0 1 0 2 1 0 1 3 2 1 2 1

Output:
6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
```

**Example 2:**
```
Input:
6
4 2 0 3 2 5

Output:
9
```

## Approach Hints

This problem involves: **arrays, two-pointers, dynamic-programming, stack**

**Method 1 - Two Pointers (Optimal):**
1. Use left and right pointers
2. Keep track of left_max and right_max
3. Move pointer with smaller max height
4. Add trapped water when current height < max height

**Method 2 - Dynamic Programming:**
1. Precompute left_max array (max height to the left)
2. Precompute right_max array (max height to the right)
3. For each position: water = min(left_max, right_max) - height

**Method 3 - Stack:**
1. Use stack to store indices of bars
2. When current bar is higher than stack top, calculate trapped water
3. Pop from stack and calculate area

## Two Pointers Solution

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water
```

## Time Complexity

- **Two Pointers:** O(n) time, O(1) space
- **Dynamic Programming:** O(n) time, O(n) space
- **Stack:** O(n) time, O(n) space
""",
                "difficulty": "Hard",
                "tags": ["arrays", "two-pointers", "dynamic-programming", "stack"],
            },
        ]

        imported_count = 0

        for problem_data in curated_problems:
            # Skip if problem already exists
            existing = (
                self.session.query(Problem)
                .filter(Problem.title == problem_data["title"])
                .first()
            )
            if existing:
                logger.info(
                    f"Problem '{problem_data['title']}' already exists, skipping"
                )
                continue

            try:
                new_problem = Problem(**problem_data)
                self.session.add(new_problem)
                self.session.commit()
                imported_count += 1
                logger.info(f"Imported curated problem: {problem_data['title']}")

            except Exception as e:
                logger.error(f"Failed to save problem {problem_data['title']}: {e}")
                self.session.rollback()

        logger.info(f"Successfully imported {imported_count} curated problems")
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
    """CLI interface for the curated problem importer"""
    print("🚀 Curated Problem Importer - High-Quality Problems")
    print("=" * 55)
    print("✨ Import professionally crafted problems with full descriptions!")
    print("=" * 55)

    importer = CuratedProblemImporter()

    # Show current stats
    print("\n📊 Current Database Stats:")
    stats = importer.get_import_stats()
    print(f"   Total Problems: {stats.get('total_problems', 0)}")
    print(f"   Easy: {stats.get('difficulty_distribution', {}).get('Easy', 0)}")
    print(f"   Medium: {stats.get('difficulty_distribution', {}).get('Medium', 0)}")
    print(f"   Hard: {stats.get('difficulty_distribution', {}).get('Hard', 0)}")

    print("\n🎯 Available Problems to Import:")
    print("   📚 8 Curated Problems with Full Descriptions:")
    print("      • 3 Easy: Two Sum, Valid Parentheses, Palindrome Number")
    print("      • 3 Medium: Longest Substring, Add Two Numbers, Maximum Subarray")
    print("      • 2 Hard: Merge k Sorted Lists, Trapping Rain Water")

    print("\n🔥 Features:")
    print("   ✅ Complete problem descriptions")
    print("   ✅ Input/Output format specifications")
    print("   ✅ Multiple examples with explanations")
    print("   ✅ Algorithm hints and approaches")
    print("   ✅ Time/Space complexity analysis")
    print("   ✅ Implementation code snippets")

    choice = input("\n🚀 Import all curated problems? (y/n): ").strip().lower()

    if choice in ["y", "yes"]:
        print("\n📥 Importing curated problems...")
        count = importer.import_curated_problems()
        print(f"✅ Successfully imported {count} curated problems!")

        # Show updated stats
        print("\n📊 Updated Stats:")
        stats = importer.get_import_stats()
        print(f"   Total Problems: {stats.get('total_problems', 0)}")
        print(f"   Easy: {stats.get('difficulty_distribution', {}).get('Easy', 0)}")
        print(f"   Medium: {stats.get('difficulty_distribution', {}).get('Medium', 0)}")
        print(f"   Hard: {stats.get('difficulty_distribution', {}).get('Hard', 0)}")

        print("\n🎉 Your platform now has professional-quality problems!")
        print("   Go to the Judge page to see the enhanced problem descriptions!")

    else:
        print("👋 Import cancelled. Run again when ready!")


if __name__ == "__main__":
    main()
