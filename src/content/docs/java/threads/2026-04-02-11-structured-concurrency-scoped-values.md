---
title: "Java Multithreading - Part 11: Structured Concurrency & Scoped Values"
date: 2026-04-02 00:00:11
categories: [java, multithreading, concurrency]
tags: [java, structured-concurrency, scoped-value, threadlocal, java21]
---

{% include toc title="Index" icon="cog" %}

# Part 11: Structured Concurrency & Scoped Values

Modern Java (21+) introduces Structured Concurrency and ScopedValue to make concurrent programming safer and more maintainable.

## Table of Contents
1. [The Problem: Unstructured Concurrency](#the-problem-unstructured-concurrency)
2. [Structured Concurrency](#structured-concurrency)
3. [StructuredTaskScope](#structuredtaskscope)
4. [Shutdown Strategies](#shutdown-strategies)
5. [ThreadLocal - Traditional Approach](#threadlocal---traditional-approach)
6. [ScopedValue - Modern Approach](#scopedvalue---modern-approach)
7. [Thread Interruption and Cancellation](#thread-interruption-and-cancellation)

---

## Scenario

When there are multiple independent tasks to be completed, and one of the tasks fails, there should be some mechanism to let others know that it has failed and let others also **fail-fast** (instead of waiting for the other tasks to finish).

---

## The Problem: Unstructured Concurrency

### Traditional Approach Issues

```java
Future<User> userFuture = executor.submit(() -> fetchUser(id));
Future<Order> orderFuture = executor.submit(() -> fetchOrder(id));

// Problems:
// 1. What if userFuture fails? orderFuture continues - resource leak!
// 2. What if main thread throws? Both futures orphaned!
// 3. Hard to track task lifecycles
```

### Visual Problem

```
Without Structured Concurrency:
┌─────────────────────┐
│     Main Task       │
│    ┌────┼────┐      │
│  Task1 Task2 Task3  │
│    ???  ???  ???    │ ← Orphaned tasks?
│  (who tracks them?) │
└─────────────────────┘
```

---

## Structured Concurrency

### Solution: Task Lifecycles Tied to Code Blocks

Structured Concurrency ensures **child tasks complete before parent** exits.

```
With Structured Concurrency:
┌─────────────────────┐
│     Main Task       │
│    (try-scope)      │
│    ┌────┴────┐      │
│  Task1     Task2    │
│    (scope.join)     │
│    All complete     │
└─────────────────────┘
```

### Benefits

1. **No orphaned tasks** - all children complete or are cancelled
2. **Clear ownership** - parent owns child tasks
3. **Predictable cleanup** - resources released when scope ends
4. **Better error handling** - failures propagate properly

---

## StructuredTaskScope

The following examples are based on the list of tasks:

```java
var tasks = List.of(
    new BlockingIOTasks("Price-1", 3, true), 
    new BlockingIOTasks("Price-2", 10, true)
);
```

### Basic Usage

Shuts down when **all child** threads complete:

```java
try (var scope = StructuredTaskScope.open(Joiner.awaitAll())) {
    // Start running tasks in parallel
    Subtask<User> userTask = scope.fork(() -> fetchUser(id));
    Subtask<Order> orderTask = scope.fork(() -> fetchOrder(id));
    
    // Wait for all tasks to complete
    scope.join();
    
    // Handle results
    User user = userTask.get();
    Order order = orderTask.get();
    return new Response(user, order);
}  // All children cleaned up
```

### Handling Task States

```java
try (var scope = new StructuredTaskScope<TaskResponse>()) {
    // Start running the tasks in parallel
    List<Subtask<TaskResponse>> subtasks = tasks.stream()
        .map(task -> scope.fork(task))
        .toList();
    
    // Wait for all tasks to complete (success or not)
    scope.join();
    
    subtasks.forEach(subTask -> {
        // Handle Child Task Results (might have succeeded or failed)
        State taskState = subTask.state();
        if (taskState == State.SUCCESS)
            System.out.println(subTask.get());
        else if (taskState == State.FAILED)
            System.out.println(subTask.exception());
    });
}
```

📁 *Code: `cVirtualThreads/v3structuredConcurrency/StructuredTaskScopeRunner.java`*

---

## Shutdown Strategies

### Joiner.awaitAll() / StructuredTaskScope (Default)

Wait for **all** child threads to complete (success or failure):

```java
try (var scope = StructuredTaskScope.open(Joiner.awaitAll())) {
    scope.fork(() -> task1());
    scope.fork(() -> task2());
    scope.join();  // Waits for ALL
}
```

### Joiner.anySuccessfulOrThrow() / ShutdownOnSuccess

Shuts down when the **first** child thread **succeeds**. First success wins - cancel others:

```java
// Modern API (Java 21+)
try (var scope = StructuredTaskScope.open(Joiner.anySuccessfulOrThrow())) {
    scope.fork(() -> fetchFromServer1());
    scope.fork(() -> fetchFromServer2());
    scope.fork(() -> fetchFromServer3());
    scope.join();
    
    // Get first successful result
    return scope.result();
}

// Legacy API
try (var scope = new StructuredTaskScope.ShutdownOnSuccess<TaskResponse>()) {
    // Start running the tasks in parallel 
    List<Subtask<TaskResponse>> list = tasks.stream()
        .map(task -> scope.fork(task))
        .toList();

    // Wait till first Child Task Succeeds. Send Cancellation to all other Child Tasks
    scope.join();
    
    // Handle Successful Child Task
    TaskResponse result = scope.result();
}
```

### Joiner.allSuccessfulOrThrow() / ShutdownOnFailure

Shuts down when the **first** child thread **fails**. All must succeed - if any fails, cancel others:

```java
// Modern API (Java 21+)
try (var scope = StructuredTaskScope.open(Joiner.allSuccessfulOrThrow())) {
    Subtask<User> user = scope.fork(() -> fetchUser());
    Subtask<Order> order = scope.fork(() -> fetchOrder());
    scope.join();  // Throws if ANY fails
    
    // Both succeeded
    return combine(user.get(), order.get());
}

// Legacy API
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    // Start running the tasks in parallel
    List<Subtask<TaskResponse>> subtasks = tasks.stream()
        .map(task -> scope.fork(task))
        .toList();

    // Wait till first Child Task fails. Send cancellation to all other Child Tasks
    scope.join();
    scope.throwIfFailed();
    
    // Handle Success Child Task Results
    subtasks.forEach(System.out::println);
}
```

### Custom Joiner

Extend `StructuredTaskScope` and implement the `handleComplete()` method.

### Summary

| Joiner | Legacy API | Behavior |
|--------|------------|----------|
| `awaitAll()` | `StructuredTaskScope` | Wait for all, collect results |
| `allSuccessfulOrThrow()` | `ShutdownOnFailure` | All must succeed, fail-fast |
| `anySuccessfulOrThrow()` | `ShutdownOnSuccess` | First success wins |
| Custom | Extend & override | Implement your own logic |

---

## ThreadLocal - Traditional Approach

### How ThreadLocal Works

Each thread has its own **instance of a map** that stores **thread-local variables**.

This map holds the associations between the thread-local variables and their corresponding values, ensuring that the variables are unique to the thread and are not shared across other threads.

This allows threads to maintain:
- Isolated states
- Preventing race conditions
- Ensuring data consistency within each thread

```java
public static ThreadLocal<Student> studentThreadLocal = new ThreadLocal<>();
```

- `studentThreadLocal` has global scope
- But the **value** inside has scope **only for duration of a thread**

### Usage

```java
// Set value for current thread
studentThreadLocal.set(new Student("Harry Potter"));

// Get value for current thread
Student student = studentThreadLocal.get();

// MUST clean up!
studentThreadLocal.remove();
```

### InheritableThreadLocal

`InheritableThreadLocal` is a subclass of `ThreadLocal`. It allows child threads to inherit the values of the parent thread.

- By Default child thread values are identical to Parent Thread

When a child thread gets created the local values of parent get copied over to the child:

- Default is **shallow copy** of the value reference
- If child **modifies the same object** (mutates it), parent sees changes
- If child **sets a new value** (reassigns), parent does **NOT** see the new value

⚠️ **Important**: For virtual threads, prefer `ScopedValue` over `InheritableThreadLocal`.

```java
private static final InheritableThreadLocal<String> threadLocalValue = 
    new InheritableThreadLocal<>();
```


### Problems with Virtual Threads

| Problem | Description |
|---------|-------------|
| **Memory** | Each virtual thread has own copy → millions of copies |
| **Mutable** | Can be changed unexpectedly |
| **Cleanup** | Must manually remove |
| **Lifecycle** | Hard to track |

📁 *Code: `cVirtualThreads/v4threadLocals/T1ThreadLocal.java`*

---

## ScopedValue - Modern Approach

[JEP 446: Scoped Values](https://openjdk.org/jeps/446)

Immutable and better way to share data between threads. Scoped Values are only available for use within the **dynamic scope** of the method.

### Advantages

- During the bounded period of execution of a method
- Bound during start of scope and unbound during end of scope (even on exception)
- Rebinding allowed but cannot modify Scoped Value
- No cleanup required - automatically handled

### Benefits over ThreadLocal

| Feature | ThreadLocal | ScopedValue |
|---------|-------------|-------------|
| Mutability | Mutable | **Immutable** |
| Cleanup | Manual | **Automatic** |
| Memory | Higher (per thread) | **Lower (shared)** |
| Virtual threads | Problematic | **Designed for** |
| Rebinding | set() anytime | New scope only |

### Creating ScopedValue

```java
ScopedValue<Student> STUDENT = ScopedValue.newInstance();
```

### Binding Values

```java
Student hp = new Student("Harry Potter");

// Using Runnable (void method)
ScopedValue.runWhere(STUDENT, hp, () -> {
    processStudent();  // STUDENT is bound here
});  // Auto-unbound

// Using Callable (returns value)
boolean result = ScopedValue.callWhere(STUDENT, hp, () -> {
    return validateStudent();
});

// Using Supplier
Student result = ScopedValue.getWhere(STUDENT, hp, () -> {
    return enrichStudent();
});
```

### Multiple ScopedValues

```java
ScopedValue<Student> studentScope = ScopedValue.newInstance();
ScopedValue<Department> deptScope = ScopedValue.newInstance();

ScopedValue.where(studentScope, harryPotter)
           .where(deptScope, gryffindor)
           .call(() -> processEnrollment());
```

### Getting Values

```java
// Return value if bound, else default
Student student = STUDENT.orElse(new Student("Default"));

// Return value if bound, else throw
Student student = STUDENT.orElseThrow(() -> 
    new RuntimeException("Not Bound"));

// Check if bound
if (STUDENT.isBound()) {
    Student s = STUDENT.get();
}
```

### Rebinding in Nested Scopes

```java
ScopedValue.where(STUDENT, harry).run(() -> {
    System.out.println(STUDENT.get());  // Harry
    
    ScopedValue.where(STUDENT, ron).run(() -> {
        System.out.println(STUDENT.get());  // Ron (rebound)
    });
    
    System.out.println(STUDENT.get());  // Harry (restored)
});
```

### Important: Works with StructuredTaskScope

Scoped values are **available for child threads** initiated with **StructuredTaskScope**:

```java
ScopedValue.where(USER, user).run(() -> {
    try (var scope = StructuredTaskScope.open(Joiner.awaitAll())) {
        scope.fork(() -> {
            // USER is accessible here!
            processUser(USER.get());
            return result;
        });
        scope.join();
    }
});
```

Why? Threads started from StructuredTaskScope are **guaranteed to complete** before try-with-resources ends, remaining within ScopedValue scope.

📁 *Code: `cVirtualThreads/v5scopedvalue/S1ScopedValue.java`*

---

## Thread Interruption and Cancellation

### Interrupt Methods

| Method | Description |
|--------|-------------|
| `void interrupt()` | Interrupts a thread by setting its interrupted flag |
| `static boolean interrupted()` | Checks **and clears** the interrupted status of the current thread |
| `boolean isInterrupted()` | Checks the interrupted status of the specified thread **without** clearing it |

### Expected Behavior

**Cooperative Interruption**: Threads should check their interrupted status periodically to respond appropriately to interruption requests.

**Handling Interruption**: Proper handling of interruptions improves application responsiveness and thread management.

- **Interrupter** must call `interrupt()` to set the flag (its own)
- **Interrupted thread**:
  - May choose to ignore the interrupt
  - Check interrupted status periodically (polling)
  - `wait()`, `sleep()`, `join()` will check status automatically
    - Throws `InterruptedException`
    - Clears the interrupted status flag
  - Cancel using `cancel(true)`

### Futures - Class Built on Top of Threads

```java
Future<TaskResponse> taskFuture = executor.submit(callable);
taskFuture.cancel(true);  // May interrupt if running
```

### How to Handle Interruption

```java
// Interrupter calls
thread.interrupt();

// Interrupted thread
// Option 1: Polling
while (!Thread.currentThread().isInterrupted()) {
    doWork();
}

// Option 2: wait(), sleep(), join() check automatically
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    // Clears interrupt flag - restore it!
    Thread.currentThread().interrupt();
}

// Option 3: Cancel Future
Future<TaskResponse> taskFuture = executor.submit(callable);
taskFuture.cancel(true);  // May interrupt if running
```

### Using CompletionService for Parallel Tasks

Handle parallel tasks using CompletionService - get results in completion order:

```java
try (var service = Executors.newVirtualThreadPerTaskExecutor()) {
    CompletionService<TaskResponse> completionService = 
        new ExecutorCompletionService<TaskResponse>(service);

    List<Future<TaskResponse>> taskFutures = tasks.stream()
        .map(completionService::submit)
        .toList();

    try {
        for (int j = 0; j < taskFutures.size(); j++) {
            completionService.take().get();  // Get in completion order
        }
    } catch (Exception e) {
        // Request that the threads terminate. Do not wait for the threads to terminate
        for (var taskFuture : taskFutures) {
            taskFuture.cancel(true);
        }
        throw e;
    }
    
    // All tasks are successful at this point
    List<TaskResponse> result = taskFutures.stream()
        .map(Future::resultNow)
        .toList();
    
    return result;
}  // Makes sure that all threads are fully terminated
```

---

## Summary

✅ **Structured Concurrency** ensures child tasks complete before parent  
✅ **StructuredTaskScope** provides fail-fast/fail-first patterns  
✅ **Joiner** strategies: awaitAll, allSuccessful, anySuccessful  
✅ **ThreadLocal** has issues with virtual threads (memory, cleanup)  
✅ **ScopedValue** is immutable, auto-cleaned, designed for virtual threads  
✅ Scoped values work with **StructuredTaskScope** child threads

### Quick Reference

```java
// Structured Concurrency
try (var scope = StructuredTaskScope.open(joiner)) {
    Subtask<T> task = scope.fork(callable);
    scope.join();
    T result = task.get();
}

// Joiners
Joiner.awaitAll()
Joiner.allSuccessfulOrThrow()
Joiner.anySuccessfulOrThrow()

// ScopedValue
ScopedValue<T> KEY = ScopedValue.newInstance();
ScopedValue.where(KEY, value).run(() -> { KEY.get(); });
ScopedValue.where(KEY, value).call(() -> result);
KEY.orElse(defaultValue);
KEY.orElseThrow(exceptionSupplier);
KEY.isBound();

// ThreadLocal (legacy)
ThreadLocal<T> local = new ThreadLocal<>();
local.set(value);
local.get();
local.remove();  // Don't forget!
```

---

*Next: [Part 12: Best Practices & Patterns →](/java/multithreading/concurrency/12-best-practices-patterns/)*

