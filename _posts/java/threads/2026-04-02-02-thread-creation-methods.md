---
title: "Java Multithreading - Part 2: Thread Creation Methods"
date: 2026-04-02 00:00:01
categories: [java, multithreading, concurrency]
tags: [java, threads, runnable, callable, daemon, creation]
---

{% include toc title="Index" icon="cog" %}

This part covers **all ways** to create threads in Java, from traditional approaches to modern Java 21+ methods.

---

## Runnable vs Callable

Two fundamental interfaces for defining tasks:

### Runnable
[Runnable Docs](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/Runnable.html#run())

```java
@FunctionalInterface
public interface Runnable {
    void run();  // No return, no checked exception
}
```

- **No return value** (`void`)
- **Cannot throw** checked exceptions
- Can be used with `Thread` or `ExecutorService`

### Callable
[Callable Docs](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/Callable.html#call())

```java
@FunctionalInterface
public interface Callable<V> {
    V call() throws Exception;  // Returns V, can throw
}
```

- **Returns** a value of type `V`
- **Can throw** exceptions
- Can only be used with `ExecutorService`

### Comparison

| Feature            | Runnable         | Callable      |
|:-------------------|:-----------------|:--------------|
| Method             | `void run()`     | `V call()`    |
| Return value       | None (void)      | Returns V     |
| Checked exceptions | Cannot throw     | Can throw     |
| Used with          | Thread, Executor | Executor only |

---

## Traditional Thread Creation

### Method 1: Extending Thread Class ❌ (Not Recommended)

```java
class SimpleThread extends Thread {
    @Override
    public void run() {
        System.out.println("Thread running: " + getName());
    }
}

// Usage
Thread thread = new SimpleThread();
thread.start();
```

**Why NOT recommended:**
- Java doesn't support multiple inheritance
- If you extend `Thread`, you **cannot extend** any other class
- Limits flexibility and reusability

📁 *Code: `aBasics/aPlatformThreads/T2ThreadByExtending.java`*

### Method 2: Implementing Runnable Interface ✅ (Preferred)

```java
class SimpleRunnable implements Runnable {
    @Override
    public void run() {
        System.out.println("Runnable running");
    }
}

// Usage
Runnable runnable = new SimpleRunnable();
Thread thread = new Thread(runnable);
thread.start();
```

**Why preferred:**
- Can still extend other classes
- Separates task from thread mechanism
- More flexible design

📁 *Code: `aBasics/aPlatformThreads/T3ThreadByRunnable.java`*

### Method 3: Using Lambda Expressions ✅ (Modern)

Since `Runnable` is a functional interface (single abstract method), we can use lambdas:

```java
Thread thread = new Thread(() -> {
    System.out.println("Lambda thread running");
});
thread.start();
```

**Inline lambda:**
```java
Thread.ofPlatform().start(() -> {
    TimeUnit.SECONDS.sleep(5);
});
```

📁 *Code: `aBasics/aPlatformThreads/T4CreateByLambda.java`*

### Method 4: Using Method Reference ✅

When lambda body just calls an existing method:

```java
Thread thr = new Thread(MethodReferenceClass::doSomething);
thr.start();

// Or
Thread.ofPlatform().start(MethodReferenceClass::doSomething);
```

📁 *Code: `aBasics/aPlatformThreads/T5CreateByMethodReference.java`*

### Comparison Table

| Approach           | Pros                                    | Cons                                 |
|:-------------------|:----------------------------------------|:-------------------------------------|
| Extend Thread      | Simple, direct access to Thread methods | Can't extend other classes           |
| Implement Runnable | Flexible, can extend other classes      | Need to wrap in Thread               |
| Lambda             | Concise, modern syntax                  | Only for simple cases                |
| Method Reference   | Clean, reusable                         | Method must match Runnable signature |

---

## Fluent API (Modern Java)

Java provides a modern fluent API for thread creation.

### Platform Thread Builder

```java
Runnable r = new SimpleRunnable();

// Named thread
Thread thread = Thread.ofPlatform()
    .name("MyThread-1")
    .start(r);

// With all options
Thread thread = Thread.ofPlatform()
    .name("Worker")
    .daemon(false)
    .priority(Thread.NORM_PRIORITY)
    .start(r);
```

### Daemon Thread via Fluent API

```java
Runnable r = new SimpleRunnable();
Thread thread = Thread.ofPlatform()
    .name("BackgroundTask")
    .daemon(true)
    .start(r);
```

### Virtual Thread Builder (Java 21+)

```java
Thread vt = Thread.ofVirtual()
    .name("VirtualWorker")
    .start(() -> doWork());
```

---

## Daemon Threads

A daemon thread is a **background thread** that does not prevent JVM from exiting.

### Characteristics

- When all **non-daemon** threads finish, JVM can shut down
- Daemon threads are **terminated abruptly** when JVM exits
- Typically used for background services like:
  - Garbage collection
  - Background monitoring
  - Signal handlers

### By Default
In Java, all threads are **non-daemon threads** (unless explicitly modified).
- JVM will not terminate until all non-daemon threads have finished
- True even if main thread has terminated

### Setting Daemon Status

```java
thread.setDaemon(true);   // Must be called BEFORE start()!
thread.setDaemon(false);  // false = non-daemon (default)
thread.start();
```

**Important**: `setDaemon()` must be called **before** `start()`!

### Explanation

```java
thread.setDaemon(false); // Non-daemon: runs even if parent dies
thread.setDaemon(true);  // Daemon: dies as soon as parent dies
```

📁 *Code: `aBasics/aPlatformThreads/T1ThreadRunsParentDies.java`*

### User vs Daemon Threads

| Aspect | User Thread | Daemon Thread |
|--------|-------------|---------------|
| JVM Exit | JVM waits for all user threads | JVM doesn't wait |
| Purpose | Main application work | Background services |
| Example | Main thread, worker threads | GC, signal handlers |
| Creation | Default | `setDaemon(true)` before start |
| Termination | Completes normally | Abruptly when JVM exits |
| Priority | High priority | Low priority |

### Virtual Threads are Always Daemon

```java
// Virtual threads are ALWAYS daemon threads
// Attempt to set as non-daemon throws exception
Thread vt = Thread.startVirtualThread(() -> task());
// vt.setDaemon(false); // Throws IllegalArgumentException!

// Don't forget to call join() to wait for virtual threads!
vt.join();
```

---

## start() vs run()

### The Difference

| `start()` | `run()` |
|-----------|---------|
| Creates a **new thread** | **No new thread** created |
| Internally calls `run()` | Just a normal method call |
| Executes **asynchronously** | Executes in **calling thread** |
| Each thread runs independently | Blocks the calling thread |

### Correct Usage

```java
Thread t = new Thread(() -> {
    System.out.println("Running in: " + Thread.currentThread().getName());
});

t.start();  // ✅ Correct: Creates new thread, prints "Thread-0"
```

### Wrong Usage

```java
Thread t = new Thread(() -> {
    System.out.println("Running in: " + Thread.currentThread().getName());
});

t.run();  // ❌ Wrong: No new thread, prints "main"
```

### Key Points

- **`start()`** → Creates new thread, internally calls `run()`. New thread executes asynchronously.
- **`run()` directly** → Just a normal method call. No new thread! Executes in the calling thread.
- **Never restart a thread** → Throws `IllegalThreadStateException`. Create a new thread instead.
- **Thread scheduler** decides execution order - output is **non-deterministic**

---

## Platform Threads - Issues

### Problem 1: Memory Intensive
- Platform Thread is an **expensive resource**
- Each thread is allocated **1 MB of memory** by default

### Problem 2: Startup Time
- Starting a platform thread takes time
- Can lead to performance issues

### Solution: Thread Pools
- Every application server creates a **default thread-pool**
- User request is handed to an **already created thread** rather than creating new one

### Example: Tomcat
- By default, Tomcat uses a thread-pool size of **200**
- If 250 concurrent users hit the application:
  - **50 will wait** for a platform thread to process their request

### Fundamental Shift in Thinking

> Instead of **creating a new thread** to do a task, think about **submitting a task** to a thread pool.

This separates the **task** from **how the task will be executed** - the execution policy.

**Unfortunately**, if you're using application servers like Tomcat or WebLogic, creating platform threads directly is **highly discouraged**.

---

## Thread Methods Quick Reference

### Instance Methods

```java
thread.start();           // Start the thread
thread.join();            // Wait for thread to complete
thread.join(2000);        // Wait max 2 seconds
thread.interrupt();       // Request thread interruption
thread.isInterrupted();   // Check interrupt status
thread.setDaemon(true);   // Make daemon (before start!)
thread.isDaemon();        // Check if daemon
thread.getName();         // Get thread name
thread.setName("name");   // Set thread name
thread.getPriority();     // Get priority (1-10)
thread.setPriority(5);    // Set priority
thread.getState();        // Get thread state
thread.isAlive();         // Check if running
```

### Static Methods

```java
Thread.currentThread();      // Get current thread
Thread.sleep(1000);          // Sleep 1 second
Thread.sleep(Duration.ofSeconds(2));  // Sleep 2 seconds
Thread.yield();              // Hint to scheduler to yield
Thread.interrupted();        // Check AND CLEAR interrupt flag
Thread.startVirtualThread(() -> task());  // Java 21+
```

### Creating Threads (Summary)

```java
// Traditional
new Thread(runnable).start();
new Thread(() -> task()).start();

// Fluent API (Modern)
Thread.ofPlatform().name("t1").daemon(false).start(runnable);
Thread.ofVirtual().name("vt1").start(runnable);  // Java 21+

// Thread Factory
ThreadFactory factory = Thread.ofPlatform().name("worker-", 0).factory();
Thread t = factory.newThread(runnable);
t.start();

// Virtual Thread Factory (Java 21+)
ThreadFactory vFactory = Thread.ofVirtual().name("vworker-", 0).factory();
Thread vt = vFactory.newThread(runnable);
vt.start();
```

---

## Code Examples for Different Approaches

Considering a method `BigInteger compute(long inputNumber)` in class `Factorial` that takes a Long integer and computes the Factorial of the long number.

### Sequential Execution

```java
private static void sequential(List<Long> inputNumbers, Factorial factorial) {
    for (long inputNumber : inputNumbers) {
        BigInteger computedFactorial = factorial.compute(inputNumber);
    }
}
```

### Sequential with Streams

```java
private static void sequentialWithStreams(List<Long> inputNumbers, Factorial factorial) {
    List<BigInteger> list = inputNumbers.stream()
            .map(factorial::compute)
            .toList();
}
```

### Traditional Platform Threads

[Platform Threads Reference](https://nitinkc.github.io/multithreading/Multithreading/#defining-platform-threads)

```java
private static void runWithTraditionalThreads(List<Long> inputNumbers, Factorial factorial) 
        throws InterruptedException {
    List<Thread> threads = new ArrayList<>();

    for (long inputNumber : inputNumbers) {
        threads.add(new Thread(() -> {
            BigInteger computedFactorial = factorial.compute(inputNumber);
        }));
    }

    for (Thread thread : threads) {
        thread.setDaemon(true);
        thread.start();
    }

    for (Thread thread : threads) {
        // thread.join(2000); // Wait for NOT MORE THAN 2 seconds
        thread.join();  // Wait for all threads
    }
}
```

### Parallel Streams

```java
private static void parallelStream(List<Long> inputNumbers, Factorial factorial) {
    List<BigInteger> result = inputNumbers.parallelStream()
            .map(factorial::compute)
            .toList();
}
```

### Executor & Futures

[Executor Services Reference](https://nitinkc.github.io/multithreading/Multithreading/#create-executorservices)

**Pros:**
- Provides better control over thread management
- Automatically handles thread pooling and task scheduling

**Cons:**
- Requires managing the lifecycle of the ExecutorService

```java
private static void runParallelFactorialWithExecutor(List<Long> inputNumbers, Factorial factorial) {
    try (ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors())) {
        List<Future<BigInteger>> futures = new ArrayList<>();
        for (long inputNumber : inputNumbers) {
            futures.add(executor.submit(() -> factorial.compute(inputNumber)));
        }
        
        List<BigInteger> results = new ArrayList<>();
        for (Future<BigInteger> future : futures) {
            try {
                results.add(future.get()); // Runs when get is executed
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
            }
        }
    }
}
```

### CompletableFutures

[CompletableFuture Reference](https://nitinkc.github.io/multithreading/asynchronous-programming/#creating-a-new-completablefuture)

```java
private static void runWithCompletableFuture(List<Long> inputNumbers, Factorial factorial) {
    List<CompletableFuture<BigInteger>> futures = inputNumbers.stream()
            .map(inputNumber -> CompletableFuture.supplyAsync(() -> factorial.compute(inputNumber)))
            .toList();

    List<BigInteger> results = futures.stream()
            .map(CompletableFuture::join)
            .toList();
}
```

### Virtual Threads

[Virtual Thread Creation Reference](https://nitinkc.github.io/multithreading/java21-virtualthreads/#virtual-thread-creation)

**Pros:**
- More scalable and efficient for I/O-bound tasks
- Reduces the overhead of managing many threads

**Cons:**
- Requires Java 21 or later
- **Not suitable for CPU-bound** tasks where traditional threads or parallel streams might be better

```java
private static void runParallelFactorialWithVirtualThreads(List<Long> inputNumbers, Factorial factorial) 
        throws InterruptedException {
    ThreadFactory threadFactory = Thread.ofVirtual().name("myThread : ", 0).factory();
    List<Future<BigInteger>> submitted = new ArrayList<>();
    
    try (ExecutorService srv = Executors.newThreadPerTaskExecutor(threadFactory)) {
        for (long inputNumber : inputNumbers) {
            submitted.add(srv.submit(() -> factorial.compute(inputNumber)));
        }

        List<BigInteger> results = submitted.stream()
                .map(future -> {
                    try {
                        return future.get();
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                })
                .toList();
    }
}
```

### Java Concurrency Utilities (CountDownLatch)

Use other concurrency utilities from `java.util.concurrent`, such as `CountDownLatch` or `CyclicBarrier`, to manage parallel execution:

```java
private static void runWithCountDownLatch(List<Long> inputNumbers, Factorial factorial) 
        throws InterruptedException {
    CountDownLatch latch = new CountDownLatch(inputNumbers.size());
    for (long inputNumber : inputNumbers) {
        new Thread(() -> {
            try {
                factorial.compute(inputNumber);
            } finally {
                latch.countDown();
            }
        }).start();
    }
    latch.await();
}
```

📁 *Code: `aBasics/aPlatformThreads/ThreadCreation.java`*

---

## Summary

✅ **Runnable** = no return, no exception; **Callable** = returns value, can throw  
✅ **Prefer Runnable/Lambda** over extending Thread  
✅ **Daemon threads** don't prevent JVM exit  
✅ **`start()`** creates new thread; **`run()`** is just method call  
✅ **Fluent API** provides modern, readable thread creation  
✅ **Thread pools** should be preferred over manual thread creation  
✅ **Virtual threads** are always daemon (Java 21+)

### Best Practices

1. **Prefer Runnable over Thread** - Allows flexibility with inheritance
2. **Use meaningful thread names** - Helps with debugging
3. **Don't restart threads** - Create new ones instead
4. **Use thread pools** - Don't create threads manually in production

---

*Next: [Part 3: Thread Control & Coordination →](/java/multithreading/concurrency/03-thread-control-coordination/)*

