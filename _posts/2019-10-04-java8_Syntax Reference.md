---
layout: post
title:  "Java 8 Syntax Reference"
date:   2019-10-04 13:43:00
---

# Topics

| S.no| Kind                                                  | Example                              |
|---- |-------------------------------------------------------|--------------------------------------+
| 1  | Reference to a static method                          | ContainingClass::staticMethodName  |
| 2  |Reference to an instance method of a particular object | containingObject::instanceMethodName |
| 3  | Reference to an instance method of an arbitrary object of a particular type | ContainingType::methodName           |
| 4  |Reference to a constructor                             | ClassName::new                       |



```Java
//For each method applies the lambda to each element of the collection
//Prints each element
list.stream().forEach(str -> System.out.println(str));

//Where ever Lambda is there it can be replaced by method reference
list.stream().forEach(System.out :: print);

```

# Predefined Functional Interfaces.

### Consumer
```java
public interface Consumer<T> {
    void accept(T t);
    ....
}
 ```

### Predicate

The Java Predicate interface, java.util.function.Predicate, represents a simple function that takes a single value as parameter, and returns true or false.
Java
```java
public interface Predicate<T> {
    boolean test(T t);
    ...
}
```

### Supplier
```java
public interface Supplier<T> {
    T get();
}


//Static method Reference
Supplier<LocalDate> s1 = LocalDate::now;
//Lambda Expression
Supplier<LocalDate> s2 = () -> LocalDate.now();

```

### Function

The Function interface represents a function (method) that takes a single parameter and returns a single value. Here is how the Function interface definition looks:
```java
public interface Function<T, R> {
    R apply(T t);
    ...
}
```

### BiFunction
```java
public interface BiFunction<T, U, R> {
     R apply(T t, U u);
     ...
}
```
higher-order functions. Two common examples are filter and map.

A filter processes a list in some order to produce a new list containing exactly those elements of the original list for which a given predicate (think Boolean expression) returns true.
A map applies a given function to each element of a list, returning a list of results in the same order.

Another common higher-order function is reduce, which is more commonly known as a fold. This function reduces a list to a single value.

##### Sorting a list

```java
// Single Line Implementation
Collections.sort(list, ((String a, String b) -> Integer.parseInt(a.substring(2)) - Integer.parseInt(b.substring(2))));

Comparator<String>  comparator = (String a, String b) -> Integer.parseInt(a.substring(2)) - Integer.parseInt(b.substring(2));
// Sorting in Natural Order
Collections.sort(list, comparator);
// Sorting in reversed order
Collections.sort(list, comparator.reversed());

//Prior to Java 8, using anonymous class
list.sort(new Comparator<String>() {
          @Override
          public int compare(String o1, String o2) {
              int interstateNumber1 = Integer.parseInt(o1.substring(2));
              int interstateNumber2 = Integer.parseInt(o2.substring(2));

              if (interstateNumber1 > interstateNumber2) {
                  return 1;
              } else if (interstateNumber1 < interstateNumber2){
                  return -1;
              }
              else{
                  throw new IllegalArgumentException("Two Interstates with same name in a Same City");
              }
          }
      });


 // Sort the List of Objects based on the Population
list.sort(Comparator
        .comparing(Data::getPopulation).reversed()
        .thenComparing(Data::getState)
        .thenComparing(Data::getCity));
```

##### Sorting a set
```java
Set<Student> students = new TreeSet<Student>(Comparator
                .comparing(Student::getName)
                .thenComparing(Student::getAge)
                .thenComparing((Student s1) -> s1.getName().length())
        );
```
