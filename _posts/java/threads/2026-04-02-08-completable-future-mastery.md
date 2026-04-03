---
title: "Java Multithreading - Part 8: CompletableFuture Mastery"
date: 2026-04-02 00:00:08
categories: [java, multithreading, concurrency]
tags: [java, threads, completablefuture, async, reactive, promise]
---

{% include toc title="Index" icon="cog" %}

# Part 8: CompletableFuture Mastery

`CompletableFuture` (Java 8+) revolutionizes asynchronous programming with non-blocking pipelines, composition, and elegant error handling.

## Video Reference

[![CompletableFuture Tutorial](https://img.youtube.com/vi/1zSF1259s6w/0.jpg)](https://www.youtube.com/watch?v=1zSF1259s6w)

## Table of Contents
1. [Why CompletableFuture?](#why-completablefuture)
2. [CompletableFuture = Java's Promise](#completablefuture--javas-promise)
3. [Creating CompletableFutures](#creating-completablefutures)
4. [Transformation Methods](#transformation-methods)
5. [Combining Futures](#combining-futures)
6. [Exception Handling](#exception-handling)
7. [Controlling Thread Pools](#controlling-thread-pools)
8. [Timeout Handling](#timeout-handling)
9. [Blocking Operations: join(), get(), getNow()](#blocking-operations-join-get-getnow)
10. [Streams API vs Async API](#streams-api-vs-async-api)
11. [Best Practices](#best-practices)

---

## Why CompletableFuture?

### Limitations of Future

| Problem | Description |
|---------|-------------|
| **Blocking `get()`** | Defeats the async purpose |
| **No chaining** | Can't compose (fetchUser → enrichUser → saveUser) |
| **No callbacks** | Must manually poll or block |
| **No combining** | Hard to combine results from multiple futures |
| **Limited functionality** | Cannot complete a future manually |

```java
// Traditional Future - BLOCKING!
Future<User> userFuture = executor.submit(() -> fetchUser(id));
User user = userFuture.get();  // BLOCKS main thread!
```

### CompletableFuture Solution

```java
// Non-blocking, chainable, composable!
CompletableFuture.supplyAsync(() -> fetchUser(id))
    .thenApply(user -> enrichUser(user))           // Transform
    .thenCombine(fetchOrdersAsync(id), this::merge) // Combine
    .exceptionally(ex -> handleError(ex))          // Error handling
    .thenAccept(dto -> sendResponse(dto));         // Consume
```

### Feature Comparison

| Feature | Future | CompletableFuture |
|---------|--------|-------------------|
| Blocking get() | Yes, always | Optional (use callbacks) |
| Chaining | ❌ No | ✅ thenApply, thenAccept, thenRun |
| Combining | ❌ No | ✅ thenCombine, allOf, anyOf |
| Error handling | ❌ No callbacks | ✅ exceptionally, handle |
| Completion | Automatic only | Manual completion possible |

---

## CompletableFuture = Java's Promise

CompletableFutures in Java is the same as **Promise in JavaScript**.

### JavaScript Comparison

```javascript
// JavaScript Promise
getData()
    .then(data => transform(data))
    .then(result => display(result))
    .catch(error => handleError(error));
```

### Java Equivalent

```java
// Java CompletableFuture
CompletableFuture.supplyAsync(() -> getData())
    .thenApply(data -> transform(data))
    .thenAccept(result -> display(result))
    .exceptionally(error -> handleError(error));
```

### Promise State Transitions

| Current State | Next State | Function called |
|:--------------|:-----------|:----------------|
| resolved | resolved | next then in pipeline |
| resolved | rejected | next catch in pipeline |
| rejected | resolved | next then in pipeline |
| rejected | rejected | next catch in pipeline |

---

## Creating CompletableFutures

### supplyAsync() - With Return Data

Runs computation asynchronously and returns a result.

```java
CompletableFuture<Double> future = CompletableFuture.supplyAsync(() -> {
    return computeValue();  // Returns result
});
// Type: CompletableFuture<V>
```

### runAsync() - No Return Data

Fire and forget - runs computation with no result.

```java
CompletableFuture<Void> future = CompletableFuture.runAsync(() -> {
    doWork();  // No return value
});
// Type: CompletableFuture<Void>
```

### completedFuture() - Immediate Value

Creates an already-completed future.

```java
CompletableFuture<String> immediate = CompletableFuture.completedFuture("Done!");
// Instantly completed, operations execute immediately
```

### Manual Completion

Create incomplete future, complete later:

```java
CompletableFuture<String> future = new CompletableFuture<>();

// Later, in another thread...
future.complete(result);              // Normal completion
future.completeExceptionally(ex);     // Error completion
```

#### complete(T value)

- Allows completing a `CompletableFuture` manually with a specific result value
- Used to provide a result explicitly, bypassing the actual asynchronous computation

📁 *Code: `bFuturesAndCompletableFutures/completableFutureBasics/A1Intro.java`*

---

## Transformation Methods

### Stages of CompletableFutures

When one stage completes, another one starts and it keeps running.

| Stage Method | Type | Functional Interface | Description |
|:-------------|:-----|:---------------------|:------------|
| `supplyAsync()` | Factory | Supplier | Initiates async computation, returns `CompletableFuture<T>` |
| `thenApply()` / `thenApplyAsync()` | Completion Stage | Function | Transform data, returns value of type T |
| `thenAccept()` / `thenAcceptAsync()` | Completion Stage | Consumer | Consume result, returns `CompletableFuture<Void>` |

### Pipeline Visualization

```
supplyAsync() ──▶ thenApply() ──▶ thenCombine() ──▶ thenAccept()
     │                │                │                │
   Async          Transform        Combine          Consume
   Start          (Function)      (BiFunction)     (Consumer)
```

### thenApply() - Transform Result

Like `map()` in streams. Takes a `Function<T, U>`, returns `CompletableFuture<U>`.

```java
CompletableFuture.supplyAsync(() -> 42)
    .thenApply(num -> num * 2)           // 84
    .thenApply(num -> "Result: " + num); // "Result: 84"
```

### thenAccept() - Consume Result

Like `forEach()` in streams. Takes a `Consumer<T>`, returns `CompletableFuture<Void>`.

```java
CompletableFuture.supplyAsync(() -> "Hello")
    .thenAccept(greeting -> System.out.println(greeting));
```

### thenRun() - Run Action (Ignores Input)

Executes action after completion, ignoring the result.

```java
CompletableFuture.supplyAsync(() -> compute())
    .thenRun(() -> System.out.println("Done!"));
```

### Method Summary

| Method | Input | Output | Use Case |
|--------|-------|--------|----------|
| `thenApply` | Function<T,U> | CF<U> | Transform result |
| `thenAccept` | Consumer<T> | CF<Void> | Consume result |
| `thenRun` | Runnable | CF<Void> | Side effect, ignore result |

📁 *Code: `bFuturesAndCompletableFutures/completableFutureBasics/A3Pipeline.java`*

---

## Combining Futures

### thenCompose() - Flatten Nested Futures (flatMap)

Chains **dependent** async operations. Prevents nested `CompletableFuture<CompletableFuture<T>>`.

```java
// ❌ BAD: thenApply creates nested CF<CF<User>>
cf.thenApply(id -> fetchUserAsync(id));  // Returns CF<CF<User>>

// ✅ GOOD: thenCompose flattens to CF<User>
cf.thenCompose(id -> fetchUserAsync(id));  // Returns CF<User>
```

**Use Case**: When second operation depends on first result.

> **Key Distinction**: 
> - `compose()` → sequencing **dependent** asynchronous tasks
> - `thenCombine()` → combine the results of two **independent** asynchronous tasks into a single result

### thenCombine() - Combine Independent Futures

Runs two futures **in parallel**, combines results when both complete.

```java
CompletableFuture<String> greeting = supplyAsync(() -> "Hello");
CompletableFuture<String> name = supplyAsync(() -> "World");

CompletableFuture<String> result = greeting.thenCombine(name, 
    (g, n) -> g + " " + n);  // "Hello World"
// Both run in parallel, total time = max(greeting, name)
```

**Use Case**: Microservice calls - bring data from multiple services and combine.

### allOf() - Wait for All

Returns `CompletableFuture<Void>` that completes when **all** complete.

```java
CompletableFuture<Void> allDone = CompletableFuture.allOf(f1, f2, f3);

allDone.thenRun(() -> {
    // All completed - get results manually
    String r1 = f1.join();
    String r2 = f2.join();
    String r3 = f3.join();
});
```

**Note**: `allOf()` does not "wait" - it returns a CompletableFuture immediately.

### anyOf() - First to Complete

Returns `CompletableFuture<Object>` with result of **first** completed. Returns the first one succeeded.

```java
CompletableFuture<Object> first = CompletableFuture.anyOf(fast, slow);
// Returns result of whichever completes first
```

Full example with error handling:

```java
CompletableFuture
        .anyOf(future1, future2, future3, future4)
        .thenAccept(result -> {
            System.out.println("Handling Accept :: " + result);
        })
        .exceptionally(throwable -> {
            System.out.println("Handling Failure :: " + throwable);
            return null;
        })
        .join();
```

### Summary

| Method | Description | Return Type |
|--------|-------------|-------------|
| `thenCompose` | Chain dependent futures (flatMap) | CF<U> |
| `thenCombine` | Combine 2 parallel futures | CF<V> |
| `allOf` | Wait for all futures | CF<Void> |
| `anyOf` | First to complete | CF<Object> |

📁 *Code: `bFuturesAndCompletableFutures/completableFutureBasics/A12ThenCompose.java`*

---

## Exception Handling

### Railway Track Pattern

```
data track  -----f------f     recovering from exception       f--continue-----
                          \                                  /
error track ----------------f---can return default data-----f--or handle------
```

### exceptionally() - Handle and Recover

Called **only on exception**. Provides fallback value.

```java
CompletableFuture.supplyAsync(() -> riskyOperation())
    .exceptionally(ex -> {
        log.error("Failed", ex);
        return fallbackValue;  // Recovery value
    });
```

**Pipeline Behavior**: Exceptions **skip stages** until `exceptionally`:

```java
future
    .thenApply(data -> 5 / data)       // May throw
    .exceptionally(ex -> 0)            // Recover with 0
    .thenApply(data -> data * 2)       // Continues with recovered value
    .thenAccept(System.out::println);
```

### handle() - Handle Both Success and Failure

Called **always** (success or failure). Can transform or recover.

```java
cf.handle((result, error) -> {
    if (error != null) {
        return "Recovered from: " + error.getMessage();
    }
    return result;
});
```

### whenComplete() - Side Effect Only

Called **always**, but **doesn't change result**. Good for logging/cleanup.

```java
cf.whenComplete((result, error) -> {
    if (error != null) logger.error("Failed", error);
    else logger.info("Success: " + result);
});  // Original result or exception passes through
```

### Comparison

| Method | Called When | Returns | Use Case |
|--------|-------------|---------|----------|
| `exceptionally` | Error only | Fallback T | Recovery |
| `handle` | Always | New T | Transform either case |
| `whenComplete` | Always | Same T | Logging, cleanup |

📁 *Code: `bFuturesAndCompletableFutures/completableFutureBasics/A5Exceptionally.java`*

---

## Controlling Thread Pools

### Default Pool

By default, uses `ForkJoinPool.commonPool()`:

```java
CompletableFuture.supplyAsync(() -> task());  // Uses commonPool()
// Common pool size = CPU cores - 1
// ⚠️ Shared across entire JVM!
```

Common ForkJoinPool is shared by:
- ParallelStreams
- CompletableFuture

### Custom Thread Pool

For **I/O-bound tasks**, use a separate pool:

```java
int cores = Runtime.getRuntime().availableProcessors();
ExecutorService ioPool = Executors.newCachedThreadPool();
ExecutorService cpuPool = Executors.newFixedThreadPool(cores);
ForkJoinPool customFJP = new ForkJoinPool(10);

// Use custom pool
CompletableFuture.supplyAsync(() -> "Hello", ioPool);

// For transformations too
future.thenApplyAsync(s -> s.toUpperCase(), cpuPool);
```

### Async Variants

| Method | Thread |
|--------|--------|
| `thenApply` | May use same thread |
| `thenApplyAsync` | New thread from common pool |
| `thenApplyAsync(fn, executor)` | New thread from custom pool |

### Best Practice: Separate Pools

```java
ExecutorService ioPool = Executors.newCachedThreadPool();      // I/O
ExecutorService cpuPool = Executors.newFixedThreadPool(cores); // CPU

cf.supplyAsync(() -> fetchFromDb(), ioPool)        // I/O
  .thenApplyAsync(data -> transform(data), cpuPool)   // CPU
  .thenAcceptAsync(result -> saveToDb(result), ioPool); // I/O
```

---

## Timeout Handling

### completeOnTimeout (Java 9+)

Complete with default value on timeout:

```java
future.completeOnTimeout(defaultValue, 5, TimeUnit.SECONDS);
// If not complete in 5 seconds, complete with defaultValue
```

### orTimeout (Java 9+)

Fail on timeout:

```java
future.orTimeout(1, TimeUnit.SECONDS);
// Throws TimeoutException if not complete in 1 second
```

---

## Blocking Operations: join(), get(), getNow()

| Operation | Description |
|-----------|-------------|
| `join()` | Waits and returns result, wraps exceptions in `CompletionException` (unchecked) |
| `get()` | Waits and returns result, throws checked exceptions (`InterruptedException`, `ExecutionException`) |
| `getNow(value)` | Returns immediately with value or default, does not block |

### join() - Blocking Until Completion

**Ensuring All Steps Complete:**
The CompletableFuture operations you chain (e.g., thenApply, exceptionally, thenAccept, thenRun) will execute asynchronously.

If the main thread exits before these operations complete, you won't see their output.
`join()` ensures that the main thread waits for the entire chain of operations to finish.

- Used to obtain the result of the asynchronous computation when it's done
- Similar to `get()` method, but doesn't throw checked exceptions
- Waits indefinitely for the computation to finish
  - Returns the result
  - Or throws any unhandled exception if one occurs

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> 100);
int result = future.join(); // Get the result when the computation is complete
// Blocks the main thread until the supplyAsync is done
```

### get() & getNow() - INSTEAD use thenAccept()

**get() is a blocking call; The best thing to do with GET is to for*GET*.**
INSTEAD use thenAccept()

- Like join(), get() is used to obtain the result of the asynchronous computation when it's done
- Unlike join(), get() can throw checked exceptions: `InterruptedException` and `ExecutionException`
- Use get() if there is a need for explicit handling for interruptions and want to differentiate between exceptions and interruptions
- If it's so important to use get, **use getNow()** with a default value:
  - getNow() is impatient, non-blocking and moves on with a value if there is no immediate response
  - If there is delay prior to getNow call then the getNow may return the correct value

```java
CompletableFuture<Integer> future = CompletableFuture.supplyAsync(() -> 100);
try {
    int result = future.get(); // Get the result and handle exceptions
    int data = future.getNow(-99); // Need to provide a value if the value is absent
    future.thenAccept(data -> System.out.println(data));
} catch (InterruptedException e) {
    System.out.println("Thread was interrupted");
    Thread.currentThread().interrupt(); // Preserve interruption status
} catch (ExecutionException e) {
    System.out.println("Caught exception: " + e.getCause()); // Print actual cause
}
```

### Usage Recommendations

- Prefer `join()` for a cleaner, unchecked exception handling
- Use `getNow(defaultValue)` for a non-blocking way to retrieve results with a default
- Use `thenAccept()` instead of blocking when possible

---

## Streams API vs Async API

| Functional Interface | Method | Streams API | Async API |
|:---------------------|:-------|:------------|:----------|
| Predicate<T> | boolean test() | filter() | - |
| Function<T,R> | R apply(T k) | map() | thenApply() |
| Consumer<T> | void accept(T) | forEach() | thenAccept() |
| Supplier<T> | T get() | Factories | supplyAsync() |

### Streams vs CompletableFuture

| Streams | CompletableFuture |
|:--------|:------------------|
| Zero, one or more data | Zero or one |
| Only data channel | Data channel + error channel |
| Pipeline & lazy | Pipeline & lazy |
| Exception - nope | Error channel (exceptionally) |
| forEach | thenAccept (consumes) |
| map | thenApply (transform) |
| flatMap (returns Stream) | thenCompose (returns CF) |
| - | thenCombine (like zip) |

---

## Best Practices

### 1. Avoid Blocking Inside Async

```java
// ❌ BAD - Blocking defeats async
CompletableFuture.supplyAsync(() -> future.get());

// ✅ GOOD - Keep chain async
CompletableFuture.supplyAsync(() -> task())
    .thenCompose(result -> anotherAsyncTask(result));
```

### 2. Don't Ignore Exceptions

```java
// ❌ BAD - Silent failure
CompletableFuture.runAsync(() -> riskyOp());

// ✅ GOOD - Handle errors
CompletableFuture.runAsync(() -> riskyOp())
    .exceptionally(ex -> { log.error(ex); return null; });
```

### 3. Use join() Over get()

```java
// get() forces checked exception handling
try { future.get(); } 
catch (InterruptedException | ExecutionException e) { }

// join() wraps in unchecked exception - cleaner
future.join();  // Throws CompletionException (unchecked)
```

### 4. Use getNow() Instead of get()

```java
// getNow() is non-blocking with default
int data = future.getNow(-99);  // Returns -99 if not done
```

### 5. Prefer Composition Over Blocking

```java
// ❌ BAD - Sequential blocking
User user = fetchUser().get();
List<Order> orders = fetchOrders(user.getId()).get();

// ✅ GOOD - Composed async
fetchUser()
    .thenCompose(user -> fetchOrders(user.getId()))
    .thenCompose(orders -> fetchProducts(orders));
```

---

## Summary

✅ **CompletableFuture** = Java's Promise  
✅ **supplyAsync** returns value, **runAsync** doesn't  
✅ **thenApply** transforms, **thenCompose** flattens, **thenCombine** merges  
✅ **exceptionally** recovers, **handle** transforms both cases  
✅ **Use custom pools** for I/O-bound tasks  
✅ **Prefer join()** over get(), **getNow()** for non-blocking  
✅ **orTimeout/completeOnTimeout** for timeout handling (Java 9+)

### Quick Reference

```java
// Create
supplyAsync(() -> value);
runAsync(() -> action());
completedFuture(value);

// Transform
.thenApply(x -> transform(x))
.thenAccept(x -> consume(x))
.thenRun(() -> action())

// Combine
.thenCompose(x -> asyncOp(x))        // Flatten (flatMap)
.thenCombine(other, (a,b) -> merge)  // Parallel combine
CompletableFuture.allOf(f1, f2);     // Wait all
CompletableFuture.anyOf(f1, f2);     // First wins

// Errors
.exceptionally(ex -> fallback)        // Recover on error
.handle((r, ex) -> result)            // Handle both
.whenComplete((r, ex) -> log())       // Side effect

// Custom pool
.supplyAsync(task, executor)
.thenApplyAsync(fn, executor)

// Get result
.join()                               // Preferred (unchecked)
.get()                                // Checked exceptions
.orTimeout(5, SECONDS)                // Java 9+
.completeOnTimeout(default, 5, SECONDS)
```

---

## Original Code Gists (Reference)

The following GitHub Gists contain the original code examples for this topic:

| Topic | Gist Link |
|-------|-----------|
| JavaScript Promise Example | {% gist nitinkc/17229c16e91766fa9eb903cad63a8def %} |
| Java CompletableFuture Basic | {% gist nitinkc/eea4fd28d7765ec964cbf9b5c270ec5c %} |
| supplyAsync() | {% gist nitinkc/7d0d331d4716151c51579d4fdda5ba94 %} |
| runAsync() | {% gist nitinkc/e186dba8001122fa5281cf979cd5ce3d %} |
| Manual Pipeline Creation | {% gist nitinkc/da36ef99c6a7e383e7aea4475328ad9c %} |
| complete(T value) | {% gist nitinkc/28618b6feb55df00447289a75b351dba %} |
| exceptionally() | {% gist nitinkc/6ddd9a3a39bb8639ffe23e9dee2ea709 %} |
| thenCombine() | {% gist nitinkc/124fce7e90ac53e72f3d45f014d8a88b %} |
| allOf() | {% gist nitinkc/ffb3f165b3b58072acd750b78c0a2644 %} |
| whenComplete() | {% gist nitinkc/3648ba0dd28d87fb5c4c13d4a77742e4 %} |

---

*Next: [Part 9: Concurrent Collections →](/java/multithreading/concurrency/09-concurrent-collections/)*

