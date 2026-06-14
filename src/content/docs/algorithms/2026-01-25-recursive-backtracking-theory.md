---
title: Recursive Backtracking - Theory
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

> Choose-explore-unchoose pattern

## What is Backtracking?

**Backtracking** is like solving a maze:
- You try a path
- If it leads to a dead end, you **go back** (backtrack) and try a different path
- You continue until you find the solution or exhaust all possibilities


```java
void explore(options, soFar)
{
    if (no more decisions to make) {
        // base case
    } else {
        // recursive case, we have a decision to make
        for (each available option) {
            choose (update options/soFar)
            explore (recur on updated options/soFar)
            unchoose (undo changes to options/soFar)
        }
    }
}
```

### Backtracking recursion
- Build up many possible solutions through multiple recursive calls at each step
- Seed the initial recursive call with an “empty” solution (Helper method parameters)
- At each base case, you have a potential solution

There are 3 main categories of problems that we be solved by using backtracking recursion:
- generate **all** possible solutions to a problem or count the total number of possible solutions to a problem
- find **one** specific solution to a problem or prove that one exists
- We can find the **best** possible solution to a given problem


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
