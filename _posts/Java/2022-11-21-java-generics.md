---
categories: Java
date: 2022-11-21 08:30:00
tags:
- Generics
- Java
title: Generics
---

# Generics as compile-time type safety

Generics in Java help catch certain **type-related** errors at compile time
rather than at runtime.

This can help in ensuring type safety and reducing the likelihood of
`ClassCastException` or other type-related exceptions during program execution.

### Generics do not accept primitive types

### Java does the auto boxing and unboxing

Java is not fully object oriented -> due to primitive and Static classes

# Generic Class

```java
// A simple generic class
@Data
class Box<T> {
    private T item;
}
```

Usage example:

```java
// Create a Box for Integer
Box<Integer> integerBox = new Box<>();
integerBox.setItem(10);

// Create a Box for String
Box<String> stringBox = new Box<>();
stringBox.setItem("Hello, Generics!");
```

# Generic Methods

```java
// Example of a generic method that accepts a generic parameter and returns a generic type
public static <T> S genericMethod(T data) {
    // Method logic using the generic parameter
    return data;
}
```

- <T> denotes that this method has a type parameter T, which can represent any reference type (class or interface)
- S is used as the return type of the method. This suggests that the method
  returns a value of type S

# Wild cards (?)

Understanding upper bounds (`<? extends T>`) and lower bounds (`<? super T>`) in
Java generics is crucial for writing flexible and reusable code.

## Upper Bounded Wildcard

# Upper Bounded Wildcard `? extends T`

- Specifies that the type parameter (?) must be a **subtype** of the specified
  type T.
- restrict the types to T or its subclasses.

# Lowerbound

Lower bounded wildcards (`? super T`) restrict the types to T or its
superclasses.

### Stream.max

Signature from `Stream<T>`

> Optional<T> max(Comparator<? super T) comparator)

The max method is going to apply on a stream, and it's going to return a single
value.

**Optional<T>** is a container object that may or may not contain a non-null
value.
This allows the max method to handle cases where the stream might be empty,
returning an empty Optional in such cases.

**Comparator<? super T> comparator**: This parameterizes the Comparator to
accept any supertype of T.
This flexibility allows the max method to compare elements **of type T or any of
its supertypes**.

**Ensures Flexibility with Inheritance**: Since Java allows subtyping, a
`Comparator<? super T>` can accept comparators for **T itself or any superclass
of T**.

- This is useful when you have a class hierarchy and want to compare elements
  based on properties defined in supertypes of T.

**Restricts Comparator Flexibility**: `Comparator<? extends T>` would **restrict
** the comparator to only accept types that extend T. This limits the comparator
to handle **only subclasses of T**,

- excluding comparators for T itself or its superclasses, which might be needed
  in certain scenarios.

# Type Erasure

In Java, generics are implemented using type erasure **to maintain backward
compatibility** with older versions of Java that do not
support generics.

**Compile-Time Enforcement**: Generics provide **compile-time type safety** by
allowing you to specify the types of objects that a collection or class can
contain.

**Erasure at Runtime**: During compilation, the compiler **removes the generic
type information** and replaces it with bounds or Object references.

- This means that generic type parameters are not available at runtime.

```java
@Data
public class Box<T> {
    private T value;
```

- At compile time, `Box<T>` is treated as Box due to type erasure.
- Any `T` in `Box<T>` is replaced with Object during compilation.

##### 2. Type Erasure Implications

```java
Box<Integer> integerBox = new Box<>();
integerBox.set(10); // Here, T is Integer

Integer val = integerBox.get(); // Compiler inserts cast to Integer
```

- At runtime, `Box<Integer>` is just Box.
- The set method accepts Object, and **the compiler inserts a cast (Integer)**
  before setting the value.

##### 3. Bounded Wildcards

When dealing with bounded wildcards (<? extends T> or <? super T>):

**Reading Elements**:

The loop for (Number n : list) iterates over elements of type Number or its
subclasses (Integer, Double, etc.).

Since list is guaranteed to contain elements that extend Number, you can safely
read these elements and treat them as Number
within the loop body.

**Adding Elements**:

The compiler prevents adding elements to list because it cannot guarantee the
type safety due to type erasure.

At runtime, list could be of any type that extends Number, such as List<Integer>
or List<Double>. Adding an element like
new Integer(10) directly to list would violate type safety because the actual
runtime type of list might not accept Integer (it could be List<Double> for
instance).

```java
 public static void processList(List<? extends Number> list) {
    // Compiler error: Cannot add elements to a list with an extends wildcard
    list.add(new Integer(10)); // This line would cause a compile-time error
}
```