---
title:  "Concurrent Collections"
date:   2024-08-20 00:17:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# The Need

1. Most of the traditional Collections are not threadsafe
2. Vector, HashTable (All has performace related issues due to primitive
   synchronized method (takes a lock))
   a. SunchronizedList
   b. SynchronizedSet
   c. SynchronizedMap

ConcurrentModification Exception (while one thread operating on a collection,
other thread trying to modify, throws this exception)

# Fail Fast and Fail Safe

Iterator returned by few Collection framework Classes are fail-fast
structural modification -> during iteration throw
ConcurrentModificationException.

Some important classes whose returned iterator is fail-fast >
• ArrayList
• LinkedList
• vector
• HashSet

While, Iterator returned by few Collection framework Classes are fail-safe,
structural modification -> during iteration won’t throw any Exception.
Some important classes whose returned iterator is fail-safe >
• CopyOnWriteArrayList
• CopyOnWriteArraySet
• ConcurrentSkipListSet
