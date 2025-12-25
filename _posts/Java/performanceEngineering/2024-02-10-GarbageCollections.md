---
categories:
- Java
- Performance Engineering
date: 2024-02-11 00:12:00
tags:
- Garbage Collection
- Java
title: Garbage Collections
---

{% include toc title="Index" %}

Garbage collection - concept with Lisp since 1959!!

Garbage collection is the automatic process to free up the memory.

- Java is a "managed Language". Java works out when objects are no longer needed
  and marks them for GC.

Any object **on the heap** which cannot be reached through a reference from *
*the stack or from the metaspace** is **"Eligible for Garbage Collection"**
{: .notice--primary}

Stack dies after the call block or the method block is over

Meta space is never garbage collected as it holds Static primitives or the
reference to static objects.

# The System.gc() method

**Suggestion** to run the Garbage collection process and **not a command**

**Not a good idea** to call and let JVM Decide when it's right. So, **DO NOT**
use.

# The finalize() method

The finalize() method of an object is called by the Garbage Collector before it
removes the object from memory
(when there are no references to that object).

Deprecated since Java 9. This method runs when the object is eligible for GC

But like GC, you will never know when it is going to run or if it will run as
per the intention

# Mark & Sweep Algorithm

- The programs execution is first paused. "**Stop The World**" event for marking
- Pauses all the threads, looks at each thread's Stack and the variables being
  referenced (recursively).
- Removed un referenced objects
- Moves the objects (that are being kept) into a single contiguous block of
  memory, Avoiding fragmentation.

# Generational Garbage Collection

[Check Java Memory](https://nitinkc.github.io/java/performance%20engineering/JavaMemory/)

Heap is divided into 2 spaces

- young and
- old generation space

New objects are created in young generation

Young generation (much smaller than the old, but can be tuned) has 3 spaces

- Eden
- S0 (Survivor 0 Space)
- S1 (Survivor 1 Space)

##### Island of isolation

**Eden Space** --> When an instance is created, stored in Eden Space (Young
generation of heap memory area)

**Survivor space** --> after Minor GC (Obj. live and referenced)

### Minor Collection

**GC of the Young Generation Space**

New objects are created in Young generation space. When its full, the GC runs
only in the Young generation space

The idea here is that the majority of the objects don't survive for long, so the
young generation which is full of **new objects** are probably mostly garbage.

The GC process, then, should be quick in Young generation space.

Any Surviving objects are then moved to the old generation, thus making up space
for the new objects in the Young generation

# Eden, S0 & S1

S0 and S1 are called the survivor spaces

When an object is created, it's placed in the eden space

When the Eden space gets full, which happens quickly because it's small, then
the
garbage collection process will **take place on the Eden space** and any
surviving objects are moved into S0.

Our application then continues running and new objects continue getting created
in the Eden space

The **next time** that the garbage collection process runs, the marking process
looks at everything in
the **Eden space and in S0** and any objects that survive get moved into **S1**.

More objects are created and Eden gets full again and the garbage collection
process takes all those
that survive. But this time it looks **at Eden and S1** and it moves any
surviving objects into S0.

So S0 and S1 are two parts of the young generation that are **used to swap the
surviving objects**.

Lots of GC which is quick and on a smaller memory footprint because only eden
and one of the Survivors are involved.

After a number of these swaps, the object is determined to be a long surviving
object and will be moved

So the threshold for the swaps (how many generations an object needs to survive)
is **configurable**.

### Major Collection

Runs only when its needed, i.e, when it gets full. It is Heavy process

The Visual GC Plugin of Visual VM
![visualvm-plugin.png](/assets/images/visualvm-plugin.png)
Heap Spaces as shown in the Visual VM for a running process
![gc-spaces.png](/assets/images/gc-spaces.png)
GC Activity for OOM
![GC_OOM.png](/assets/images/GC_OOM.png)

# Jshell

Pass in the PID for the running Java progam along with the flag to know its
current settings. To find the process id for the java program run `jps`

```shell
❯ jps
❯ jinfo -flag NewRatio 46615
-XX:NewRatio=2

❯ jinfo -flag SurvivorRatio 46615
-XX:SurvivorRatio=8
```

# Monitoring Garbage Collections

Spits out the garbage collection logs on console
`-Xmx10m -verbose:gc`

```
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

# Tuning Garbage Collections

Turned on by default for most JVM's. It dynamically adapts the size of the S0 &
S1 space during runtime.
`-XX:-UseAdaptiveSizePolicy`

Minimize the full GC

- **New Ratio** : resizing the different part of the heap (allow more for young
  gen and less for old)
    - `-XX:NewRatio=n` - how many times should the old generation be in
      camparson to young gen
    - Find the default value for NewRatio
    - ```shell
    ❯ jinfo -flag NewRatio 46615
    -XX:NewRatio=2
    ```
- **Survivor ratio** - how much of the young generation should be taken up by
  the survivor spaces S0 and S1.
    - `-XX:SurvivorRatio=n`
    - Virtual machine can anyway resize it dynamically if it thinks some
      optimization is needed
- **Max Tenuring Threshold** : how many generations should an object survive
  before it becomes part of the old generation
    - `-XX:MaxTenuringThreshold=n`
    - 15 is the max value

# Selecting a Minor Garbage Collector Algo

The virtual machine then has **three** types of collector algo called

- The serial collector uses a single thread to perform all the garbage
  collection work.
    - Single Threaded `-XX:+UseSerialGC`
- Parallel - `-XX:+UseParallelGC`
- Mostly Concurrent garbage collector.
    - Mark Sweep Collector - General Algorithm that GC uses-
      `-XX:+UseConcMarkSweepGC`
    - G1 Garbage Collector - default java 10 onwards
        - `-XX:+UseG1GC`
        - Tuning G1GC
        - specify the number of concurrent threads available for the smaller
          regional collections.`-XX:ConcGCThreads=n`
        - the GC process starts when the heap reaches a certain level of
          fullness. By default, this is 45%. G1 runs whenever the entire heap
          gets to 45% full.
        - you can change this figure from the 45% default by using this flag.
          `-XX:InitiatingHeapOccupancyPercent=n`

# String Deduplication - G1 Garbage Collector

it allows the garbage collector to make more space if it finds duplicate strings
in the heap.

`-XX:UseStringDeDuplication`