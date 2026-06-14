---
title: "Java Multithreading - Part 9: Concurrent Collections"
date: 2026-04-02 00:00:09
categories: [java, multithreading, concurrency]
tags: [java, threads, concurrent-collections, concurrenthashmap, blockingqueue]
---

{% include toc title="Index" icon="cog" %}

# Part 9: Concurrent Collections

{% include toc title="Index" %}

Thread-safe collections designed for high-performance concurrent access.

## Table of Contents
1. [Problems with Traditional Collections](#problems-with-traditional-collections)
2. [Synchronized Wrappers Issues](#synchronized-wrappers-issues)
3. [Concurrent Collection Types](#concurrent-collection-types)
4. [ConcurrentHashMap Deep Dive](#concurrenthashmap-deep-dive)
5. [CopyOnWriteArrayList](#copyonwritearraylist)
6. [BlockingQueue](#blockingqueue)
7. [Fail-Fast vs Fail-Safe Iterators](#fail-fast-vs-fail-safe-iterators)
8. [Operation-Level vs Object-Level Locking](#operation-level-vs-object-level-locking)

---

## Problems with Traditional Collections

### Traditional Collections and Their Limitations

In multi-threaded environments, traditional collections like `ArrayList`, `HashMap`, and `HashSet`:

1. **ConcurrentModificationException**: One thread modifies a collection while another thread is iterating over it
2. **Not Thread-Safe**: Most traditional collections are not designed for concurrent access (**not thread-safe**)
3. **Data corruption**: Inconsistent states during concurrent modifications

```java
// ❌ PROBLEM: ConcurrentModificationException
List<String> list = new ArrayList<>();
// Thread 1 iterating, Thread 2 modifying simultaneously
```

To address these issues, Java provides **concurrent collections** in the `java.util.concurrent` package.

---

## Synchronized Wrappers Issues

### The Old Approach

```java
List<String> syncList = Collections.synchronizedList(new ArrayList<>());
Map<K,V> syncMap = Collections.synchronizedMap(new HashMap<>());
Set<E> syncSet = Collections.synchronizedSet(new HashSet<>());
```

### Synchronized Wrappers

Collections like `Vector` and `Hashtable` use **primitive synchronized methods**, which can lead to performance bottlenecks due to **excessive locking**.

Synchronized wrappers like `Collections.synchronizedList`, `Collections.synchronizedSet`, and `Collections.synchronizedMap` too can suffer from performance issues.

### Performance Problems with Synchronized Wrappers

| Problem | Description |
|---------|-------------|
| **Lock Contention** | When multiple threads attempt to access a synchronized collection, they must acquire a lock before proceeding. If one thread holds the lock, other threads are blocked until the lock is released. This contention can lead to significant delays, especially under high concurrency. |
| **Single Lock for Entire Collection** | This means that even read operations, which could be performed concurrently, are serialized. This reduces the overall throughput of the application. |
| **Memory Barriers** | Synchronization introduces memory barriers, which force the JVM to flush data to main memory to ensure visibility across threads. This can prevent certain optimizations and increase the overhead of synchronization. |
| **Poor Scalability** | Performance degrades with more threads |

**Result**: Only one thread can access the collection at a time, even for read operations.

---

## Concurrent Collection Types

Java's `java.util.concurrent` package offers a variety of **thread-safe collections** designed to **handle concurrent access efficiently**:

| Collection Type                 | Description                                                                                                                      |
|:--------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| **ConcurrentHashMap**           | High-performance, thread-safe map with concurrent reads/updates without locking the entire map.                                  |
| **CopyOnWriteArrayList**        | Thread-safe list for **read-heavy, write-rare** workloads; writes copy the underlying array.                                     |
| **CopyOnWriteArraySet**         | Set backed by `CopyOnWriteArrayList`; good for read-heavy workloads.                                                             |
| **ConcurrentLinkedQueue**       | Non-blocking, FIFO queue based on linked nodes.                                                                                  |
| **ConcurrentLinkedDeque**       | Non-blocking, double-ended queue; insert/remove from both ends concurrently.                                                     |
| **BlockingQueue**               | Producer-consumer patterns with blocking operations.                                                                             |
|                                 | Implementations: `ArrayBlockingQueue` (bounded array), `LinkedBlockingQueue` (optionally bounded), `PriorityBlockingQueue`.      |
|                                 | Implementations: `DelayQueue` (delayed availability), `SynchronousQueue` (no internal capacity).                                 |
| **BlockingDeque**               | Double-ended blocking queue. Implementation: `LinkedBlockingDeque`.                                                              |
| **ConcurrentSkipListMap / Set** | Thread-safe, sorted concurrent map/set using **skip lists**; maintains elements in **sorted order**.                             |

---

## ConcurrentHashMap Deep Dive

The most commonly used concurrent collection.

### Why ConcurrentHashMap?

Instead of locking the entire map for every read or write, it uses **fine-grained locking mechanisms** to maximize concurrency and performance.

### Evolution

#### 1. Lock Striping (Java 7 and earlier)

- The map was divided into **segments** (like mini hash tables)
- Each segment had its own lock, allowing multiple threads to access different segments **simultaneously**
- This significantly reduced contention compared to synchronizing the entire map

#### 2. Bucket-Level Synchronization (Java 8 and later)

- Java 8 replaced segments with a **lock-free, bucket-based structure**
- Internally, it uses a `Node[]` table (similar to `HashMap`) and **CAS (Compare-And-Swap)** operations for atomic updates
- For hash collisions:
   - Initially uses **linked lists**
   - Converts to **balanced trees (TreeNodes)** when a bucket becomes too full, improving lookup performance

### Key Features

#### 3. Fine-Grained Synchronization

- Only **individual buckets** are locked during updates like `put` or `remove`
- **Read operations (`get`) are non-blocking** and extremely fast, thanks to minimal locking

#### 4. Optimistic Reads

- `ConcurrentHashMap` uses an **optimistic locking strategy** for reads
- Reads proceed without locking. If a concurrent modification is detected, the operation is retried with a lock to ensure consistency

#### 5. Atomic Methods

- Methods like `putIfAbsent`, `compute`, `merge`, and `computeIfAbsent` are **atomic**
- These ensure thread-safe updates without requiring external synchronization

### Usage

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();

// Basic operations
map.put("key", 1);
int value = map.get("key");

// Atomic operations
map.putIfAbsent("key", 2);  // Only if absent
map.computeIfAbsent("key", k -> computeValue(k));
map.compute("key", (k, v) -> v == null ? 1 : v + 1);
map.merge("key", 1, Integer::sum);

// Bulk operations (Java 8+)
map.forEach((k, v) -> process(k, v));
map.search(1, (k, v) -> v > 100 ? k : null);
map.reduce(1, (k, v) -> v, Integer::sum);
```

{% gist /nitinkc/9b122aaa11f92b38cb42a8ae27cf3b42 %}

### When NOT Thread-Safe

Compound operations are still not atomic:

```java
// ❌ NOT atomic - race condition!
if (!map.containsKey(key)) {
    map.put(key, value);
}

// ✅ Use atomic method instead
map.putIfAbsent(key, value);
```

---

## CopyOnWriteArrayList

Thread-safe list optimized for **read-heavy, write-rare** scenarios.

### How It Works - Operation-Level Locking

`CopyOnWriteArrayList` uses operation-level locking, but in a different way:

1. **Copy on Write**: When a write operation (such as `add` or `remove`) is performed, the entire underlying array is copied
   - This ensures that the write operation does not interfere with ongoing read operations
2. **Read Operations**: Since the array is copied on write, read operations can proceed **without any locking**
   - This makes `CopyOnWriteArrayList` very efficient for scenarios with frequent reads and infrequent writes

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();

// Reads are fast - no locking
String item = list.get(0);

// Writes copy the array
list.add("new item");  // Copies entire array!
```

{% gist nitinkc/b67916c4147ab0657bfbfe133e47a256 %}

### Characteristics

| Aspect | Behavior |
|--------|----------|
| Read Performance | Excellent (no locking) |
| Write Performance | Poor (copies entire array) |
| Iterator | Snapshot at creation time |
| Best For | Read-heavy, small lists |

### Use Cases

- Event listener lists
- Observer patterns
- Configuration settings (rarely change)

---

## BlockingQueue

Queues that support blocking operations for producer-consumer patterns.

### Types

| Queue | Characteristics |
|-------|-----------------|
| **ArrayBlockingQueue** | Bounded, array-based, FIFO |
| **LinkedBlockingQueue** | Optionally bounded, linked nodes |
| **PriorityBlockingQueue** | Unbounded, priority ordering |
| **SynchronousQueue** | Zero capacity, direct handoff |
| **DelayQueue** | Elements available after delay |

### Blocking Operations

```java
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);

// Producer
queue.put(task);     // Blocks if full
queue.offer(task, 1, TimeUnit.SECONDS);  // Timeout

// Consumer
Task task = queue.take();  // Blocks if empty
Task task = queue.poll(1, TimeUnit.SECONDS);  // Timeout
```

### Method Summary

| Operation | Throws | Blocks | Times Out | Returns Special |
|-----------|--------|--------|-----------|-----------------|
| Insert | add(e) | put(e) | offer(e,t,u) | offer(e) |
| Remove | remove() | take() | poll(t,u) | poll() |
| Examine | element() | - | - | peek() |

### Producer-Consumer Example

```java
BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);

// Producer
new Thread(() -> {
    while (true) {
        queue.put(produceTask());  // Blocks if full
    }
}).start();

// Consumer
new Thread(() -> {
    while (true) {
        Task task = queue.take();  // Blocks if empty
        processTask(task);
    }
}).start();
```

---

## Fail-Fast vs Fail-Safe Iterators

### Fail-Fast Iterators

**Throw `ConcurrentModificationException`** if the collection is **structurally modified** during iteration.

- This behavior is implemented using an internal modification count (`modCount`)
- **Examples**: Iterators for `ArrayList`, `LinkedList`, `Vector`, and `HashSet`

```java
List<String> list = new ArrayList<>();
for (String s : list) {
    list.add("new");  // Throws ConcurrentModificationException!
}
```

### Fail-Safe Iterators

**Operate on a copy of the collection**, allowing modifications without throwing exceptions.

- No exception thrown
- May not reflect latest changes
- **Examples**: Iterators for `CopyOnWriteArrayList`, `CopyOnWriteArraySet`, and `ConcurrentSkipListSet`

```java
CopyOnWriteArrayList<String> list = new CopyOnWriteArrayList<>();
for (String s : list) {
    list.add("new");  // Works! Iterates over snapshot
}
```

### Comparison

| Aspect | Fail-Fast | Fail-Safe |
|--------|-----------|-----------|
| Exception | ConcurrentModificationException | None |
| Data | Current data | Snapshot (may be stale) |
| Memory | No extra memory | May use extra memory |
| Examples | ArrayList, HashMap | CopyOnWrite*, Concurrent* |

---

## Operation-Level vs Object-Level Locking

### Object-Level Locking

Locks the **entire object** for every operation.

- Common in synchronized wrappers like `Collections.synchronizedList`
- **Drawback**: Only one thread can access the collection at a time, even if operations are unrelated
- **Result**: High contention and poor scalability in multi-threaded environments

```java
// synchronized wrappers use object-level locking
List<String> list = Collections.synchronizedList(new ArrayList<>());

// Only ONE thread can access at a time, even for reads
```

### Operation-Level Locking

**Operation-level locking** means that the lock is applied only to the **specific operation** being performed, rather than locking the entire object.

This allows multiple threads to perform different operations on the same collection **concurrently**, as long as those operations don't interfere with each other.

```java
// ConcurrentHashMap uses operation-level locking
ConcurrentHashMap<K, V> map = new ConcurrentHashMap<>();

// Multiple threads can access different buckets simultaneously
```

### Benefits of Operation-Level Locking

1. **Improved Concurrency**: By locking only the necessary parts of the collection, multiple threads can perform operations concurrently, leading to better throughput
2. **Reduced Contention**: Finer-grained locks reduce the likelihood of contention between threads, which can improve performance in multi-threaded environments
3. **Scalability**: Operation-level locking allows collections to scale better with the number of threads, as different threads can work on different parts of the collection simultaneously

### Comparison

| Feature | Object-Level Locking | Operation-Level Locking |
|:--------|:---------------------|:------------------------|
| **Granularity** | Coarse (entire object) | Fine (specific operation or segment) |
| **Concurrency** | Low | High |
| **Performance** | Degrades with more threads | Scales well with more threads |
| **Use Case** | Simple synchronization | High-performance, multi-threaded applications |
| **Example** | `Collections.synchronizedList` | `ConcurrentHashMap`, `CopyOnWriteArrayList` |

---

## Summary

✅ **Traditional collections** not thread-safe; synchronized wrappers have poor performance  
✅ **ConcurrentHashMap** uses bucket-level locking + CAS for high concurrency  
✅ **CopyOnWriteArrayList** best for read-heavy, write-rare scenarios  
✅ **BlockingQueue** for producer-consumer patterns  
✅ **Fail-fast iterators** throw ConcurrentModificationException; **fail-safe** work on snapshots  
✅ **Operation-level locking** scales better than object-level

### Quick Reference

```java
// ConcurrentHashMap
ConcurrentHashMap<K, V> map = new ConcurrentHashMap<>();
map.putIfAbsent(key, value);
map.computeIfAbsent(key, k -> compute(k));
map.merge(key, value, (old, new) -> old + new);

// CopyOnWriteArrayList
CopyOnWriteArrayList<E> list = new CopyOnWriteArrayList<>();

// BlockingQueue
BlockingQueue<E> queue = new LinkedBlockingQueue<>(capacity);
queue.put(e);      // Block if full
queue.take();      // Block if empty
queue.offer(e, timeout, unit);
queue.poll(timeout, unit);

// ConcurrentSkipListMap (sorted)
ConcurrentSkipListMap<K, V> sortedMap = new ConcurrentSkipListMap<>();
```

### Choosing the Right Collection

| Use Case | Collection |
|----------|------------|
| Key-value, high concurrency | ConcurrentHashMap |
| List, read-heavy | CopyOnWriteArrayList |
| Queue, producer-consumer | BlockingQueue |
| Sorted map, concurrent | ConcurrentSkipListMap |
| Sorted set, concurrent | ConcurrentSkipListSet |

---

*Next: [Part 10: Virtual Threads →](/java/multithreading/concurrency/10-virtual-threads/)*
