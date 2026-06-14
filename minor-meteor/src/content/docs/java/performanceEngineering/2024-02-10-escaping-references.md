---
title: Escaping references
date: 2024-02-10 20:11:00
categories:
- Performance Engineering
tags:
- Java
- Memory
- Performance
- Best Practices
---

{% include toc title="Index" %}

The **"escaping reference"** problem in Java occurs when **a reference to an
object is passed outside its intended scope**
or context, allowing the object's state to be modified unexpectedly.

This problem commonly arises in situations where references to mutable objects
are passed to external code or
stored in a shared context, leading to unintended modifications that can result
in bugs or unexpected behavior.

One common example of the escaping reference problem is when a reference to an
object stored within
a container (such as a collection) is returned or passed to external code *
*without proper encapsulation**.

If the external code **modifies the object's state** directly through this
reference,
it can lead to unexpected changes affecting other parts of the program that
_rely on the object's_ **original state**.

To mitigate the escaping reference problem, it's important to ensure proper
encapsulation and control access to mutable objects.

This can be achieved by:

# For Collections

## 1. Return an Iterator

has issues as iterator can also be used to remove or mutate the items

## 2. Duplicating Collections

imperfect

## 3. Immutable collections

Best one

return `Collections.unmodifiableMap(records)`. Always creates a copy. Java 9 or
earlier

Java 10 onwards - Slight performance improvement

return `Map.copyOf(records)`. If collection is already an unmodifiable map, then
only the reference to that is returned, else a new copy is created

# For Other types of Object

## 4. Duplicating Objects

## 5. Using Interfaces to create Immutable Objects

```java
public interface ReadonlyCustomer {
	String getName();
	String toString();
}
```

## 6. Using Modules to hide implementation