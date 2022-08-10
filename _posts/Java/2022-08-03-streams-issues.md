---
title:  "Java Streams"
date:   2022-08-03 18:16:00
categories: ['Java']
tags: ['Java']
---

# Java Streams

* A stream in Java is a sequence of data that takes input from Collections or IO Channels
* Streams **don’t change** the original data structure.
* A Stream Pileline is the operation (STREAM OPERATIONS) that run on a stream to produce a result
* Each intermediate operation is lazily executed and returns a stream as a result.
* Terminal operations mark the end of the stream and return the result.
* Finite Streams have a limit
* infinite Streams are like sunrise/sunset cycle

## Stream Operations

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

## Object Creation & Assignment In Streams

Object Assignment using traditional for loop VS in Streams.Notice in Streams, instead of individually assigning object to each element of Arraylist, an entire collection is assigned

{% gist nitinkc/3bc7cde3d5c123c3fdec9d96a56dbd9f %}


### Wrong Expectation for Streams to work

In case of applying operations on Stream, it is necessasary to assign the result of the stream back to the collection.

For example, if the class Person has persontFullName as the property
```java
@Getter @Setter @AllArgsConstructor @NoArgsConstructor @ToString
class Person {
    private String personFullName; //Last ,First,Mid
}
```

and if a list of persons needs to be sorted in natural order, the return list will not be sorted this way :-
```java
listOfPersons.stream()
    .sorted(Comparator.comparing(Person::getPersontFullName,Comparator.nullsLast(Comparator.naturalOrder())));

return listOfPersons;
```

the code needs to be refactored like 
```java
listOfPersons = listOfPersons.stream()
    .sorted(Comparator.comparing(Person::getPersontFullName,Comparator.nullsLast(Comparator.naturalOrder())))
    .collect(Collectors.toList());

return listOfPersons;
```
or simply like below, without using streams at all. The sorted method of collections takes care of sorting the list itself.
```java
listOfPersons
    .sort(Comparator.comparing(Person::getPersontFullName,Comparator.nullsLast(Comparator.naturalOrder())));

return listOfPersons;
```

or use Collections sort method
```java
Collections.sort(listOfPersons, Comparator.comparing(Person::getPersontFullName,Comparator.nullsLast(Comparator.naturalOrder())));
```

### Parallel Stream issues 

The behavoiur of list.parallelStream() or list.stream().parallel() is unpredictable in certain scenarios.

{% gist nitinkc/c34b3f61fff2fe68f9d00b2ae95f635e %}

