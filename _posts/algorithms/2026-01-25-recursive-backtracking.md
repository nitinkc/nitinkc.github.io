---
title: Recursive Backtracking - Step by Step Guide
date: 2026-01-25 13:05:00
categories:
- Algorithms
tags:
- Recursion
- Backtracking
---

{% include toc title="Index" %}

Recursive backtracking is a powerful algorithmic technique used to solve problems incrementally by 
trying partial solutions and **abandoning them if they are not valid**. 

It is commonly used in constraint satisfaction problems, combinatorial optimization, and puzzles.

## What is Backtracking?

**Backtracking** is like solving a maze:
- You try a path
- If it leads to a dead end, you **go back** (backtrack) and try a different path
- You continue until you find the solution or exhaust all possibilities

### The Basic Pattern

Every backtracking problem follows this template:

Backtracking solutions generally involve two different base cases. 
- You tend to stop the backtracking when you find a solution, so that becomes one of our base cases. 
- be on the lookout for what is called a dead-end

 ```java
 boolean solve(parameters) {
    // Base case: Check if we found a solution
    if (goalReached()) {
        return true;
    }
    
    // Base case: Check if this path is invalid
    if (invalidPath()) {
        return false;
    }
    
    // Recursive case: Try all possible choices
    for (each choice) {
        // 1. Make a choice
        makeChoice();
        
        // 2. Recursively explore with this choice
        if (solve(newParameters)) {
            return true;  // Found solution!
        }
        
        // 3. Undo the choice (backtrack)
        unmakeChoice();
    }
    
    // No solution found
    return false;
}
```

---

## Level 1: The Simplest Backtracking - Binary Choices
[https://codingbat.com/java/Recursion-2](https://codingbat.com/java/Recursion-2)

Let's start with the absolute simplest backtracking pattern: **include or exclude** each element.

### Problem 1.1: Find All Subsets (Warmup)

**Problem**: Given `[1, 2]`, find all possible subsets.

**Think**: For each number, you have 2 choices: **include it** or **don't include it**.

```
[1, 2] → 
  - Include nothing: []
  - Include 1 only: [1]
  - Include 2 only: [2]  
  - Include both: [1, 2]
```

**Decision Tree**:
```
                    Start []
                   /        \
            include 1      exclude 1
              [1]             []
             /   \           /   \
        incl 2  excl 2   incl 2  excl 2
        [1,2]    [1]      [2]      []
```

**Code**:
```java
public static List<List<Integer>> subsets(int[] nums) {
   List<List<Integer>> result = new ArrayList<>();
   backtrack(0, nums, new ArrayList<>(), result);//Helper method returns void and fills result as an argument
   return result;
}

private static void backtrack(int idx, int[] nums, List<Integer> current, List<List<Integer>> result) {
   // base case: we've considered all elements
   if (idx == nums.length) {
      result.add(new ArrayList<>(current)); // add a copy
      return;
   }

   // Decision 1: exclude nums[idx]
   backtrack(idx + 1, nums, current, result);

   // Decision 2: include nums[idx]
   current.add(nums[idx]);
   backtrack(idx + 1, nums, current, result);
   current.remove(current.size() - 1); // backtrack
}
```
**Key Insight**: The `current.remove()` at the end is the **backtracking** step - we undo our choice before returning.

---

### Problem 1.2: Can Sum to Target? (Subset Sum)
[https://codingbat.com/prob/p145416](https://codingbat.com/prob/p145416)

**Problem**: Given numbers `[2, 3, 7]` and target `10`, can we pick some numbers that sum to exactly 10?

**Answer**: Yes! `3 + 7 = 10` ✓

**Think**: Same as subsets, but we **stop early** when we find a valid sum.

**Simple Version**
```java
public boolean groupSum(int start, int[] nums, int target) {
  if(start >= nums.length) return target==0;
  
  //If chosen
  if(groupSum(start+1,nums,target-nums[start])) return true;
  
  //If not chosen
  if(groupSum(start+1,nums,target)) return true;
  
  return false;

}
```
**More Efficient**
```java
public boolean canSum(int[] nums, int target) {
    return canSum(nums, 0, 0, target);
}

private boolean canSum(int[] nums, int index, int currentSum, int target) {
    // Base case 1: Found the target!
    if (currentSum == target) {
        return true;
    }
    
    // Base case 2: Went too far or ran out of numbers
    if (currentSum > target || index == nums.length) {
        return false;
    }
    
    // Choice 1: Include this number
    if (canSum(nums, index + 1, currentSum + nums[index], target)) {
        return true;
    }
    
    // Choice 2: Skip this number
    if (canSum(nums, index + 1, currentSum, target)) {
        return true;
    }
    
    return false;
}
```

**Trace** for `[2, 3, 7]`, target = `10`:
```
canSum(index=0, sum=0)
├─ Include 2 → canSum(index=1, sum=2)
│  ├─ Include 3 → canSum(index=2, sum=5)
│  │  ├─ Include 7 → sum=12 > 10 → FALSE (too big!)
│  │  └─ Skip 7 → sum=5, index=3 (end) → FALSE
│  └─ Skip 3 → canSum(index=2, sum=2)
│     ├─ Include 7 → sum=9, index=3 (end) → FALSE
│     └─ Skip 7 → sum=2, index=3 (end) → FALSE
└─ Skip 2 → canSum(index=1, sum=0)
   ├─ Include 3 → canSum(index=2, sum=3)
   │  ├─ Include 7 → sum=10 = target → TRUE ✓
```

---

## Level 2: Balance Scale Problems ⚖️

Now let's tackle the classic **canBalance** problem from [CodeStepByStep](https://www.codestepbystep.com/r/problem/view/java/backtracking/canBalance).

### Problem 2.1: Can Balance (CodeStepByStep Version)

**Problem**: You have a bag of weights and a balance scale. Can you place the weights on two sides so the scale balances?

**Rules**:
- You have an empty scale (nothing on either side initially)
- Each weight MUST go on one side (LEFT or RIGHT) - **no skipping**
- Goal: left side total = right side total

**Example 1**: `[1, 2, 3]`
```
    LEFT          RIGHT
   ──────        ──────
    1, 2            3
   ──────        ──────
   Total: 3      Total: 3  ✓ BALANCED!
```
Answer: `true`

**Example 2**: `[1, 2]`
- Try: left=[1], right=[2] → 1 ≠ 2 ✗
- Try: left=[2], right=[1] → 2 ≠ 1 ✗
- Try: left=[1,2], right=[] → 3 ≠ 0 ✗
- Try: left=[], right=[1,2] → 0 ≠ 3 ✗
Answer: `false`

**Think**: For each weight, we have **2 choices**: put on LEFT or put on RIGHT.

```java
public boolean canBalance(List<Integer> weights) {
    return canBalance(weights, 0, 0, 0);
}

private boolean canBalance(List<Integer> weights, int index, 
                           int leftSum, int rightSum) {
    // Base case: placed all weights
    if (index == weights.size()) {
        return leftSum == rightSum;
    }
    
    int weight = weights.get(index);
    
    // Choice 1: Put weight on LEFT side
    if (canBalance(weights, index + 1, leftSum + weight, rightSum)) {
        return true;
    }
    
    // Choice 2: Put weight on RIGHT side
    if (canBalance(weights, index + 1, leftSum, rightSum + weight)) {
        return true;
    }
    
    return false;
}
```

**Trace** for `[1, 2, 3]`:
```
canBalance(index=0, left=0, right=0)
├─ Put 1 on LEFT → canBalance(index=1, left=1, right=0)
│  ├─ Put 2 on LEFT → canBalance(index=2, left=3, right=0)
│  │  ├─ Put 3 on LEFT → (left=6, right=0) → FALSE
│  │  └─ Put 3 on RIGHT → (left=3, right=3) → TRUE ✓ FOUND!
```

**Test Cases**:
```java
canBalance([1, 2, 3])          → true  (left: 1,2  right: 3)
canBalance([1, 2])             → false (no way to balance)
canBalance([1, 1])             → true  (left: 1  right: 1)
canBalance([1, 2, 1, 2])       → true  (left: 1,2  right: 1,2)
canBalance([7])                → false (can't split single item)
canBalance([7, 7])             → true  (left: 7  right: 7)
canBalance([6, 3, 2, 1])       → true  (left: 6  right: 3,2,1)
```

---

### Problem 2.2: Balance Scale with Target Weight

**Different Problem**: What if there's already a target weight on one side?

**Problem**: Target weight is on the LEFT. You have a bag of weights. Can you balance the scale? You can put weights on either side OR leave them unused.

**Example**: Target = `5`, Bag = `[1, 2, 6]`
```
    LEFT          RIGHT
   ──────        ──────
      5             6
      1            ---
   ──────        ──────
   Total: 6      Total: 6  ✓ BALANCED!
   
(Weight 2 is unused)
```

**Think**: Now we have **3 choices** per weight: LEFT, RIGHT, or SKIP.

```java
public boolean canBalanceWithTarget(int target, List<Integer> weights) {
    return canBalanceWithTarget(weights, 0, target, 0);
}

private boolean canBalanceWithTarget(List<Integer> weights, int index, 
                                      int leftSum, int rightSum) {
    // Base case: processed all weights
    if (index == weights.size()) {
        return leftSum == rightSum;
    }
    
    int weight = weights.get(index);
    
    // Choice 1: Add to LEFT side (with target)
    if (canBalanceWithTarget(weights, index + 1, leftSum + weight, rightSum)) {
        return true;
    }
    
    // Choice 2: Add to RIGHT side
    if (canBalanceWithTarget(weights, index + 1, leftSum, rightSum + weight)) {
        return true;
    }
    
    // Choice 3: Don't use this weight
    if (canBalanceWithTarget(weights, index + 1, leftSum, rightSum)) {
        return true;
    }
    
    return false;
}
```

**Trace** for Target=5, Bag=[1, 2, 6]:
```
canBalance(index=0, left=5, right=0)
├─ Put 1 on LEFT → (index=1, left=6, right=0)
│  ├─ Put 2 on LEFT → (index=2, left=8, right=0)
│  │  └─ ... all paths fail
│  ├─ Put 2 on RIGHT → (index=2, left=6, right=2)
│  │  └─ ... all paths fail
│  └─ Skip 2 → (index=2, left=6, right=0)
│     ├─ Put 6 on LEFT → (left=12, right=0) → FALSE
│     ├─ Put 6 on RIGHT → (left=6, right=6) → TRUE ✓
```

---

### Comparison: Two Similar Problems

| Feature | canBalance (CodeStepByStep) | canBalanceWithTarget |
|---------|----------------------------|----------------------|
| Starting state | Both sides empty | Target on left |
| Choices per weight | 2 (left/right) | 3 (left/right/skip) |
| Must use all weights? | YES | NO |
| Branches in tree | 2^n | 3^n |


---

## Level 2.5: String Interleaving Problem

This is a fantastic backtracking problem from [CodeStepByStep](https://www.codestepbystep.com/r/problem/view/java/backtracking/canInterleave).

### Problem 2.3: Can Interleave Strings

**Problem**: Given three strings `s1`, `s2`, and `s3`, determine if `s3` can be formed by interleaving characters from `s1` and `s2` while maintaining the **relative order** of characters in each string.

**Example**: `canInterleave("aabcc", "dbbca", "aadbbcbcac")` → `true`

```
s1 = "aabcc"
s2 = "dbbca"  
s3 = "aadbbcbcac"

Building s3:
  a  a  d  b  b  c  b  c  a  c
  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑  ↑
  s1 s1 s2 s2 s1 s1 s2 s2 s2 s1
  
s1: a → a → b → c → c  ✓ (same order)
s2: d → b → b → c → a  ✓ (same order)
```

**Why Backtracking is Essential Here**:

At some positions, **BOTH** s1 and s2 might have the matching character:
```
s1 = "aabcc"    s2 = "dbbca"    s3 = "aadbbcbcac"
          ^              ^               ^
       idx1=2         idx2=2          idx3=4
       
s3[4] = 'b' → s1[2]='b' matches AND s2[2]='b' matches!
Which do we pick? Try s1 first, if it fails, BACKTRACK and try s2.
```

**Code (Index-based approach)**:

```java
public boolean canInterleave(String s1, String s2, String s3) {
    // Quick check: lengths must add up
    if (s1.length() + s2.length() != s3.length()) {
        return false;
    }
    return helper(s1, 0, s2, 0, s3, 0);
}

private boolean helper(String s1, int idx1, String s2, int idx2, String s3, int idx3) {
    // Base case: consumed all characters from all strings
    if (idx1 == s1.length() && idx2 == s2.length() && idx3 == s3.length()) {
        return true;
    }
    
    // Base case: consumed s3 but not s1/s2 (shouldn't happen if lengths match)
    if (idx3 == s3.length()) {
        return false;
    }
    
    char currChar = s3.charAt(idx3);
    
    // Choice 1: Try taking from s1 (if chars remain AND it matches)
    if (idx1 < s1.length() && s1.charAt(idx1) == currChar) {
        if (helper(s1, idx1 + 1, s2, idx2, s3, idx3 + 1)) {
            return true;  // Found a valid interleaving!
        }
        // If this path fails, backtrack and try s2 below
    }
    
    // Choice 2: Try taking from s2 (if chars remain AND it matches)
    if (idx2 < s2.length() && s2.charAt(idx2) == currChar) {
        if (helper(s1, idx1, s2, idx2 + 1, s3, idx3 + 1)) {
            return true;
        }
    }
    
    // Neither choice worked
    return false;
}
```

**Alternative Code (Substring approach - often expected by CodeStepByStep)**:

Some online judges expect you to work with substrings directly:

```java
public boolean canInterleave(String s1, String s2, String s3) {
    // Base case: all strings empty
    if (s1.isEmpty() && s2.isEmpty() && s3.isEmpty()) {
        return true;
    }
    
    // Base case: s3 is empty but s1 or s2 still has characters
    if (s3.isEmpty()) {
        return false;
    }
    
    // Quick length check
    if (s1.length() + s2.length() != s3.length()) {
        return false;
    }
    
    char currChar = s3.charAt(0);
    
    // Choice 1: Try taking first char from s1
    if (!s1.isEmpty() && s1.charAt(0) == currChar) {
        if (canInterleave(s1.substring(1), s2, s3.substring(1))) {
            return true;
        }
    }
    
    // Choice 2: Try taking first char from s2
    if (!s2.isEmpty() && s2.charAt(0) == currChar) {
        if (canInterleave(s1, s2.substring(1), s3.substring(1))) {
            return true;
        }
    }
    
    return false;
}
```

**Note**: The substring approach is less efficient (creates new String objects) but matches how CodeStepByStep often structures these problems.

**⚠️ Common Bugs to Avoid**:

1. **Using `idx++` instead of `idx + 1`**:
   ```java
   helper(s1, idx1++, ...)  // ❌ WRONG - passes OLD value, then increments
   helper(s1, idx1 + 1, ...) // ✅ CORRECT - passes incremented value
   ```

2. **Using if-else instead of two separate if's**:
   ```java
   // ❌ WRONG - if s1 matches but path fails, never tries s2
   if (s1.charAt(idx1) == currChar)
       return helper(s1, idx1 + 1, ...);
   else if (s2.charAt(idx2) == currChar)
       return helper(s1, idx1, ...);
   
   // ✅ CORRECT - tries s1, if fails, tries s2
   if (s1.charAt(idx1) == currChar) {
       if (helper(s1, idx1 + 1, ...)) return true;
   }
   if (s2.charAt(idx2) == currChar) {
       if (helper(s1, idx1, ...)) return true;
   }
   ```

3. **Forgetting bounds check before `charAt()`**:
   ```java
   // ❌ Crashes when idx1 >= s1.length()
   if (s1.charAt(idx1) == currChar)
   
   // ✅ Check bounds first
   if (idx1 < s1.length() && s1.charAt(idx1) == currChar)
   ```

**Trace** for `canInterleave("ab", "cd", "acbd")`:
```
helper(idx1=0, idx2=0, idx3=0)  currChar='a'
├─ s1[0]='a' matches → try s1
│  helper(idx1=1, idx2=0, idx3=1)  currChar='c'
│  ├─ s1[1]='b' ≠ 'c'
│  └─ s2[0]='c' matches → try s2
│     helper(idx1=1, idx2=1, idx3=2)  currChar='b'
│     ├─ s1[1]='b' matches → try s1
│     │  helper(idx1=2, idx2=1, idx3=3)  currChar='d'
│     │  ├─ idx1=2 out of bounds for s1
│     │  └─ s2[1]='d' matches → try s2
│     │     helper(idx1=2, idx2=2, idx3=4)
│     │     └─ All indices at end → TRUE ✓
```

**Test Cases**:
```java
canInterleave("aabcc", "dbbca", "aadbbcbcac") → true
canInterleave("aabcc", "dbbca", "aadbbbaccc") → false
canInterleave("", "", "")                      → true
canInterleave("a", "", "a")                    → true
canInterleave("", "b", "b")                    → true
canInterleave("ab", "cd", "acbd")              → true
canInterleave("ab", "cd", "abcd")              → true
canInterleave("ab", "cd", "cadb")              → true
canInterleave("abc", "dde", "addce")           → false (missing 'b')
```

---

## Level 3: Permutations and Arrangements

Now let's move to problems where **order matters** and we need to track what's been used.

### Problem 3.1: Generate All Permutations

**Problem**: Given `[1, 2, 3]`, generate all possible arrangements.

**Output**: `[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]`

**Key Difference from Subsets**:
- Subsets: Each element included or excluded (2 choices)
- Permutations: Each position can be ANY unused element (n choices for 1st, n-1 for 2nd, etc.)

**Think**: We need to track which elements we've already used.

```java
public List<List<Integer>> permute(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, new ArrayList<>(), new boolean[nums.length], result);
    return result;
}

private void backtrack(int[] nums, List<Integer> current, 
                       boolean[] used, List<List<Integer>> result) {
    // Base case: permutation is complete
    if (current.size() == nums.length) {
        result.add(new ArrayList<>(current));
        return;
    }
    
    // Try each number that hasn't been used yet
    for (int i = 0; i < nums.length; i++) {
        if (used[i]) continue;  // Skip if already used
        
        // Make choice
        current.add(nums[i]);
        used[i] = true;
        
        // Recurse
        backtrack(nums, current, used, result);
        
        // Undo choice (backtrack)
        current.remove(current.size() - 1);
        used[i] = false;
    }
}
```

**Visual Decision Tree** for `[1, 2]`:
```
                      []
        ┌──────────────┴──────────────┐
     pick 1                         pick 2
       [1]                            [2]
        │                              │
     pick 2                         pick 1
      [1,2]                          [2,1]
```

---

### Problem 3.2: Generate All Subsets (Return List Version)

Going back to subsets, but now returning the result:

```java
public List<List<Integer>> subsets(int[] nums) {
    List<List<Integer>> result = new ArrayList<>();
    backtrack(nums, 0, new ArrayList<>(), result);
    return result;
}

private void backtrack(int[] nums, int index, List<Integer> current, 
                       List<List<Integer>> result) {
    // Base case: processed all elements
    if (index == nums.length) {
        result.add(new ArrayList<>(current));  // Make a COPY!
        return;
    }
    
    // Choice 1: Don't include nums[index]
    backtrack(nums, index + 1, current, result);
    
    // Choice 2: Include nums[index]
    current.add(nums[index]);
    backtrack(nums, index + 1, current, result);
    current.remove(current.size() - 1);  // Backtrack!
}
```

**⚠️ Common Bug**: Forgetting `new ArrayList<>(current)` - if you just add `current`, all results will be empty because `current` gets emptied by backtracking!

---

## Level 4: Grid and Board Problems

The most complex backtracking problems involve navigating grids or placing items with constraints.

### Problem 4.1: N-Queens

**Problem**: Place N chess queens on an N×N board so no two queens attack each other.

**Think**: Place one queen per row. For each row, try each column. Check if placement is safe.

```java
public List<List<String>> solveNQueens(int n) {
    List<List<String>> result = new ArrayList<>();
    char[][] board = new char[n][n];
    
    // Initialize board with empty cells
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            board[i][j] = '.';
        }
    }
    
    backtrack(board, 0, result);
    return result;
}

private void backtrack(char[][] board, int row, List<List<String>> result) {
    // Base case: placed all queens
    if (row == board.length) {
        result.add(constructBoard(board));
        return;
    }
    
    // Try placing queen in each column of current row
    for (int col = 0; col < board.length; col++) {
        if (isSafe(board, row, col)) {
            board[row][col] = 'Q';           // Make choice
            backtrack(board, row + 1, result);
            board[row][col] = '.';           // Backtrack
        }
    }
}

private boolean isSafe(char[][] board, int row, int col) {
    int n = board.length;
    
    // Check column (only need to check rows above)
    for (int i = 0; i < row; i++) {
        if (board[i][col] == 'Q') return false;
    }
    
    // Check diagonal (top-left)
    for (int i = row - 1, j = col - 1; i >= 0 && j >= 0; i--, j--) {
        if (board[i][j] == 'Q') return false;
    }
    
    // Check diagonal (top-right)
    for (int i = row - 1, j = col + 1; i >= 0 && j < n; i--, j++) {
        if (board[i][j] == 'Q') return false;
    }
    
    return true;
}

private List<String> constructBoard(char[][] board) {
    List<String> result = new ArrayList<>();
    for (char[] row : board) {
        result.add(new String(row));
    }
    return result;
}
```

**4-Queens Solution Example**:
```
. Q . .      . . Q .
. . . Q      Q . . .
Q . . .      . . . Q
. . Q .      . Q . .
```

---

## Key Patterns Summary

### Pattern 1: Include/Exclude (Binary Choice)
```
For each element: include OR exclude
Examples: Subsets, Subset Sum, canBalance
Branches: 2^n
```

### Pattern 2: Multiple Choices per Element
```
For each element: multiple options (e.g., left/right/skip)
Examples: Balance with target, Expression operators
Branches: 3^n or k^n
```

### Pattern 3: Permutations
```
For each position: pick any unused element
Track: boolean[] used or remaining list
Branches: n!
```

### Pattern 4: Combinations
```
Pick k elements from n, order doesn't matter
Key: Start from current index (avoid [1,2] and [2,1])
Branches: C(n,k)
```

### Pattern 5: Grid Navigation
```
For each cell: try valid moves
Constraints: bounds, visited, validity checks
Examples: N-Queens, Sudoku, Word Search
```

---

## Common Optimizations

### 1. Early Termination (Pruning)
Stop exploring paths that can't possibly lead to a solution:

```java
// If sum already exceeds target, stop
if (currentSum > target) return false;

// If remaining elements can't possibly reach target
int remaining = totalSum - processedSum;
if (currentSum + remaining < target) return false;
```

### 2. Memoization
Cache results for repeated subproblems:

```java
Map<String, Boolean> memo = new HashMap<>();

private boolean solve(int index, int sum1, int sum2) {
    String key = index + "," + sum1 + "," + sum2;
    if (memo.containsKey(key)) {
        return memo.get(key);
    }
    
    boolean result = // ... recursive logic
    memo.put(key, result);
    return result;
}
```

### 3. Sorting for Better Pruning
```java
Arrays.sort(nums);  // Now can break early when elements too large
```

---

## Practice Problems (Ordered by Difficulty)

### Beginner
1. **[Print All Subsets](https://www.codestepbystep.com/r/problem/view/java/backtracking/printAllSubsets)** - Foundation of backtracking
2. **[Can Balance](https://www.codestepbystep.com/r/problem/view/java/backtracking/canBalance)** - Balance scale problem

### Intermediate
3. **[Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum/)** - Can split array into two equal halves?
4. **[Letter Combinations of Phone](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)** - Multiple choices per digit
5. **[Combination Sum](https://leetcode.com/problems/combination-sum/)** - Find all combinations summing to target
6. **[Permutations](https://leetcode.com/problems/permutations/)** - Generate all orderings

### Advanced
7. **[Word Search](https://leetcode.com/problems/word-search/)** - Find word in 2D grid
8. **[N-Queens](https://leetcode.com/problems/n-queens/)** - Classic constraint satisfaction
9. **[Palindrome Partitioning](https://leetcode.com/problems/palindrome-partitioning/)** - Partition into palindromes
10. **[Sudoku Solver](https://leetcode.com/problems/sudoku-solver/)** - Solve 9x9 Sudoku

### Expert
11. **[Expression Add Operators](https://leetcode.com/problems/expression-add-operators/)** - Add +, -, * to reach target
12. **[Word Search II](https://leetcode.com/problems/word-search-ii/)** - Find multiple words with Trie

---

## Debugging Tips

### 1. Add Debug Prints
```java
private boolean solve(int index, int left, int right, int depth) {
    String indent = "  ".repeat(depth);
    System.out.println(indent + "index=" + index + ", left=" + left + ", right=" + right);
    
    // ... rest of code with depth + 1 in recursive calls
}
```

### 2. Test Smallest Cases First
```java
// Test with size 1-2 before larger inputs
canBalance([1])        // false
canBalance([1, 1])     // true
canBalance([1, 2])     // false
canBalance([1, 2, 3])  // true
```

### 3. Common Mistakes Checklist
- [ ] Base case handles all termination conditions?
- [ ] Backtracking (undo) happens after recursive call?
- [ ] Making a COPY when adding to result list?
- [ ] Index bounds checked properly?
- [ ] All choices explored (not just first one)?

---

## Summary

**The Backtracking Recipe**:
```
1. Identify the CHOICES at each step
2. MAKE a choice
3. RECURSE to explore that choice
4. CHECK if solution found → return success
5. UNDO the choice (backtrack)
6. TRY next choice
7. Return failure if no choice worked
```

**Remember**: Backtracking = DFS on a decision tree. Every node is a partial solution, every edge is a choice, every leaf is a complete solution (valid or invalid).

**The key insight**: Don't be afraid of trying "wrong" choices - that's the whole point! The algorithm systematically explores ALL possibilities, so you're guaranteed to find a solution if one exists.
