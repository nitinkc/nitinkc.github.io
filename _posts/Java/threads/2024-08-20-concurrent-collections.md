---
title:  "Java Concurrent Collections"
date:   2024-08-20 00:17:00
categories: ['Java','Multithreading']
tags: ['Java','Multithreading']
---

{% include toc title="Index" %}

### The Need for Concurrent Collections

In multi-threaded environments, traditional collections like `ArrayList`, `HashMap`, and `HashSet` are **not thread-safe**.
- can lead to issues such as `ConcurrentModificationException` (one thread modifies a collection while another thread is iterating over it)
- To address these issues, Java provides **concurrent collections** in the `java.util.concurrent` package.

### Traditional Collections and Their Limitations

1. **Non-Thread-Safe Collections**: Most traditional collections are not designed for concurrent access.
2. **Synchronized Wrappers**: Collections like `Vector` and `Hashtable` use primitive synchronized methods, which can lead to performance bottlenecks due to excessive locking.
   3. Java also provides synchronized wrappers like `Collections.synchronizedList`, `Collections.synchronizedSet`, and `Collections.synchronizedMap`, but these too can suffer from performance issues.

##### Performance Issues with Synchronized Wrappers
- **Lock Contention**: When multiple threads attempt to access a synchronized collection, they must acquire a lock before proceeding. If one thread holds the lock, other threads are blocked until the lock is released. This contention can lead to significant delays, especially under high concurrency.
- **Single Lock for Entire Collection**: This means that even read operations, which could be performed concurrently, are serialized. This reduces the overall throughput of the application.
- **Memory Barriers**: Synchronization introduces memory barriers, which force the JVM to flush data to main memory to ensure visibility across threads. This can prevent certain optimizations and increase the overhead of synchronization.

### Concurrent Collections in Java

Java's `java.util.concurrent` package offers a variety of thread-safe collections designed to **handle concurrent access efficiently**:

1. **BlockingQueue**: Supports operations that wait for the queue to become non-empty when retrieving an element and for space to become available when storing an element. 
   2. Examples include `ArrayBlockingQueue` and `LinkedBlockingQueue`.
2. **ConcurrentMap**: Provides atomic operations for put and remove. 
   3. The most commonly used implementation is `ConcurrentHashMap`, which allows concurrent read and write operations without locking the entire map.
3. **ConcurrentNavigableMap**: Extends `ConcurrentMap` and `NavigableMap`, providing concurrent access and navigation methods.
   4. `ConcurrentSkipListMap` is a common implementation, which is a concurrent version of `TreeMap`.
4. **CopyOnWriteArrayList** and **CopyOnWriteArraySet**: These collections create a copy of the underlying array on each modification, making them ideal for scenarios with frequent reads and infrequent writes.
5. **ConcurrentSkipListSet**: A concurrent version of `TreeSet`, providing scalable and thread-safe sorted sets.

### Fail-Fast and Fail-Safe Iterators

**Fail-Fast Iterators**: These iterators throw a `ConcurrentModificationException` if the collection is **structurally modified** during iteration. 
- This behavior is implemented using an internal modification count (`modCount`).
- Examples : iterators for `ArrayList`, `LinkedList`, `Vector`, and `HashSet`.

**Fail-Safe Iterators**: These iterators operate on **a copy of the collection**, allowing modifications without throwing exceptions. 
- Examples: iterators for `CopyOnWriteArrayList`, `CopyOnWriteArraySet`, and `ConcurrentSkipListSet`.

### Operation-Level Locking

**Operation-level locking** means that the lock is applied only to **the specific operation** being performed, rather than locking the entire object. 
- This allows multiple threads to perform different operations on the same collection concurrently, as long as those operations do not interfere with each other.

##### `ConcurrentHashMap` 
- uses operation-level locking. 
- Instead of locking the entire map for every read or write operation, `ConcurrentHashMap` uses a technique called **lock striping**.

1. **Lock Striping**: The map is divided into segments, each of which can be locked independently. This means that multiple threads can access different segments of the map concurrently without contention.
2. **Fine-Grained Locks**: Each segment has its own lock, and operations on different segments can proceed in parallel. For example, if one thread is updating a key in one segment, another thread can simultaneously read or write a key in a different segment.
3. **Optimistic Reads**: For read operations, `ConcurrentHashMap` uses an optimistic locking strategy. It allows reads to proceed without locking, but if a modification is detected during the read, the operation is retried with a lock.

```java
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentHashMapExample {
    public static void main(String[] args) {
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        map.put("A", 1);
        map.put("B", 2);

        // Concurrent read and write operations
        map.computeIfAbsent("C", k -> 3);
        map.forEach((key, value) -> System.out.println(key + ": " + value));
    }
}
```

#### `CopyOnWriteArrayList`

operation-level locking, but in a different way:

1. **Copy on Write**: When a write operation (such as `add` or `remove`) is performed, the entire underlying array is copied.
   2. This ensures that the write operation does not interfere with ongoing read operations.
2. **Read Operations**: Since the array is copied on write, read operations can proceed **without any locking**.
   3. This makes `CopyOnWriteArrayList` very efficient for scenarios with frequent reads and infrequent writes.

```java
import java.util.concurrent.CopyOnWriteArrayList;

public class CopyOnWriteArrayListExample {
    public static void main(String[] args) {
        CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
        list.add("A");
        list.add("B");

        // Concurrent read and write operations
        list.add("C");
        list.forEach(System.out::println);
    }
}
```

### Benefits of Operation-Level Locking

1. **Improved Concurrency**: By locking only the necessary parts of the collection, multiple threads can perform operations concurrently, leading to better throughput.
2. **Reduced Contention**: Finer-grained locks reduce the likelihood of contention between threads, which can improve performance in multi-threaded environments.
3. **Scalability**: Operation-level locking allows collections to scale better with the number of threads, as different threads can work on different parts of the collection simultaneously.