---
title:  "Static Factory Methods"
date:   2022-08-06 08:30:00
categories: ['Java']
tags: ['Java']
---


# What is Static Factory Method?

When a static method returns the same Class Object (reference type) of its own class, its called Static Factory Method

example        
```java
Runtime r = Runtime.getRuntime();
```

 JAVA 9 Enhancement; of() method is static factory method 

 ```java
// shortcut way to create UNMODIFIABLE Collection Object (no add or remove works after it)
List<Integer> l = List.of(2, 3, 4, 5, 6, 7);//upto 10 elements, post which var-arg method
// but using var arg is costly

Optional<List<String>> strOptional = Optional.of(Arrays.asList("John","Doe"));
List<String> stringList = strOptional.get();
```