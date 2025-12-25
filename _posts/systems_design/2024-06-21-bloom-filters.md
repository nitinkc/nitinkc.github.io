---
categories: System Design
date: 2024-06-18 11:45:00
tags:
- Data Structures
- Probabilistic
title: Bloom Filters
---

{% include toc title="Index" %}

# Bloom Filters - Probabilistic Data structure

[https://hur.st/bloomfilter/](https://hur.st/bloomfilter/)

A Bloom filter is a probabilistic data structure that is used to **test whether
an element is a member of a set**.

It is highly space-efficient and allows for fast membership queries, but it can
produce false positives

# Applications

- Databases: To quickly check if a value might be in a database before doing a
  more expensive query.
- Networking: For efficient routing and packet processing.
- Security: To filter out malicious URLs or content quickly.

# How Bloom Filters Work

### Initialization:

A Bloom filter is represented by an **array of m bits**, all set to 0 initially.

It uses **k different hash functions**, each of which maps an element to one of
the m bit positions.

### Adding Elements:

To add an element to the Bloom filter, the element is **hashed using each of the
k hash functions**.

- Each hash function produces a position in the bit array.
- The bits at all k positions are set to 1.

### Checking Membership:

To check if an element is in the set, it is hashed using the same k hash
functions.

- If all k bits at the positions specified by the hash functions are 1, the
  element is considered to be in the set.
- If any of the k bits is 0, the element is definitely not in the set.

```markdown
Initialization:

Bit array: 0 0 0 0 0 0 0 0 0 0 (m = 10 bits)
Hash functions: h1, h2, h3 (k = 3)

Adding an element "A":

1. Hash "A" with h1, h2, h3:
   h1("A") = 2
   h2("A") = 5
   h3("A") = 8

2. Set the bits at positions 2, 5, 8 to 1:
   Bit array: 0 0 1 0 0 1 0 0 1 0

Checking membership for "X":

1. Hash "X" with h1, h2, h3:
   h1("X") = 2
   h2("X") = 5
   h3("X") = 8

2. Check the bits at positions 2, 5, 8:
   All bits are 1 -> "X" is **possibly** in the set

Checking membership for "C":

1. Hash "C" with h1, h2, h3:
   h1("C") = 0
   h2("C") = 4
   h3("C") = 6

2. Check the bits at positions 0, 4, 6:
   Bit at position 4 is 0 -> "C" is **definitely not** in the set
```