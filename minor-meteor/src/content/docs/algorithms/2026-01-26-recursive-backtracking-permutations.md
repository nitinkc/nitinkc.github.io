---
title: Recursive Backtracking - Permutations
date: 2026-01-26 13:05:00
categories:
- Algorithms
tags:
- Recursion
- Backtracking
---

{% include toc title="Index" %}

[Stanford Lecture](https://web.stanford.edu/class/cs106b-8/lectures/backtracking-optimization/Lecture13.pdf)

## Dice Rolls
To generate all possible sequences of values.

for (each possible first die value):
    for (each possible second die value):
        for (each possible third die value):
            ...
                print or keep in some Data Structure!

– This is called a depth-first search

```java
public void diceRolls(int n){
    List<Integer> chosen = new ArrayList<>();
    diceRollHelper(n, chosen);
}

private static void diceRollHelper(int dice, List<Integer> chosen) {
    if (dice == 0) {
        System.out.println(formatChosen(chosen));
    } else {
        for (int i = 1; i <= 6; i++) {
        chosen.add(i);                     // choose
        diceRollHelper(dice - 1, chosen);  // explore
        chosen.remove(chosen.size() - 1);  // un-choose
        }
    }
}
```

Returns all possible dice roll combinations as a list of lists
```java
public List<List<Integer>> diceRolls(int n){
    List<List<Integer>> result = new ArrayList<>();
    List<Integer> chosen = new ArrayList<>();
    diceRollHelper(n, chosen, result);
    return result;
}

private static void diceRollHelper(int dice, List<Integer> chosen, List<List<Integer>> result) {
    if (dice == 0) {
        result.add(new ArrayList<>(chosen));  // base case: add a copy
    } else {
        for (int i = 1; i <= 6; i++) {
            chosen.add(i);                     // choose
            diceRollHelper(dice - 1, chosen, result);  // explore
            chosen.remove(chosen.size() - 1);  // un-choose
        }
    }
}
```

### Dice Roll Sum
It also accepts a desired sum and prints only combinations that add up to exactly that sum.
```java
public void diceSum(int numDice, int sum){
  List<Integer> chosen = new ArrayList<>();
  helper(numDice, sum, chosen);
}
private void helper(int numDice, int sum, List<Integer> chosen){
  if(numDice == 0){
    if(sumAll(chosen) == sum){//Printing only the combinations that add up to exactly the desired sum
      System.out.println(printAll(chosen));
    }
    return;
  }
  for(int i=1; i<=6; i++){//6 types of choices
    //choose
    chosen.add(i);
    //explore
    helper(numDice-1,sum,chosen);
    //unchoose
    chosen.remove(chosen.size()-1);
  }
  return;
}

private int sumAll(List<Integer> chosen){
  return chosen.stream().mapToInt(Integer::intValue).sum();
}
```
#### Optimized with pruning
```java
public void diceSum(int numDice, int target){
    List<Integer> chosen = new ArrayList<>();
    helper(numDice, 0,target, chosen);
}
private void helper(int numDice, int sum, int target, List<Integer> chosen){
    if(numDice == 0){
        if(sum==target){
            System.out.println(printAll(chosen));
            return;
        }
        return;
    } else if(sum+(1*numDice) <= target && sum+(6*numDice) >= target){
        for(int i=1; i<=6; i++){//6 types of choices
            //choose
            chosen.add(i);
            //explore
            helper(numDice-1,sum+i,target,chosen);
            //unchoose
            chosen.remove(chosen.size()-1);
        }
    }
    return;
}
```

## Permutations and Arrangements

A permutation is a **rearrangement** of the elements of a sequence

**Decision** at each step (each level of the tree):
- What is the next element going to get added to the permutation?

**Options** at each decision (branches from each node):
- One option for every remaining element that hasn't been selected yet
- Note: **The number of options will be diﬀerent at each level of the tree!**

Information we need to store along the way:
- The permutation you’ve built so far
- The remaining elements in the original sequence

![permutation_backtracking.png](/assets/images/permutation_backtracking.png)

### Problem 3.1: Generate All Permutations

**Problem**: Given `[1, 2, 3]`, generate all possible arrangements.

**Output**: `[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]`

**Key Difference from Subsets**:
- Subsets: Each element included or excluded (2 choices)
- Permutations: Each position can be ANY unused element (n choices for 1st, n-1 for 2nd, etc.)

**Think**: We need to track which elements we've already used.

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

Inefficient but intuitive
```java
public void permute(String str){
  helper(str,"");
}

private void helper(String remaining, String sofar){
  if(remaining.isEmpty()){
    System.out.println(sofar);
  } else {
    for(int i = 0; i < remaining.length(); i++){
      char next = remaining.charAt(i);
      String rest = remaining.substring(0,i) + remaining.substring(i+1);//choose
      helper(rest,sofar+next);//explore
    }
  }
}
```
