---
title:  "Iterator As a Design Pattern"
date:   2023-11-06 08:30:00
categories: ['Java','Design Patterns']
tags: ['Java']
---
{% include toc title="Index" %}


break & limit of Impertive style coding

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

limit and takeWhile are the functional equivalent of break from the imperative style.
```java
 List<Integer> numbers = Stream.iterate(1, n -> n + 1)
                .takeWhile(n -> n <= 10) // Take elements while the condition is true (less than or equal to 10).
                .limit(5) // Limit the stream to the first 5 elements.
                .collect(Collectors.toList());

```


# Shared Mutability

Impurity in Functional Programming : The given functional pipeline is *not* pure. We are doing shared mutability.

The result may be unpredictable if we ever **change** this code to run in **parallel** by adding .parallel() or by changing .stream() to .parallelStream()

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

A pure function is idempotent : Returns the same result for the same input (Immutability)
and does not have any side-effects

##### Rules :
1. It does not change any state that is visible outside
2. It does not **depend** on anything outside that may change

##### Why ??
Functional programming relies on lazy evaluation for efficiency.

Lazy evaluation and parallel execution rely on
**immutability** and **purity** of functions for correctness.

FP emphasizes immutability and purity, not because
but because it is essential to it's survival/efficiency.