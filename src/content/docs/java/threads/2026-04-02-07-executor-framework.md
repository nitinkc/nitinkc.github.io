---
title: "Java Multithreading - Part 7: Executor Framework & Thread Pools"
date: 2026-04-02 00:00:07
categories: [java, multithreading, concurrency]
tags: [java, threads, executor, threadpool, future, callable]
---

{% include toc title="Index" icon="cog" %}

# Part 7: Executor Framework & Thread Pools

Managing threads manually becomes complex at scale. The Executor Framework provides a higher-level abstraction.

## Table of Contents
1. [Why Executor Framework?](#why-executor-framework)
2. [ExecutorService Interface](#executorservice-interface)
3. [Types of Thread Pools](#types-of-thread-pools)
4. [Future Interface](#future-interface)
5. [ExecutorCompletionService](#executorcompletionservice)
6. [Shutdown and Lifecycle](#shutdown-and-lifecycle)
7. [Practical Examples](#practical-examples)

---

## Why Executor Framework?

### Problems with Manual Thread Management

```java
// ❌ DON'T: Create threads manually
for (int i = 0; i < 1000; i++) {
    new Thread(task).start();  // Resource intensive, no control
}
```

**Issues:**
- **Expensive creation**: Thread creation involves OS-level operations
- **No limit**: Can accidentally create thousands of threads
- **No reuse**: Threads are discarded after execution
- **Hard to manage**: Tracking lifecycle is complex
- **No return values**: `Runnable.run()` returns void

### Benefits of Executor Framework

| Benefit | Description |
|---------|-------------|
| **Thread reuse** | Pool threads are reused for multiple tasks |
| **Bounded threads** | Control max concurrent threads |
| **Task queuing** | Tasks wait in queue if all threads busy |
| **Return values** | `Future` provides task results |
| **Graceful shutdown** | Proper lifecycle management |
| **Exception handling** | Centralized error handling |

### Fundamental Shift in Thinking

> Instead of **creating a new thread** to do a task, think about **submitting a task** to a thread pool.

This separates the **task** from **how the task will be executed** - the execution policy.

---

## ExecutorService Interface

[ExecutorService Docs](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ExecutorService.html)

```java
public interface ExecutorService extends Executor, AutoCloseable {
    Future<?> submit(Runnable task);
    <T> Future<T> submit(Callable<T> task);
    void shutdown();
    List<Runnable> shutdownNow();
    default void close();  // Java 19+, AutoCloseable
    // ...
}
```

### Key Points

- Implements **AutoCloseable** - can use try-with-resources
- A thread executor creates **non-daemon threads** by default
- Failing to call `shutdown()` will result in application never terminating

### Creating and Using

```java
ExecutorService executor = Executors.newFixedThreadPool(4);

// Submit tasks
executor.execute(runnable);      // No result
Future<?> f = executor.submit(runnable);   // Returns Future
Future<T> f = executor.submit(callable);   // Returns Future<T>

// IMPORTANT: Always shutdown!
executor.shutdown();
```

### Executor Hierarchy

```
                    Executor
                       │
                       ▼
              ExecutorService
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
AbstractExecutor  ScheduledExecutor  ThreadPoolExecutor
Service           Service
```

📁 *Code: `aBasics/cThreadPoolsAKAExecutorFW/aExecutorDemo.java`*

---

## Types of Thread Pools

### 1. Fixed Thread Pool

**Fixed number of threads**. Best for known workload, limiting resource usage.

```java
ExecutorService fixed = Executors.newFixedThreadPool(
    Runtime.getRuntime().availableProcessors()
);
```

```
Task Queue (unbounded):  [T1][T2][T3][T4][T5][T6]...
                              │     │     │
Thread Pool (fixed):        [P1]  [P2]  [P3]
```

### 2. Cached Thread Pool

**Creates threads as needed**, reuses idle threads. Threads idle for 60 seconds are terminated.

⚠️ **Warning**: Can create unbounded threads!

```java
ExecutorService cached = Executors.newCachedThreadPool();
```

**Best for**: Many short-lived tasks.

### 3. Single Thread Executor

**Single thread**, tasks execute sequentially. If thread dies, new one is created.

```java
ExecutorService single = Executors.newSingleThreadExecutor();
// Guarantees FIFO order
```

**Best for**: Sequential task execution.

### 4. Scheduled Thread Pool

**Schedule tasks** for future or periodic execution.

```java
ScheduledExecutorService scheduled = Executors.newScheduledThreadPool(2);

// Execute once after delay
scheduled.schedule(task, 5, TimeUnit.SECONDS);

// Execute repeatedly at fixed rate
scheduled.scheduleAtFixedRate(task, 0, 10, TimeUnit.SECONDS);

// Execute repeatedly with fixed delay between executions
scheduled.scheduleWithFixedDelay(task, 0, 10, TimeUnit.SECONDS);
```

### 5. Work Stealing Pool (Java 8+)

Uses **ForkJoinPool**, work-stealing algorithm.

```java
ExecutorService stealing = Executors.newWorkStealingPool();
// Uses all available processors
```

**Best for**: CPU-intensive parallel tasks.

### 6. Virtual Thread Executor (Java 21+)

Creates a **virtual thread per task**.

```java
ExecutorService virtual = Executors.newVirtualThreadPerTaskExecutor();
// Can handle 100,000+ concurrent tasks!
```

**Best for**: I/O-bound, high-concurrency scenarios.

### Comparison Table

| Pool Type | Threads | Queue | Best For |
|-----------|---------|-------|----------|
| Fixed | N (fixed) | Unbounded | Server requests, known workload |
| Cached | 0 to ∞ | None (direct handoff) | Short async tasks |
| Single | 1 | Unbounded | Sequential execution |
| Scheduled | N (fixed) | Delay queue | Periodic/delayed tasks |
| WorkStealing | CPU cores | Work queues | CPU parallelism |
| Virtual | ∞ (lightweight) | N/A | High-concurrency I/O |

---

## Future Interface

`Future` represents the result of an asynchronous computation.

### Methods

```java
Future<String> future = executor.submit(callable);

// Check status (non-blocking)
future.isDone();
future.isCancelled();

// Get result (BLOCKING!)
String result = future.get();  // Blocks until complete
String result = future.get(1, TimeUnit.SECONDS);  // Blocks with timeout

// Cancel
future.cancel(true);  // mayInterruptIfRunning
```

### Limitations of Future

⚠️ **`get()` blocks!** This defeats the purpose of async:

```java
// Problem: Blocking defeats async purpose
Future<User> userFuture = executor.submit(() -> fetchUser());
User user = userFuture.get();  // BLOCKS main thread!

// Problem: No chaining
// How to: fetchUser → enrichUser → saveUser ?

// Problem: No combining
// How to combine results from multiple futures?
```

**Solution**: `CompletableFuture` (Part 8)

📁 *Code: `bFuturesAndCompletableFutures/futures/FuturesPlay.java`*

---

## ExecutorCompletionService

`ExecutorCompletionService` provides results **as they complete** (not submission order).

### Problem: Regular Future

```java
// Results in submission order - may wait unnecessarily
Future<String> slow = executor.submit(() -> { sleep(3000); return "slow"; });
Future<String> fast = executor.submit(() -> { sleep(1000); return "fast"; });

slow.get();  // Waits 3 seconds, even though fast is done!
fast.get();  // Already done
```

### Solution: CompletionService

```java
ExecutorCompletionService<String> cs = new ExecutorCompletionService<>(executor);

cs.submit(() -> { sleep(3000); return "slow"; });
cs.submit(() -> { sleep(1000); return "fast"; });

// Results in completion order
Future<String> first = cs.take();   // fast (completed first)
Future<String> second = cs.take();  // slow
```

### Visualization

```
Regular Future (submission order):
Submit: T1(3s), T2(1s), T3(2s)
Wait for T1 ──────────────▶ Get T1 (waited 3s even though T2, T3 done)

CompletionService (completion order):
Submit: T1(3s), T2(1s), T3(2s)
T2 done ─▶ Process T2 immediately (1s)
T3 done ─▶ Process T3 immediately (2s)
T1 done ─▶ Process T1 (3s)
```

---

## Shutdown and Lifecycle

### Proper Shutdown

**Always shutdown executors** to prevent resource leaks!

```java
executor.shutdown();              // No new tasks, finish existing
executor.shutdownNow();           // Cancel all tasks, return queue

// Wait for completion
if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
    executor.shutdownNow();       // Force shutdown
}
```

### Try-With-Resources (Java 19+)

```java
// Auto-closes and waits for completion
try (ExecutorService executor = Executors.newFixedThreadPool(4)) {
    executor.submit(task1);
    executor.submit(task2);
}  // Automatically waits and shuts down
```

This is especially useful with **virtual threads**:

```java
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 10000; i++) {
        executor.submit(() -> ioTask());
    }
}  // Waits for all virtual threads to complete
```

### Shutdown Methods

| Method | Description |
|--------|-------------|
| `shutdown()` | No new tasks, complete existing |
| `shutdownNow()` | Cancel all, return waiting tasks |
| `awaitTermination(timeout)` | Wait for completion |
| `close()` | Java 19+, calls shutdown and waits |

---

## Practical Examples

### Sequential vs Parallel Comparison

```java
// Sequential
for (long inputNumber : inputNumbers) {
    BigInteger result = factorial.compute(inputNumber);
}

// With ExecutorService
try (ExecutorService executor = Executors.newFixedThreadPool(
        Runtime.getRuntime().availableProcessors())) {
    
    List<Future<BigInteger>> futures = new ArrayList<>();
    for (long inputNumber : inputNumbers) {
        futures.add(executor.submit(() -> factorial.compute(inputNumber)));
    }
    
    List<BigInteger> results = new ArrayList<>();
    for (Future<BigInteger> future : futures) {
        results.add(future.get());
    }
}
```

### With CompletableFuture

```java
List<CompletableFuture<BigInteger>> futures = inputNumbers.stream()
    .map(n -> CompletableFuture.supplyAsync(() -> factorial.compute(n)))
    .toList();

List<BigInteger> results = futures.stream()
    .map(CompletableFuture::join)
    .toList();
```

### With Virtual Threads (Java 21+)

```java
ThreadFactory factory = Thread.ofVirtual().name("vThread-", 0).factory();
try (ExecutorService srv = Executors.newThreadPerTaskExecutor(factory)) {
    List<Future<BigInteger>> submitted = new ArrayList<>();
    for (long inputNumber : inputNumbers) {
        submitted.add(srv.submit(() -> factorial.compute(inputNumber)));
    }
    
    List<BigInteger> results = submitted.stream()
        .map(future -> {
            try { return future.get(); }
            catch (Exception e) { throw new RuntimeException(e); }
        })
        .toList();
}
```

📁 *Code: `aBasics/cThreadPoolsAKAExecutorFW/bCallableDemo.java`*

---

## Summary

✅ **Executor Framework** manages thread lifecycle automatically  
✅ **Fixed pool** for known workload, **Cached** for many short tasks  
✅ **Scheduled pool** for delayed/periodic execution  
✅ **Virtual Thread Executor** for high-concurrency I/O (Java 21+)  
✅ **Future.get()** blocks - consider CompletableFuture instead  
✅ **CompletionService** provides results as they complete  
✅ **Always shutdown** executors - use try-with-resources (Java 19+)

### Quick Reference

```java
// Create pools
Executors.newFixedThreadPool(n);
Executors.newCachedThreadPool();
Executors.newSingleThreadExecutor();
Executors.newScheduledThreadPool(n);
Executors.newWorkStealingPool();
Executors.newVirtualThreadPerTaskExecutor();  // Java 21+

// Submit tasks
executor.execute(runnable);        // No result
executor.submit(runnable);         // Future<?>
executor.submit(callable);         // Future<T>

// Future methods
future.get();                      // Block
future.get(timeout, unit);         // Block with timeout
future.isDone();
future.cancel(mayInterrupt);

// Shutdown
executor.shutdown();
executor.awaitTermination(60, SECONDS);
executor.shutdownNow();
```

---

*Next: [Part 8: CompletableFuture Mastery →](/java/multithreading/concurrency/08-completable-future-mastery/)*

