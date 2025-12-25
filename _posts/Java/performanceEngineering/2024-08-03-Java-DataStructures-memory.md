---
title: String Intern pool, Hashmaps and Collections
date: 2024-07-03 00:10:00
categories:
- Performance Engineering
tags:
- Java
- Memory
- Performance
- HashMap
- Collections
---

{% include toc title="Index" %}

# The String Pool $ string deduplication.

Since Java 8, Spring pools libe in Heap.

The virtual machine can actually detect the duplicated strings and it will
remove one of them
and make the two variables point to the same underlying reference.

Explicitly specifying a string to be placed in string pool

```java
String x = 100.toString().intern();
String y = "100";
//x.equals(y);//True
```

String Pool is internally saved in a HashMap. The String is hashed and kept in
the respective HashMap. If 2 strings
map to a same hashkey, then chaining happens.

```java
-XX:+PrintStringTableStatistics: Prints statistics about the String pool.
```

The default number of buckets are 65536 when the JVM begins.

```
StringTable statistics:
Number of buckets       :     65536 =    524288 bytes, each 8
Number of entries       :        31 =       496 bytes, each 16
Number of literals      :        31 =      2256 bytes, avg  72.000
```

# Lists

**CopyOnWriteArrayList**

- Thread-safe variant of ArrayList where all mutative operations (add, set, and
  so on) are implemented by making a fresh copy of the underlying array.
- Suitable for use with concurrent read operations.
- When read operations are frequent, and write/delete operations are rare and
  need to be thread-safe.

- ArrayList
    - [initialized with size 10 on the heap](https://github.com/openjdk/jdk/blob/8bd3cd51562ff9e76fa0e3d49d38e6e19210f878/src/java.base/share/classes/java/util/ArrayList.java#L119)
    -
    size [increases dynamically (upon getting full) by 50%](https://github.com/openjdk/jdk/blob/8bd3cd51562ff9e76fa0e3d49d38e6e19210f878/src/java.base/share/classes/java/util/ArrayList.java#L235-L237)
    - If large list size id anticipated, initialize it with a large initial size
      `List<Book> initialSizeList = new ArrayList<>(SIZE);`
- Vector
    - like ArrayList, since 1.1, but threadsafe. ArrayList was added in Java 1.2
    - **Alternative to CopyOnWriteArrayList**
    - Comes with a performance cost because of being threadsafe
- Stack
    - Child Class of Vector
    - Use LinkedList instead as it provides Doubly ended Queue(Deque)
- LinkedList
    - The get() method will be extremely slow for large lists due to sequential
      search
    - Sorting will be slow with linked lists as it is first converted to
      ArrayList. Both uses Arrays.sort() internally

AttributeList

- A list specifically designed to hold MBean attributes, extending
  ArrayList<Attribute>.

RoleList

- A list of Role objects, extending ArrayList<Role>.

RoleUnresolvedList

- A list specifically designed to hold RoleUnresolved objects, extending
  ArrayList<RoleUnresolved>.

# Maps

HAshmaps doubles its size when the initial capacity is full.

- it involves reshuffling old keys in the new increased hashMap which is a
  significant overhead.