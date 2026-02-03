---
title: Gatherers
date: 2026-01-21 14:17:00
categories:
- Java
tags:
- Functional Programming
---

{% include toc title="Index" %}

In Java, the **Stream API** provides a powerful way to process sequences of elements in a functional style. One of the key components of this API is the concept of **gatherers**, which are used to collect the results of stream operations into various data structures.

Martin Fowler  - "Functional Programming is about building software by composing pure functions, avoiding shared state, mutable data, and side-effects."

Collection Pipeline Pattern: A pipeline of functions through which data flows and gets transformed.
1. Source: A data source (like a Collection, array, or I/O channel)
2. Intermediate Operations: Transformations that produce a new stream (like filter, map, sorted)
3. Terminal Operation: Produces a result or side-effect (like collect, forEach, reduce)

Imperative style programming has higher accidental complexity due to managing state and control flow, 
- while functional programming emphasizes declarative constructs that express the logic of computation without describing its control flow.

```
data -> Stage1 -> Stage2 -> ... -> StageN -> Terminal Operation
```

Gatherer represents a stage

## Common Gatherers in Java Streams


Fold() - takes in reduce function and an initial value, and combines all elements of the stream into a single result.

```java