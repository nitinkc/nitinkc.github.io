---
categories: Java
date: 2018-01-24 00:32:00
tags:
- Collections
- Data Structures
- List
title: Java Collection Class
---

{% include toc title="Index" %}

*[Collection API]({{ site.url }}/assets/media/Collections.docx)*.

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

[Collection Interface](http://blogs.bgsu.edu/nitinc/2017/02/11/collection/){:
target="_blank"}