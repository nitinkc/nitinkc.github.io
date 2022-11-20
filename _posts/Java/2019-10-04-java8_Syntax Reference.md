---
title:  "Java Syntax Reference"
date:   2019-10-04 13:43:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

##### ForEach in Streams

**applies the lambda** to each element of the collection

```java
//Prints each element
list.forEach(str -> System.out.println(str));
//Lambda can be replaced by method reference
list.forEach(System.out :: print);
```

## The Double Colon Operator - Method Reference

|S.no| Kind | Example | Method Reference | Equivalent Labmda |
| :----:  | :---- | :---- | :---- |
| 1  | Ref. to a static method (Simplest Type) | ContainingClass::staticMethodName  | System.out :: print <br /> MyStringUtils :: isPalindrome | x -> System.out.println(x) <br /> (str) -> MyStringUtils.isPalindrome(str)
| 2  | Ref. to an instance method of a particular object | someObject::instanceMethodName | obj :: test  <br /> | () -> obj.test() <br />  |
| 3  | Ref. to an instance method of an arbitrary object of a particular type | ContainingType::methodName| String :: toUpperCase | str -> str.toUpperCase()
| 4  | Ref. to a constructor  | ClassName::new       | MyClass :: new | () - > new MyClass()|

**Instance method** are methods which can only be invoked through an object of the class. It needs an object if a class to be called.

## Predefined Functional Interface

Defined in java.util.function

|1.| Predicate &lt;T> | test(), takes T in, returns boolean | Used with filter() in Stream API|
|2.| Function<T,R> |apply(T k), T in return user defined TYPE R | Used with map() in Stream API
|3.| Consumer&lt;T> |accept(), T in, void out |Used with forEach() method |
|4.| Supplier&lt;T> |get(), nothing in, T out |Used with .collect tereminal operator|

### Predicate 

`java.util.function.Predicate` represents a simple function that takes a single value as parameter, and returns true or false. Predicate uses a Lambda that returns true and false

Commonly used with Filters. 

Here is how the Function interface definition looks:

```java
public interface Predicate<T> {
    boolean test(T t);
}
```
Predicate can be defined within Labda or can be separately defined and invoked using test method.

{% gist nitinkc/b63f8cbb3d13cab6ba1fb5256d748d6f %}


### Function 

The Function interface represents a function that **takes a single parameter T and returns a single value R**.

Commonly used with streams.map()

```java
public interface Function<T, R> {
    R apply(T t);
}
```

Write Lambda in such a way that it **accepts an argument and performs an action** on it to return an Object

{% gist nitinkc/bed9ceea341088f49355f8422958d04a %}


### BiFunction

```java
public interface BiFunction<T, U, R> {
     R apply(T t, U u);
     ...
}
```
higher-order functions. Two common examples are filter and map.

A filter processes a list in some order to produce a new list containing exactly those elements of the original list for which a given predicate (the Boolean expression) returns true.

A map applies a given function to each element of a list, returning a list of results in the same order.

Another common higher-order function is reduce, which is more commonly known as a fold. This function reduces a list to a single value.


### Higher-order functions in function

|compose|f1.compose(f2) -> first run f2, then pass the result to f1||
|andThen|f1.andThen(f2) -> first run f1, then pass the result to f2. So, f2.andThen(f1) is same as f1.compose(f2).||
|identity|Function.identity() creates a function whose apply method just returns the argument unchanged||

Methods that Return Functions

Two common examples are filter and map.

##### Sorting a Primitive list
{% gist nitinkc/d55b4541f27fc0bfd86f122d35c2b527 %}

##### Sorting a list of certain Type
{% gist nitinkc/bb52e836bb4a5472959ebbd5c95375f5 %}


##### Sorting a set
{% gist nitinkc/61476aad3b16d3c29e843553788e640b %}

### Consumer 
(used with forEach) takes generified argument and returns nothing

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

BiConsumer example. Using BiConsumer to insert values into hashmap.

{% gist nitinkc/f0cdad5af384796e2c5684cb6e5cdc34 %}

Parenthesis Checker using Consumer
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

### Filthy way of sorting a list
```java
// Sort method under Collection takes the same comparator
list.sort(Comparator.comparing(String::toString, (String a, String b) -> Integer.parseInt(a.substring(2)) - Integer.parseInt(b.substring(2))));
list.sort(Comparator.comparing(String::toString,comparator.reversed()));

// Single Line Implementation using Collections Arrays Utility Class
Collections.sort(list, ((String a, String b) -> Integer.parseInt(a.substring(2)) - Integer.parseInt(b.substring(2))));

Comparator<String>  comparator = (String a, String b) -> Integer.parseInt(a.substring(2)) - Integer.parseInt(b.substring(2));
Collections.sort(list, comparator);
list.sort(comparator);

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
```