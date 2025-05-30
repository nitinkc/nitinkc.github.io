---
title:  "Collectors - Deep Dive"
date:   2022-12-31 05:00:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

[Collectors in Java Streams](https://nitinkc.github.io/java/Collectors-in-Java-Stream/)

![](https://www.youtube.com/watch?v=pGroX3gmeP8)

# `toSet`
Converts a stream into a `Set`, removing duplicate elements.

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 5, 6);
Set<Integer> numberSet = numbers.stream()
    .collect(Collectors.toSet());
```

# `toMap`
Converts a stream into a Map, where you can specify the key and value mapping functions.

**_Create a Map where each string is mapped to its length_**
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

For the next sections the following object structure and values are used

```
EmployeeSimple(name=John, age=20, salary=65000.0, level=C, experience=5)
EmployeeSimple(name=Wayne, age=20, salary=65430.0, level=C, experience=4)
EmployeeSimple(name=Dow, age=30, salary=74445.0, level=B, experience=6)
EmployeeSimple(name=Jane, age=35, salary=76546.0, level=B, experience=5)
EmployeeSimple(name=Don, age=35, salary=90000.0, level=A, experience=10)
EmployeeSimple(name=Wayne, age=20, salary=65430.0, level=C, experience=4)
EmployeeSimple(name=John, age=23, salary=75430.0, level=B, experience=5)
EmployeeSimple(name=John, age=32, salary=85430.0, level=C, experience=12)
EmployeeSimple(name=null, age=null, salary=null, level= , experience=0)
EmployeeSimple(name=null, age=99, salary=85430.0, level=C, experience=12)
EmployeeSimple(name=null, age=35, salary=90000.0, level=A, experience=10)
```

# min, max & minBy maxBy

Min and Max of Streams return **Optional**.

```java
// Max and Min return Optional Integer
OptionalInt max = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .mapToInt(EmployeeSimple::getAge)
        .max();//35
```

With Collectors, the method is minBy and maxBy which returns an Optional of Collector

```java
 // MaxBy and MinBy return Optional of the Object
EmployeeSimple maxBy = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .collect(Collectors.maxBy(
                Comparator.comparing(
                        EmployeeSimple::getAge))).orElse(new EmployeeSimple());
System.out.println(maxBy);//EmployeeSimple(name=Jane, age=35, salary=76546.0, level=B, experience=5)
        
EmployeeSimple minBy = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .collect(Collectors.minBy(Comparator.comparing(EmployeeSimple::getAge)))
        .orElse(new EmployeeSimple());
System.out.println(minBy);//EmployeeSimple(name=John, age=20, salary=65000.0, level=C, experience=5)
```

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

# Joining

```java
List<String> strings = List.of("java", "is", "cool");
String message = String.join(" ", strings);
System.out.println(message);//Java is cool
        
String test = strings.stream()
        .collect(Collectors.joining(","));
System.out.println(test);//java,is,cool
```

# `collectingAndThen`
Apply a finishing transformation to the result of another **collector**.

```java
List<String> strings = Arrays.asList("apple", "banana", "cherry");
// Collects the strings into a Set and then transforms the Set into an unmodifiable Set.
Set<String> immutableSet = strings.stream()
    .collect(Collectors.collectingAndThen(Collectors.toSet(), Collections::unmodifiableSet));
```

`groupingBy` and `mapping`
- Apply a function, and then a collector as a second argument.

`collectingAndThen`
- For scenarios where the requirement is to get the entire object/collector first and then do the map operations, use `collectingAndThen`.

**_Find the name of the person with the max age.**_
```java
// Find the name of the Person with max age
String maxByName = employees.stream()
        .filter(Objects::nonNull).filter(emp -> null != emp.getName()).filter(emp -> null != emp.getAge())
        .collect(
                Collectors.collectingAndThen(
                        Collectors.maxBy(Comparator.comparing(EmployeeSimple::getAge)), // Collector as the first argument
                        emp -> emp.map(EmployeeSimple::getName) // Mapping function as the second argument
                                .orElse("") // maxBy returns an optional so use orElse for default value
                    )
                );
System.out.println(maxByName); // Jane

employees.stream().forEach(System.out::println);
```

**_Group employees by name and count them.**_
```java
Map<String, Integer> byName =
     employeeSimples.stream()
             .filter(Objects::nonNull).filter(emp -> null != emp.getAge()).filter(emp -> null != emp.getName())
             .collect(groupingBy(
                               EmployeeSimple::getName, // First argument of groupingBy, key
                               collectingAndThen( // Collector as second argument of groupingBy
                                       Collectors.counting(), // Collector as first argument of collectingAndThen
                                       Long::intValue // Finisher function as second argument
                               ) // collectingAndThen returns a collector, so it can be further continued
                            )
                    );

System.out.println(byName); // {Wayne=2, Don=1, John=3, Jane=1, Dow=1}
```

# Summary of Java Stream Collectors

1. **Recursive Structure**
- The first argument is a function, and the second is another collection.
  ```java
  Collector(Function, Collector(Function, Collector))
  ```

2. **Single vs Two-Argument groupingBy**
- **Two-Argument groupingBy**: Uses the classifier function and a specified downstream collector.
  ```java
  .collect(Collectors.groupingBy(str -> str.length(), Collectors.toList()));
  ```
- **Single-Argument groupingBy**: Uses the classifier function and defaults to collecting elements into a list.
  ```java
  .collect(Collectors.groupingBy(String::length));//Method Reference
  ```

3. **groupingBy and mapping**
- `groupingBy` and `mapping` take a function as the first argument and a collector as the second argument.
  ```java
  .collect(groupingBy(str -> str.length(), mapping(str -> str.toUpperCase(), toList())));
  ```
  - Key: Length of the string.
  - Value: Result after applying the mapping collector.

4. **collectingAndThen**
- Takes a collector as the first argument and a function as the second argument.
  ```java
  .collect(collectingAndThen(toList(), list -> list.size()));
  ```

5. **teeing**
- Introduced in Java 12 to combine two collectors together.
- Syntax: `teeing(Collector, Collector, operation)`

6. **filtering**
- Takes a predicate as the first argument and a collector as the second argument.
- First applies the predicate, then collects the result.

7. **groupingBy vs partitioningBy**
- `groupingBy` can create multiple groups based on the classification function.
- `partitioningBy` always creates exactly two groups based on the predicate.
- `groupingBy` uses the result of the classification function as keys, which can be any type.
- `partitioningBy` uses Boolean keys (true and false).

8. **Function.identity()**
- Used when the element itself is the key.
  ```java
  .collect(groupingBy(element -> element, counting())); // Equivalent to Function.identity()
  .collect(groupingBy(identity(), counting()));
  ```
9. **Streams vs Collectors**
  1. **map (Streams)**
  - Takes a `Stream<T>` and returns `Stream<R>`.
  - Transforms elements from one type to another.

  2. **mapping (Reduce)**
  - Used for transforming elements in the middle of a reduce operation.

  3. **filter (Streams)**
  - Filters elements in a stream based on a predicate.

  4. **filtering (Reduce)**
  - Filters elements during a reduce operation.

# Summary - Tabular

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

# Do's and Don't Scenarios

* If you have a one-to-one function , use a map to go from `Stream<T>` to `Stream<R>`

```java
List<Integer> numbers = List.of(1,2,3,4);

//one-to-one function
//Stream<T>.map(oneToOneFunction) ==> Stream<R>
 List<Integer> collect = numbers.stream()
      .map(element -> element * 2)//Takes a Stream of <T> and returns a Stream of <R>
      .collect(Collectors.toList());
System.out.println(collect);//[2, 4, 6, 8]
```

* If you have a one-to-many function , use a map to go from `Stream<T>` to `Stream<Collection<R>>`

```java
//one-to-many
//Stream<T>.map(oneToManyFunction) ==> Stream<List<R>>
List<List<Integer>> collect = numbers.stream()
        .map(element -> List.of(element + 1, element - 1))
        .collect(Collectors.toList());
System.out.println(collect);//[[2, 0], [3, 1], [4, 2], [5, 3]]
//use Case : Given a list of employees, give the personal email id and official email id as pair
```

* If you have a one-to-many function , use a flatMap to go from `Stream<T>` to `Stream<R>`

```java
//one-to-many function
//Stream<T>.map(oneToManyFunction) ==> Stream<R> (not Stream of List of R)
List<Integer> numbers = List.of(1,2,3,4);

List<Integer> collect = numbers.stream()
        .flatMap(element -> List.of(element + 1, element - 1).stream())
        .collect(Collectors.toList());
System.out.println(collect);//[2, 0, 3, 1, 4, 2, 5, 3]
```

