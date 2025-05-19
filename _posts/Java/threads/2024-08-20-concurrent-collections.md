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

##### Traditional Collections and Their Limitations
- **Non-Thread-Safe Collections**: Most traditional collections are not designed for concurrent access.

**Synchronized Wrappers**: 
- Collections like `Vector` and `Hashtable` use **primitive synchronized methods**, which can lead to performance bottlenecks due to **excessive locking**.
- synchronized wrappers like `Collections.synchronizedList`, `Collections.synchronizedSet`, and `Collections.synchronizedMap` too can suffer from performance issue

##### Performance Issues with Synchronized Wrappers
- **Lock Contention**: When multiple threads attempt to access a synchronized collection, they must acquire a lock before proceeding. If one thread holds the lock, other threads are blocked until the lock is released. This contention can lead to significant delays, especially under high concurrency.
- **Single Lock for Entire Collection**: This means that even read operations, which could be performed concurrently, are serialized. This reduces the overall throughput of the application.
- **Memory Barriers**: Synchronization introduces memory barriers, which force the JVM to flush data to main memory to ensure visibility across threads. This can prevent certain optimizations and increase the overhead of synchronization.

### Concurrent/Thread-Safe Collections in Java
Java's `java.util.concurrent` package offers a variety of **thread-safe collections** designed to **handle concurrent access efficiently**:

#### 1. **ConcurrentHashMap**
- A high-performance, thread-safe hash table.
- Allows concurrent reads and updates without locking the entire map.

#### 2. **CopyOnWriteArrayList**
- A thread-safe variant of `ArrayList`.
- Ideal for scenarios with **frequent reads** and **infrequent writes**.
- On write, it creates a **new copy** of the underlying array.

#### 3. **CopyOnWriteArraySet**
- Backed by a `CopyOnWriteArrayList`.
- Thread-safe set with similar characteristics: good for read-heavy workloads.

#### 4. **ConcurrentLinkedQueue**
- A non-blocking, thread-safe queue based on linked nodes.
- Suitable for **FIFO** (first-in-first-out) operations in concurrent environments.

#### 5. **ConcurrentLinkedDeque**
- A thread-safe, non-blocking **double-ended queue**.
- Allows insertion and removal from both ends concurrently.

#### 6. **BlockingQueue Interface and Implementations**
Used for **producer-consumer** scenarios with blocking behavior.
- **ArrayBlockingQueue** – bounded, backed by an array.
- **LinkedBlockingQueue** – optionally bounded, backed by linked nodes.
- **PriorityBlockingQueue** – unbounded, orders elements based on priority.
- **DelayQueue** – elements become available after a delay.
- **SynchronousQueue** – no internal capacity; each insert waits for a remove.

#### 7. **BlockingDeque Interface and Implementations**
- **LinkedBlockingDeque** – supports blocking operations on both ends.

#### 8. **ConcurrentSkipListMap / ConcurrentSkipListSet**
- Thread-safe sorted map and set.
- Based on **skip list** data structure.
- Maintains elements in **sorted order**.


### 🧠 When to Use What?

| Collection Type                 | Description                                                                                                                                                                |
|:--------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **ConcurrentHashMap**           | High-performance, thread-safe map with **lock striping**.                                                                                                                  |
| **CopyOnWriteArrayList**        | Thread-safe list optimized for read-heavy workloads with rare modifications.                                                                                               |
| **CopyOnWriteArraySet**         | Set backed by `CopyOnWriteArrayList`.                                                                                                                                      |
| **ConcurrentLinkedQueue**       | Non-blocking, FIFO queue.                                                                                                                                                  |
| **ConcurrentLinkedDeque**       | Non-blocking, double-ended queue.                                                                                                                                          |
| **BlockingQueue**               | Producer-consumer patterns. Supports blocking operations. <br/>Includes `ArrayBlockingQueue`,<br/> `LinkedBlockingQueue`, <br/>`PriorityBlockingQueue`, <br/>`DelayQueue`,<br/> `SynchronousQueue`. |
| **BlockingDeque**               | Double-ended blocking queue. Example: `LinkedBlockingDeque`.                                                                                                               |
| **ConcurrentSkipListMap / Set** | Thread-safe, sorted concurrent map/set using skip lists.                                                                                                                              


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

        // Thread for adding elements
        Thread writerThread = new Thread(() -> {
            list.add("C");
            list.add("D");
        });

        // Thread for reading elements
        Thread readerThread = new Thread(() -> {
            list.forEach(System.out::println);
        });

        // Start both threads
        writerThread.start();
        readerThread.start();

        // Wait for both threads to finish
        try {
            writerThread.join();
            readerThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}

```

### Benefits of Operation-Level Locking

1. **Improved Concurrency**: By locking only the necessary parts of the collection, multiple threads can perform operations concurrently, leading to better throughput.
2. **Reduced Contention**: Finer-grained locks reduce the likelihood of contention between threads, which can improve performance in multi-threaded environments.
3. **Scalability**: Operation-level locking allows collections to scale better with the number of threads, as different threads can work on different parts of the collection simultaneously.