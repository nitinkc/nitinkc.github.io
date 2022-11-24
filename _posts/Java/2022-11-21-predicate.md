---
title:  "Predicate Functional Interface"
date:   2022-11-21 08:30:00
categories: ['Java']
tags: ['Java']
---

`java.util.function.Predicate` represents a simple function that takes a single value as parameter, 
and returns true or false. Predicate uses a Lambda that returns true and false

With Streams Predicate is used with Filter. A filter processes a list in some order to produce a new list containing exactly those elements
of the original list for which a given predicate (the Boolean expression) returns true.


```java
public interface Predicate<T> {
    boolean test(T t);
}
```

Predicate can be defined within Lambda or can be separately defined and invoked using test method.
{% gist nitinkc/b63f8cbb3d13cab6ba1fb5256d748d6f %}

With multiple predicates, we can use chaining and use **type casting** with multiple filter chaining
{% gist nitinkc/b03e110b64c954d9c480ebcb4ce310af %}