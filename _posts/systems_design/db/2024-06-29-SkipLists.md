---
categories: System Design
date: 2024-06-29 11:02:00
tags:
- System Design
title: Skip Lists
---

{% include toc title="Index" %}

in-memory index type. Used in Redis

A skip list consists of **multiple layers of linked lists**.
The bottom layer is an ordinary sorted linked list.

Each higher layer acts as an "express lane" for the layers below, providing
shortcuts to speed up traversal.

Key Operations
Search: Similar to binary search, you start at the top layer and move forward
until you find the range where the element might exist, then drop down a layer
and continue.
Insertion: When inserting, you place the element in the appropriate position in
the bottom list, and then randomly decide how many layers it should be promoted
to.
Deletion: To delete an element, you remove it from all the layers in which it
appears.

Complexity
Search: Average O(log n), worst-case O(n)
Insertion: Average O(log n), worst-case O(n)
Deletion: Average O(log n), worst-case O(n)

Advantages

Simpler to implement compared to balanced trees like AVL or Red-Black trees.

Provides **probabilistic** balancing without complex rotations.

Can be more efficient in practice due to lower constant factors in the average
case.

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