---
title: B Trees, B+ Trees, m-ary/m-way Trees
date: 2025-01-21 09:26:00
categories:
- Algorithms
tags:
- Trees
- Data Structures
---

{% include toc title="Index" %}

# HDD Key Concepts:
1. Sector: The smallest physical unit of storage (e.g., 512 bytes or 4 KB).
2. Block: A group of consecutive sectors (e.g., 4 sectors make up 1 block).
3. Offset: Specific location within a block or sector (measured in bytes).
4. Track: Circular path on the disk platter where data is stored.
5. Cylinder: A collection of tracks across all platters aligned vertically.

# Flow of Access:
- Locate Cylinder (Track).
- Identify Sector within the Cylinder.
- Navigate to the Block (Logical grouping of sectors).
- Use Offset for finer-grained location within the Block.

![](https://en.wikipedia.org/wiki/Disk_sector#/media/File:Disk-structure2.svg)

![](https://www.youtube.com/watch?v=aZjYr87r1b8)

# B-Trees of Order m
B-Trees are self-balancing search trees designed to efficiently handle disk storage or large datasets. 
They are particularly useful in d**atabase systems (for indexing and multilevel indexing) and file systems**.

## Key Properties of B-Trees:
- Balanced Tree: All leaf nodes are at the same level.
- - Grows "bottom-up"
- Node Properties:
  - Each node has at most m children (where m is the order of the tree).
  - Each node except the root must have at least ⌈m/2⌉ children.
  - Root can have minimum or 2 children (1 key)
- Keys:
  - Keys within a node are sorted.
  - Keys in a node partition the keys in the subtrees.

## Node
```java
class BTreeNode {
    int t; // Minimum degree (defines the range for keys)
    ArrayList<Integer> keys; // Keys stored in this node
    ArrayList<BTreeNode> children; // Child pointers
    boolean isLeaf; // Is true if this node is a leaf 
```
## Splitting while inserting new keys

```java
// Split child node
public void splitChild(int i) {
    BTreeNode child = children.get(i);
    BTreeNode sibling = new BTreeNode(t, child.isLeaf);

    for (int j = 0; j < t - 1; j++) {
        sibling.keys.add(child.keys.remove(t));
    }
    if (!child.isLeaf) {
        for (int j = 0; j < t; j++) {
            sibling.children.add(child.children.remove(t));
        }
    }

    children.add(i + 1, sibling);
    keys.add(i, child.keys.remove(t - 1));
}
```

### [B-Tree Index](https://nitinkc.github.io/sql/query-optimization/#b-tree-index)

# B+ Trees
- No record pointers from inner nodes.
- the inner nodes(every key) are replicated(have copy) into the leaf nodes and only leaf nodes has the record pointers
-