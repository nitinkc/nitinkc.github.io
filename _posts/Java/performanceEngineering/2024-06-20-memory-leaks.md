---
title: Memory Leaks
date: 2024-06-20 00:10:00
categories:
- Performance Engineering
tags:
- Java
- Debugging
- Performance
- Troubleshooting
---

{% include toc title="Index" %}

• In C explicit call free()

Objects that aren’t freed-up, continue to consume memory. This is memory leak

Java avoids memory leaks by
• Running on a Virtual Machine
Adopts the GC Strategy (invented with LISP in 1959 )

## [https://blog.heaphero.io/types-of-outofmemoryerror/](https://blog.heaphero.io/types-of-outofmemoryerror/)

# Java Memory Leaks

A memory leak happens **only if the allocated objects can't be garbage-collected
** because they are referenced from somewhere in the running application.
While allocation profiling doesn't tell us anything about the garbage
collection, it can still give us hints for further investigation.

Regular profiling and memory analysis are essential to detect and resolve memory
leaks in Java applications.

using the memory analyzer tool or Visual VM, figured out the large memory
objects

Memory leaks in Java can occur in various ways, despite the automatic garbage
collection provided by the JVM. Understanding these scenarios is crucial for
developing robust applications. Here are several common causes of memory leaks,
along with real-world examples and their solutions:

# 1. Unintentional Object Retention

Objects that are no longer needed but are still referenced can cause memory
leaks.

```java
private final List<byte[]> list = new ArrayList<>();

public void addData() {
    for (int i = 0; i < 1000; i++) {
        list.add(new byte[1024 * 1024]); // 1 MB each
    }
}
```

list holds references to large byte arrays, causing them to remain in memory (
may lead to OOM).

**Solution**:

Explicitly clear references when they’re no longer needed.

```java
public void clearData() {
    list.clear();
}
```

# 2. Static Field Holding Objects

Static fields can hold references to objects throughout the application's
lifetime, leading to memory leaks.

```java
public class StaticMemoryLeak {
    private static final List<byte[]> list = new ArrayList<>();

    public static void addData() {
        for (int i = 0; i < 1000; i++) {
            list.add(new byte[1024 * 1024]); // 1 MB each
        }
    }
}
```

The list in this example will not be garbage collected until the application
stops.

**Solution:**

Avoid using static fields for objects that should have a limited lifespan.

```java
public class StaticMemoryLeakFixed {
    private final List<byte[]> list = new ArrayList<>();

    public void addData() {
        for (int i = 0; i < 1000; i++) {
            list.add(new byte[1024 * 1024]); // 1 MB each
        }
    }

    public void clearData() {
        list.clear();
    }
}
```

# Caching

Improperly managed caches can hold references to objects longer than necessary.

```java
public class CacheExample {
    private final Map<String, byte[]> cache = new HashMap<>();

    public void addToCache(String key, byte[] value) {
        cache.put(key, value);
    }
}
```

If the cache is not cleared, it can grow indefinitely.

**Solution:**

Use a cache with eviction policies, such as WeakHashMap or Guava Cache.

```java
import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;

public class CacheExample {
    private final Cache<String, byte[]> cache = CacheBuilder.newBuilder()
            .maximumSize(100)
            .expireAfterWrite(10, TimeUnit.MINUTES)
            .build();

    public void addToCache(String key, byte[] value) {
        cache.put(key, value);
    }
}
```

# Summary

Memory leaks in Java can occur due to

- unintentional object retention,
- static fields,
- listeners,
- inner classes,
- ThreadLocals,
- custom class loaders,
- and improperly managed caches.

Using proper coding practices, such as clearing references, using static nested
classes,
and leveraging libraries with built-in eviction policies, can help prevent these
leaks.