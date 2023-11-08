---
title:  "Functional Programming"
date:   2023-11-06 08:30:00
categories: ['Java','Design Patterns']
tags: ['Java']
---

{% include toc title="Index" %}

* As Polymorphism is to object-oriented Programming
* Functional Composition + Lazy Evaluation is to functional programming

Lazy evaluation required purity of functions

# What is a pure function :

A pure function is idempotent : Returns the same result for the same input, if executed any arbitrary number of time  (Immutability)
and does not have any side-effects

##### Rules :
1. It does not change any state that is visible outside. Pure function do not change anything
2. It does not **depend** on anything outside that may change

##### Why ?
Functional programming relies on lazy evaluation for efficiency.

Lazy evaluation and parallel execution rely on
**immutability** and **purify** of functions for correctness.

FP emphasizes immutability and purity, not because
but because it is essential to it's survival/efficiency.


```java
//Return the list of names of employees, in upper case, younger than 25
List<String> youngEmployees = new ArrayList<>();

employees.stream()
        .filter(employee -> employee.getAge() < 25)
        .map(EmployeeSimple::getName)//get the name
        .map(String::toUpperCase)//convert to upper case
        .forEach(upprCaseEmp -> youngEmployees.add(upprCaseEmp)); //Don't do this. Shared mutabilty is evil.
//This code can't ever be parallelized and it will misbehave.
```

the filter and map is pure function above, but the forEach has shared mutability and thus code wouldn;t behave as expected on applying parallelStream


It is programmers responsibility to keep the function pure and if the function is impure, lazy evaluation would not be possible.

Function has to be pure
Avoid Shared Responsibility

the Right Way -> delegate, be declarative, leave it to the API's

** Collectors is a Reduce operation

