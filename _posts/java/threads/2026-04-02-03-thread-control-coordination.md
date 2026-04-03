---
title: "Java Multithreading - Part 3: Thread Control & Coordination"
date: 2026-04-02 00:00:03
categories: [java, multithreading, concurrency]
tags: [java, threads, sleep, yield, join, interrupt, priority]
---

{% include toc title="Index" icon="cog" %}

# Part 3: Thread Control & Coordination

This part covers how to control thread execution, manage priorities, and coordinate between threads.

## Table of Contents
1. [Thread Priority](#thread-priority)
2. [Sleep - Pausing Execution](#sleep---pausing-execution)
3. [Yield - Giving Up CPU](#yield---giving-up-cpu)
4. [Join - Waiting for Completion](#join---waiting-for-completion)
5. [Interrupt - Stopping Threads](#interrupt---stopping-threads)
6. [Thread Groups](#thread-groups)
7. [Quick Reference](#quick-reference)

---

## Thread Priority

Thread priority is a **hint** to the thread scheduler about relative importance. Higher priority threads are generally scheduled before lower priority ones.

### Priority Constants

```java
Thread.MIN_PRIORITY   = 1
Thread.NORM_PRIORITY  = 5  // Default
Thread.MAX_PRIORITY   = 10
```

### Setting Priority

```java
thread.setPriority(Thread.MAX_PRIORITY);   // 10
thread.setPriority(Thread.NORM_PRIORITY);  // 5 (default)
thread.setPriority(Thread.MIN_PRIORITY);   // 1

int priority = thread.getPriority();       // Get current priority
```

### Priority Inheritance

- Default priority for main thread is **5**
- **Child threads inherit parent's priority**
- With same priority, execution order is **undeterministic**

⚠️ **Warning**: Thread priority behavior is **platform-dependent**. Don't rely on it for correctness!

📁 *Code: `aBasics/aPlatformThreads/T6ThreadPriority.java`*

---

## Sleep - Pausing Execution

`Thread.sleep()` pauses the **current thread** for a specified duration.

### Key Characteristics

- **Releases CPU** but **NOT locks** (if holding any)
- Thread goes to **TIMED_WAITING** state
- Guaranteed **minimum** sleep time (may sleep longer)
- Throws `InterruptedException` (must handle)

### Usage

```java
// Basic usage
Thread.sleep(1000);  // Sleep 1 second (milliseconds)

// More readable (Java 8+)
TimeUnit.SECONDS.sleep(2);
TimeUnit.MILLISECONDS.sleep(500);

// Duration API (Java 9+)
Thread.sleep(Duration.ofSeconds(2));
```

### Exception Handling

```java
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();  // Restore interrupt flag
    // Handle interruption
}
```

### Sleep Visualization

```
Thread State Timeline:
────────────────────────────────────────────────────────
RUNNABLE ──▶ TIMED_WAITING ──▶ RUNNABLE
          │                  │
       sleep()           time elapsed
                         or interrupted
```

### What Sleep Does

`Thread.sleep(1000)` instructs the operating system to **not schedule** the current thread until the given time passes. During that time, the thread is **not consuming any CPU**.

📁 *Code: `aBasics/aPlatformThreads/T3SleepDemo.java`*

---

## Yield - Giving Up CPU

`Thread.yield()` is a **hint** to the scheduler that the current thread is willing to give up its current use of the processor.

### Key Characteristics

- Just a **hint** to scheduler (can be **ignored**)
- Gives chance to threads of **same or higher priority**
- If no waiting threads, same thread continues
- **No exception** thrown
- Thread stays in **RUNNABLE** state (doesn't change to WAITING)

### Usage

```java
Thread.yield();  // "I'm willing to pause, give others a chance"
```

### What Happens

- Thread transitions **from RUNNING to RUNNABLE**
- Allows other threads to be scheduled
- **Not guaranteed** that:
  - Current thread will stop immediately
  - Other threads will be scheduled right away

### Sleep vs Yield Comparison

| Aspect | sleep() | yield() |
|--------|---------|---------|
| State Change | RUNNABLE → TIMED_WAITING | Stays RUNNABLE |
| Duration | Specified time | Immediate return possible |
| Guarantee | Minimum sleep guaranteed | No guarantee |
| Exception | InterruptedException | None |
| Use Case | Timed pauses | Cooperative multitasking |

📁 *Code: `aBasics/executionPrevention/T1YieldDemo.java`*

---

## Join - Waiting for Completion

`join()` makes the **calling thread wait** until the target thread completes. This is crucial for making execution **deterministic**.

### Key Characteristics

- **Calling thread waits** for target thread to complete
- Throws `InterruptedException`
- Makes execution **deterministic**
- Overloaded versions available

### Usage

```java
Thread t = new Thread(task);
t.start();
t.join();           // Block until t completes
// Code here runs AFTER t finishes

// With timeout
t.join(1000);       // Wait max 1 second
t.join(1000, 500);  // Wait max 1 second and 500 nanoseconds
```

### Important Note on Lambda

When using Lambda with Fluent API:
```java
Thread t = Thread.ofPlatform().start(() -> {
    TimeUnit.SECONDS.sleep(5);
});
t.join();  // Still need join() to wait!
```

⚠️ **Common Misconception**: `start()` returns immediately - you still need `join()` if you want the main thread to wait for completion.

### Join Visualization

```
Without join():                 With join():
┌────────┐   ┌────────┐        ┌────────┐   ┌────────┐
│ Main   │   │ Child  │        │ Main   │   │ Child  │
├────────┤   ├────────┤        ├────────┤   ├────────┤
│ start  │──▶│ runs   │        │ start  │──▶│ runs   │
│ runs   │   │ runs   │        │ join() │   │ runs   │
│ ends?  │   │ runs   │        │ WAITS  │   │ runs   │
└────────┘   │ ends   │        │ WAITS  │   │ ends   │
             └────────┘        │ resumes│◀──┘        
                               └────────┘
     Output: UNPREDICTABLE          Output: DETERMINISTIC
```

📁 *Code: `aBasics/executionPrevention/T2JoinDemo.java`*

---

## Interrupt - Stopping Threads

Interruption is a **cooperative** mechanism - the thread must check and respond to interrupts.

### Why Cooperative?

Java doesn't provide a way to **forcibly stop** a thread. The deprecated `stop()` method is unsafe because it can:
- Leave shared data in inconsistent state
- Release locks unexpectedly
- Cause resource leaks

### How Interruption Works

When `interrupt()` is called:
- If thread is **sleeping/waiting**: `InterruptedException` is thrown
- If thread is **running**: Interrupt flag is set (thread must check)

### Usage

```java
// Interrupting a thread
t.interrupt();

// Inside the thread - check interrupt status
while (!Thread.currentThread().isInterrupted()) {
    doWork();
}
// Clean up and exit gracefully

// If thread is sleeping/waiting
try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();  // Restore flag!
    return;  // Exit gracefully
}
```

### Interrupt Methods

| Method | Description |
|--------|-------------|
| `t.interrupt()` | Set interrupt flag / throws InterruptedException if waiting |
| `Thread.interrupted()` | Returns AND **clears** interrupt flag (static) |
| `t.isInterrupted()` | Returns interrupt flag (**doesn't clear**) |

### Handling InterruptedException

```java
// Methods that throw InterruptedException automatically
// clear the interrupt flag when the exception is thrown
// So you need to restore it:

try {
    Thread.sleep(1000);
} catch (InterruptedException e) {
    // Interrupt flag is cleared when exception thrown
    Thread.currentThread().interrupt();  // Restore it!
    // Now handle the interruption
}
```

📁 *Code: `aBasics/executionPrevention/T3InterruptDemo.java`*

---

## Thread Groups

Thread groups organize threads into logical groups for collective operations. Every thread belongs to a thread group.

### Hierarchy

```
system
  └── main (default group)
       ├── Workers
       │    ├── Worker-1
       │    └── Worker-2
       └── Readers
            ├── Reader-1
            └── Reader-2
```

### Usage

```java
// Get default thread group
ThreadGroup currentGroup = Thread.currentThread().getThreadGroup();

// Create custom thread group
ThreadGroup workers = new ThreadGroup("Workers");

// Create thread in specific group
Thread t = new Thread(workers, task, "Worker-1");
t.start();

// Group operations
workers.activeCount();       // Count active threads
workers.activeGroupCount();  // Count active subgroups
workers.list();              // Print thread info (debugging)
workers.enumerate(Thread[] list);  // Get all threads
```

### Use Cases

- **Logical organization** of related threads
- **Bulk operations** on related threads
- **Security** - restrict thread creation in certain groups
- **Debugging** - easily identify thread relationships

📁 *Code: `aBasics/bThreadGroups/aBasicsThreadGroups.java`*

---

## Quick Reference

### Priority
```java
t.setPriority(1-10);
t.getPriority();
// Priority is a HINT, platform-dependent
```

### Sleep
```java
Thread.sleep(ms);
TimeUnit.SECONDS.sleep(n);
Thread.sleep(Duration.ofSeconds(n));
// Goes to TIMED_WAITING, releases CPU but NOT locks
```

### Yield
```java
Thread.yield();
// Hint only, stays RUNNABLE, may be ignored
```

### Join
```java
t.join();
t.join(timeout);
// Calling thread waits for t to complete
```

### Interrupt
```java
t.interrupt();             // Set flag or throw exception
Thread.interrupted();      // Check AND clear flag
t.isInterrupted();         // Check only (don't clear)
// Always restore flag after catching InterruptedException
```

### Thread Groups
```java
ThreadGroup group = new ThreadGroup("name");
Thread t = new Thread(group, runnable, "threadName");
group.activeCount();
group.list();
```

---

## Summary

✅ **Priority** is platform-dependent hint (1-10, default 5)  
✅ **`sleep()`** releases CPU, goes to TIMED_WAITING, keeps locks  
✅ **`yield()`** is just a hint, stays RUNNABLE  
✅ **`join()`** makes calling thread wait - deterministic execution  
✅ **Interruption** is cooperative - thread must check and respond  
✅ **Thread groups** organize threads for collective operations

### Best Practices

1. **Don't rely on priority** for correctness
2. **Always restore interrupt flag** after catching InterruptedException
3. **Use join()** when you need deterministic ordering
4. **Handle interruption gracefully** - clean up resources

---

*Next: [Part 4: Race Conditions & Critical Sections →]({% post_url /java/threads/2026-04-02-04-race-conditions-critical-sections %})*

