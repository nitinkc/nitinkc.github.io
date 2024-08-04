---
title:  "String Intern pool, Hashmaps and Collections"
date:   2024-07-03 00:10:00
categories: ['Java',"Performance Engineering"]
tags: ['Java',"Performance Engineering"]
---
{% include toc title="Index" %}


# The String Pool $ string deduplication.

Since Java 8, Spring pools libe in Heap.


The virtual machine can actually detect the duplicated strings and it will remove one of them 
and make the two variables point to the same underlying reference.

Explicitly specifying a string to be placed in string pool
```java
String x = 100.toString().intern();
String y = "100";
//x.equals(y);//True
```

String Pool is internally saved in a HashMap. The String is hashed and kept in the respective HashMap. If 2 strings 
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