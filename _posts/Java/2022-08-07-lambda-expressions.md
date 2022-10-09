---
title:  "Lambda Expressions & Functional Interface"
date:   2022-08-06 08:30:00
categories: ['Java']
tags: ['Java']
---

 
# Functional Interface

Interface with SAM : Single Abstract Method
Functional Interface : can automatically be elevated to lambda expression. In other words, you can Only use lambdas for functional interfaces
Functional interface assign a contract!!

```java
@FunctionalInterface
interface MyFunctionalInterface0{
    //SAM : Single Abstract Method
    void doSomework();
}

@FunctionalInterface
interface MyFunctionalInterface1{
    Integer doSomeJob(int a);
}

@FunctionalInterface
interface MyFunctionalInterface2{
    Integer doSomeTask(int a, int b);
}
```

The definition to the interface methods can be given as below
```java
MyfunctionalInterface0 functionalInterfaceWithZeroParam = () -> System.out.println("Some String");//Providing the definition to the abstract method
MyFunctionalInterface1 functionalInterfaceWithOneParam = (x -> x+x);//Providing the definition to the abstract method
MyFunctionalInterface2 functionalInterfaceWithTwoParam = (val1, val2) -> val1 * val2;//Valid Lambda as 2 arguments are expected
```

Any method that accepts Functional Interface as parameter, needs a Lambda, For Example
```java
default void forEach(Consumer<? super T> action);

// Usage with forEach        
list.forEach(val -> System.out.println(val));

//OR
Consumer d = x -> System.out.println(x);
list.forEach(val -> d.accept(val));
```
## Valid Lamdba

* Lambda expression can access static variables, instance variables,
* effectively final variables and effectively Final local variables

For Simpler one liner Lambdas, with or without parameters


