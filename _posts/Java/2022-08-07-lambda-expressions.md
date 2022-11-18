---
title:  "Lambda Expressions & Functional Interface"
date:   2022-08-06 08:30:00
categories: ['Java']
tags: ['Java']
---

# Lambda 
Lambda Expression is just an anonymous (nameless) function/class.

# Functional Interface

Interface with SAM : Single Abstract Method
Functional Interface : can automatically be elevated to lambda expression. In other words, you can Only use lambdas for functional interfaces
Functional interface assign a contract!!

* Strategy pattern. writing a function to be called from Lambda

Function does not have a state.

Object has a state

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

## Writing Lambda

![Image Text]({{ site.url }}/assets/images/lambda.png)




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

