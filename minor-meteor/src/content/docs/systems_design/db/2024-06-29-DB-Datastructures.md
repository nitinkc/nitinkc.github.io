---
title: DB Data Structures
date: 2024-06-28 11:02:00
categories:
- System Design
tags:
- Database
- Data Structures
---

{% include toc title="Index" %}

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#8-data-structures-that-power-your-databases](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#8-data-structures-that-power-your-databases)

![](https://www.youtube.com/watch?v=W_v05d_2RTo)

# Skip List

[Skip Lists]({% post_url /systems_design/db/2024-06-29-SkipLists %})

# Hash index:

a very common implementation of the "Map" data structure (or "Collection")

# SSTable - Sorted String Tables

[SSTables]({% post_url /systems_design/db/2024-06-29-SSTables %})

# LSM tree: Skiplist + SSTable

[LSM Tree]({% post_url /systems_design/db/2024-06-29-LSM-Tree %})

# B-tree:

disk-based solution. Consistent read/write performance

# Inverted index:

used for document indexing. Used in Lucene

# Suffix tree:

for string pattern search

# R-tree:

multi-dimension search, such as finding the nearest neighbor