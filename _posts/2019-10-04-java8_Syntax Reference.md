---
layout: post
title:  "Java 8 Syntax Reference"
date:   2019-10-04 13:43:00
---

##### For each method **applies the lambda** to each element of the collection

```java
//Prints each element
list.stream().forEach(str -> System.out.println(str));

//Where ever Lambda is there it can be replaced by method reference
list.stream().forEach(System.out :: print);
```

## Double Colon Operator

| S.no| Kind                                                  | Example                              |
|---- |-------------------------------------------------------|--------------------------------------+
| 1  | Reference to a static method                          | ContainingClass::staticMethodName  |
| 2  |Reference to an instance method of a particular object | containingObject::instanceMethodName |
| 3  | Reference to an instance method of an arbitrary object of a particular type | ContainingType::methodName           |
| 4  |Reference to a constructor                             | ClassName::new                       |

## Predefined Functional Interface

Defined in java.util.function

1. Predicate (test(), returns boolean) - Used with filter() in Stream API
2. Function (apply(T k), return user defined TYPE) - Used with map() in Stream API
3. Consumer (accept()), - Used with forEach() method
4. Supplier (get()),

### Predicate (used with Filters)

java.util.function.Predicate, represents a simple function that takes a single value as parameter, and returns true or false.

```java
public interface Predicate<T> {
    boolean test(T t);
}

**Predicate uses a Lambda that returns true and false**

Predicate<Student> firstNameLength = Student -> (Student.getfName().length() <= 3);
Predicate<Student> semPredicate = Student -> (Student.getSem() == 1);
Predicate<Student> deptPredicate = Student -> (Student.getDeptCode().equalsIgnoreCase("mec"));

//Find out all the students based on firstNameLength predicate
System.out.println("Find out all the students based on firstNameLength predicate");
studentList
  .stream()
  .filter(firstNameLength)
  .forEach(System.out::println);

//Find all students from 1st Sem
System.out.println("Find all students from 1st Sem");
studentList
  .stream()
  .filter(semPredicate)
  .forEach(System.out::println);

//Composite Predicate : All Students from CSE of First sem
System.out.println("Composite Predicate : All Students from CSE of First sem");
studentList
  .stream()
  .filter(semPredicate.and(deptPredicate.negate()))
  .forEach(System.out::println);

//Same as above
studentList
  .stream()
  .filter(semPredicate)
  .filter(deptPredicate.negate())
  .forEach(System.out::println);
```

### Function (used with MAP)

The Function interface represents a function (method) that takes a single parameter and returns a single value. Here is how the Function interface definition looks:
```java
public interface Function<T, R> {
    R apply(T t);
}

**Write Lambda in such a way that it accepts an argument and performs an action on it**
List<String> list = Arrays.asList("1","2","3", "n", "",null);

// Function to convert Strings to Int, put 9999 as default value for other cases
Function<String, Integer> function = x -> NumberUtils.toInt(x,DEFAULT_VALUE);

Predicate<Integer> predicate = (Integer x) -> (x == DEFAULT_VALUE);
//MAP is used to apply a function
list
    .stream()
    .map(function)
    .forEach(System.out::println);

//all the numbers except for the default replacement number
list.stream()
    .map(function)
    .filter(predicate.negate())
    .forEach(System.out::println);
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

{% gist nitinkc/d55b4541f27fc0bfd86f122d35c2b527 %}

##### Sorting a set

{% gist nitinkc/61476aad3b16d3c29e843553788e640b %}

### Consumer : (used with forEach) takes generified argument and returns nothing

It is a function that is representing side effects
```java
public interface Consumer<T> {
    void accept(T t);
}

List<String> strList = Arrays.asList("test","this","is","a","test","this","test","is","not","complex");

Consumer<String> c = s -> System.out.print(s + " ,");
//Consumer<String> c = System.out::println;
strList.stream().forEach(c);
```
{% gist nitinkc/f0cdad5af384796e2c5684cb6e5cdc34 %}

{% gist nitinkc/ff63f3c1d164ef3b8dfe3a91a02e3259 %}

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
