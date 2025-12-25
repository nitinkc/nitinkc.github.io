---
categories:
- Java
date: 2025-04-08 02:17:00
tags:
- Collectors
- Streams
- Java 8
- Functional Programming
title: Collectors in Java Streams
---

{% include toc title="Index" %}

[Also Check : Collectors - Deep Dive](https://nitinkc.github.io/java/collectors-deep-dive/)

Collectors (from `java.util.stream.Collectors` package) are used to perform **mutable reduction operations** on the elements of a stream,
transforming them into different data structures or aggregating their values.

# `collect`
- Collect the data into a list using 
  - `.collect(Collectors.toList())` or just `.toList()`
- Pass a **key mapper function** and **value mapper function** to create a map
  - `.collect(Collectors.toMap(Function.identity(), String::length))`
- If data need to be passed to a client, it's a good idea to use unmodifiable collection 
  - `.collect(Collectors.toUnmodifiableList())`
- Returns an immutable list containing only one specified object(singleton) 
  - `Collections.singletonList(s)`
    ```java
        parentDto.setStringList(Collections.singletonList(businessDto.getStringList()));
    ```

# Grouping `groupingBy`
Categorize elements of a stream based on **a classification function**. 
It **returns a Map** where 
- the keys are the result of applying the classification function (takes a function as first parameter), 
- and the values are **lists of items** that match the classification. It's another Collector that can have the values.
  - **The collector can be another operation that returns a collector like filtering, mapping, filtering etc.**

**Single-Argument** groupingBy: Uses the classifier function and defaults to collecting elements into a List.

**Two-Argument** groupingBy: Uses the classifier function and a specified downstream collector to determine how 
the grouped elements are collected.

**_Categorize a list of strings based on their length._**
```java
List<String> strings = Arrays.asList("apple", "banana", "cherry", "date");
// The Map will have the lengths as keys and lists of strings with those lengths as values
Map<Integer, List<String>> categorizedByLength = strings.stream()
        //.collect(Collectors.groupingBy(str -> str.length(), Collectors.toList()));//Two-Argument groupingBy: Uses the classifier function and a specified downstream collector to determine how the grouped elements are collected.
        .collect(Collectors.groupingBy(String::length));//Single-Argument groupingBy: Uses the classifier function and defaults to collecting elements into a List.

System.out.println(categorizedByLength);//{4=[date], 5=[apple], 6=[banana, cherry]}
```

**_Categorize a list of strings based on their length and count the number of strings in each category._**
```java
List<String> strings = Arrays.asList("apple", "banana", "cherry", "date");
Map<Integer, Long> countedByLength = strings.stream()
      .collect(Collectors.groupingBy(String::length, Collectors.counting()));
//    .collect(Collectors.groupingBy(String::length, 
//            Collectors.collectingAndThen(Collectors.mapping(s -> s, Collectors.toList()),
//                    list -> (long) list.size())
//    ));
```

**_Count Frequency of each integer_**
```java
List<Integer> list = Arrays.asList(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);

//Find frequency of all the numbers
Map<Integer,Long> map = list.stream()
     //.collect(groupingBy(element -> element, counting()));// Function.identity() Equivalent to an i in a for loop
       .collect(Collectors.groupingBy(Function.identity(), counting()));//collect takes a COLLECTOR as parameter. any method that returns a collector can be used

System.out.println(map);//{1=3, 2=2, 3=3, 4=2, 5=2, 6=2, 7=1, 8=1}
```

# Partitioning - `partitioningBy`
Split the elements of a stream into **two** groups based on a **predicate**.

`Collectors.partitioningBy` accepts a predicate and returns **a map** 
- with one key for `true` with all the values with true results and 
- another with false results.
- The values are lists of items that match or do not match the predicate

_Partition a list of integers into even and odd numbers._
```java
List<Integer> list = Arrays.asList(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);
Map<Boolean, List<Integer>> collect = list.stream()
        .collect(partitioningBy(number -> number % 2 == 0));
        //.collect(partitioningBy(evenAgedEmpPredicate));//Predicate can be extracted out and can be passed as an argument

System.out.println(collect);//{false=[1, 1, 3, 3, 5, 7, 5, 3, 1], true=[2, 4, 6, 8, 6, 4, 2]}
```
# Filtering
`Collectors.filtering()` takes a predicate as a first argument and another Collector as second argument.

```java
List<Integer> list = List.of(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);
List<Integer> evenNumberList = list.stream()
      .collect(Collectors.filtering(number -> number % 2 == 0, toList()));

System.out.println(evenNumberList);//[2, 4, 6, 8, 6, 4, 2]
```

# Mapping
`Collectors.mapping` takes a function (as first parameter) based on which the
transformation happens and a Collector as second parameter

With the mapping function, use `Stream.of()` or `collections.stream()`

```java
List<Integer> list = List.of(1,2,1,3,3,4,5,6,7,8,6,5,4,3,2,1);

List<Integer> doubleNumberList = list.stream()
        .distinct()//Finds unique elements 
        .collect(Collectors.mapping(number -> number * 2 , Collectors.toList()));
System.out.println(doubleNumberList);//[2, 4, 6, 8, 10, 12, 14, 16]
```

# Flat Mapping
`Collectors.flatMapping` takes a `Stream` as first input and takes `Collector` as second parameter.

The method signatures of map from Stream and flatMap of Collectors looks like below
```java
 <R> Stream<R> flatMap(Function<? super T, ? extends Stream<? extends R>> mapper)
 <R> Stream<R> map    (Function<? super T, ? extends R> mapper)
```
- flatMapping applies the map first and then does the flattening.

```java
List<String> list = List.of("one", "two wings", "three tyres", "four turbo combustion engine");
//Fnd a list of each word separated without space
List<String> collect = list.stream()
        .collect(flatMapping(str -> Stream.of(str.split(" ")), toList()));

System.out.println(collect);//[one, two, wings, three, tyres, four, turbo, combustion, engine]
```

# `counting`
Counts the number of elements in a stream.

```java
import static java.util.stream.Collectors.counting;

List<String> strings = Arrays.asList("apple", "banana", "cherry");
long count = strings.stream()
    .collect(Collectors.counting());
```

# `mapping`
Applies a function to each element of a stream and collects the results using another collector.

```java
List<String> strings = Arrays.asList("apple", "banana", "cherry", "date");
Map<Integer, List<String>> uppercaseByLength = strings.stream()
    .collect(Collectors.groupingBy(String::length, Collectors.mapping(String::toUpperCase, Collectors.toList())));
```

# `joining`
Concatenates the elements of a stream into a single String, with an optional delimiter, prefix, and suffix.
```java
List<String> strings = Arrays.asList("apple", "banana", "cherry");
String joined = strings.stream()
    .collect(Collectors.joining(", "));
```