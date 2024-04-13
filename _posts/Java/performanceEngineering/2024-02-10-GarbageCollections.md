---
title:  "Garbage Collections"
date:   2024-02-11 00:12:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

Garbage collection is the process to free up the memory.

Garbage collection - concept with Lisp in 1959!!

Java is a "managed Language". Java works out when objects are no longer needed and marks them for GC.

Any object on the heap which cannot be reached through a reference 
from **the stack or from the metaspace** is **"Eligible for Garbage Collection"**

# The System.gc() method

**Suggestion** to run the Garbage collection process and **not a command**

Not a good idea to call and let JVM Decide when it's right.


# Generational Garbage Collection 

[Check Java Memory](https://nitinkc.github.io/java/JavaMemory/)

Heap is divided into young and old generation space

New objects are created in young generation

Young generation has 3 spaces
* Eden
* S0 - Survivor 0
* S1 - Survivor 1

The Visual GC Plugin of Visual VM
![visualvm-plugin.png](..%2F..%2Fassets%2Fimages%2Fvisualvm-plugin.png)

Heap Spaces as shwon in the Visual VM for a running process
![gc-spaces.png](..%2F..%2Fassets%2Fimages%2Fgc-spaces.png)

# Monitoring Garbage Collections

`-verbose:gc`

`-XX:-UseAdaptiveSizePolicy`

`-XX:SurvivorRatio=n`

`-XX:MaxTenuringThreshold=n`

```log
[0.008s][info][gc] Using G1
[0.216s][info][gc] GC(0) Pause Young (Normal) (G1 Evacuation Pause) 25M->17M(516M) 10.468ms
[0.329s][info][gc] GC(1) Pause Young (Normal) (G1 Evacuation Pause) 45M->39M(516M) 12.175ms
[0.263s][info][gc] GC(19) Concurrent Mark Cycle 41.388ms
[0.265s][info][gc] GC(21) Pause Young (Normal) (G1 Evacuation Pause) 9M->9M(10M) 0.353ms
[0.268s][info][gc] GC(22) Pause Full (G1 Compaction Pause) 9M->1M(8M) 3.152ms
[0.222s][info][gc] GC(17) Pause Young (Concurrent Start) (G1 Evacuation Pause) 9M->9M(10M) 0.467ms
[0.222s][info][gc] GC(19) Concurrent Mark Cycle
[0.240s][info][gc] GC(18) Pause Full (G1 Compaction Pause) 9M->9M(10M) 18.397ms

```


```shell
❯ jinfo -flag NewRatio 46615
-XX:NewRatio=2

❯ jinfo -flag SurvivorRatio 46615
-XX:SurvivorRatio=8
```

# Selecting a Garbage Collector Algo

The virtual machine then has **three** types of collector algo called 

Serial - Single Threaded `-XX:+UseSerialGC` <br>
Parallel - `-XX:+UseParallelGC` <br>
Mostly Concurrent garbage collector.
* Mark Sweep Collector - `-XX:+UseConcMarkSweepGC`
* G1 Garbage Collector - 
  * `-XX:+UseG1GC` `-XX:ConcGCThreads=n`
  * `-XX:InitiatingHeapOccupancyPercent=n`

# G1 Garbage Collector

String Deduplication

`-XX:UseStringDeDuplication`

The serial collector uses a single thread to perform all the garbage collection work.

