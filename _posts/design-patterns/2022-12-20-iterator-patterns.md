---
title:  "Iterator As a Design Pattern"
date:   2023-11-06 08:30:00
categories: ['Java','Design Patterns']
tags: ['Java']
---
{% include toc title="Index" %}


break & limit of Imperative style coding

```java
/* LIMIT */
 int limit = 3;
int counter = 0;

while (counter < limit) {
    counter++; // Increment the counter to limit the number of iterations.
}

/* BREAK */
for (int i = 0; i < 10; i++) {
    if (i == 5) {
        break; // This will exit the loop when i is 5.
    }
}
```

`limit` and `takeWhile` are the functional equivalent of `break` from the imperative style.
```java
 List<Integer> numbers = Stream.iterate(1, n -> n + 1)
                .takeWhile(n -> n <= 10) // Take elements while the condition is true (less than or equal to 10).
                .limit(5) // Limit the stream to the first 5 elements.
                .toList();
```

# Shared Mutability
**Impurity in Functional Programming** : The given functional pipeline is *not* pure due to shared mutability.

The result may be unpredictable if we ever **change** this code to run in **parallel** by adding 
`.parallel()` or by changing `.stream()` to `.parallelStream()`

```java
var ret = new ArrayList<String>();

// Code behaves - erratically with parallel Stream
list.parallelStream()
        .filter(Objects::nonNull)
        .filter(name -> name.length() > 4)
        .map(nameInLowerCase -> nameInLowerCase.toUpperCase())
        .limit(count)
        .forEach(name -> ret.add(name));//BAD IDEA with ParallelStream - due to shared mutability - this is impure
```

Change the above code to use `collect(Collectors.toList())` to collect the list
```java
var ret = list.parallelStream()
            .filter(Objects::nonNull)
            .filter(name -> name.length() > 4)
            .map(nameInLowerCase -> nameInLowerCase.toUpperCase())
            .limit(count)
            .collect(Collectors.toList());
```

Also, we should not use impure functions in the intermediate stages

```java
//Really frustrating to replicate and unpredictable
var result2 = new ArrayList<String>();
names.stream()
    .filter(name -> name.length() == 4)
    //.map(name -> performImpureOperation(name)) //AVOID + DANGEROUS
    .map(String::toUpperCase)
    //.forEach(name -> result2.add(name)); //BAD IDEA with ParallelStream
    .collect(Collectors.toList()); //to List is a better option
```

Functional pipeline offers internal iterators
* is less complex
* easy to modify
* easy to understand

**BUT**

* Avoid **shared mutable** variables
* Ensure that we make the functional pipeline pure

# What is a pure function:
[functional-programming/#pure-function]({% post_url /Java/2022-08-06-functional-programming %})
