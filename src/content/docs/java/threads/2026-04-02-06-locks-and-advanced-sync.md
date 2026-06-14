---
title: "Java Multithreading - Part 6: Locks & Advanced Synchronization"
date: 2026-04-02 00:00:06
categories: [java, multithreading, concurrency]
tags: [java, threads, reentrantlock, readwritelock, deadlock, semaphore, condition]
---

{% include toc title="Index" icon="cog" %}

# Part 6: Locks & Advanced Synchronization

This part covers advanced locking mechanisms, deadlock prevention, condition variables, semaphores, and inter-thread communication.

## Table of Contents

### Part A: Locks (Mutual Exclusion)
1. [What is a Lock?](#what-is-a-lock)
2. [Lock Interface & Implementations](#lock-interface--implementations)
3. [ReentrantLock](#reentrantlock)
4. [ReentrantReadWriteLock](#reentrantreadwritelock)
5. [StampedLock](#stampedlock)
6. [Deadlocks](#deadlocks)

### Part B: Synchronization Aids & Coordination
7. [Condition Variables](#condition-variables)
8. [Semaphores](#semaphores)
9. [Inter-Thread Communication (wait/notify)](#inter-thread-communication)
10. [CountDownLatch and CyclicBarrier](#countdownlatch-and-cyclicbarrier)
11. [Lock-Free Algorithms](#lock-free-algorithms)

---

## Locks vs Synchronization Aids - What's the Difference?

Before diving in, let's clarify an important distinction:

| Category | Purpose | Examples |
|:---------|:--------|:---------|
| **Locks** | **Mutual exclusion** - protect shared data from concurrent access | `synchronized`, `ReentrantLock`, `ReadWriteLock`, `StampedLock` |
| **Synchronization Aids** | **Coordination** - control thread execution flow/timing | `Semaphore`, `CountDownLatch`, `CyclicBarrier`, `Phaser` |

### Why Are They in the Same Article?

Both solve **thread coordination problems**, but differently:

```
LOCKS (Part A)                          SYNCHRONIZATION AIDS (Part B)
─────────────────                       ────────────────────────────
"Only ONE can access this data"         "Wait until condition is met"

┌─────────┐                             ┌─────────┐
│ Thread1 │ ◀── has lock                │ Thread1 │ ── countDown()
├─────────┤                             ├─────────┤
│ Thread2 │ ── waiting for lock         │ Thread2 │ ── countDown()
├─────────┤                             ├─────────┤
│ Thread3 │ ── waiting for lock         │ Thread3 │ ── await() (blocked)
└─────────┘                             └─────────┘
     ↓                                       ↓
Protects SHARED DATA                    Coordinates THREAD TIMING
(race condition prevention)             (orchestration/sequencing)
```

### Quick Classification

```
java.util.concurrent.locks
├── Lock (interface)
│   ├── ReentrantLock         ← LOCK (mutual exclusion)
│   └── ReadWriteLock         ← LOCK (read/write separation)
├── StampedLock               ← LOCK (optimistic locking)
└── Condition                 ← Communication (wait/signal)

java.util.concurrent
├── Semaphore                 ← NOT a lock! (permit-based access control)
├── CountDownLatch            ← NOT a lock! (one-time barrier)
├── CyclicBarrier             ← NOT a lock! (reusable barrier)
├── Phaser                    ← NOT a lock! (flexible barrier)
└── Exchanger                 ← NOT a lock! (data exchange point)
```

**Key insight**: Semaphore with 1 permit *behaves* like a lock (binary semaphore/mutex), but it's conceptually different - it controls **access count**, not **ownership**.

---

# PART A: LOCKS

---

## What is a Lock?

A **Lock** is a synchronization mechanism that controls access to a shared resource by multiple threads. Only one thread (or multiple for read locks) can hold the lock at a time — others must wait.

### Why Do We Need Locks?

When multiple threads access shared data simultaneously, we get **race conditions**:

```java
// WITHOUT LOCK - Race Condition!
class Counter {
    private int count = 0;
    
    void increment() {
        count++;  // NOT atomic! Read → Modify → Write
    }
}

// Thread 1: reads count=5, adds 1, writes 6
// Thread 2: reads count=5 (before T1 writes!), adds 1, writes 6
// Result: count=6 instead of 7! 💥
```

### Two Ways to Lock in Java

| Approach | Mechanism | Flexibility |
|:---------|:----------|:------------|
| **Intrinsic Lock** | `synchronized` keyword | Simple, automatic |
| **Explicit Lock** | `Lock` interface (java.util.concurrent.locks) | Powerful, manual |

```java
// 1. Intrinsic Lock (synchronized)
synchronized (this) {
    // critical section - automatic lock/unlock
}

// 2. Explicit Lock (Lock interface)
Lock lock = new ReentrantLock();
lock.lock();
try {
    // critical section
} finally {
    lock.unlock();  // MUST unlock manually!
}
```

### What is "Reentrant"?

**Reentrant** means a thread can acquire the **same lock multiple times** without deadlocking itself.

```java
// Reentrant = Same thread can enter again
synchronized void methodA() {
    methodB();  // This works! Same thread already holds the lock
}

synchronized void methodB() {
    // Same lock as methodA - reentrant allows this
}

// Without reentrancy, methodA calling methodB would DEADLOCK!
```

Both `synchronized` and `ReentrantLock` are reentrant. The lock maintains a **hold count**:

```
Thread-1 calls methodA()     → hold count = 1
Thread-1 calls methodB()     → hold count = 2  (same thread, allowed)
Thread-1 exits methodB()     → hold count = 1
Thread-1 exits methodA()     → hold count = 0  (lock released)
```

---

## Lock Interface & Implementations

### The Lock Interface (`java.util.concurrent.locks.Lock`)

```java
public interface Lock {
    void lock();                     // Acquire lock (blocks if unavailable)
    void unlock();                   // Release lock
    boolean tryLock();               // Try to acquire, return immediately
    boolean tryLock(long time, TimeUnit unit);  // Try with timeout
    void lockInterruptibly();        // Acquire, but can be interrupted
    Condition newCondition();        // Create condition for wait/signal
}
```

### Lock Class Hierarchy

```
                    ┌─────────────────┐
                    │   <<interface>> │
                    │      Lock       │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              │              ▼
    ┌─────────────────┐      │    ┌─────────────────────┐
    │  ReentrantLock  │      │    │   <<interface>>     │
    │                 │      │    │   ReadWriteLock     │
    │ • Reentrant     │      │    └──────────┬──────────┘
    │ • Fair/Unfair   │      │               │
    │ • Conditions    │      │               ▼
    └─────────────────┘      │    ┌─────────────────────┐
                             │    │ReentrantReadWriteLock│
                             │    │                     │
                             │    │ • readLock()  ──────┼──► Lock
                             │    │ • writeLock() ──────┼──► Lock
                             │    └─────────────────────┘
                             │
                             ▼
                   ┌─────────────────┐
                   │   StampedLock   │
                   │                 │
                   │ • NOT a Lock!   │
                   │ • Stamp-based   │
                   │ • Optimistic    │
                   └─────────────────┘
```

### Quick Comparison of Lock Types

| Lock Type | Reentrant | Multiple Readers | Optimistic Read | Conditions | Use Case |
|:----------|:---------:|:----------------:|:---------------:|:----------:|:---------|
| `synchronized` | ✅ | ❌ | ❌ | ❌ | Simple cases |
| `ReentrantLock` | ✅ | ❌ | ❌ | ✅ | Need tryLock/fair/conditions |
| `ReentrantReadWriteLock` | ✅ | ✅ | ❌ | ✅ | Read-heavy, need reentrancy |
| `StampedLock` | ❌ | ✅ | ✅ | ❌ | Read-heavy, max performance |

### When to Use Which?

```
Start Here
    │
    ▼
Need more than synchronized offers?
    │
    ├── NO → Use synchronized (simplest)
    │
    └── YES → What do you need?
              │
              ├── tryLock / timeout / fairness / conditions
              │   └── Use ReentrantLock
              │
              ├── Multiple simultaneous readers
              │   │
              │   ├── Need reentrancy or conditions?
              │   │   └── Use ReentrantReadWriteLock
              │   │
              │   └── Need max read performance?
              │       └── Use StampedLock (with optimistic reads)
              │
              └── Simple mutual exclusion with more control
                  └── Use ReentrantLock
```

---

## ReentrantLock

`ReentrantLock` is a more flexible lock than the built-in synchronized block. It works same as `synchronized` but requires **explicit locking and unlocking**.

### Advantages

- Can be unlocked in a different method or class from where it was locked
- Provides more control over the lock (e.g., timed lock, interruptible lock)
- Can maintain fairness `ReentrantLock(true)` but may come with a cost of throughput
- Use unlock in finally block so that it is always guaranteed that the resource is unlocked

**Use Case**: When you need advanced locking features not provided by the synchronized block.

### Why Use ReentrantLock Over synchronized?

| Feature | synchronized | ReentrantLock |
|---------|--------------|---------------|
| Acquire | Automatic | Manual (`lock()`) |
| Release | Automatic | Manual (`unlock()` in finally!) |
| Try lock | ❌ No | ✅ `tryLock()` |
| Timeout | ❌ No | ✅ `tryLock(time)` |
| Interruptible | ❌ No | ✅ `lockInterruptibly()` |
| Fair locking | ❌ No | ✅ `new ReentrantLock(true)` |
| Multiple conditions | ❌ No | ✅ `newCondition()` |

### Basic Usage

```java
Lock lock = new ReentrantLock();

public int task() {
    lock.lock();
    try {
        // Critical section
        return doTask();
    } finally {  // GUARANTEED to execute
        lock.unlock();  // With return statements, this is the only way
    }
}
```

**SOLUTION**: Always lock in try block and unlock in finally block!

### Reentrancy

The same thread can acquire the lock multiple times without deadlock:

```java
lock.lock();
try {
    // Already holding lock
    lock.lock();  // Works! Count increases
    try {
        // Do something
    } finally {
        lock.unlock();  // Count decreases
    }
} finally {
    lock.unlock();  // Count reaches 0, lock released
}
```

### Fairness

```java
Lock fairLock = new ReentrantLock(true);   // Fair - FIFO order
Lock unfairLock = new ReentrantLock(false); // Default - no guaranteed order
```

**Fair Lock**: Threads granted locks in order they requested (prevents starvation).  
**Unfair Lock** (default): "Barging" allowed - better throughput but possible starvation.

### tryLock - Non-Blocking

```java
// Immediate attempt
if (lock.tryLock()) {
    try { /* work */ }
    finally { lock.unlock(); }
} else {
    // Lock not available - do something else
}

// With timeout
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try { /* work */ }
    finally { lock.unlock(); }
} else {
    // Timeout - lock not acquired
}
```

**Use Cases**: Video/Image processing, Trading systems, UI Applications

### lockInterruptibly

Useful for deadlock detection and recovery:

```java
try {
    lock.lockInterruptibly();
    // work
} catch (InterruptedException e) {
    if (Thread.currentThread().isInterrupted()) {
        doCleanupAndExit();
    }
}
```

### Query Methods

With explicit locking we have more control over the lock and get more Lock operations:

| Method | Description |
|--------|-------------|
| `int getQueueLength()` | Returns an estimate of the number of threads waiting to acquire the lock |
| `Thread getOwner()` | Returns the thread currently holding the lock, or null if no thread holds it |
| `boolean isHeldByCurrentThread()` | Returns true if the current thread holds the lock |
| `boolean isLocked()` | Returns true if the lock is currently held by any thread |

```java
int waiting = lock.getQueueLength();        // Threads waiting for lock
Thread owner = lock.getOwner();             // Thread holding lock
boolean held = lock.isHeldByCurrentThread(); // Current thread holds lock?
boolean locked = lock.isLocked();           // Lock held by any thread?
```

📁 *Code: `raceCondition/bReentrantLocks/C1ReentrantLock.java`*

---

## ReentrantReadWriteLock

A `ReadWriteLock` allows multiple threads to read a resource concurrently but only one thread to write.

`synchronized` and `ReentrantLock` do not allow **multiple readers** concurrently. `ReentrantReadWriteLock` solves this.

### Advantages

- Improves performance in scenarios where reads are more frequent than writes
- Since the method is guarded by a read lock, many threads can acquire that lock as long as no other thread is holding the write lock

### Rules

- **Multiple threads can hold read lock** simultaneously
- **Only one thread can hold write lock**
- **Write lock blocks all** readers and writers

### When to Use

When read operations are predominant or not fast due to:
- Reading from many variables
- Reading from complex data structures

### Usage

```java
ReadWriteLock rwLock = new ReentrantReadWriteLock();
Lock readLock = rwLock.readLock();
Lock writeLock = rwLock.writeLock();

// Read operation (many can run simultaneously)
public int read(int key) {
    readLock.lock();
    try {
        return readFromDatabase(key);
    } finally {
        readLock.unlock();
    }
}

// Write operation (exclusive)
public void update(int key, int value) {
    writeLock.lock();
    try {
        writeToDatabase(key, value);
    } finally {
        writeLock.unlock();
    }
}
```

### Visualization

```
Timeline with ReadWriteLock:
──────────────────────────────────────────────────────────────
Writer: ████████                    ████████
Reader1:        ████████████████████        ████████████████
Reader2:        ████████████████████        ████████████████
Reader3:        ████████████████████        ████████████████

vs. synchronized (only one at a time):
──────────────────────────────────────────────────────────────
Writer: ████████
Reader1:        ████████
Reader2:                ████████
Reader3:                        ████████
```

📁 *Code: `raceCondition/bReentrantLocks/C2ReadWriteLock.java`*

### ReentrantReadWriteLock Summary

For `ReadWriteLock lock = new ReentrantReadWriteLock();`:

- `writeToDatabase(key, value)` method is guarded by a **write lock**, and only **one thread** can acquire a write lock at a time
- `readFromDatabase(key)` is guarded by a **read lock**. **Many threads** can acquire that lock as long as no other thread is holding the write lock

---

## StampedLock

`StampedLock` (Java 8+) is a capability-based lock that provides **three modes** for controlling read/write access, with better performance than `ReentrantReadWriteLock` in read-heavy scenarios.

### Why StampedLock?

The key innovation is **optimistic reading** - a non-blocking read that doesn't acquire any lock, just validates afterward. This dramatically reduces contention when writes are infrequent.

### Three Locking Modes

| Mode | Method | Description |
|:-----|:-------|:------------|
| **Write Lock** | `writeLock()` | Exclusive access, blocks all readers and writers |
| **Read Lock** | `readLock()` | Shared access, multiple readers allowed, blocks writers |
| **Optimistic Read** | `tryOptimisticRead()` | Non-blocking, doesn't acquire lock, validates later |

### Stamp-Based API

Every lock operation returns a `long` **stamp** that must be used to unlock or validate:

```java
StampedLock lock = new StampedLock();

// Write lock (exclusive)
long stamp = lock.writeLock();
try {
    // exclusive write access
} finally {
    lock.unlockWrite(stamp);
}

// Read lock (shared)
long stamp = lock.readLock();
try {
    // shared read access
} finally {
    lock.unlockRead(stamp);
}
```

### Optimistic Reading (Key Feature)

This is the **main advantage** over `ReentrantReadWriteLock` - reads don't block!

```java
// Optimistic read pattern
long stamp = lock.tryOptimisticRead();  // Returns immediately, no blocking!

// Read shared data (without holding any lock)
int currentX = x;
int currentY = y;

// Validate: was there a write during our read?
if (!lock.validate(stamp)) {
    // A write occurred! Fall back to pessimistic read lock
    stamp = lock.readLock();
    try {
        currentX = x;
        currentY = y;
    } finally {
        lock.unlockRead(stamp);
    }
}
// Safe to use currentX and currentY
```

### Lock Conversion (Upgrade/Downgrade)

Stamps can be converted between modes without releasing and reacquiring:

```java
long stamp = lock.readLock();
try {
    while (someCondition) {
        // Try to upgrade to write lock
        long writeStamp = lock.tryConvertToWriteLock(stamp);
        if (writeStamp != 0L) {
            stamp = writeStamp;  // Upgrade successful
            // Now have write lock - modify data
            break;
        } else {
            // Upgrade failed - release read, acquire write manually
            lock.unlockRead(stamp);
            stamp = lock.writeLock();
        }
    }
} finally {
    lock.unlock(stamp);  // Works for any mode
}
```

### Visualization: Optimistic vs Pessimistic Reading

```
Traditional ReadWriteLock (pessimistic):
──────────────────────────────────────────────────────────────
Writer:  ████████                         ████████
Reader1:         [wait]████████████████████
Reader2:         [wait]████████████████████
         ↑ Readers BLOCKED during write

StampedLock with Optimistic Read:
──────────────────────────────────────────────────────────────
Writer:  ████████                         ████████
Reader1: ○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○
Reader2: ○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○○
         ↑ Readers proceed optimistically (○ = optimistic read)
           Retry only if validate() fails
```

### StampedLock vs ReentrantReadWriteLock

| Feature | StampedLock | ReentrantReadWriteLock |
|:--------|:------------|:-----------------------|
| Optimistic reads | ✅ Yes | ❌ No |
| Reentrant | ❌ **No** | ✅ Yes |
| Condition support | ❌ No | ✅ Yes |
| Lock conversion | ✅ Yes | ❌ No |
| Performance (read-heavy) | **Better** | Good |
| Complexity | Higher | Lower |
| Fair mode | ❌ No | ✅ Yes |

### When to Use StampedLock

✅ **Good for:**
- Read-heavy workloads where optimistic reads can avoid contention
- Short read operations where validation overhead is minimal
- High-throughput scenarios where avoiding blocking is critical
- Point/coordinate classes (classic use case from JDK docs)

❌ **Avoid when:**
- You need reentrant locking (same thread acquiring lock twice)
- You need Condition variables (`await()`/`signal()`)
- Lock hold times are long (optimistic validation more likely to fail)
- Write-heavy workloads (optimistic reads will constantly retry)

### ⚠️ Critical Warnings

1. **Not Reentrant** - Calling `writeLock()` twice from the same thread causes **deadlock**!
   ```java
   // DEADLOCK!
   long stamp1 = lock.writeLock();
   long stamp2 = lock.writeLock();  // Blocks forever
   ```

2. **Stamps Must Match** - Using the wrong stamp causes undefined behavior
   ```java
   long stamp = lock.writeLock();
   lock.unlockRead(stamp);  // WRONG! Used unlockRead for write stamp
   ```

3. **Optimistic Reads Can Fail** - Always have a fallback strategy
   ```java
   // Always validate and have a backup plan
   if (!lock.validate(stamp)) {
       // Must re-read with actual lock
   }
   ```

4. **Not Serializable** - Unlike `ReentrantReadWriteLock`

### Complete Example: Point Class

```java
class Point {
    private double x, y;
    private final StampedLock lock = new StampedLock();

    // Exclusive write
    void move(double deltaX, double deltaY) {
        long stamp = lock.writeLock();
        try {
            x += deltaX;
            y += deltaY;
        } finally {
            lock.unlockWrite(stamp);
        }
    }

    // Optimistic read with fallback
    double distanceFromOrigin() {
        long stamp = lock.tryOptimisticRead();
        double currentX = x, currentY = y;
        
        if (!lock.validate(stamp)) {
            // Fallback to read lock
            stamp = lock.readLock();
            try {
                currentX = x;
                currentY = y;
            } finally {
                lock.unlockRead(stamp);
            }
        }
        return Math.sqrt(currentX * currentX + currentY * currentY);
    }

    // Conditional write with upgrade
    void moveIfAtOrigin(double newX, double newY) {
        long stamp = lock.readLock();
        try {
            while (x == 0.0 && y == 0.0) {
                long writeStamp = lock.tryConvertToWriteLock(stamp);
                if (writeStamp != 0L) {
                    stamp = writeStamp;
                    x = newX;
                    y = newY;
                    break;
                } else {
                    lock.unlockRead(stamp);
                    stamp = lock.writeLock();
                }
            }
        } finally {
            lock.unlock(stamp);
        }
    }
}
```

📁 *Code: `raceCondition/bReentrantLocks/C3StampedLock.java`*

---

## Deadlocks

A **deadlock** occurs when two or more threads are blocked forever, each waiting for the other.

### Classic Example

```java
// Thread 1                    // Thread 2
synchronized(lockA) {          synchronized(lockB) {
    synchronized(lockB) { }        synchronized(lockA) { }  // DEADLOCK!
}                              }
```

### Four Conditions for Deadlock (ALL Required)

| Condition | Description | Prevention |
|-----------|-------------|------------|
| **Mutual Exclusion** | Resource held exclusively | Can't always avoid |
| **Hold and Wait** | Hold one, wait for another | Request all at once |
| **No Preemption** | Can't take from another | Allow timeouts |
| **Circular Wait** | A waits B waits A | **Lock ordering** |

### Easiest Solution: Break Circular Wait

> **Lock resources in the same order everywhere!**

```java
// Solution: Same lock order in all methods
void method1() { 
    synchronized(lockA) { 
        synchronized(lockB) { } 
    } 
}

void method2() { 
    synchronized(lockA) {        // Same order as method1!
        synchronized(lockB) { } 
    } 
}
```

### Prevention Strategies

1. **Lock Ordering**: Always acquire locks in the same order
2. **tryLock with Timeout**: Back off on failure
3. **Single Lock**: Use one lock instead of multiple when possible

### Deadlock Detection

1. **Watchdog**: Periodically checks if threads are responsive
2. **Thread Interruption**: Not possible with synchronized, use ReentrantLock
3. **tryLock Operations**: Not possible with synchronized

```java
// Solution with tryLock
if (lock.tryLock(1, TimeUnit.SECONDS)) {
    try { /* work */ }
    finally { lock.unlock(); }
} else {
    // Back off and retry
}
```

📁 *Code: `raceCondition/deadLocks/DeadLockDemo.java`*

---

## Condition Variables

Condition variables are used with locks to allow threads to wait for certain conditions to be met. They are always associated with a lock.

### Advantages

- Allows for complex waiting conditions
- More flexible than wait/notify (can have multiple conditions per lock)

### Why Use Condition Variables?

A semaphore is a particular example: "Is number of permits > 0?"

- If condition not met, thread sleeps until another thread changes state
- Lock ensures **atomic** check and modification

### Usage

```java
Lock lock = new ReentrantLock();
Condition condition = lock.newCondition();

// Shared resources
String username = null, password = null;
```

### await() - Wait for Condition

Unlocks the lock and waits until signal or timeout:

```java
lock.lock();
try {
    while (username == null || password == null) {
        condition.await();  // Releases lock, waits
        // condition.await(1, TimeUnit.SECONDS);  // With timeout
    }
    performTask();
} finally {
    lock.unlock();
}
```

### signal() - Wake Up Waiting Thread

```java
lock.lock();
try {
    username = getUserFromUiTextBox();
    password = getPasswordFromUiTextBox();
    condition.signal();  // Wake ONE waiting thread
    // condition.signalAll();  // Wake ALL waiting threads
} finally {
    lock.unlock();
}
```

📁 *Code: Referenced in `2024-08-18-condition-variables.md`*

---

## Semaphores

A `Semaphore` restricts the **number of threads** that can access a resource.

[English meaning](https://www.merriam-webster.com/dictionary/semaphore)

![Semaphore Signal](https://merriam-webster.com/assets/mw/static/art/dict/semaphor.gif)

### Basic Concept

```java
Semaphore semaphore = new Semaphore(int permits);
```

- Initialize with N permits
- `acquire()` - Take a permit (block if none available)
- `release()` - Return a permit

### Usage

```java
Semaphore semaphore = new Semaphore(3);  // 3 concurrent threads

try {
    semaphore.acquire();  // Block until permit available
    // Critical section - max 3 threads here
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
} finally {
    semaphore.release();  // ALWAYS release!
}
```

### tryAcquire

```java
if (semaphore.tryAcquire(1, TimeUnit.SECONDS)) {
    try {
        // Critical section
    } finally {
        semaphore.release();
    }
} else {
    // Handle failure to acquire
}
```

### Semaphore vs Lock

| Feature | Semaphore | Lock |
|---------|-----------|------|
| **Purpose** | Control N concurrent accesses | Mutual exclusion (1 thread) |
| **Basic Operation** | **Acquire**: Threads acquire permits before accessing the resource. If no permits are available, threads **block** until a permit becomes available.<br>**Release**: Threads release permits when done with the resource. | **Lock**: A thread acquires the lock to access the resource. If the lock is held by another thread, the current thread blocks.<br>**Unlock**: The thread releases the lock. |
| **Permits** | N permits (configurable) | 1 (binary) |
| **Owner notion** | No owner | Has owner thread |
| **Reentrancy** | Not reentrant. The binary semaphore (permits = 1) is **not reentrant**; if the same thread acquires it and tries to reacquire, it is stuck. | Can be reentrant (e.g., `ReentrantLock`) |
| **Release** | Any thread can release (even without acquiring!) - can create bugs | Only owner can release |
| **Example Use Cases** | Database Connection Pool, Thread Pool Management | Critical Section, Atomic Operations |

**Note**: A lock is a special case of semaphore with `permits = 1`.

**Warning**: Semaphore permits can be released by any thread, even if it did not acquire the permit. This can create bugs as it allows multiple threads to enter a critical section simultaneously.

### Producer-Consumer with Semaphores

This pattern allows many producers and many consumers, and enables the consumers to apply **back pressure** on the producers, if the producers produce faster than the consumers can consume.

```java
final int QUEUE_CAPACITY = 10;
Semaphore emptySemaphore = new Semaphore(QUEUE_CAPACITY);
Semaphore fullSemaphore = new Semaphore(0);
ReentrantLock lock = new ReentrantLock();
Queue<Integer> queue = new ArrayDeque<>();

// Producer
while (true) {
    emptySemaphore.acquire();  // Wait for empty slot
    lock.lock();
    try {
        queue.add(produceItem());
    } finally {
        lock.unlock();
    }
    fullSemaphore.release();   // Signal item available
}

// Consumer
while (true) {
    fullSemaphore.acquire();   // Wait for available item
    lock.lock();
    try {
        consumeItem(queue.remove());
    } finally {
        lock.unlock();
    }
    emptySemaphore.release();  // Signal empty slot available
}
```

📁 *Code: `raceCondition/semaphore/ProducerConsumer.java`*

---

## Inter-Thread Communication

Traditional `wait()`, `notify()`, `notifyAll()` for thread coordination.

### How It Works

- **`wait()`**: Release lock and wait until notified
- **`notify()`**: Wake up ONE waiting thread (arbitrary)
- **`notifyAll()`**: Wake up ALL waiting threads (preferred)

### Important Rules

1. **Must be in synchronized block** - Otherwise `IllegalMonitorStateException`
2. **Always use while loop** for wait condition (spurious wakeups)
3. **Prefer `notifyAll()` over `notify()`**

### Producer-Consumer Pattern

```java
// Consumer
synchronized (lock) {
    while (buffer.isEmpty()) {
        lock.wait();      // Release lock and wait
    }
    item = buffer.remove();
}

// Producer
synchronized (lock) {
    buffer.add(item);
    lock.notifyAll();     // Wake all waiting consumers
}
```

### Method Summary

| Method | Description |
|--------|-------------|
| `wait()` | Release lock, wait indefinitely |
| `wait(ms)` | Wait with timeout |
| `notify()` | Wake ONE waiting thread (arbitrary) |
| `notifyAll()` | Wake ALL waiting threads (preferred) |

📁 *Code: `raceCondition/dInterThreadComm/I3NotifyAll.java`*

---

## CountDownLatch and CyclicBarrier

Higher-level synchronization utilities from `java.util.concurrent`.

### CountDownLatch - Wait for N Events (One-Time)

Cannot be reset after reaching zero.

```java
CountDownLatch latch = new CountDownLatch(3);

// Workers signal completion
latch.countDown();  // Decrement counter

// Main thread waits
latch.await();      // Block until counter reaches 0
latch.await(5, TimeUnit.SECONDS);  // With timeout
```

**Use Case**: Wait for multiple services to initialize.

### CyclicBarrier - Threads Wait for Each Other (Reusable)

Threads wait at barrier until all arrive, then can be reused.

```java
CyclicBarrier barrier = new CyclicBarrier(3, () -> {
    System.out.println("All parties arrived!");  // Optional action
});

// Each thread
barrier.await();  // Wait for all parties
// Continue after all arrive
```

**Use Case**: Parallel algorithms with multiple phases.

### Comparison

| Feature | CountDownLatch | CyclicBarrier |
|---------|----------------|---------------|
| Reusable | ❌ No (one-time) | ✅ Yes |
| Counter | Decremented externally | Internal wait count |
| Use Case | Wait for N events | N threads synchronize |
| Reset | Cannot reset | Automatic after barrier |
| Barrier Action | None | Optional runnable |

📁 *Code: `raceCondition/dSynchronization/C4CyclicBarrier.java`*

---

## Exchanger

An `Exchanger` allows two threads to exchange data with each other at a synchronization point.

### Usage

```java
Exchanger<String> exchanger = new Exchanger<>();

// Thread 1
String dataFromThread2 = exchanger.exchange("Data from Thread 1");
// Now has data from Thread 2

// Thread 2
String dataFromThread1 = exchanger.exchange("Data from Thread 2");
// Now has data from Thread 1
```

### Advantages

- Useful for thread communication where each thread provides data to the other

### Use Case

Pairwise data exchange between threads, such as:
- Producer-Consumer where they swap buffers
- Genetic algorithms exchanging chromosomes
- Pipeline processing stages

---

## Phaser

A `Phaser` is a more flexible version of `CountDownLatch` and `CyclicBarrier` combined.

### Advantages

- Supports **dynamic registration** of parties (threads can join/leave)
- Supports **multiple phases** of synchronization
- More flexible than CountDownLatch (reusable) and CyclicBarrier (dynamic parties)

### Usage

```java
Phaser phaser = new Phaser(1);  // Register self

// Dynamic registration
phaser.register();  // Add a party

// Arrive and wait for others
phaser.arriveAndAwaitAdvance();

// Arrive without waiting
phaser.arrive();

// Deregister
phaser.arriveAndDeregister();

// Get current phase
int phase = phaser.getPhase();
```

### Use Case

Complex synchronization scenarios with:
- Multiple phases of computation
- Dynamic participants (threads joining/leaving during execution)
- Hierarchical synchronization (phasers can be tiered)

---

## Synchronizers Comparison

| Synchronizer | Reusable | Dynamic Parties | Multiple Phases | Use Case |
|:-------------|:--------:|:---------------:|:---------------:|:---------|
| CountDownLatch | ❌ No | ❌ No | ❌ No | Wait for N events once |
| CyclicBarrier | ✅ Yes | ❌ No | ✅ Yes (reuse) | N threads sync repeatedly |
| Phaser | ✅ Yes | ✅ Yes | ✅ Yes | Complex multi-phase coordination |
| Exchanger | ✅ Yes | ❌ No (2 only) | ❌ No | Pairwise data exchange |

---

## Note on Distributed Systems

> Synchronization mechanisms like `CountDownLatch` and `CyclicBarrier` can be applicable in distributed systems.

Their usage and considerations differ compared to their usage in single-process applications:
- In distributed systems, you typically use distributed coordination services (e.g., ZooKeeper, etcd)
- Network latency and partition tolerance become critical factors
- Consider using distributed locks, barriers, and latches from frameworks like Apache Curator

---

## Lock-Free Algorithms

### What's Wrong with Locks?

1. **Deadlocks** - Threads waiting forever
2. **Slow critical section** - Slowest thread determines speed
3. **Priority inversion** - Low-priority thread blocks high-priority
4. **Kill tolerance** - Thread dies without releasing lock
5. **Performance overhead** - Context switches for contention

### Lock-Free Solutions

Use operations guaranteed as single hardware operation:

- **CAS (Compare-And-Swap)** - Atomic check-then-update
- Single hardware operation = Atomic by definition = Thread-safe

```java
AtomicInteger counter = new AtomicInteger(0);
counter.compareAndSet(expected, newValue);  // CAS operation
```

### When to Use

- Simple counters and flags
- Lock-free data structures
- High-contention scenarios

---

## Summary

✅ **What is a Lock** - Synchronization mechanism for mutual exclusion  
✅ **Lock Interface** - Explicit locking with more control than synchronized  
✅ **ReentrantLock** - More features than synchronized (tryLock, fairness, interruptible)  
✅ **ReadWriteLock** - Multiple readers OR single writer  
✅ **StampedLock** - Optimistic reads for maximum read performance (not reentrant!)  
✅ **Deadlock** - Break circular wait with lock ordering  
✅ **Condition Variables** - Wait for specific conditions  
✅ **Semaphores** - Control N concurrent accesses (NOT a lock!)  
✅ **wait/notify** - Traditional inter-thread communication  
✅ **Latch/Barrier** - Higher-level coordination (NOT locks!)  

### Quick Reference

```java
// ReentrantLock
Lock lock = new ReentrantLock();
lock.lock(); try { } finally { lock.unlock(); }
lock.tryLock(timeout, unit);

// ReadWriteLock
rwLock.readLock().lock();
rwLock.writeLock().lock();

// StampedLock
StampedLock sl = new StampedLock();
long stamp = sl.writeLock(); try { } finally { sl.unlockWrite(stamp); }
long stamp = sl.readLock(); try { } finally { sl.unlockRead(stamp); }
long stamp = sl.tryOptimisticRead(); if (!sl.validate(stamp)) { /* retry */ }

// Condition
Condition cond = lock.newCondition();
cond.await();
cond.signal();

// Semaphore
Semaphore sem = new Semaphore(permits);
sem.acquire();
sem.release();

// wait/notify (inside synchronized)
synchronized (obj) {
    while (!condition) obj.wait();
    obj.notifyAll();
}

// Latch/Barrier
latch.countDown(); latch.await();
barrier.await();
```

---

*Next: [Part 7: Executor Framework →](/java/multithreading/concurrency/07-executor-framework/)*

