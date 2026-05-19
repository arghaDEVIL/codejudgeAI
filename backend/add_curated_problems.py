#!/usr/bin/env python3
"""
Add curated problems directly to database
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.models.problem import Problem


def add_curated_problems():
    """Add curated problems with full descriptions"""

    db = SessionLocal()

    problems = [
        {
            "title": "Two Sum",
            "statement": """# Two Sum

**Difficulty:** Easy  
**Topics:** arrays, hash-table, algorithms  

## Problem Description

Given an array of integers `nums` and an integer `target`, return **indices** of the two numbers such that they add up to `target`.

You may assume that each input would have **exactly one solution**, and you may not use the same element twice.

You can return the answer in any order.

## Detailed Explanation

You are given an array of numbers and a target sum. Your task is to find two different numbers in the array that add up to the target. Instead of returning the numbers themselves, you need to return their positions (indices) in the array.

**Important Notes:**
- Array indices start from 0
- You cannot use the same element twice (e.g., if target is 6 and array has [3, 5], you cannot use 3 twice)
- There is always exactly one valid answer
- The order of indices in the output doesn't matter

## Input Format
- **Line 1:** An integer `n` (2 ≤ n ≤ 10⁴) - the length of the array
- **Line 2:** `n` space-separated integers representing the array `nums` (-10⁹ ≤ nums[i] ≤ 10⁹)
- **Line 3:** An integer `target` (-10⁹ ≤ target ≤ 10⁹)

## Output Format
Two space-separated integers representing the indices (0-indexed) of the two numbers that add up to the target.

## Examples

### Example 1
```
Input:
4
2 7 11 15
9

Output:
0 1

Explanation:
nums[0] + nums[1] = 2 + 7 = 9
So we return indices 0 and 1
```

### Example 2
```
Input:
3
3 2 4
6

Output:
1 2

Explanation:
nums[1] + nums[2] = 2 + 4 = 6
We cannot use nums[0] twice (3 + 3 = 6) because we need two different elements
```

### Example 3
```
Input:
2
3 3
6

Output:
0 1

Explanation:
nums[0] + nums[1] = 3 + 3 = 6
Here we have two different elements with the same value, which is allowed
```

### Example 4
```
Input:
5
-1 -2 -3 -4 -5
-8

Output:
2 4

Explanation:
nums[2] + nums[4] = -3 + (-5) = -8
The solution works with negative numbers too
```

## Approach Hints

### Brute Force Approach (O(n²))
Try all possible pairs of numbers:
```
for i from 0 to n-1:
    for j from i+1 to n-1:
        if nums[i] + nums[j] == target:
            return [i, j]
```

### Optimal Approach (O(n)) - Hash Map
Use a hash map to store numbers you've seen and their indices:

1. Create an empty hash map
2. For each number at index i:
   - Calculate complement = target - nums[i]
   - If complement exists in hash map, return [hash_map[complement], i]
   - Otherwise, store nums[i] and its index i in hash map
3. Continue until solution is found

**Why this works:** When we're at index i, we check if we've already seen the number that would complete the sum. If yes, we found our pair!

## Pseudocode
```
function twoSum(nums, target):
    hash_map = {}
    
    for i from 0 to length(nums)-1:
        complement = target - nums[i]
        
        if complement exists in hash_map:
            return [hash_map[complement], i]
        
        hash_map[nums[i]] = i
    
    return []  // No solution found (won't happen per problem constraints)
```

## Time & Space Complexity
- **Time Complexity:** O(n) - single pass through the array
- **Space Complexity:** O(n) - hash map can store up to n elements

## Edge Cases to Consider
- Array with exactly 2 elements (minimum size)
- Negative numbers in the array
- Target is 0
- Duplicate numbers in the array
- Large numbers (close to 10⁹)
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
1. Open brackets must be closed by the **same type** of brackets
2. Open brackets must be closed in the **correct order**
3. Every close bracket has a corresponding open bracket of the same type

## Detailed Explanation

Think of this like checking if parentheses in a mathematical expression are balanced. Each opening bracket must have a matching closing bracket of the same type, and they must be in the correct order.

**Valid Examples:**
- `()` - One pair of parentheses
- `()[]{}` - Three different types, all properly closed
- `{[]}` - Nested brackets, properly ordered

**Invalid Examples:**
- `(]` - Wrong closing bracket type
- `([)]` - Wrong order (should be `([])`)
- `{{{` - Opening brackets without closing

## Input Format
- **Line 1:** A string `s` consisting only of characters `'()[]{}'` (1 ≤ |s| ≤ 10⁴)

## Output Format
Print `true` if the string is valid, `false` otherwise.

## Examples

### Example 1
```
Input:
()

Output:
true

Explanation:
One opening parenthesis '(' followed by one closing parenthesis ')'
This is valid and balanced
```

### Example 2
```
Input:
()[]{}

Output:
true

Explanation:
Three pairs of brackets, each properly opened and closed:
- () - parentheses pair
- [] - square brackets pair
- {} - curly braces pair
All are in correct order
```

### Example 3
```
Input:
(]

Output:
false

Explanation:
Opening parenthesis '(' but closing with square bracket ']'
The types don't match, so it's invalid
```

### Example 4
```
Input:
([)]

Output:
false

Explanation:
The brackets are interleaved incorrectly:
- '(' opens
- '[' opens
- ')' closes the '(' but '[' is still open
- ']' closes the '[' but order is wrong

Correct version would be: ([])
```

### Example 5
```
Input:
{[]}

Output:
true

Explanation:
Properly nested brackets:
- '{' opens
- '[' opens
- ']' closes the '[' (correct)
- '}' closes the '{' (correct)
This follows the correct order
```

### Example 6
```
Input:
((

Output:
false

Explanation:
Two opening parentheses but no closing ones
Unbalanced - invalid
```

### Example 7
```
Input:
))

Output:
false

Explanation:
Two closing parentheses but no opening ones
Cannot close what wasn't opened - invalid
```

## Approach Hints

### Stack-Based Solution (Optimal)

A **stack** is perfect for this problem because:
- Last opened bracket should be first to close (LIFO - Last In First Out)
- We can track which brackets are currently "open"

**Algorithm:**
1. Create an empty stack
2. Iterate through each character in the string:
   - If it's an **opening bracket** `(`, `[`, or `{`:
     - Push it onto the stack
   - If it's a **closing bracket** `)`, `]`, or `}`:
     - Check if stack is empty (no matching opening bracket) → return false
     - Pop from stack and check if it matches:
       - `)` should match `(`
       - `]` should match `[`
       - `}` should match `{`
     - If doesn't match → return false
3. After processing all characters:
   - If stack is empty → return true (all brackets matched)
   - If stack has elements → return false (unmatched opening brackets)

## Pseudocode
```
function isValid(s):
    stack = []
    
    // Define matching pairs
    pairs = {')': '(', ']': '[', '}': '{'}
    
    for each character c in s:
        if c is opening bracket ('(', '[', '{'):
            stack.push(c)
        else:  // c is closing bracket
            if stack is empty:
                return false
            
            if stack.top() != pairs[c]:
                return false
            
            stack.pop()
    
    return stack is empty
```

## Step-by-Step Example

Let's trace through `"([])"`

| Step | Character | Action | Stack | Valid? |
|------|-----------|--------|-------|--------|
| 1 | `(` | Push | `['(']` | ✓ |
| 2 | `[` | Push | `['(', '[']` | ✓ |
| 3 | `]` | Pop & Match `[` | `['(']` | ✓ |
| 4 | `)` | Pop & Match `(` | `[]` | ✓ |
| End | - | Stack empty | `[]` | **true** |

Now let's trace through `"([)]"` (invalid)

| Step | Character | Action | Stack | Valid? |
|------|-----------|--------|-------|--------|
| 1 | `(` | Push | `['(']` | ✓ |
| 2 | `[` | Push | `['(', '[']` | ✓ |
| 3 | `)` | Try to match | `['(', '[']` | ✗ |
|  |  | Top is `[`, not `(` |  | **false** |

## Time & Space Complexity
- **Time Complexity:** O(n) - single pass through the string
- **Space Complexity:** O(n) - worst case all opening brackets (e.g., "((((")

## Edge Cases to Consider
- Empty string (should return true)
- Single character (always false)
- Only opening brackets
- Only closing brackets
- Very long strings (up to 10,000 characters)
- Deeply nested brackets
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

Given an integer array `nums`, find the **contiguous subarray** (containing at least one number) which has the largest sum and return its sum.

A **subarray** is a contiguous part of an array (elements must be adjacent).

## Detailed Explanation

You need to find a sequence of consecutive numbers in the array that gives you the maximum possible sum. The subarray can be:
- The entire array
- A portion of the array
- A single element

**Key Points:**
- Must be contiguous (no skipping elements)
- Must contain at least one element
- Can include negative numbers
- The subarray with maximum sum might be anywhere in the array

## Input Format
- **Line 1:** An integer `n` (1 ≤ n ≤ 10⁵) - the length of the array
- **Line 2:** `n` space-separated integers (-10⁴ ≤ nums[i] ≤ 10⁴)

## Output Format
An integer representing the maximum sum of any contiguous subarray.

## Examples

### Example 1
```
Input:
9
-2 1 -3 4 -1 2 1 -5 4

Output:
6

Explanation:
The subarray [4, -1, 2, 1] has the largest sum = 6

Let's see why:
- Starting at index 3: 4
- Add index 4: 4 + (-1) = 3
- Add index 5: 3 + 2 = 5
- Add index 6: 5 + 1 = 6
- If we add index 7: 6 + (-5) = 1 (worse, so we stop)

Other subarrays and their sums:
- [-2] = -2
- [1] = 1
- [-3] = -3
- [4] = 4
- [4, -1] = 3
- [4, -1, 2] = 5
- [4, -1, 2, 1] = 6 ← Maximum!
```

### Example 2
```
Input:
1
1

Output:
1

Explanation:
Only one element, so the maximum sum is that element itself
```

### Example 3
```
Input:
5
5 4 -1 7 8

Output:
23

Explanation:
The entire array [5, 4, -1, 7, 8] gives the maximum sum
5 + 4 + (-1) + 7 + 8 = 23

Even though -1 is negative, including it gives us a better total
because the positive numbers after it are large enough
```

### Example 4
```
Input:
3
-2 -3 -1

Output:
-1

Explanation:
All numbers are negative, so we pick the least negative one
The subarray [-1] has the maximum sum = -1
```

### Example 5
```
Input:
6
-2 1 -3 4 -1 2

Output:
4

Explanation:
Multiple subarrays could work:
- [4] = 4
- [4, -1, 2] = 5

Wait, [4, -1, 2] = 5 is actually better!
Let me recalculate: 4 + (-1) + 2 = 5

So the answer should be 5, not 4.
The subarray [4, -1, 2] has the maximum sum = 5
```

### Example 6
```
Input:
7
1 2 3 -10 5 6 7

Output:
18

Explanation:
We have two potential subarrays:
- [1, 2, 3] = 6
- [5, 6, 7] = 18 ← Maximum!

Including -10 would give us: 1+2+3-10+5+6+7 = 14 (worse)
So it's better to start fresh from 5
```

## Approach Hints

### Brute Force Approach (O(n²))
Try all possible subarrays:
```
max_sum = -infinity

for start from 0 to n-1:
    current_sum = 0
    for end from start to n-1:
        current_sum += nums[end]
        max_sum = max(max_sum, current_sum)

return max_sum
```

### Kadane's Algorithm (O(n)) - Optimal

This is a classic dynamic programming problem with an elegant solution!

**Key Insight:** At each position, we decide:
- Should we extend the previous subarray? (add current element to previous sum)
- Or start a new subarray from here? (current element alone)

**Algorithm:**
1. Initialize:
   - `max_so_far` = first element (best sum found so far)
   - `max_ending_here` = first element (best sum ending at current position)

2. For each element from index 1 to n-1:
   - `max_ending_here` = max(nums[i], max_ending_here + nums[i])
     - This decides: start fresh OR extend previous subarray
   - `max_so_far` = max(max_so_far, max_ending_here)
     - Update global maximum if current is better

3. Return `max_so_far`

**Why it works:** 
- If adding current element to previous sum makes it worse than the element alone, start fresh
- Always keep track of the best sum we've seen

## Pseudocode
```
function maxSubArray(nums):
    max_so_far = nums[0]
    max_ending_here = nums[0]
    
    for i from 1 to length(nums)-1:
        // Decide: extend previous subarray or start new one
        max_ending_here = max(nums[i], max_ending_here + nums[i])
        
        // Update global maximum
        max_so_far = max(max_so_far, max_ending_here)
    
    return max_so_far
```

## Step-by-Step Trace

Let's trace through `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| i | nums[i] | max_ending_here | max_so_far | Decision |
|---|---------|-----------------|------------|----------|
| 0 | -2 | -2 | -2 | Start |
| 1 | 1 | 1 | 1 | Start fresh (1 > -2+1=-1) |
| 2 | -3 | -2 | 1 | Extend (1+(-3)=-2 > -3) |
| 3 | 4 | 4 | 4 | Start fresh (4 > -2+4=2) |
| 4 | -1 | 3 | 4 | Extend (4+(-1)=3 > -1) |
| 5 | 2 | 5 | 5 | Extend (3+2=5 > 2) |
| 6 | 1 | 6 | 6 | Extend (5+1=6 > 1) |
| 7 | -5 | 1 | 6 | Extend (6+(-5)=1 > -5) |
| 8 | 4 | 5 | 6 | Extend (1+4=5 > 4) |

**Final Answer:** 6

## Time & Space Complexity
- **Time Complexity:** O(n) - single pass through the array
- **Space Complexity:** O(1) - only using constant extra space

## Edge Cases to Consider
- Array with one element
- All negative numbers
- All positive numbers
- Mix of positive and negative
- Very large arrays (up to 100,000 elements)
- Maximum/minimum integer values

## Follow-up Challenge
Can you also return the actual subarray (start and end indices) that gives the maximum sum?
""",
            "difficulty": "Medium",
            "tags": ["arrays", "dynamic-programming", "algorithms"],
        },
    ]

    imported_count = 0

    try:
        for problem_data in problems:
            # Check if problem already exists
            existing = (
                db.query(Problem).filter(Problem.title == problem_data["title"]).first()
            )
            if existing:
                print(f"Problem '{problem_data['title']}' already exists, skipping")
                continue

            # Create new problem
            new_problem = Problem(**problem_data)
            db.add(new_problem)
            db.commit()
            imported_count += 1
            print(f"✅ Imported: {problem_data['title']}")

        print(f"\n🎉 Successfully imported {imported_count} curated problems!")

        # Show stats
        total = db.query(Problem).count()
        easy = db.query(Problem).filter(Problem.difficulty == "Easy").count()
        medium = db.query(Problem).filter(Problem.difficulty == "Medium").count()
        hard = db.query(Problem).filter(Problem.difficulty == "Hard").count()

        print(f"\n📊 Updated Stats:")
        print(f"   Total Problems: {total}")
        print(f"   Easy: {easy}")
        print(f"   Medium: {medium}")
        print(f"   Hard: {hard}")

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Adding Curated Problems...")
    print("=" * 40)
    add_curated_problems()
