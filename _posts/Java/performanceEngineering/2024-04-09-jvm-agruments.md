---
categories:
- Performance Engineering
date: 2024-04-09 12:30:00
tags:
- Java
- JVM
- Configuration
- Performance
title: JVM Arguments
---

{% include toc title="Index" %}

* -XX means it's an advanced option
* a plus or a minus indicates the option to be switched on or off
* and then the option name in `SentenceCase`

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

**Get all the possible flags/options**
`-XX:+PrintFlagsFinal` :

```shell
java -XX:+PrintFlagsFinal
```

Check the following flags
`CICompilerCount` - how many threads are available to run the compiling process

`CompileThreshold` - the number of times a method/code needs to run before it is
natively compiled

# Compilation

`-XX:+PrintCompilation` - provides insight into the compilation process of
methods by the JVM, including information about their optimization levels and
status

`-XX:-TieredCompilation`: This option disables tiered compilation, meaning that
only the C2 compiler will be used.

`-client`: This option instructs the JVM to use the client compiler (C1) as the
default compiler. Prevent's C2 compiler to kick in if needed.

`-server`: This option instructs the JVM to use the server compiler (C2) as the
default compiler.

`-d64`: This option specifies that the JVM should run in 64-bit mode, utilizing
the larger address space available on 64-bit architectures.

`-XX:CICompilerCount=n`

`-XX:CompileThreshold=n`

`-XX:+PrintCodeCache` : If the code cache is full, the warning message is
`code cache is full, compiler has been disabled.`

`InitialCodeCacheSize` is the size of the code cache when the application
starts.
The default size varies based on available memory, but it's often around about
160kB.

`-XX:ReservedCodeCacheSize=150M` : is the maximum size of the code cache. In
other words, the code cache can grow over time
**up to the size** of the reserved code cache.

`CodeCacheExpansionSize` dictates how quickly the code cache should grow as it
gets full. How much extra space should be
added each time the code cache is grown

# Diagnostic and Troubleshooting

`-XX:+UnlockDiagnosticVMOptions`: Unlocks diagnostic VM options for
troubleshooting.

`-XX:+HeapDumpOnOutOfMemoryError`: Generates heap dump on OutOfMemoryError.

`-XX:HeapDumpPath=<path>`: Specifies heap dump file path where it needs to be
saved.

`-XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation` : creates a log file like
`hotspot_pid1234.log`

# String Pool Management

`XX:+PrintStringTableStatistics` : Prints statistics about the String pool.

`XX:StringTableSize=120121`: Sets the size of the String table at the beginning
of the JVM start

# Heap Management

`-XX:MaxHeapSize=1g` or `-Xmx1g`: Sets maximum heap size.

`-XX:InitialHeapSize=4g` or `-Xms4g`: Sets initial heap size.

`-Xss` for stack

`-XX:+HeapDumpOnOutOfMemoryError`

`-XX:HeapDumpPath=<>`

# Garbage Collections

`-Xmx10m -verbose:gc` : Spits out the garbage collection logs on console

`-XX:-UseAdaptiveSizePolicy` : Turned on by default for most JVM's. It
dynamically adapts the size of the S0 & S1 space during runtime.

`-XX:NewRatio=n` : how many times should the old generation be in camparson to
young gen

`-XX:SurvivorRatio=n` : how much of the young generation should be taken up by
the survivor spaces S0 and S1.

`-XX:MaxTenuringThreshold=n` : how many generations should an object survive
before it becomes part of the old generation

`-XX:+UseSerialGC` : Single Threaded GC Algo

`-XX:+UseParallelGC` : Parallel

`-XX:+UseConcMarkSweepGC` : Mark Sweep Collector - General Algorithm that GC
uses

`-XX:+UseG1GC` : G1 Garbage Collector - default java 10 onwards

`-XX:ConcGCThreads=n` : with G1GC : specify the number of concurrent threads
available for the smaller regional collections.

`-XX:InitiatingHeapOccupancyPercent=n` : G1 runs whenever the entire heap gets
to 45% full. Change this from the 45% default by using this flag.

`-XX:UseStringDeDuplication` : G1 Garbage Collector - Allows GC to make more
space if it finds duplicate strings in the heap.