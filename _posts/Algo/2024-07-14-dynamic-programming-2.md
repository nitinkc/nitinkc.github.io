---
categories: Algorithms
date: 2024-07-15 18:27:00
tags:
- Dynamic Programming
- DP
- Iteration
- Optimization
title: Dynamic Programming - Iteration
---

{% include toc title="Index" %}---

# Iteration in the recurrence relation

When the recurrence relation is a static equation - there is no iteration.

- [Min Cost Climbing Stairs](https://leetcode.com/problems/min-cost-climbing-stairs/description/){:target="_blank"}

- climb 1 or 2 steps at a time.
  $$ dp(i) = \min(dp(i - 1) + \text{cost}[i - 1], \, dp(i - 2) + \text{cost}[i - 2]) $$

- if the question is to take `k` steps at a time, the recurrence relation would
become dynamic 
 $$ dp(i) = \min_{(i - k) \leq j < i} (dp(j) + \text{cost}[j]) $$

{% gist nitinkc/853b26bd2bc230596529de8ad27c4247 %}