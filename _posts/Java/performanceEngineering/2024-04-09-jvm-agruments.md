---
title:  "JVM Arguments"
date:   2024-04-09 12:30:00
categories: ['Java',"Performance Engineering"]
tags: ['Java',"Performance Engineering"]
---
{% include toc title="Index" %}

* -XX means it's an advanced option
* a plus or a minus indicates the option to be switched on or off
* and then the option name in `SentenceCase`

# Jshell
Pass in the PID for the running Java progam along with the flag to know its current settings. To find the process id for the java program run `jps`
```shell
❯ jps
❯ jinfo -flag NewRatio 46615
-XX:NewRatio=2

❯ jinfo -flag SurvivorRatio 46615
-XX:SurvivorRatio=8
```

# Compilation

`-XX:+PrintCompilation` : see the output on console

`-XX:-TieredCompilation` : Turn off the Tiered Compilation

Get all the possible flags/options
```shell
java -XX:+PrintFlagsFinal
```
Check the following flags
`CICompilerCount` -  how many threads are available to run the compiling process

`CompileThreshold` - the number of times a method/code needs to run before it is natively compiled

# Diagnostic and Troubleshooting
`-XX:+UnlockDiagnosticVMOptions`: Unlocks diagnostic VM options for troubleshooting.

`-XX:+HeapDumpOnOutOfMemoryError`: Generates heap dump on OutOfMemoryError.

`-XX:HeapDumpPath=<path>`: Specifies heap dump file path where it needs to be saved.

`-XX:+UnlockDiagnosticVMOptions -XX:+LogCompilation` : creates a log file like `hotspot_pid1234.log`

# String Pool Management
`XX:+PrintStringTableStatistics` : Prints statistics about the String pool.

`XX:StringTableSize=120121`: Sets the size of the String table at the beginning of the JVM start


# Heap Management
`-XX:MaxHeapSize=1g` or `-Xmx1g`: Sets maximum heap size.

`-XX:InitialHeapSize=4g` or `-Xms4g`: Sets initial heap size.

`-Xss` for stack


# Garbage Collections

`-Xmx10m -verbose:gc` : Spits out the garbage collection logs on console

`-XX:-UseAdaptiveSizePolicy` : Turned on by default for most JVM's. It dynamically adapts the size of the S0 & S1 space during runtime.

`-XX:NewRatio=n` : how many times should the old generation be in camparson to young gen

`-XX:SurvivorRatio=n` : how much of the young generation should be taken up by the survivor spaces S0 and S1.

`-XX:MaxTenuringThreshold=n` : how many generations should an object survive before it becomes part of the old generation

`-XX:+UseSerialGC` : Single Threaded GC Algo

`-XX:+UseParallelGC` : Parallel

`-XX:+UseConcMarkSweepGC` : Mark Sweep Collector - General Algorithm that GC uses

`-XX:+UseG1GC` : G1 Garbage Collector - default java 10 onwards

`-XX:ConcGCThreads=n` : with G1GC : specify the number of concurrent threads available for the smaller regional collections.

`-XX:InitiatingHeapOccupancyPercent=n` : G1 runs whenever the entire heap gets to 45% full. Change this from the 45% default by using this flag. 

`-XX:UseStringDeDuplication` : G1 Garbage Collector - Allows GC to make more space if it finds duplicate strings in the heap.




