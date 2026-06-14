---
title: Union Find  - Disjoint Set Data structure
date: 2024-06-16 18:27:00
categories:
- Algorithms
tags:
- Data Structures
---

{% include toc title="Index" %}

# Disjoint Set data structure

The primary use of disjoint sets is to address the connectivity between the
components of a network.
Given the vertices and edges between the vertices, how could we quickly check
whether two vertices are connected?

**“disjoint set”** data structure is also known as the **“union-find”** data
structure

To check if two vertices are connected, we only need to check if they have the *
*same root node**.

The two most important functions for the “disjoint set”

- The find function locates the root node of a given vertex.
- The union function connects two previously unconnected vertices by giving them
  the same root node.

> memorize the implementation of “disjoint set with path compression and union
> by rank”.

```java
public class UnionFind {
    public UnionFind(int size)// Constructor of Union-find. The size is the length of the root array.
    
    int find(int node);//Finds the root of the node (Not the parent)
    void union(int x, int y);//Connect 2 nodes, or merge 2 disjoint sets
    //Two nodes are considered connected if they are in the same set or they have the same root.
    boolean isConnected(int x, int y);//check connectivity between 2 nodes, or check if 2 sets are connected
}
```

# 1. Quick Find

- Eager Approach
- defect : union is too expensive. Takes $ O(N) $ array access to process
  sequence of N union commands on N objects
- find: O(1). but the trade-offis in union O(N)

```java
public int quickFind(int x) {
    return root[x];//
}
```

```java
public void union(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);

    if (rootX != rootY) {
        for (int i = 0; i < root.length; i++) {
            if (root[i] == rootY) {
                root[i] = rootX;
            }
        }
    }
}
```

# 2. Quick union

> Quick union is more efficient than Quick find

O(n) worst case complexity when the graph is a chain `1->2->3->4->5->6`

Find : O(N)

Union : O(N)
The union operation consists of two find operations which (only in the
worst-case) will take O(N) time,

```java
public int find(int x) {
    while (x != root[x]) {
        x = root[x];
    }
    return x;
}

//Recursive find
public int find(int x) {
   if(x == root[x])
    return x;
   return root[x] = find(root[x]);//Recursive
}
```

```java
public void quickUnion(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY) {
        root[rootY] = rootX;
    }
}
```

# 3. Union by Rank

The “rank” refers to the height of each vertex

Merge the shorter tree under the taller tree and assign the root node of the
taller
tree as the root node for both vertices

```java
public UnionFind(int size) {
        root = new int[size];
        rank = new int[size];
        for (int i = 0; i < size; i++) {
            root[i] = i;
            rank[i] = 1; 
        }
    }

    public int find(int x) {
        while (x != root[x]) {
            x = root[x];
        }
        return x;
    }

    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            if (rank[rootX] > rank[rootY]) {
                root[rootY] = rootX;
            } else if (rank[rootX] < rank[rootY]) {
                root[rootX] = rootY;
            } else {
                root[rootY] = rootX;
                rank[rootX] += 1;
            }
        }
    }
```

# 4. Path Compression Optimization

optimization for find() method -> optimization of quick union

```java
 public UnionFind(int size) {
        root = new int[size];
        for (int i = 0; i < size; i++) {
            root[i] = i;
        }
    }

    public int find(int x) {
        if (x == root[x]) {
            return x;
        }
        return root[x] = find(root[x]);
    }

    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            root[rootY] = rootX;
        }
    }

    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }
}

```

```java
public int find(int x) {
    if (x == root[x]) {
        return x;
    }
    return root[x] = find(root[x]);//Path compression implementation
}
```

```java
public void union(int x, int y) {
    int rootX = find(x);
    int rootY = find(y);
    if (rootX != rootY) {
        root[rootY] = rootX;
    }
}
```

# 5. Path Compression and Union by Rank - Optimized “disjoint set” with

O(1) time for the best case (when the parent node for some vertex is the root
node itself). In the worst case, it would be
O(N) time when the tree is skewed. However, on average, the time complexity will
be
O(logN).

[Top-Down Analysis of Path Compression](https://www.cs.tau.ac.il/~michas/ufind.pdf)

```java
 public UnionFind(int size) {
        root = new int[size];
        rank = new int[size];
        for (int i = 0; i < size; i++) {
            root[i] = i;
            rank[i] = 1; // The initial "rank" of each vertex is 1, because each of them is
                         // a standalone vertex with no connection to other vertices.
        }
    }

	// The find function here is the same as that in the disjoint set with path compression.
    public int find(int x) {
        if (x == root[x]) {
            return x;
        }
	// Some ranks may become obsolete so they are not updated
        return root[x] = find(root[x]);
    }
    
    @Override
    public int find(int x) {
        while (x != root[x]) {
            root[x] = root[root[x]];
            x = root[x];
        }
        return x;
    }

	// The union function with union by rank
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            if (rank[rootX] > rank[rootY]) {
                root[rootY] = rootX;
            } else if (rank[rootX] < rank[rootY]) {
                root[rootX] = rootY;
            } else {
                root[rootY] = rootX;
                rank[rootX] += 1;
            }
        }
    }

    public boolean connected(int x, int y) {
        return find(x) == find(y);
    }
```

# Path Compression and Union by Rank

When using the combination of union by rank and the path compression
optimization, the find operation will take
O(α(N)) time on average. Since union and connected both make calls to find and
all other operations require constant time, union and connected functions will
also take
O(α(N)) time on average.

# Dynamic Connectivity Problem