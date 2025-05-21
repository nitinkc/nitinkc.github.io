---
title: "Data Structures - Java Classes"
date:  2025-01-01 15:27:00
categories: Algorithms
tags: [Algorithms]
---

{% include toc title="Index" %}

### 1. **Array**
```java
int[] a = new int[3]; // use [] for array instead of ()
int[] a = new int[] {1, 2, 3, 4, 5};
int[] arr = {1, 2, 3, 4, 5}; // Same as above
```

**`List`**: Ordered collection allowing duplicate elements.
- Implementations: `ArrayList`, `LinkedList`, `CopyOnWriteArrayList`.

### **ArrayList**
```java
List<Integer> list = new ArrayList<>();
```

### **LinkedList**
```java
List<String> list = new LinkedList<>();
```

### **Stack**
```java
import java.util.Stack;
Stack<Integer> stack = new Stack<>();
```

**`Queue`**: Collection designed for holding elements prior to processing (FIFO).
- Implementations: `PriorityQueue`, `ArrayDeque`, `ConcurrentLinkedQueue`, `ArrayBlockingQueue`, `LinkedBlockingQueue`.

**`Deque`**: Double-ended queue supporting addition/removal from both ends.
    - Implementations: `ArrayDeque`, `LinkedBlockingDeque`.

### **Queue**
```java
Queue<Integer> queue = new LinkedList<>();
queue.add(1);//ENQUEUE
queue.add(2);
int val = queue.poll();//Poll method removes and returns the head of the queue.DEQUEUE
// Check if the queue is empty
System.out.println("Is the queue empty? " + queue.isEmpty()); // true
```

### **PriorityQueue**
**`Heaps`** : Implemented via Priority Queues in Java

```java
Queue<Integer> pq = new PriorityQueue<>();
Queue<Integer> maxHeap = new PriorityQueue<>(Comparator.reverseOrder());
```

### **HashSet**
**`Set`**: Unordered collection with no duplicate elements.
- Implementations: `HashSet`, `LinkedHashSet`, `TreeSet`, `ConcurrentSkipListSet`.

```java
Set<Integer> set = new HashSet<>();
```

### **HashMap**
**`Map`**: Collection of key-value pairs with unique keys.
- Implementations: `HashMap`, `LinkedHashMap`, `TreeMap`, `ConcurrentHashMap`, `WeakHashMap`.

```java
HashMap<String, Integer> map = new HashMap<>();
map.put("A", 1);
map.put("B", 2);
System.out.println(map.get("A"));
```

### **TreeMap**
```java
Map<String, Integer> treeMap = new TreeMap<>(); // Default Natural Sorting Order
Map<String, Integer> treeMapReversed = new TreeMap<>(Comparator.reverseOrder());
Map<String, Integer> treeMapCustom = new TreeMap<>(Comparator.comparing(String::length)); // Custom key sorter

for (String name : namesList) { // From a list of Strings, put String as key
        treeMap.put(name, name.length());
}
```
