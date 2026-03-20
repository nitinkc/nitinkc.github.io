---
title: Collection Framework
date: 2018-01-24 00:32:00
categories:
- Java
tags:
- Collections
- Data Structures
---

{% include toc title="Index" %}

```scss
Collection (Interface)
├── List (Interface)
│   ├── ArrayList
│   ├── LinkedList  ← also implements Deque
│   ├── Vector
│   │   └── Stack
│
├── Set (Interface)
│   ├── HashSet
│   │   └── LinkedHashSet
│   ├── TreeSet  ← implements NavigableSet
│   └── ConcurrentSkipListSet  ← implements NavigableSet
│
├── Queue (Interface)
│   ├── PriorityQueue
│   ├── BlockingQueue (Interface)
│   │   ├── LinkedBlockingQueue
│   │   └── LinkedBlockingDeque  ← also implements Deque
│   └── Deque (Interface)
│       ├── ArrayDeque
│       └── LinkedList  ← also implements List
│
Map (Interface)  ← Not a subtype of Collection
├── HashMap
│   └── LinkedHashMap
├── TreeMap  ← implements NavigableMap
├── WeakHashMap
├── ConcurrentHashMap
└── ConcurrentSkipListMap  ← implements NavigableMap

NavigableMap (Interface)
├── TreeMap
└── ConcurrentSkipListMap

NavigableSet (Interface)
├── TreeSet
└── ConcurrentSkipListSet
```

### Collection Interface (core methods)
- `boolean add(E e)`
- `boolean contains(Object o)` — Returns true if this collection contains the specified element.
- `Iterator<E> iterator()` — Returns an iterator over the elements in this collection.
- `boolean remove(Object o)` — Removes a single instance of the specified element.
- `int size()` — Returns the number of elements in this collection.
- `Object[] toArray()` — Returns an array containing all of the elements in this collection.

### List

#### ArrayList
- `boolean add(E e)` — Appends the specified element to the end of this list.
- `void add(int index, E element)` — Inserts at the specified position; shifts subsequent elements right.
- `int indexOf(Object o)` — Index of the first occurrence, or `-1` if not present.
- `E get(int index)` — Returns the element at the specified position.
- `ListIterator<E> listIterator()`
- `E set(int index, E element)` — Replaces at position; returns previous element.
- `E remove(int index)` — Removes at position; shifts subsequent elements left.
- `boolean remove(Object o)` — Removes the first occurrence if present.

#### LinkedList
- `boolean add(E e)` — Appends to the end of this list.
- `void add(int index, E element)` — Inserts at the specified position.
- `void addFirst(E e)` — Inserts at the beginning.
- `void addLast(E e)` — Appends at the end.
- `E element()` — Retrieves, but does not remove, the head (first element).
- `Iterator<E> descendingIterator()` — Iterates in reverse order.
- `E getFirst()` — Returns the first element.
- `E getLast()` — Returns the last element.
- `boolean offer(E e)` — Adds the specified element as the tail (last element).
- `E peek()` — Retrieves, but does not remove, the head.
- `E poll()` — Retrieves and removes the head.

#### Vector / Stack
- `boolean empty()` — Tests if this stack is empty.
- `E peek()` — Looks at the top element without removing it.
- `E pop()` — Removes the top element and returns it.
- `E push(E item)` — Pushes an item onto the stack.
- `int search(Object o)` — Returns the 1-based position where an object is on this stack.

### Set

#### HashSet / LinkedHashSet
- Same as Collection interface methods.

#### TreeSet
- `E first()` — Returns the first (lowest) element in this set.
- `E last()` — Returns the last (highest) element in this set.

### Queue
- `boolean add(E e)` — Inserts the element, throwing `IllegalStateException` if no space.
- `boolean offer(E e)` — Inserts the element; preferred over `add` when capacity-restricted.
- `E element()` — Retrieves, but does not remove, the head.
- `E peek()` — Retrieves, but does not remove, the head (or `null` if empty).
- `E poll()` — Retrieves and removes the head (or `null` if empty).
- `E remove()` — Retrieves and removes the head.

#### PriorityQueue (heap representation in Java)
- `boolean offer(E e)` — Inserts the specified element.
- `E peek()` — Retrieves, but does not remove, the head (or `null` if empty).
- `E poll()` — Retrieves and removes the head (or `null` if empty).

#### BlockingQueue
- `add()` internally just calls `offer()` and does nothing extra.

### Map
- `boolean containsKey(Object key)` — Returns true if this map contains a mapping for the specified key.
- `boolean containsValue(Object value)` — Returns true if this map maps one or more keys to the specified value.
- `boolean isEmpty()` — Returns true if this map contains no key-value mappings.
- `int size()` — Returns the number of key-value mappings in this map.
- `Set<K> keySet()` — Returns a Set view of the keys contained in this map.
- `V put(K key, V value)` — Associates the specified value with the specified key.
- `V remove(Object key)` — Removes the mapping for a key if present.

#### HashMap
- `boolean isEmpty()` — Returns true if this map contains no key-value mappings.

#### TreeMap
- Inherits core `Map` methods plus `NavigableMap` operations.


[Collection Interface   ](http://blogs.bgsu.edu/nitinc/2017/02/11/collection/){:
target="_blank"}