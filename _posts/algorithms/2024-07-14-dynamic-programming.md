---
title: Dynamic Programming - DP
date: 2024-07-14 18:27:00
categories:
- Algorithms
tags:
- Recursion
- Dynamic Programming
---

{% include toc title="Index" %}

The common characteristics of problems that can be solved with dynamic programming are:
- **the optimum value** (maximum or minimum)
- or **the number of ways**
- future "**decisions**" depend on earlier decisions
    - This characteristic makes a greedy algorithm invalid for a DP problem
- If you can think of an example where **earlier decisions affect future
  decisions**, then DP is applicable.

## Mnemonics to remember:

> Bottom-up (Tabulation) = “build the table” / think `array`.

> Top-down (Memoization)= “start from the goal” / think `recursion + cache`.

# Bottom-up (Tabulation)
- Build answers from the smallest subproblems upward into a table/array until you reach the target.
- bottom-up implementations usually use an array

The Climbing Stairs problem — a Fibonacci-like DP
- [Climbing Stairs Problem](https://leetcode.com/problems/climbing-stairs/description/){:target="_blank"}
- [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/description/){:target="_blank"}
  ```java
  public int dp(int n) {
      if (n == 1) return 1;
      // The array's length should be 1 longer than the length of the problem input 
      // to accommodate the base cases and the final result at index n
      int[] dp = new int[n + 1];//beginning from index = 1
      dp[1] = 1; // Base cases
      dp[2] = 2; // Base cases
      for (int i = 3; i <= n; i++) {
          dp[i] = dp[i - 1] + dp[i - 2]; // Recurrence relation
      }
      return dp[n];
  ```

# Top-down (Memoization)
- Start at the final goal, recursively break it into subgoals, and cache results to avoid recomputation.
- Visualize an exploration tree that gets pruned by a memo cache.
- Natural for complex recurrences or when many states are never needed.

Climbing Stairs Problem : recurrence relation `dp(i) = dp(i - 1) + dp(i - 2)`

```java
// store calculated values inside a hashmap to refer to in the future
private final HashMap<Integer, Integer> memoCache = new HashMap<>();

private int dp(int i) {
    if (i <= 2) return i;
    if (!memoCache.containsKey(i)) {
      memoCache.put(i, dp(i - 1) + dp(i - 2));//Use putIfAbsent if the calculated value doesn't change
    }
    return memoCache.get(i);
}
```

### With Recursion, the time complexity is high.
Without memoization The code above has a time complexity of `𝑂(2^𝑛)` because
every call to `dp()` creates 2 more calls to `dp()`

```java
private int dp(int i) {
    if (i <= 2) return i; // Base cases
    return dp(i - 1) + dp(i - 2); // Recurrence relation
}
```

# Min Cost Climbing Stairs
[Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/description/){:target="_blank"}

- Go reversed
  ```java
  public int minCostClimbingStairs(int[] cost) {
      int size = cost.length;
      int[] dp = new int[size+1];
      dp[size] = 0;
      dp[size-1] = Math.min(cost[size-1],cost[size-2]);
      
      //Go reversed which will give the price starting from step 0 or step 1
      for(int i = size-2; i >= 0; i--){
          dp[i] = cost[i] + Math.min(dp[i+1],dp[i+2]);
      }
      
      return Math.min(dp[0],dp[1]);
  }
  ```

- Fill from the beginning
  ```java
  public int minCostClimbingStairs(int[] cost) {
      int[] dp = new int[cost.length + 1];
      // step 0 and step 1 is 0, no need to set as its by-default
  
      // Start iteration from step 2, since the minimum cost of reaching
      for (int i = 2; i < minimumCost.length; i++) {
          int takeOneStep = minimumCost[i - 1] + cost[i - 1];
          int takeTwoSteps = minimumCost[i - 2] + cost[i - 2];
          dp[i] = Math.min(takeOneStep, takeTwoSteps);
      }
          
      // The final element refers to the top floor
      return dp[dp.length - 1];
  }
  ```

# House Robber

[House Robber](https://leetcode.com/problems/house-robber/description/){:target="_blank"}

- If decided not to rob the house, then we don't gain any money. Whatever money
  from the previous house is how much money have at this house -  `dp(i - 1)`
- If we decide to rob the house, then gain = `money[i]` from current house PLUS
  the money from the previous house `dp(i - 2)`

Recurrence Relation : `dp(i)=max(dp(i - 1), dp(i - 2) + money[i])`

```java
public int rob(int[] money) {
    if (money.length == 1)
        return money[0];

    int[] dp = new int[money.length];
    dp[0] = money[0];
    dp[1] = Math.max(money[0], money[1]);

    for (int i = 2; i < nums.length; i++) {
        dp[i] = Math.max(dp[i - 1], dp[i - 2] + money[i]);
    }

    return dp[money.length - 1];
}
```