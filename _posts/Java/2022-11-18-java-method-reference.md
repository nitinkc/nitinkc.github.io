---
title:  "Method Reference"
date:   2022-11-18 08:30:00
categories: ['Java']
tags: ['Java']
---


* Lambda expression can access static variables, instance variables,
* effectively final variables and effectively Final local variables

For Simpler one liner Lambdas, with or without parameters


```java
.map(w ->  vcw.toLowerCase())

.map(String :: toLowerCase())
```

And it turns out that when we have any one of these four forms but notice it must be exactly these four forms we don't
get to reorder the arguments or anything like that

private static final Pattern WORD_BREAK = Pattern.compile("\\W+");

//Word break is an object .flatMap( l -> WORD_BREAK.splitAsStream(l))
.flatMap(WORD_BREAK::splitAsStream)


## The Four Kinds of Method References

| **Method Ref**             | **Type Example**        | **Equivalent Lambda**          |
|----------------------------|-------------------------|--------------------------------|
| SomeClass::staticMethod    | Math::cos               | x -> Math.cos(x)               |
| someObject::instanceMethod | someString::toUpperCase | () -> someString.toUpperCase() |
| SomeClass::instanceMethod  | String::toUpperCase     | s -> s.toUpperCase()           |
| SomeClass::new             | Employee::new           | () -> new Employee()           |



| ****Description****                                                                                                                                                                                   | ****Method Ref****         | ****Type Example****    | ****Equivalent Lambda****      |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------|-------------------------|--------------------------------|
| Take some arguments and invoke a static method on a class passing exactly the arguments to the lambda expression, directly to the method arguments of that static method.                             | SomeClass::staticMethod    | Math::cos               | x -> Math.cos(x)               |
| Produces a lambda that takes exactly as many arguments as the method expects                                                                                             | someObject::instanceMethod | someString::toUpperCase | () -> someString.toUpperCase() |
| And another format will take the first argument from the lambda, and use that to invoke a method. The remaining arguments from the lambda are then passed as the method arguments to that invocation. | SomeClass::instanceMethod  | String::toUpperCase     | s -> s.toUpperCase()           |
| Case gain takes the lambdas arguments and passes them to a constructor                                                                                                                                | SomeClass::new             | Employee::new           | () -> new Employee()           |

