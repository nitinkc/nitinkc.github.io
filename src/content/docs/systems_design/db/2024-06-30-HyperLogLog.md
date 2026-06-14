---
title: HyperLogLog
date: 2024-06-30 11:02:00
categories:
- System Design
tags:
- Algorithms
---

{% include toc title="Index" %}

# HyperLogLog

[https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/](https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/)

HyperLogLog is a **probabilistic data structure** used for estimating the
cardinality of a multiset, which is the number of unique elements in a large
dataset.

It is particularly useful in situations where exact counting is computationally
infeasible due to the size of the data.

## Key Characteristics of HyperLogLog

1. **Space Efficiency:** HyperLogLog uses much less memory compared to storing
   the entire dataset. It requires only a few kilobytes of memory to estimate
   cardinality, even for very large sets.

2. **Approximation Accuracy:** It provides an approximate count with a
   controllable error margin. The standard error is typically around 2%, but
   this can be adjusted by tuning the parameters.

3. **Algorithm:**
    - It works by hashing each element of the dataset and using the **position
      of the leftmost 1-bit** in the hash to determine which bucket to update.
    - The data structure maintains multiple registers, each recording the
      maximum rank (the position of the leftmost 1-bit) seen so far.
    - The **harmonic mean** of these maximum ranks is then used to estimate the
      cardinality of the set.

4. **Mergeable:** HyperLogLog structures can be merged together, which is useful
   for distributed systems. You can combine the results of multiple HyperLogLog
   instances to get a global estimate of the unique elements across all
   datasets.

## Applications

- **Database Query Optimization:** Estimating the number of distinct values in a
  column to optimize query execution plans.
- **Network Monitoring:** Counting the number of unique IP addresses accessing a
  network.
- **Big Data Analytics:** Estimating the cardinality of large-scale data streams
  for real-time analytics.

## Example Use Case

Imagine you are managing a large-scale web application and you need to estimate
the number of unique visitors over a period of time. Storing every visitor's ID
and counting them is impractical due to the high memory requirement. Instead,
you can use HyperLogLog to estimate the unique visitor count with a small and
fixed amount of memory, providing you with a fast and space-efficient solution.

## Summary

HyperLogLog is a powerful tool for situations where an approximate count of
unique elements is sufficient and memory efficiency is crucial. It is widely
used in big data applications and distributed systems due to its mergeability
and low memory footprint.