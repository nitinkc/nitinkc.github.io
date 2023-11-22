---
title:  "Java Tests"
date:   2023-10-20 15:16:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# Type inference

- helps remove the noise from the code
- IDE's provides the hover and know the type of the variables.
- allows the compiler to know the type about

```java
var test = "test";
test.foo();
```
Notice the compile time log : _location: variable test of **type String**_
```java
error: cannot find symbol
        test.foo();
            ^
  symbol:   method foo()
  location: variable test of type String
```

notice in the [byte code `LOCALVARIABLE test Ljava/lang/String; L1 L2 1`](https://nitinkc.github.io/shortcuts/intelliJ-Debug-tricks/#show-bytecode)
```java
 public static main([Ljava/lang/String;)V
   L0
    LINENUMBER 5 L0
    LDC "test"
    ASTORE 1
   L1
    LINENUMBER 7 L1
    RETURN
   L2
    LOCALVARIABLE args [Ljava/lang/String; L0 L2 0
    LOCALVARIABLE test Ljava/lang/String; L1 L2 1
    MAXSTACK = 1
    MAXLOCALS = 2
```

### Use type inference carefully

**Use case** : When the response is received from a call of a method or a service, use type inference because its type 
is determined by the return type of the method or the service being called.

# Arrays asList

```java
List<Integer> numbers = Arrays.asList(1,2,3);
System.out.println(numbers.getClass());//class java.util.Arrays$ArrayList
//it is far from immutable. does not support add method

try{
    numbers.add(4);
} catch (Exception e){
    System.out.println("add unsupported ");//This runs, as add is not supported in Arrays.asList()
}
```

Instead of using `Arrays.asList` use `List.of()`, the immutable variant. Similarly, use `Set.of` and `Map.of`.

* The Set's of does not provide duplicate
* the of methods does not permit nulls

# Streams Purity - Shared Mutability

- The execution is always lazy in Java or C#. 
  - For Kotlin and Scala you can choose between eager and lazy
- Functional programming relies on lazy evaluation for efficiency
- Lazy evaluation relies on **purity of functions** for correctness.

Programmers need to make sure that Lambdas are pure

### Rule for purity

Rule 1 is necessary but not sufficient
1. **No shared mutability** :  The function does not make any change that is visible outside
2. The function does not depend on anything that may change from outside

### Parallels


```java
//Which Thread will transform run
List.of(1,2,3).stream()
        .parallel()
        .map(number -> transform(number))
        .sequential()
        .forEach(number -> print(number));
```
Java 8 streams do not segment the pipeline for different threading model. The last setting overrides the entire 
pipeline.

Reactive streams segment the pipeline for different threading model

# Inheritance

Do not do anything serious in the constructor, especially do not call virtual method

**Lesson from effective Java**: Make the constructor simple and private and make the Factory method create it. By the 
time you get to the Factory method, the constructor would have been completed.


```java
class Base{
    public Base(){//Constructor
        System.out.println("In base");
        check();// The check of the Derived is called
    }
    public void check(){}
}

class Derived extends Base {
    private String value;

    public Derived(String value) {
        System.out.println("In Derived");
        this.value = value;
    }

    @Override
    public void check() {
        if (value.length() == 0) {
            throw new RuntimeException("Null Value");
        }
    }
}


public static void main(String[] args) {
    try {
        new Derived("");//Null Pointer exception
    } catch (Exception e){
        System.out.println(e);
    }
}
```

# toList or .collect(Collectors.toList())

It is better to use toList directly in the stream rather than 

```java
.toList();//Immutable
.collect(Collectors.toList()); //Mutable
.collect(Collectors.toUnmodifiableList())//Immutable
```

# Records

```java
record Year(int year){
    //Avoid Canonical constructors as much as possible.
    // Use the compact constructor instead
    //Compact constructor is a filter or a pre-processor before the constructor is called.

    //code -->  Compact constructor --> constructor.
    
    Year {
        if(year < 0){
            throw new RuntimeException("Negative Year");
        }
        if(year < 100){
            //this.year = 2000 + year;//This is not available yet
            year = 2000 + year;
        }
    }
}
```


# CopyOf

asList creates a mutable List
ofList creates immutable

What is immutable is safe to share - returns the same reference to it
What is immutable is safe to copy - it never changes ever

Stock price at an instant of time is immutable

In Domain Driven Design, the value objects are expected to be immutable

# Teeing


# Exceptions

### catch expressions (introduced in Java 16) and

**Use Case** : well-suited for simple exception handling cases without complex logic or control flow change

* Catch expressions are limited to a single expression, so cannot use control flow statements directly within the catch expression.

```java
// Using Catch Expressions (Java 16+)
try {
    int result = 10 / 0; // ArithmeticException
} catch (ArithmeticException e) -> System.err.println("Arithmetic Exception occurred: " + e.getMessage());
```

* Encapsulate any control flow logic within a separate method or code block and call it from catch expression

```java
try {
    int result = performComplexOperation();
} catch (CustomException e) -> logAndThrow(e);


private void logAndThrow(CustomException e) {
    System.err.println("Custom Exception occurred: " + e.getMessage());
    logError(e);
    throw new AnotherException();
}
```

* Catch Expressions Encapsulating Control Flow
```java
try {
    int result = performComplexOperation();
} catch (CustomException e) -> {
    System.err.println("Custom Exception occurred: " + e.getMessage());
    return; // Encapsulating control flow
}
```

### catch statements (traditional approach)
* The catch block can contain multiple statements, including control flow statements like return or break.
* Provides flexibility to control the program's flow after catching an exception
* **Use Cases**: Suitable for handling complex exception scenarios.
