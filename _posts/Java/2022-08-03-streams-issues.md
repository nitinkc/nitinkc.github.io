---
title:  "Java Streams Nuances"
date:   2022-08-03 18:16:00
categories: ['Java']
tags: ['Java']
---


### Wrong Expectation for Streams to work

In case of applying operations on Stream, it is necessasary to assign the result of the stream back to the collection.

For example, of the class Person has persontFullName as the property
```java
@Getter @Setter @AllArgsConstructor @NoArgsConstructor @ToString
class Person {
    private String personFullName; //Last ,First,Mid
}
```

and if a list of persons needs to be sorted in natural order like this, the return list will not be sorted.
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


### 

