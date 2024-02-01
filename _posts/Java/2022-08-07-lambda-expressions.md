---
title:  "Lambda Expressions & Functional Interface"
date:   2022-08-06 08:30:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}


# Lambda 
Lambda Expression is just an anonymous (nameless) function. A function does not have a state. Object has a state.

Best  Practices
1. Be declarative and less imperative
2. Favor immutability
3. Reduce side effects
4. Expressions over statements
5. Design with Higher-Order functions


# Functional Interface
* Interface with SAM : Single Abstract Method
* Functional Interface : can automatically be elevated to lambda expression. In other words, you can only use lambdas for functional interfaces
* Functional interface assign a contract!!

<details>
<summary> 
View Functional Interfaces
</summary>
{% gist nitinkc/1460522d8e96dc6bb2a7058ed190b9e2 %}
</details>

## Writing Lambda
A function/method has 4 parts : name, return type, params/args list & method body
![Parts of a Method/Function]({{ site.url }}/assets/images/methodParts.png)

The most important parts are just the arguments and body. In Functional interface, there is only one method, so the name
of the method is implied and the override has to be done by any class implementing the method.

Lambda with parameter/argument data type
![Image Text]({{ site.url }}/assets/images/lambda1.png)


even the argument/parameter data type can removed as
![Image Text]({{ site.url }}/assets/images/lambda2.png)

## Method Accepting Lambda
Any method that accepts Functional Interface as parameter, needs a Lambda, For Example `forEach` accepts
a Consumer (a functional interface) as a parameter.
```java
default void forEach(Consumer<? super T> action);
```

Traditionally the anonymous class implementation is done :-
```java
List<Integer> list = Arrays.asList(1,4,6,8,9,7,5,3,2);

//Implemenation via anonymous inner class
list.forEach(new Consumer<Integer>() {
    @Override
    public void accept(Integer i) {
        System.out.println(i);
    }
});
```

Above can be reduced by just keeping only the args and the method body
```java
list.forEach((Integer i) -> {
        System.out.println(i);
        return;
    });
//i -> params/args & System.out.println(i) -> body
```

This can further be reduced by removing data type from argument, and removing unnecessasary return statement
```java
list.forEach(i -> System.out.println(i));
```

This can be further reduced with the usage of method reference
```java
list.forEach(System.out::println);
```

For better understanding, step by step declaration and usage can be tried.
```java
Consumer consumer = x -> System.out.println(x);//since for each accepts a consumer, declare it first
//use the consumer with the method present in the Consumer interface
list.forEach(val -> consumer.accept(val));
//Or for simplicity just pass the consumer
list.forEach(consumer);
//or just replace the variable
list.forEach(x -> System.out.println(x));
```

# Strategy Pattern

Strategy pattern. writing a function to be called as Lambda

Consider a method written in such a way that it accepts a functional interface as an argument.

Just pass a Lambda as parameter
{% gist nitinkc/23bcaf8a1576ed48f144fe852f059f97 %}

Since the strategy can be decided at runtime, we can pass the strategy right at the time when its needed
```java
List<Integer> values = Arrays.asList(1, 2, 3, 4, 5, 6);

//Print sum of all numbers
System.out.println(totalValues(values, e -> true));

//Print sum of all all Even numbers
System.out.println(totalValues(values, e -> e % 2 == 0));

//Print sum of all odd numbers
System.out.println(totalValues(values, e -> e % 2 != 0));
```


* Lambda expression can access static variables, instance variables,
* effectively final variables and effectively Final local variables

