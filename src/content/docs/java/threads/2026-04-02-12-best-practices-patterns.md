---
title: "Java Multithreading - Part 12: Best Practices & Patterns"
date: 2026-04-02 00:00:12
categories: [java, multithreading, concurrency]
tags: [java, threads, best-practices, patterns, interview, pitfalls]
---

{% include toc title="Index" icon="cog" %}

# Part 12: Best Practices & Patterns

The final part covers essential best practices, common pitfalls, design patterns, and interview preparation.

## Table of Contents
1. [Best Practices Summary](#best-practices-summary)
2. [Common Pitfalls](#common-pitfalls)
3. [Design Patterns](#design-patterns)
4. [Performance Tuning](#performance-tuning)
5. [Testing Concurrent Code](#testing-concurrent-code)
6. [Interview Questions](#interview-questions)
7. [Timeline of Java Concurrency](#timeline-of-java-concurrency)
8. [Key Takeaways](#key-takeaways)

---

## Best Practices Summary

### Thread Creation

```java
// ❌ DON'T: Create threads manually
for (int i = 0; i < 1000; i++) new Thread(task).start();

// ✅ DO: Use ExecutorService
try (var executor = Executors.newFixedThreadPool(cores)) {
    for (int i = 0; i < 1000; i++) executor.submit(task);
}

// ✅ BETTER (Java 21+): Virtual Threads for I/O
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(ioTask);
}
```

### Synchronization

```java
// ❌ DON'T: Over-synchronize entire method
public synchronized void method() { 
    readOnly(); critical(); readOnly(); 
}

// ✅ DO: Minimize synchronized scope
public void method() {
    readOnly();
    synchronized (lock) { critical(); }
    readOnly();
}

// ✅ DO: Use appropriate tools
private volatile boolean running = true;           // Flag
private final AtomicInteger counter = new AtomicInteger(0);  // Counter
private final ReadWriteLock lock = new ReentrantReadWriteLock();  // R/W
```

### Exception Handling

```java
// ❌ DON'T: Ignore exceptions
executor.submit(() -> riskyOp());  // Silently swallowed!

// ✅ DO: Handle properly
executor.submit(() -> {
    try { riskyOp(); }
    catch (Exception e) { log.error("Failed", e); }
});

// ✅ OR: Use CompletableFuture
CompletableFuture.supplyAsync(this::riskyOp)
    .exceptionally(ex -> { log.error(ex); return fallback; });
```

### Resource Management

```java
// ❌ DON'T: Forget shutdown
ExecutorService executor = Executors.newFixedThreadPool(4);
executor.submit(task);
// Resource leak!

// ✅ DO: Always shutdown (Java 19+ try-with-resources)
try (var executor = Executors.newFixedThreadPool(4)) {
    executor.submit(task);
}  // Auto-closes
```

---

## Common Pitfalls

### Pitfall 1: Race Conditions

```java
// ❌ counter++ is NOT atomic
private int counter = 0;
public void increment() { counter++; }

// ✅ FIX: synchronized OR AtomicInteger
public synchronized void increment() { counter++; }
// OR
private final AtomicInteger counter = new AtomicInteger(0);
```

### Pitfall 2: Deadlocks

```java
// ❌ DEADLOCK - Different lock order
method1(): lock(A) → lock(B)
method2(): lock(B) → lock(A)  // Opposite!

// ✅ FIX: Same lock order everywhere
// ✅ OR: Use tryLock with timeout
if (lock.tryLock(1, SECONDS)) { ... }
```

### Pitfall 3: Memory Visibility

```java
// ❌ Loop may never exit (CPU caches running)
private boolean running = true;
while (running) { doWork(); }

// ✅ FIX: volatile
private volatile boolean running = true;
```

### Pitfall 4: Double-Checked Locking

```java
// ❌ BROKEN (pre-Java 5)
if (instance == null) {
    synchronized(cls) { 
        if (instance == null) instance = new X(); 
    }
}

// ✅ FIX: volatile instance
private static volatile X instance;

// ✅ BETTER: Holder pattern
private static class Holder { 
    static final X INSTANCE = new X(); 
}

// ✅ BEST: Enum singleton
public enum Singleton { INSTANCE; }
```

### Pitfall 5: ThreadLocal Leaks

```java
// ❌ LEAK in thread pools
ThreadLocal<X> local = new ThreadLocal<>();
local.get();  // Forgot to remove!

// ✅ FIX: Always clean up
try { local.get(); } 
finally { local.remove(); }

// ✅ BETTER (Java 21+): ScopedValue
ScopedValue.where(KEY, value).run(() -> { ... });  // Auto-cleaned
```

### Pitfall 6: Busy Waiting

```java
// ❌ Wastes CPU
while (!condition) { }

// ✅ FIX: wait/notify or higher-level constructs
synchronized(lock) { 
    while (!condition) lock.wait(); 
}
// OR
latch.await();
```

### Pitfall 7: Not Restoring Interrupt Flag

```java
// ❌ BAD: Swallowing interrupt
try { Thread.sleep(1000); }
catch (InterruptedException e) { }  // Lost!

// ✅ FIX: Restore interrupt flag
try { Thread.sleep(1000); }
catch (InterruptedException e) {
    Thread.currentThread().interrupt();  // Restore!
}
```

---

## Design Patterns

### Producer-Consumer

```java
BlockingQueue<T> queue = new LinkedBlockingQueue<>(capacity);

// Producer
queue.put(item);  // Blocks if full

// Consumer
T item = queue.take();  // Blocks if empty
```

### Thread-Safe Singleton

```java
// ✅ BEST: Enum singleton
public enum Singleton { INSTANCE; }

// ✅ GOOD: Holder pattern
private static class Holder { 
    static final X INSTANCE = new X(); 
}
public static X getInstance() { return Holder.INSTANCE; }
```

### Object Pool

```java
BlockingQueue<T> pool = new LinkedBlockingQueue<>(size);
T obj = pool.take();     // Borrow
pool.offer(obj);         // Return
```

### Async Request Handler

```java
CompletableFuture.supplyAsync(() -> validate(request))
    .thenCompose(valid -> fetchData(request.userId()))
    .thenCombine(fetchPermissions(request.userId()), this::process)
    .thenApply(result -> new Response(200, result))
    .exceptionally(ex -> new Response(500, ex.getMessage()));
```

---

## Performance Tuning

### Thread Pool Sizing

```java
int cores = Runtime.getRuntime().availableProcessors();

// CPU-bound: number of cores
int cpuBound = cores;

// I/O-bound: cores * (1 + wait/compute ratio)
int ioBound = cores * 10;  // Heavy I/O

// Mixed workload: separate pools
ExecutorService cpuPool = Executors.newFixedThreadPool(cpuBound);
ExecutorService ioPool = Executors.newCachedThreadPool();

// Java 21+: Virtual threads for I/O
Executors.newVirtualThreadPerTaskExecutor();
```

### Lock-Free Data Structures

```java
// Use Atomic classes for simple lock-free operations
AtomicReference<Node<T>> head = new AtomicReference<>();
head.compareAndSet(oldNode, newNode);  // CAS
```

### Avoiding False Sharing

```java
// Pad cache lines (64 bytes) between contended variables
@Contended volatile long counter1;
@Contended volatile long counter2;
```

---

## Testing Concurrent Code

### Using CountDownLatch

```java
CountDownLatch startLatch = new CountDownLatch(1);
CountDownLatch endLatch = new CountDownLatch(threads);

for (int i = 0; i < threads; i++) {
    new Thread(() -> {
        startLatch.await();  // Wait for signal
        doWork();
        endLatch.countDown();
    }).start();
}

startLatch.countDown();  // Start all simultaneously
endLatch.await();        // Wait for all to finish
assertEquals(expected, actual);
```

### Repeated Tests for Race Conditions

```java
@RepeatedTest(100)  // Run many times to catch races
void testRaceCondition() { ... }
```

---

## Interview Questions

### Q1: wait() vs sleep()

| wait() | sleep() |
|--------|---------|
| Object method | Thread method |
| **Releases lock** | Does NOT release lock |
| Must be in synchronized | Can be anywhere |
| Woken by notify | Wakes after time |

### Q2: How to prevent deadlock?

1. **Lock ordering** - Same order everywhere
2. **Lock timeout** - `tryLock(timeout)`
3. **Single lock** - Minimize nesting
4. **Higher-level constructs** - Semaphore, Latch

### Q3: volatile vs synchronized?

| volatile | synchronized |
|----------|--------------|
| Visibility only | Visibility + Atomicity |
| No blocking | Blocking |
| Simple flags | Compound operations |

### Q4: Future vs CompletableFuture?

| Future | CompletableFuture |
|--------|-------------------|
| Blocking get() | Non-blocking callbacks |
| No chaining | thenApply, thenCompose |
| No combining | allOf, anyOf, thenCombine |

### Q5: When to use Virtual Threads?

- **USE**: I/O-bound (HTTP, DB, files)
- **DON'T USE**: CPU-bound (no benefit, blocks carrier)

### Q6: Happens-before relationship?

```
// Program order within thread
// synchronized: unlock → lock
// volatile: write → read
// Thread: start() → run(), run() → join()
```

### Q7: What makes counter++ not thread-safe?

It's **3 operations**, not 1:
1. Read current value
2. Increment
3. Write new value

Another thread can interleave between these operations.

### Q8: ReentrantLock vs synchronized?

| Feature | synchronized | ReentrantLock |
|---------|--------------|---------------|
| tryLock | ❌ | ✅ |
| Timeout | ❌ | ✅ |
| Interruptible | ❌ | ✅ |
| Fairness | ❌ | ✅ |
| Conditions | 1 (wait/notify) | Multiple |

### Q9: What is a memory barrier?

Prevents CPU/compiler from reordering reads/writes across the barrier:
- **Store barrier**: Writes can't move after barrier
- **Load barrier**: Reads can't move before barrier

### Q10: ConcurrentHashMap vs synchronized HashMap?

| ConcurrentHashMap | synchronized HashMap |
|-------------------|---------------------|
| Bucket-level locking | Object-level locking |
| Multiple concurrent reads/writes | One at a time |
| Lock-free reads | All operations locked |
| Better scalability | Poor scalability |

---

## Timeline of Java Concurrency

```
Java 1.0  │ synchronized, Thread, wait/notify
Java 5    │ ExecutorService, Locks, Atomics, Concurrent Collections
Java 7    │ Fork/Join Framework
Java 8    │ CompletableFuture, Parallel Streams
Java 21   │ Virtual Threads, Structured Concurrency, ScopedValue
```

---

## Key Takeaways

### 1. Understand Fundamentals
- Thread lifecycle, synchronization, visibility
- Race conditions vs data races

### 2. Use High-Level Constructs
- Executors over raw threads
- CompletableFuture over callbacks
- Concurrent collections over synchronized wrappers

### 3. Choose Right Tool

| Need | Tool |
|------|------|
| Flag | volatile |
| Counter | AtomicInteger |
| Compound ops | synchronized/Lock |
| Multiple readers | ReadWriteLock |
| Resource limiting | Semaphore |
| Coordination | Latch/Barrier |

### 4. Consider Virtual Threads (Java 21+)
- For I/O-bound scalability
- One-thread-per-request is viable again

### 5. Test Thoroughly
- Concurrency bugs are hard to reproduce
- Use repeated tests, stress tests

### 6. Keep It Simple
- Complexity breeds bugs
- Prefer immutability when possible

---

## Series Recap

| Part | Topic | Key Concepts |
|------|-------|--------------|
| 1 | Fundamentals | Theory, Process vs Thread, Memory Model |
| 2 | Thread Creation | Runnable, Callable, Daemon, Fluent API |
| 3 | Control | Priority, sleep, yield, join, interrupt |
| 4 | Race Conditions | Atomic operations, Critical sections |
| 5 | Synchronization | synchronized, volatile, Atomic |
| 6 | Locks | ReentrantLock, ReadWriteLock, Semaphore |
| 7 | Executors | Thread pools, Future, Callable |
| 8 | CompletableFuture | Async pipelines, combining, errors |
| 9 | Collections | ConcurrentHashMap, BlockingQueue |
| 10 | Virtual Threads | Project Loom, Carrier threads |
| 11 | Structured Concurrency | TaskScope, ScopedValue |
| 12 | Best Practices | Patterns, pitfalls, interview |

---

## Further Reading

- [Java Concurrency in Practice](https://jcip.net/) - Brian Goetz
- [JEP 444: Virtual Threads](https://openjdk.org/jeps/444)
- [JEP 453: Structured Concurrency](https://openjdk.org/jeps/453)
- [JEP 446: Scoped Values](https://openjdk.org/jeps/446)
- [Inside the Linux 2.6 CFS](https://developer.ibm.com/tutorials/l-completely-fair-scheduler/)

---

## Final Checklist

Before your interview or code review, verify:

- [ ] No race conditions (atomic ops or synchronized)
- [ ] No deadlocks (consistent lock ordering)
- [ ] Proper visibility (volatile or synchronized)
- [ ] ExecutorService shut down properly
- [ ] ThreadLocal cleaned up (or use ScopedValue)
- [ ] InterruptedException handled (flag restored)
- [ ] Appropriate thread pool sizes
- [ ] CompletableFuture errors handled

---

*This concludes the Java Multithreading Mastery series. Happy concurrent programming! 🚀*

*Last Updated: April 2026*

