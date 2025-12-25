---
title: Data Structures - Implementations
date: 2025-04-30 15:06:00
categories:
- Algorithms
tags:
- Data Structures
- Implementation
- Java
- Tutorial
---

{% include toc title="Index" %}


# **Graph and Tree Structures**
Java does not provide built-in graph or tree libraries (except `TreeMap`/`TreeSet`). Use libraries like:
- **JGraphT**: For graph data structures and algorithms.
- **Apache Commons Graph**: For directed and undirected graphs.

## **Third-Party Libraries**
For advanced data structures, consider:

### **Google Guava**
- **`Multimap`**: A map that allows multiple values for a key.
- **`Table`**: Two-dimensional data structure.
- **`BiMap`**: A map that enforces unique values.

### **Apache Commons Collections**
- **`Bag`**: A collection that counts occurrences of elements.
- **`Trie`**: A prefix tree implementation.


# **Graph (Adjacency List)**
```java
import java.util.ArrayList;

public class GraphExample {
    static class Graph {
        int vertices;
        ArrayList<ArrayList<Integer>> adjList;

        Graph(int vertices) {
            this.vertices = vertices;
            adjList = new ArrayList<>();
            for (int i = 0; i < vertices; i++) {
                adjList.add(new ArrayList<>());
            }
        }

        void addEdge(int src, int dest) {
            adjList.get(src).add(dest);
            adjList.get(dest).add(src); // For undirected graph
        }

        void printGraph() {
            for (int i = 0; i < adjList.size(); i++) {
                System.out.println(i + " -> " + adjList.get(i));
            }
        }
    }

    public static void main(String[] args) {
        Graph graph = new Graph(3);
        graph.addEdge(0, 1);
        graph.addEdge(1, 2);
        graph.printGraph();
    }
}
```

# **Binary Tree**
```java
class TreeNode {
    int value;
    TreeNode left, right;

    TreeNode(int value) {
        this.value = value;
        left = right = null;
    }
}

public class BinaryTreeExample {
    TreeNode root;

    void inOrderTraversal(TreeNode node) {
        if (node != null) {
            inOrderTraversal(node.left);
            System.out.print(node.value + " ");
            inOrderTraversal(node.right);
        }
    }

    public static void main(String[] args) {
        BinaryTreeExample tree = new BinaryTreeExample();
        tree.root = new TreeNode(1);
        tree.root.left = new TreeNode(2);
        tree.root.right = new TreeNode(3);
        tree.inOrderTraversal(tree.root);
    }
}
```

#### Heaps
##### **Min-Heap:**
```java
class MinHeap {
    private int[] Heap;
    private int size;
    private int maxsize;

    private static final int FRONT = 1;

    public MinHeap(int maxsize) {
        this.maxsize = maxsize;
        this.size = 0;
        Heap = new int[this.maxsize + 1];
        Heap[0] = Integer.MIN_VALUE;
    }

    private int parent(int pos) { return pos / 2; }
    private int leftChild(int pos) { return (2 * pos); }
    private int rightChild(int pos) { return (2 * pos) + 1; }
    private boolean isLeaf(int pos) { return pos >= (size / 2) && pos <= size; }
    private void swap(int fpos, int spos) {
        int tmp;
        tmp = Heap[fpos];
        Heap[fpos] = Heap[spos];
        Heap[spos] = tmp;
    }

    private void minHeapify(int pos) {
        if (!isLeaf(pos)) {
            if (Heap[pos] > Heap[leftChild(pos)] || Heap[pos] > Heap[rightChild(pos)]) {
                if (Heap[leftChild(pos)] < Heap[rightChild(pos)]) {
                    swap(pos, leftChild(pos));
                    minHeapify(leftChild(pos));
                } else {
                    swap(pos, rightChild(pos));
                    minHeapify(rightChild(pos));
                }
            }
        }
    }

    public void insert(int element) {
        if (size >= maxsize) return;
        Heap[++size] = element;
        int current = size;
        while (Heap[current] < Heap[parent(current)]) {
            swap(current, parent(current));
            current = parent(current);
        }
    }

    public void print() {
        for (int i = 1; i <= size / 2; i++) {
            System.out.print(" PARENT : " + Heap[i] + " LEFT CHILD : " + Heap[2 * i] + " RIGHT CHILD :" + Heap[2 * i + 1]);
            System.out.println();
        }
    }

    public int remove() {
        int popped = Heap[FRONT];
        Heap[FRONT] = Heap[size--];
        minHeapify(FRONT);
        return popped;
    }
}
```

##### **Max-Heap:**
```java
class MaxHeap {
    private int[] Heap;
    private int size;
    private int maxsize;

    private static final int FRONT = 1;

    public MaxHeap(int maxsize) {
        this.maxsize = maxsize;
        this.size = 0;
        Heap = new int[this.maxsize + 1];
        Heap[0] = Integer.MAX_VALUE;
    }

    private int parent(int pos) { return pos / 2; }
    private int leftChild(int pos) { return (2 * pos); }
    private int rightChild(int pos) { return (2 * pos) + 1; }
    private boolean isLeaf(int pos) { return pos >= (size / 2) && pos <= size; }
    private void swap(int fpos, int spos) {
        int tmp;
        tmp = Heap[fpos];
        Heap[fpos] = Heap[spos];
        Heap[spos] = tmp;
    }

    private void maxHeapify(int pos) {
        if (!isLeaf(pos)) {
            if (Heap[pos] < Heap[leftChild(pos)] || Heap[pos] < Heap[rightChild(pos)]) {
                if (Heap[leftChild(pos)] > Heap[rightChild(pos)]) {
                    swap(pos, leftChild(pos));
                    maxHeapify(leftChild(pos));
                } else {
                    swap(pos, rightChild(pos));
                    maxHeapify(rightChild(pos));
                }
            }
        }
    }

    public void insert(int element) {
        if (size >= maxsize) return;
        Heap[++size] = element;
        int current = size;
        while (Heap[current] > Heap[parent(current)]) {
            swap(current, parent(current));
            current = parent(current);
        }
    }

    public void print() {
        for (int i = 1; i <= size / 2; i++) {
            System.out.print(" PARENT : " + Heap[i] + " LEFT CHILD : " + Heap[2 * i] + " RIGHT CHILD :" + Heap[2 * i + 1]);
            System.out.println();
        }
    }

    public int remove() {
        int popped = Heap[FRONT];
        Heap[FRONT] = Heap[size--];
        maxHeapify(FRONT);
        return popped;
    }
}
```

##### **Heapify:**
```java
void heapify(int[] arr, int n, int i) {
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest]) largest = left;
    if (right < n && arr[right] > arr[largest]) largest = right;

    if (largest != i) {
        int swap = arr[i];
        arr[i] = arr[largest];
        arr[largest] = swap;
        heapify(arr, n, largest);
    }
}
```

##### **Priority Queue:**
```java
pq.add(20);
pq.add(15);

System.out.println(pq.peek()); // 10
System.out.println(pq.poll()); // 10
System.out.println(pq.peek()); // 15
```

# Trie

```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEndOfWord;
}

public class TrieExample {
    TrieNode root = new TrieNode();

    void insert(String word) {
        TrieNode node = root;
        for (char ch : word.toCharArray()) {
            if (node.children[ch - 'a'] == null) {
                node.children[ch - 'a'] = new TrieNode();
            }
            node = node.children[ch - 'a'];
        }
        node.isEndOfWord = true;
    }

    boolean search(String word) {
        TrieNode node = root;
        for (char ch : word.toCharArray()) {
            if (node.children[ch - 'a'] == null) return false;
            node = node.children[ch - 'a'];
        }
        return node.isEndOfWord;
    }

    public static void main(String[] args) {
        TrieExample trie = new TrieExample();
        trie.insert("hello");
        System.out.println(trie.search("hello")); // true
        System.out.println(trie.search("world")); // false
    }
}
```
**Insertion:**
```java
class TrieNode {
    TrieNode[] children = new TrieNode[26];
    boolean isEndOfWord;
    TrieNode() { isEndOfWord = false; for (int i = 0; i < 26; i++) children[i] = null; }
}

class Trie {
    TrieNode root = new TrieNode();

    void insert(String key) {
        TrieNode node = root;
        for (int i = 0; i < key.length(); i++) {
            int index = key.charAt(i) - 'a';
            if (node.children[index] == null) node.children[index] = new TrieNode();
            node = node.children[index];
        }
        node.isEndOfWord = true;
    }
}
```

**Search:**
```java
boolean search(String key) {
    TrieNode node = root;
    for (int i = 0; i < key.length(); i++) {
        int index = key.charAt(i) - 'a';
        if (node.children[index] == null) return false;
        node = node.children[index];
    }
    return (node != null && node.isEndOfWord);
}
```

**Deletion:**
```java
boolean delete(TrieNode node, String key, int depth) {
    if (node == null) return false;
    if (depth == key.length()) {
        if (!node.isEndOfWord) return false;
        node.isEndOfWord = false;
        return node.children.length == 0;
    }
    int index = key.charAt(depth) - 'a';
    if (delete(node.children[index], key, depth + 1)) {
        node.children[index] = null;
        return !node.isEndOfWord && node.children.length == 0;
    }
    return false;
}
```

**Prefix Matching:**
```java
boolean startsWith(String prefix) {
    TrieNode node = root;
    for (int i = 0; i < prefix.length(); i++) {
        int index = prefix.charAt(i) - 'a';
        if (node.children[index] == null) return false;
        node = node.children[index];
    }
    return true;
}
```