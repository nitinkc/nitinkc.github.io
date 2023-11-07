---
title:  "Iterator As a Design Pattern"
date:   2023-11-06 08:30:00
categories: ['Java','Design Patterns']
tags: ['Java']
---


//break -> limit

//limit and takeWhile are the functional equivalent of break from the imperative style.

limit and takeWhile are the functional equivalent of break from the imperative style.


The functional pipeline is *not* pure. We are doing shared mutability


The functional pipeline is *not* pure. We are doing shared mutability
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

The result may be unpredicatable if we
ever **change** this code to run in **parallel** by adding .parallel() or
by changing .stream() to .parallelStream()

```java
//Really frustrating to replicate and unpredictable


var result2 = new ArrayList<String>();
names.stream()
        .filter(name -> name.length() == 4)
        //.map(name -> performImpureOperation(name)) //AVOID + DANGEROUS
        .map(String::toUpperCase)
        //.forEach(name -> result2.add(name)); //BAD IDEA with ParallelStream
        .collect(Collectors.toList()); //to Listis a better option
```

Functional pipeline offers internal iterators
* is less complex
* easy to modify
* easy to understand

**BUT**

Avoid shared mutable variables

it is very important that we make the functional pipeline pure

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