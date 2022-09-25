---
title:  "Java Stream Issues"
date:   2022-08-03 18:16:00
categories: ['Java']
tags: ['Java']
---



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

