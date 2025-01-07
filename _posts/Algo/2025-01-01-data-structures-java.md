---
title: "Data Structures in Java"
date:  2025-01-01 15:27:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

# 1. **Collection Framework Overview**

### **Common Interfaces**
- **`Collection`**: The root interface for all collections.
    - Examples: `List`, `Set`, `Queue`.
- **`List`**: Ordered collection allowing duplicate elements.
    - Implementations: `ArrayList`, `LinkedList`, `CopyOnWriteArrayList`.
- **`Set`**: Unordered collection with no duplicate elements.
    - Implementations: `HashSet`, `LinkedHashSet`, `TreeSet`, `ConcurrentSkipListSet`.
- **`Queue`**: Collection designed for holding elements prior to processing (FIFO).
    - Implementations: `PriorityQueue`, `ArrayDeque`, `ConcurrentLinkedQueue`, `ArrayBlockingQueue`, `LinkedBlockingQueue`.
- **`Deque`**: Double-ended queue supporting addition/removal from both ends.
    - Implementations: `ArrayDeque`, `LinkedBlockingDeque`.
- **`Map`**: Collection of key-value pairs with unique keys.
    - Implementations: `HashMap`, `LinkedHashMap`, `TreeMap`, `ConcurrentHashMap`, `WeakHashMap`.

# 2. **Interfaces and Implementations**

### **1. List Interface**
- **Description**: Ordered collection that allows duplicate elements.
- **Common Implementations**:
    - `ArrayList`: Resizable array; fast random access.
    - `LinkedList`: Doubly linked list; efficient for frequent insertions/deletions.
    - `CopyOnWriteArrayList`: Thread-safe version of `ArrayList`.

### **2. Set Interface**
- **Description**: Unordered collection without duplicate elements.
- **Common Implementations**:
    - `HashSet`: Uses a hash table; fast for lookups.
    - `LinkedHashSet`: Maintains insertion order.
    - `TreeSet`: Sorted set based on `Comparable` or `Comparator`.
    - `ConcurrentSkipListSet`: Thread-safe, sorted set.

### **3. Queue Interface**
- **Description**: FIFO structure for holding elements before processing.
- **Common Implementations**:
    - `PriorityQueue`: Min-heap for priority-based processing.
    - `ArrayDeque`: Resizable array-based deque; can function as a queue or stack.
    - `ConcurrentLinkedQueue`: Non-blocking, thread-safe queue.
    - `ArrayBlockingQueue`: Bounded blocking queue.
    - `LinkedBlockingQueue`: Unbounded (or optionally bounded) blocking queue.
    - `PriorityBlockingQueue`: Thread-safe priority queue.
    - `SynchronousQueue`: Queue with no capacity (direct handoff between producer and consumer).

### **4. Deque Interface**
- **Description**: Double-ended queue supporting addition/removal from both ends.
- **Common Implementations**:
    - `ArrayDeque`: High-performance deque implementation.
    - `LinkedBlockingDeque`: Thread-safe deque.

### **5. Map Interface**
- **Description**: Collection of key-value pairs with unique keys.
- **Common Implementations**:
    - `HashMap`: Hash table implementation; allows `null` keys/values.
    - `LinkedHashMap`: Maintains insertion/access order.
    - `TreeMap`: Sorted map using `Comparable` or `Comparator`.
    - `ConcurrentHashMap`: Thread-safe hash table.
    - `ConcurrentSkipListMap`: Thread-safe, sorted map.
    - `WeakHashMap`: Entries are garbage collected when keys are no longer in use.

# 3. **Concurrency and Specialized Collections**

### **Concurrent Utilities**
- **Thread-Safe Queues**:
    - `ConcurrentLinkedQueue`: Non-blocking queue.
    - `LinkedBlockingQueue`: Blocking queue based on linked nodes.
    - `PriorityBlockingQueue`: Blocking priority queue.
    - `SynchronousQueue`: Direct producer-consumer handoff.

- **Thread-Safe Maps**:
    - `ConcurrentHashMap`: Optimized for high-concurrency scenarios.
    - `ConcurrentSkipListMap`: Sorted map for concurrent usage.

- **Thread-Safe Sets**:
    - `ConcurrentSkipListSet`: Sorted set for concurrent usage.
    - `CopyOnWriteArraySet`: Efficient for iteration in concurrent environments.
  
- **`BlockingQueue`**: Interface for queues like `ArrayBlockingQueue`, `LinkedBlockingQueue`, etc.


### **Other Specialized Structures**
- **`BitSet`**: Efficient storage for a sequence of bits.
- **`EnumSet`**: Set implementation for enumerations.
- **`EnumMap`**: Map implementation for enumerations.
- **`WeakHashMap`**: Entries are garbage collected when keys are no longer in use.
- **`SoftHashMap`**: Similar to `WeakHashMap`, but uses soft references.

# 5. **Graph and Tree Structures**
Java does not provide built-in graph or tree libraries (except `TreeMap`/`TreeSet`). Use libraries like:
- **JGraphT**: For graph data structures and algorithms.
- **Apache Commons Graph**: For directed and undirected graphs.

# 6. **Third-Party Libraries**
For advanced data structures, consider:

### **Google Guava**
- **`Multimap`**: A map that allows multiple values for a key.
- **`Table`**: Two-dimensional data structure.
- **`BiMap`**: A map that enforces unique values.

### **Apache Commons Collections**
- **`Bag`**: A collection that counts occurrences of elements.
- **`Trie`**: A prefix tree implementation.

# Code Examples

### 1. **Array**
```java
public class ArrayExample {
    public static void main(String[] args) {
        int[] arr = {1, 2, 3, 4, 5};
        for (int num : arr) {
            System.out.print(num + " ");
        }
    }
}
```

### 2. **ArrayList**
```java
import java.util.ArrayList;

public class ArrayListExample {
    public static void main(String[] args) {
        ArrayList<Integer> list = new ArrayList<>();
        list.add(1);
        list.add(2);
        list.remove(0);
        System.out.println(list);
    }
}
```

### 3. **LinkedList**
```java
import java.util.LinkedList;

public class LinkedListExample {
    public static void main(String[] args) {
        LinkedList<String> list = new LinkedList<>();
        list.add("Hello");
        list.add("World");
        list.removeFirst();
        System.out.println(list);
    }
}
```

### 4. **Stack**
```java
import java.util.Stack;

public class StackExample {
    public static void main(String[] args) {
        Stack<Integer> stack = new Stack<>();
        stack.push(10);
        stack.push(20);
        stack.pop();
        System.out.println(stack.peek());
    }
}
```

### 5. **Queue**
```java
import java.util.LinkedList;
import java.util.Queue;

public class QueueExample {
    public static void main(String[] args) {
        Queue<Integer> queue = new LinkedList<>();
        queue.add(1);
        queue.add(2);
        queue.poll();
        System.out.println(queue);
    }
}
```

### 6. **PriorityQueue**
```java
import java.util.PriorityQueue;

public class PriorityQueueExample {
    public static void main(String[] args) {
        PriorityQueue<Integer> pq = new PriorityQueue<>();
        pq.add(3);
        pq.add(1);
        pq.add(2);
        System.out.println(pq.poll());
    }
}
```

### 7. **HashSet**
```java
import java.util.HashSet;

public class HashSetExample {
    public static void main(String[] args) {
        HashSet<Integer> set = new HashSet<>();
        set.add(10);
        set.add(20);
        set.add(10); // Duplicate ignored
        System.out.println(set);
    }
}
```

### 8. **HashMap**
```java
import java.util.HashMap;

public class HashMapExample {
    public static void main(String[] args) {
        HashMap<String, Integer> map = new HashMap<>();
        map.put("A", 1);
        map.put("B", 2);
        System.out.println(map.get("A"));
    }
}
```

### 9. **TreeMap**
```java
import java.util.TreeMap;

public class TreeMapExample {
    public static void main(String[] args) {
        TreeMap<Integer, String> map = new TreeMap<>();
        map.put(2, "B");
        map.put(1, "A");
        System.out.println(map);
    }
}
```

### 10. **Graph (Adjacency List)**
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

### 11. **Binary Tree**
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

### 12. **Trie**
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