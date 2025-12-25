---
categories: System Design
date: 2024-06-17 11:45:00
tags:
- Distributed Computing
- MapReduce
- Hadoop
- Spark
- Processing
title: Distributed Computations
---

{% include toc title="Index" %}

Comes into being after deploying distributed data storage

# Scatter/Gather

Scatter the data to a lots of individual nodes where its processed and gather
those results back together.

- Data stored locally is the key

Spark :  scatter/Gather rater than map-reduce

Map-reduce

- Hadoop - legacy pattern

Apache Storm : event based processing rather than Batch processing.

# Map reduce

mappers and reducers

```markdown
1. **Map Phase:**

   +------------------------+      +------------------------+
   |        Input Data      | ---> |        Mapper          |
   +------------------------+      +------------------------+
                                  |   (Key, Value) Pairs    |
                                  +------------------------+
                                         |         |
                                         |         |
                                         |         |
                                  +------------------------+
                                  |     Shuffle & Sort      |
                                  +------------------------+
                                         |         |
                                         V         V
                                 +----------+  +----------+
                                 |   Key    |  |   Key    |
                                 | Partition|  | Partition|
                                 +----------+  +----------+
                                         |         |
                                         V         V
                                  +------------------------+
                                  |      Reducer           |
                                  +------------------------+
                                         |         |
                                         V         |
                                  +------------------------+
                                  |      Output Data       |
                                  +------------------------+

2. **Reduce Phase:**

   +------------------------+
   |     Intermediate      |
   |     Key-Value Pairs   |
   +------------------------+
              |
              V
   +------------------------+
   |        Reducer         |
   +------------------------+
   |    (Key, List of Values)|
   +------------------------+
              |
              V
   +------------------------+
   |      Output Data       |
   +------------------------+

```

# Hadoop

Distributed Computing Framework

- map reduce API
- map reduce job management
- HDFS (Hadoop distributed filesystem)
- Enormous eco system
    - hbase, hive, pig, zoo keeper, mahaut, sqoop, flume

## HDFS

- files & directories
- metadata management by a replicated master
- files stored in large, immutable, replicated blocks