---
title: Generics
date: 2022-11-21 08:30:00
categories:
- Java
tags:
- Collections
---

## Generics as compile-time type safety

Generics in Java help catch certain **type-related** errors at compile time
rather than at runtime. With the help of Generics, the possible runtime 
Exceptions can be converted to Compile time Exceptions.

This can help in ensuring type safety and reducing the likelihood of
`ClassCastException` or other type-related exceptions during program execution.

>  Generics do not accept primitive types
> Java does the auto boxing and unboxing

Java is not fully object-oriented language -> due to primitive and Static classes

```java
List<Integer> intsList = new ArrayList<>();
intsList.add(3);//Adding primitive
intsList.add(Integer.valueOf(4));//Unnecessary Boxing
```

## Generic Class

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

X is a type variable in Java's terminology and when we have a variable, we need
to declare it before we use it.

The Type declaration of the Generic Variable is placed immediately before the
Return Type.

# Generics in List Interface and Collections

```java
// Generic Type is declared on Class/Interface
public interface List<E> extends Collection<E>

boolean add(E e)
boolean addAll(Collection<? extends E> c)
boolean containsAll(Collection<?> c)
E get(int index)
```

```java
// Collections Utility Class, Generic Type is not declared on the Class so each method
// has to declare its own Generic return type
public class Collections

// Collections does not declare a type. So if you want to use a generic type, you have to 
// declare it on the method. And in this case, the empty list method is declaring T after the word final, 
// but before the return type. And the return type is list of T.
public static <T> List<T> emptyList();//<T> between final and List<T>

public static final <K,V> Map<K,V> emptyMap();

public static <T> boolean addAll(Collection<? super T> c, T... elements);

// Return type is simply T
// we're saying that whatever the generic type is it must implement the comparable interface. 
// Because the min method is going to cast all of the elements of the collection to comparable, 
// in order to determine the minimum one.
public static <T> T min(Collection<? extends T> coll, Comparator<? super T> comp)
```

### Complex Generic Examples from JDK

```java
// Example From java.util.Map.Entry<K,V>
public static <K extends Comparable<? super K>, V> Comparator<Map.Entry<K,V>> comparingByKey();

// Example from java.util.Comparator<T>
public static <T, U extends Comparable<? super U>> Comparator<T> comparing(Function<? super T, ? extends U> keyExtractor)

// From java.util.stream.Collectors
public static <T, K, D, A, M extends Map<K, D>>
    Collector<T, ?, M> groupingBy(Function<? super T, ? extends K> classifier,
                                  Supplier<M> mapFactory,
                                  Collector<? super T, A, D> downstream);

// Collectors.toMap - Collectors is a utility Class just like Collections
public static <T, K, U>
    Collector<T, ?, Map<K,U>> toMap(Function<? super T, ? extends K> keyMapper,
                                    Function<? super T, ? extends U> valueMapper)
```

# Wild cards (?)

Understanding upper bounds (`<? extends T>`) and lower bounds (`<? super T>`) in
Java generics is crucial for writing flexible and reusable code.

## Wildcards, Generics and Inheritance

String extends Object, and Array of Strings extends Array of Object.

BUT

```
List<String> does **NOT** extend List<Object>
```

Number is Super class to other Wrapper Classes
![](https://docs.oracle.com/javase/tutorial/figures/java/objects-numberHierarchy.gif)

## Unbounded Wildcard (?)

The idea behind the question mark operator is that when we declare a
collection of that type, we're saying we don't know what the underlying type is.

- Can **Read** from it, but cannot **write** to it.

## Upper Bounded Wildcard `? extends T`

- Specifies that the type parameter (?) must be a **subtype** of the specified
  type T.
- Restrict the types to T or its subclasses.
- A wildcard allows you to tell the compiler what type you're expecting, and also
  allows you to provide elements that are that type, or subclasses of that type.
- Use the extends keyword and give a maximum class
- Can be defined and be read from
- **Cannot add to**, as the data type cannot be resolved

> **Covariance** - preserves the ordering of types from more specific to more general

> Generic java collections are covariant when extends is used with a wild card.
> This means - if you declare a collection with a bounded wildcard, you can
> use methods from the Bound. E.g: `List<? extends Number>`, the methods of Number 
> can also be used along with class of ?. Each element supports Number methods as well.

## Lower Bounded Wildcard `? super T`

Lower bounded wildcards (`? super T`) restrict the types to T or its
superclasses. It must be T or above.

Example: forEach as the default method of Java 8 - Bound on the ? is AClass or above.

> **Contravariant** - preserves the ordering of types from **more general** to **more specific**

> Generic java collections are Contravariant when **super** is used with a wild card

## PECS - Producer Extends, Consumer Super

Acronym coined by Joshua Bloch in "Effective Java"

Mnemonic for:

- Use **extends** keyword when we **consume** the value
    - when there's a value that's coming in that we're going to invoke methods on.

- Use **super** when we **provide** a value,
    - because then we can provide either the value itself or one of its superclass types.

- Use explicit type when we have both an upper and a lower bound.

> For example, in Java 8 streams, if we're pulling a value from the stream to
> use, that's super. Whereas if we are using the value in the lambda that we're
> providing, that's extends.

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

**Restricts Comparator Flexibility**: `Comparator<? extends T>` would **restrict** the comparator to only accept types that extend T. This limits the comparator
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