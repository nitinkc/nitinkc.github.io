---
title:  "Collectors in Java Streams"
date:   2025-04-08 02:17:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# Recursive Structure
Collector(Function, Collector(Function, Collector))

[Collectors - Deep Dive]()
Collectors (from `java.util.stream.Collectors` package) are used to perform **mutable reduction operations** on the elements of a stream,
transforming them into different data structures or aggregating their values.

| Function           | Return Type             | Summary                                                                             | Important Details                                                              |
|:-------------------|:------------------------|:------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------|
| `groupingBy`       | `Map<K, List<T>>`       | Groups elements by a classifier function.                                           | Can be combined with downstream collectors for more complex groupings.         |
| `partitioningBy`   | `Map<Boolean, List<T>>` | Partitions elements into two groups based on a predicate.                           | Returns a map with Boolean keys (`true` and `false`).                          |
| `counting`         | `Long`                  | Counts the number of elements.                                                      | Simple and efficient way to get the count of elements.                         |
| `mapping`          | `Collector<T, A, R>`    | Applies a mapping function to elements before collecting.                           | Useful for transforming elements before collecting them.                       |
| `joining`          | `String`                | Concatenates elements into a single `String`.                                       | Can specify a delimiter, prefix, and suffix.                                   |
| `counting`         | `Long`                  | Counts the number of elements.                                                      | Simple and efficient way to get the count of elements.                         |
| `mapping`          | `Collector<T, A, R>`    | Applies a mapping function to elements before collecting.                           | Useful for transforming elements before collecting them.                       |
| `flatMapping`      | `Collector<T, ?, R>`    | Flattens a stream of collections into a single collection.                          | Useful for flattening nested collections before collecting them.               |
| `joining`          | `String`                | Concatenates elements into a single `String`.                                       | Can specify a delimiter, prefix, and suffix.                                   |
| `collectingAndThen`| `R`                     | Applies a finishing transformation to the result of another collector.              | Useful for performing a final transformation on the collected result.          |
| `toSet`            | `Set<T>`                | Collects elements into a `Set`.                                                     | Ensures no duplicate elements.                                                 |
| `toMap`            | `Map<K, V>`             | Collects elements into a `Map` using key and value mapping functions.               | Requires handling of duplicate keys (e.g., using merge functions).             |
| `summingInt`       | `Integer`               | Sums the integer values of elements.                                                | Often used with `mapToInt` to convert elements to integers before summing.     |
| `teeing`           | `Collector<T, ?, R>`    | Combines two collectors and merges their results.                                   | Useful for performing two independent collections and combining their results. |
| `reducing`         | `Optional<T>` or `T`    | Performs a reduction on the elements using an associative accumulation function.    | Can be used to produce a single result from a stream of elements.              |
| `summarizingInt`   | `IntSummaryStatistics`  | Collects statistics, such as count, sum, min, average, and max, for integer values. | Provides a comprehensive summary of integer values.                            |
| `maxBy`            | `Optional<T>`           | Finds the maximum element according to a comparator.                                | Returns an `Optional` containing the maximum element, if any.                  |
| `minBy`            | `Optional<T>`           | Finds the minimum element according to a comparator.                                | Returns an `Optional` containing the minimum element, if any.                  |

## Streams vs Collectors

| Concept        | Context        | Description                                                                    |
|:---------------|:---------------|:-------------------------------------------------------------------------------|
| `map`          | Streams        | Takes a `Stream<T>` returns `Stream<R>`. Transforms from one style to another. |
| `mapping`      | Reduce         | Transforming in the middle of a reduce.                                        |
| `filter`       | Streams        | Filtering elements.                                                            |
| `filtering`    | Reduce         | Filtering elements during a reduce operation.                                  |

## Nuances
- groupingBy can **create multiple groups** based on the classification function, while partitioningBy always creates exactly **two groups** based on the predicate.
- groupingBy uses the **_result of the classification function as keys_**, which can be any type, whereas partitioningBy uses **Boolean keys** (true and false).
- Teeing -> Java 12 -  to combine 2 collectors together
- teeing(Collector, Collector, operation)
- groupingBy and mapping (apply a Function, and then Collector as a second argument)
- collectingAndThen(Collection, then use a Function as a second argument)

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

# `toSet`
Converts a stream into a `Set`, removing duplicate elements.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 5, 6);
Set<Integer> numberSet = numbers.stream()
    .collect(Collectors.toSet());
```

# `toMap`
Converts a stream into a Map, where you can specify the key and value mapping functions.

_Create a Map where each string is mapped to its length_
```java
List<String> strings = Arrays.asList("apple", "banana", "cherry");
Map<String, Integer> stringLengthMap = strings.stream()
    .collect(Collectors.toMap(Function.identity(), String::length));
```

# `summingInt`
Performs a reduction operation on the elements of a stream, summing the results of applying a function to the elements.
```java
List<String> strings = Arrays.asList("apple", "banana", "cherry");
int totalLength = strings.stream()
    .collect(Collectors.summingInt(String::length));
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
# `collectingAndThen`
Apply a finishing transformation to the result of another **collector**.
```java
List<String> strings = Arrays.asList("apple", "banana", "cherry");
//collects the strings into a Set and then transforms the Set into an unmodifiable Set.
Set<String> immutableSet = strings.stream()
    .collect(Collectors.collectingAndThen(Collectors.toSet(), Collections::unmodifiableSet));
```
- `groupingBy` and `mapping` (apply a Function, and then Collector as a second argument)
- `collectingAndThen`      (Collection, then use a Function as a second argument)

# `teeing`
Combines the results of two independent collectors into a single result.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
double average = numbers.stream()
    .collect(Collectors.teeing(
        Collectors.summingDouble(Integer::doubleValue),
        Collectors.counting(),
        (sum, count) -> sum / count
    ));
```