---
title: Default method in Interface
date: 2022-07-27 13:06:00
categories:
- Microservices
tags:
- Java
- Java 8
---

{% include toc title="Index" %}

# Context

The major advantage of a default method in an Interface comes into play in this
scenario.

Need a convertor that can convert or map one Object type into another. Often the
data returned from DB needs to be mapped with business objects and it could be a
list of objects or a single object. To accomodate both types (Single object or a
list of object), the default method in the interface can be written like this :-

### Defining the Interface

{% gist nitinkc/83007b76b4afc24ca39761195af2de35 %}

Lets take an example of the implementation. On the implementation side,
developer has to focus on just converting one object into another and the rest
gets taken care of by default method

### Implementing the interface

For all tyopes od tables in the DB, same concerter can be used by defining the
individual converters by overriding the convert method.
{% gist nitinkc/f5149ff2a6dacd72b24732c5f52dfc94 %}

The interface can be used to convert an entire list

```java
@Autowired
MyConvertor myConverter;
...
...
List<Data> dataList = someRepo.findAll();
List<DataDto> dataDtoList =  myConverter.convert(dataList);
```

or the same can used to convert just one object

```java
Data data = someRepo.findById('someId');//returns one row
DataDto dataDto =  myConverter.convert(dataList);
```

---

# Interface Reference (Summary + Examples)

This section keeps the detailed interface notes in one place for easy reference.

## Interface vs Abstract vs Concrete (quick recap)

- Interface: a contract; supports default/static methods (Java 8) and private helper methods (Java 9+).
- Abstract class: partial implementation + shared state for related classes.
- Concrete class: fully implemented, instantiable type.

## Types of Interfaces

### Marker (tag) interfaces

- Empty interfaces used to mark a class with a capability or semantic meaning.
- Examples: `java.io.Serializable`, `java.lang.Cloneable`.
- Libraries use `instanceof` or type checks to enable special handling.

```java
public interface MyMarker { }

public class Foo implements MyMarker { }

if (obj instanceof MyMarker) {
    // enable special handling
}
```

### Functional interfaces (SAM types)

- Exactly one abstract method (Single Abstract Method — SAM).
- Target type for lambda expressions and method references.
- Use `@FunctionalInterface` to document intent and let the compiler validate it.

```java
@FunctionalInterface
public interface Transformer<T, R> {
    R apply(T t);
    default R applyTwice(T t) { return apply(apply(t)); } // allowed
}

Transformer<String, Integer> len = s -> s.length();
int n = len.apply("hello");
```

### Protocol / capability interfaces

- Declare behavior contracts (`Comparable`, `Closeable`, `Runnable`).
- Implemented by many unrelated classes.

```java
public interface Closeable {
    void close() throws IOException;
}
```

### Sealed interfaces (Java 17+)

- Restrict which types may implement the interface.
- Useful for closed hierarchies and pattern matching.

```java
public sealed interface Expr permits Literal, Add, Mul { }
```

## Interface Features and Rules

- **Constants**: fields are implicitly `public static final`.
- **Multiple inheritance**: a class can implement multiple interfaces.
- **Default method conflicts**: if two interfaces provide the same default method,
  the class must override and resolve the conflict.

```java
interface A { default void hello() { System.out.println("A"); } }
interface B { default void hello() { System.out.println("B"); } }

class C implements A, B {
    @Override
    public void hello() {
        A.super.hello(); // or B.super.hello(); or custom logic
    }
}
```

- **Private methods (Java 9+)**: helper methods for default methods without exposing them.

```java
interface Audit {
    default void logInfo(String msg) { log("INFO", msg); }
    default void logWarn(String msg) { log("WARN", msg); }

    private void log(String level, String msg) {
        System.out.println(level + ": " + msg);
    }
}
```

- **SAM conversion**: lambdas only target functional interfaces. Method references are shorthand.

```java
Runnable r = System.out::println; // not valid, println needs args
Runnable ok = () -> System.out.println("hi");
```

## Why default methods exist

Default methods allow interface evolution without breaking existing implementations.
The JDK used this to add methods like `List.sort(Comparator)` and `Collection.stream()`.

## When to use which construct

- Use interfaces for public contracts and multiple inheritance of type.
- Use abstract classes when you need shared state or common protected helpers.
- Use concrete classes for instantiable implementations.

## Summary Table

| Construct | Best For | Can hold state? | Multiple inheritance? |
|:----------|:---------|:----------------|:----------------------|
| Interface | Contracts, APIs, capabilities | No (only constants) | Yes |
| Abstract class | Shared code + state | Yes | No (single inheritance) |
| Concrete class | Instantiable implementation | Yes | No (single inheritance) |
