---
title: "Java Multithreading - Part 5: Synchronization Mechanisms"
date: 2026-04-02 00:00:05
categories: [java, multithreading, concurrency]
tags: [java, threads, synchronized, volatile, atomic, memory-visibility]
---
{% include toc title="Index" icon="cog" %}

# Part 5: Synchronization Mechanisms

This part covers the core synchronization mechanisms in Java: synchronized keyword, volatile, and atomic variables.

## Table of Contents
1. [The synchronized Keyword](#the-synchronized-keyword)
2. [Object-Level vs Class-Level Locks](#object-level-vs-class-level-locks)
3. [The volatile Keyword](#the-volatile-keyword)
4. [Atomic Variables](#atomic-variables)
5. [Happens-Before Relationship](#happens-before-relationship)
6. [Choosing the Right Tool](#choosing-the-right-tool)

---

## The synchronized Keyword

`synchronized` ensures that only **one thread can execute** a block of code at a time. It provides both **mutual exclusion** and **memory visibility**.

### Synchronized Method

When you declare a method as synchronized, the thread acquires the lock on the object (or class for static methods) before executing.

```java
public synchronized void method() {
    // Only one thread per object instance can execute this
}
```

### Synchronized Block

For finer control, synchronize only a portion of the method:

```java
public void method() {
    // Non-critical code (can run concurrently)
    
    synchronized (lockObject) {
        // Critical section - only one thread at a time
    }
    
    // Non-critical code
}
```

### Types of Lock Objects

```java
synchronized (this)           // Lock on current object instance
synchronized (MyClass.class)  // Lock on Class object (for static)
synchronized (customLock)     // Lock on any object
```

### Synchronized Block Advantage

More granular control - lock only what's necessary:

```java
private final Object lock = new Object();

public void method() {
    doSomeWork();  // Multiple threads can run this
    
    synchronized (lock) {
        // Only critical code is locked
        counter++;
    }
    
    doMoreWork();  // Multiple threads can run this
}
```

📁 *Code: `raceCondition/dSynchronization/S3SynchronizedMethodDemo.java`*

---

## Object-Level vs Class-Level Locks

Understanding the difference is crucial for correct synchronization.

### Object-Level Lock (Instance Lock)

```java
// Lock is on 'this' object instance
public synchronized void instanceMethod() { }

// Equivalent to:
public void instanceMethod() {
    synchronized (this) { }
}
```

**Key Point**: Different objects = Different locks!

Two threads accessing the same synchronized method on **different objects** can run simultaneously.

```java
Counter c1 = new Counter();
Counter c2 = new Counter();

// Thread 1 on c1.increment() and Thread 2 on c2.increment()
// CAN run simultaneously! (different locks)
```

### Class-Level Lock (Static Lock)

```java
// Lock is on the Class object
public static synchronized void staticMethod() { }

// Equivalent to:
public void staticMethod() {
    synchronized (MyClass.class) { }
}
```

**Key Point**: One lock for entire class!

All threads share the same lock regardless of which object they use.

### Visual Comparison

```
Object Lock:                    Class Lock:
┌─────────┐ ┌─────────┐        ┌───────────────────┐
│  obj1   │ │  obj2   │        │    Class Lock     │
│  Lock   │ │  Lock   │        │     (one)         │
└────┬────┘ └────┬────┘        └─────────┬─────────┘
     ↑           ↑                       ↑
   T1,T3       T2,T4               T1,T2,T3,T4
   
Different objects can             All threads compete
run simultaneously               for same lock
```

⚠️ **Key Rule**: Synchronization only works when threads operate on the **SAME lock**!

---

## The volatile Keyword


`volatile` provides **visibility guarantee** but does NOT provide atomicity.

Volatile variables are **stored in main memory** and their changes are visible to all threads immediately.

- The volatile keyword **prevents the CPU from caching** the variable's value in a local register or cache.

### Atomicity - No Guarantee

The volatile keyword **does not guarantee atomicity** for compound operations (e.g., incrementing a variable, `count++`).

- It only ensures that the latest value of the variable is visible across threads
- For atomic operations, additional synchronization mechanism or atomic classes (like `AtomicInteger`) are needed

### The Memory Visibility Problem

Without volatile, threads may cache variable values in CPU registers/cache:

```
Without volatile:
┌───────────────────┐    ┌───────────────────┐
│    Thread 1       │    │    Thread 2       │
│  ┌─────────────┐  │    │  ┌─────────────┐  │
│  │ CPU Cache   │  │    │  │ CPU Cache   │  │
│  │ flag = true │  │    │  │ flag = false│  │ ← Stale!
│  └──────┬──────┘  │    │  └──────┬──────┘  │
└─────────┼─────────┘    └─────────┼─────────┘
          │                        │
          ▼                        ▼
    ┌─────────────────────────────────────┐
    │           Main Memory               │
    │          flag = true                │
    └─────────────────────────────────────┘
```

### Volatile Solution

Volatile variables are **stored in main memory** and changes are visible to all threads immediately.

```java
private volatile boolean running = true;

// Thread 1                    // Thread 2
running = false;              while (running) { }  
                              // Sees change immediately!
```

### What volatile Guarantees

1. **Visibility**: Changes are immediately visible to all threads
2. **No Caching**: Prevents CPU from caching the variable
3. **Happens-Before**: Writes happen-before subsequent reads
4. **No Reordering**: Reads/writes cannot be reordered

### What volatile Does NOT Guarantee

**Atomicity for compound operations!**

```java
private volatile int counter;

// Still NOT atomic - still has race condition!
counter++;  // Read + Increment + Write

// Still needs synchronization for compound operations
```

### volatile vs synchronized

| Feature | volatile | synchronized |
|---------|----------|--------------|
| Visibility | ✅ Yes | ✅ Yes |
| Atomicity | ❌ No | ✅ Yes |
| Blocking | ❌ No | ✅ Yes (waits for lock) |
| Use Case | Simple flags, single read/write | Compound operations |

### Volatile Implementation

The JVM uses **memory barriers** (fences):

- **Store Barrier**: Ensures writes to volatile aren't reordered with preceding writes
- **Load Barrier**: Ensures reads of volatile aren't reordered with following reads

```java
volatile int sharedVar = 0;

public void task() {
    // All instructions WILL be executed before
    write(sharedVar);  // Memory barrier here
    // All instructions will be executed after
}
```

### Shared Multiprocessor Architecture

Also see: [Shared Multiprocessor Architecture (Baeldung)](https://www.baeldung.com/java-volatile#shared-multiprocessor-architecture)

![CPU Architecture](https://www.baeldung.com/wp-content/uploads/2017/08/cpu.png)

| Other Variables | One Possible State |
|:---------------:|:------------------:|
| ![java-volatile-1.png](/assets/images/java-volatile-1.png) | ![java-volatile-2.png](/assets/images/java-volatile-2.png) |

📁 *Code: `raceCondition/eVolatileVar/VolatileTest.java`*

---

## Atomic Variables

Atomic classes in `java.util.concurrent.atomic` package provide **lock-free thread-safe operations** using CAS (Compare-And-Swap).

### Available Types

- `AtomicInteger`, `AtomicLong`, `AtomicBoolean`
- `AtomicReference<T>` for object references
- `AtomicIntegerArray`, `AtomicLongArray`, `AtomicReferenceArray`

### AtomicInteger Example

```java
int initialValue = 0;
AtomicInteger atomicInteger = new AtomicInteger(initialValue);

// Increment operations
int previousValue = atomicInteger.getAndIncrement(); // counter++ (returns OLD)
int updatedValue = atomicInteger.incrementAndGet();  // ++counter (returns NEW)

// Add operations
atomicInteger.addAndGet(5);     // Returns new value
atomicInteger.getAndAdd(5);     // Returns old value

// Read
int value = atomicInteger.get();

// CAS (Compare-And-Set)
atomicInteger.compareAndSet(expected, newValue);
```

### Method Summary

| Method | Description | Return |
|--------|-------------|--------|
| `get()` | Get current value | Current value |
| `set(v)` | Set value | void |
| `incrementAndGet()` | ++value | New value |
| `getAndIncrement()` | value++ | Old value |
| `addAndGet(delta)` | value += delta | New value |
| `compareAndSet(e, n)` | Set if current == expected | true if successful |

### Pros and Cons

**Pros:**
- Simplicity
- No synchronization or locks needed
- No race conditions or data races

**Cons:**
- Only the operation itself is atomic
- Race condition between 2 separate atomic operations:

```java
AtomicInteger atomicInteger = new AtomicInteger(0);

int a = atomicInteger.incrementAndGet();
int b = atomicInteger.addAndGet(-1);  // RACE CONDITION between these!
```

### AtomicLong and AtomicDouble

For long and double (64-bit values):

```java
AtomicLong atomicLong = new AtomicLong();
atomicLong.incrementAndGet();
long value = atomicLong.get();
```

**Note**: `AtomicDouble` is **not in standard library** - available in Google Guava.

### AtomicReference<T>

For atomic operations on object references:

```java
AtomicReference<MyObject> atomicRef = new AtomicReference<>(new MyObject());

// Atomic assignment
atomicRef.set(newValue);

// Atomic read
MyObject obj = atomicRef.get();

// CAS
atomicRef.compareAndSet(expectedObj, newObj);
```

📁 *Code: `raceCondition/fAtomicVar/AtomicIntCounter.java`*

---

## Happens-Before Relationship

The **Happens-Before** relationship guarantees ordering between operations.

### Rules

1. **Program Order**: Within a thread, each action happens-before subsequent actions
2. **Monitor Lock**: Unlock happens-before subsequent lock on same monitor
3. **Volatile**: Write to volatile happens-before subsequent reads
4. **Thread Start**: `start()` happens-before any action in started thread
5. **Thread Join**: All actions in thread happen-before `join()` returns
6. **Transitivity**: If A happens-before B, and B happens-before C, then A happens-before C

### volatile and Happens-Before

```java
volatile int x;
int y;

// Thread 1
y = 1;      // (1)
x = 1;      // (2) - volatile write

// Thread 2
if (x == 1) {  // (3) - volatile read
    // y is GUARANTEED to be 1 here
    // Because (1) happens-before (2) (program order)
    // And (2) happens-before (3) (volatile rule)
    // So (1) happens-before (3) (transitivity)
}
```

---

## Choosing the Right Tool

### Decision Tree

```
Need thread safety?
│
├── Single boolean flag?
│   └── volatile
│
├── Single counter/number?
│   └── AtomicInteger/AtomicLong
│
├── Single reference?
│   └── AtomicReference<T>
│
├── Multiple variables together?
│   └── synchronized
│
├── Compound check-then-act?
│   └── synchronized or Lock
│
└── Complex operations?
    └── ReentrantLock (Part 6)
```

### Comparison Table

| Feature | synchronized | volatile | Atomic |
|---------|--------------|----------|--------|
| Mutual Exclusion | ✅ Yes | ❌ No | ❌ No |
| Visibility | ✅ Yes | ✅ Yes | ✅ Yes |
| Atomicity | ✅ Yes | ❌ No | ✅ Single op |
| Blocking | Yes | No | No |
| Performance | Slower | Fast | Fast |
| Use Case | Compound ops | Flags | Counters |

### Best Practices

1. **Minimize synchronized scope** - Only lock what's necessary
2. **Use appropriate tools** - volatile for flags, Atomic for counters
3. **Prefer higher-level constructs** - Concurrent collections when possible
4. **Understand your locks** - Same lock = mutual exclusion

---

## Summary

✅ **`synchronized`** provides mutual exclusion + visibility (blocking)  
✅ **Object lock** vs **Class lock** - different scopes  
✅ **`volatile`** provides visibility only, not atomicity  
✅ **Atomic classes** provide lock-free atomic operations via CAS  
✅ **Happens-Before** guarantees ordering of operations

### Quick Reference

```java
// Synchronized method
public synchronized void method() { }

// Synchronized block
synchronized (lock) { }

// Volatile flag
private volatile boolean running = true;

// Atomic counter
AtomicInteger counter = new AtomicInteger(0);
counter.incrementAndGet();
counter.compareAndSet(expected, newValue);
```

---

## Related Resources


---

*Next: [Part 6: Locks & Advanced Synchronization →](/java/multithreading/concurrency/06-locks-and-advanced-sync/)*

