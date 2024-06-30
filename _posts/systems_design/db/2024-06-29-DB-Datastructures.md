---
title:  "DB Data Structures"
date:   2024-06-28 11:02:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#8-data-structures-that-power-your-databases](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#8-data-structures-that-power-your-databases)
![](https://www.youtube.com/watch?v=W_v05d_2RTo)

# Skip List

in-memory index type. Used in Redis

A skip list consists of **multiple layers of linked lists**. 
The bottom layer is an ordinary sorted linked list. 

Each higher layer acts as an "express lane" for the layers below, providing shortcuts to speed up traversal.

Key Operations
Search: Similar to binary search, you start at the top layer and move forward until you find the range where the element might exist, then drop down a layer and continue.
Insertion: When inserting, you place the element in the appropriate position in the bottom list, and then randomly decide how many layers it should be promoted to.
Deletion: To delete an element, you remove it from all the layers in which it appears.

Complexity
Search: Average O(log n), worst-case O(n)
Insertion: Average O(log n), worst-case O(n)
Deletion: Average O(log n), worst-case O(n)

Advantages

Simpler to implement compared to balanced trees like AVL or Red-Black trees.

Provides **probabilistic** balancing without complex rotations.

Can be more efficient in practice due to lower constant factors in the average case.

```markdown
Level 3:     1 ------------> 5 -----------------> 9
                  |______________|
                          |
Level 2:     1 -----> 3 ----> 5 -----------------> 9
                          |___________|
                                  |
Level 1:     1 -----> 3 ----> 5 ---------> 7 -----> 9
                                |_____________|
                                          |
Level 0:     1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9
                                              |____|
```
 Java Implementation

```java
import java.util.Random;

class SkipListNode<T> {
    T value;
    SkipListNode<T>[] forward;

    @SuppressWarnings("unchecked")
    public SkipListNode(T value, int level) {
        this.value = value;
        forward = new SkipListNode[level + 1];
    }
}

public class SkipList<T extends Comparable<? super T>> {
    private static final int MAX_LEVEL = 16;
    private final SkipListNode<T> head = new SkipListNode<>(null, MAX_LEVEL);
    private int level = 0;
    private final Random random = new Random();

    public void insert(T value) {
        SkipListNode<T>[] update = new SkipListNode[MAX_LEVEL + 1];
        SkipListNode<T> x = head;

        for (int i = level; i >= 0; i--) {
            while (x.forward[i] != null && x.forward[i].value.compareTo(value) < 0) {
                x = x.forward[i];
            }
            update[i] = x;
        }

        x = new SkipListNode<>(value, randomLevel());
        for (int i = 0; i <= level; i++) {
            x.forward[i] = update[i].forward[i];
            update[i].forward[i] = x;
        }
    }

    private int randomLevel() {
        int lvl = 0;
        while (random.nextDouble() < 0.5 && lvl < MAX_LEVEL) {
            lvl++;
        }
        return lvl;
    }

    public boolean search(T value) {
        SkipListNode<T> x = head;
        for (int i = level; i >= 0; i--) {
            while (x.forward[i] != null && x.forward[i].value.compareTo(value) < 0) {
                x = x.forward[i];
            }
        }
        x = x.forward[0];
        return x != null && x.value.compareTo(value) == 0;
    }

    public void delete(T value) {
        SkipListNode<T>[] update = new SkipListNode[MAX_LEVEL + 1];
        SkipListNode<T> x = head;

        for (int i = level; i >= 0; i--) {
            while (x.forward[i] != null && x.forward[i].value.compareTo(value) < 0) {
                x = x.forward[i];
            }
            update[i] = x;
        }

        x = x.forward[0];
        if (x != null && x.value.compareTo(value) == 0) {
            for (int i = 0; i <= level; i++) {
                if (update[i].forward[i] != x) break;
                update[i].forward[i] = x.forward[i];
            }
            while (level > 0 && head.forward[level] == null) {
                level--;
            }
        }
    }
}

```


# Hash index: 
a very common implementation of the “Map” data structure (or “Collection”)

# SSTable - Sorted String Tables
immutable on-disk “Map” implementation

SSTables (Sorted String Tables) are an immutable data structure used in databases, especially those designed for 
**high write** throughput and large-scale data management like Apache Cassandra and LevelDB.

An SSTable contains **a set of sorted key-value pairs** and is written to disk in a single pass.

### Key Characteristics of SSTables
**Immutability**: Once an SSTable is written to disk, it is never modified. This immutability simplifies concurrency control and ensures data consistency.

**Sorted**: Keys in an SSTable are stored in a sorted order. This property allows efficient range queries and quick lookups.

**Efficient Writes**: Since SSTables are written in bulk and not modified later, write operations are fast.

**Efficient Reads**: The sorted nature of SSTables **enables binary search** for key lookups, making read operations efficient.

**Compaction**: Over time, multiple SSTables are merged (compacted) into fewer, larger SSTables to reclaim space and reduce read amplification.

### Structure of an SSTable

**Data File**: Contains the actual key-value pairs.

**Index File**: Provides an offset for each key, allowing for efficient lookups.

**Bloom Filter**: A probabilistic data structure that helps quickly determine if a key is not present in the SSTable.

**Summary File**: A reduced index that allows for quick binary search in the index file.

### Writing Data:

Data is initially written to a memtable (an in-memory structure).

Once the memtable reaches a certain size, it is flushed to disk as a new SSTable.
This new SSTable is immutable and will not be modified.

### Reading Data:

To read a key, the database first checks **the bloom filter** to see if the key is likely present in the SSTable.

If the bloom filter indicates the key might be present, **the index file is consulted** to find **the offset** of the key in the data file.

The data file is then accessed at the given offset to retrieve the value.

### Compaction:

Over time, multiple SSTables can accumulate, which may lead to increased read latency.

The compaction process merges these SSTables into fewer, larger SSTables, discarding deleted data and redundant entries.

This process reduces the number of SSTables that need to be checked during read operations, improving read performance.

### Use Cases
NoSQL Databases: Databases like Apache Cassandra and HBase utilize SSTables for their storage engines.

Log-Structured Merge-Trees (LSM-Trees): SSTables are a key component of LSM-Trees, which are used in storage systems requiring high write throughput.

SSTables are fundamental to the performance and scalability of modern distributed databases, providing a robust solution for handling large volumes of data efficiently.

# LSM tree: Skiplist + SSTable


# B-tree: 
disk-based solution. Consistent read/write performance


# Inverted index:
used for document indexing. Used in Lucene

# Suffix tree: 
for string pattern search

# R-tree: 
multi-dimension search, such as finding the nearest neighbor