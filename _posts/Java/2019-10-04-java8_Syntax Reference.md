---
title:  "Java 8 Syntax Reference"
date:   2019-10-04 13:43:00
categories: ['Java']
tags: ['Java']
---

##### For each method **applies the lambda** to each element of the collection

```java
//Prints each element
list.stream()
    .forEach(str -> System.out.println(str));

//Where ever Lambda is there it can be replaced by method reference
list.stream()
    .forEach(System.out :: print);
```

## Double Colon Operator

| S.no| Kind                                                  | Example                              |
|---- |-------------------------------------------------------|--------------------------------------+
| 1  | Reference to a static method                          | ContainingClass::staticMethodName  |
| 2  |Reference to an instance method of a particular object | containingObject::instanceMethodName |
| 3  | Reference to an instance method of an arbitrary object of a particular type | ContainingType::methodName           |
| 4  |Reference to a constructor                             | ClassName::new                       |

## Predefined Functional Interface

Defined in java.util.function

1. Predicate (test(), returns boolean) - Used with filter() in Stream API
2. Function (apply(T k), return user defined TYPE) - Used with map() in Stream API
3. Consumer (accept()), - Used with forEach() method
4. Supplier (get()),

### Predicate 

`java.util.function.Predicate`, represents a simple function that takes a single value as parameter, and returns true or false.

/**Predicate uses a Lambda that returns true and false**

Commonly used with Filters. 

Here is how the Function interface definition looks:

```java
public interface Predicate<T> {
    boolean test(T t);
}
```

{% gist nitinkc/b63f8cbb3d13cab6ba1fb5256d748d6f %}


### Function 

Commonly used with streams.map()

The Function interface represents a function (method) that **takes a single parameter and returns a single value**. Here is how the Function interface definition looks:

function is used in map() function

```java
public interface Function<T, R> {
    R apply(T t);
}
```

Write Lambda in such a way that it **accepts an argument and performs an action** on it

{% gist nitinkc/bed9ceea341088f49355f8422958d04a %}


### BiFunction

```java
public interface BiFunction<T, U, R> {
     R apply(T t, U u);
     ...
}
```
higher-order functions. Two common examples are filter and map.

A filter processes a list in some order to produce a new list containing exactly those elements of the original list for which a given predicate (think Boolean expression) returns true.

A map applies a given function to each element of a list, returning a list of results in the same order.

Another common higher-order function is reduce, which is more commonly known as a fold. This function reduces a list to a single value.


### Higher-order functions. 
Methods that Return Functions

Two common examples are filter and map.

##### Sorting a list

{% gist nitinkc/d55b4541f27fc0bfd86f122d35c2b527 %}

##### Sorting a set

{% gist nitinkc/61476aad3b16d3c29e843553788e640b %}

### Consumer : (used with forEach) takes generified argument and returns nothing

It is a function that is representing side effects
```java
public interface Consumer<T> {
    void accept(T t);
}

List<String> strList = Arrays.asList("test","this","is","a","test","this","test","is","not","complex");

Consumer<String> c = s -> System.out.print(s + " ,");
//Consumer<String> c = System.out::println;
strList.stream().forEach(c);
```

BiConsumer example. Using BiConsumer to insert values into hashmap.

{% gist nitinkc/f0cdad5af384796e2c5684cb6e5cdc34 %}

Parenthesis Checker using Consumer
{% gist nitinkc/ff63f3c1d164ef3b8dfe3a91a02e3259 %}

### Supplier
```java
public interface Supplier<T> {
    T get();
}


//Static method Reference
Supplier<LocalDate> s1 = LocalDate::now;
//Lambda Expression
Supplier<LocalDate> s2 = () -> LocalDate.now();

```

# Java Streams

* A stream in Java is a sequence of data that takes input from Collections or IO Channels
* Streams **don’t change** the original data structure.
* A Stream Pileline is the operation (STREAM OPERATIONS) that run on a stream to produce a result
* Each intermediate operation is lazily executed and returns a stream as a result.
* Terminal operations mark the end of the stream and return the result.
* Finite Streams have a limit
* infinite Streams are like sunrise/sunset cycle

Stream Operations

* **SOURCE** : Where the stream comes from
* **INTERMEDIATE OPERATIONS** : Transforms the stream into another stream. STREAMS USE LAZY EVALUATION.
  * **map**: The map method is used to returns a stream consisting of the results of applying the given function to the elements of this stream.
  * **filter**: The filter method is used to select elements as per the Predicate passed as argument.
  * **sorted**: The sorted method is used to sort the stream.
* **The intermediate operations do not run until the terminal operation runs.**
* **TERMINAL OPERATION**: Actually produces a result. Stream becomes invalid after terminal operation
  * **collect**: The collect method is used to return the result of the intermediate operations performed on the stream.
  * **forEach**: The forEach method is used to iterate through every element of the stream.
  * **reduce**: The reduce method is used to reduce the elements of a stream to a single value. The reduce method takes a BinaryOperator as a parameter.

### Non-Terminal Operations
filter()
map()
flatMap()
distinct()
limit()
peek()

### Terminal Operations
anyMatch()
allMatch()
noneMatch()
collect()
count()
findAny()
findFirst() - returns Optional
forEach()
min()
max()
reduce()
toArray()

# Optional

* New class Optional in java.util package.
* It is a Container to hold at most one value, like Collections and Arrays.
* To represent a value if its present or absent.
* Avoids any runtime NullPointerExceptions

In Streams API, Optional is returned


## Object Creation & Assignment In Streams

Object Assignment using traditional for loop VS in Streams.Notice in Streams, instead of individually assigning object to each element of Arraylist, an entire collection is assigned

{% gist nitinkc/3bc7cde3d5c123c3fdec9d96a56dbd9f %}