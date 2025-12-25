---
categories: Java
date: 2022-08-06 08:30:00
tags:
- Functional Programming
- Lambda
- Streams
- Java 8
title: Functional Programming Concepts
---

{% include toc title="Index" %}

* How to get behavior out of a method and
  ```java
  // Method that returns behavior as a Predicate
  public static Predicate<Integer> getThresholdPredicate(int threshold) {
      return number -> number > threshold;
  }
  ```
* Passing that behavior into a method.
  ```java
   // Obtain a behavior (Predicate) that checks if a number is greater than 10
   Predicate<Integer> isGreaterThanTen = getThresholdPredicate(10);

  // Passing that behavior into a method
  List<Integer> filteredNumbers = filterNumbers(numbers, isGreaterThanTen);
  // Method that accepts a Predicate to filter numbers
  public static List<Integer> filterNumbers(List<Integer> numbers, Predicate<Integer> predicate) {
  return numbers.stream()
      .filter(predicate)
      .collect(Collectors.toList());
  }
  ```

Good Design Principle `keep together what belongs together`

> The Right Way --> Delegate

- be declarative (leave it to the API's)
- not imperative.

# Pure Function

**Rules:**

- **No Side Effects**: A pure function does not alter any state outside itself.
  It does not produce side effects.
- **Dependence on External State**: A pure function **does not rely** on
  external variables or states that may change.

**Characteristics of Pure Functions:**

- **Idempotent**: A pure function is idempotent, meaning it will return the same
  result when executed multiple times with the same input.
- **No Side Effects**: It does not affect or rely on any external state.
- **Concurrency**: Pure functions can be executed in parallel without causing
  issues, improving concurrency and performance.

### Why Are Pure Functions Important?

Functional programming emphasizes **immutability** and **purity** for
_efficiency_:

- **Lazy Evaluation**: Functional programming relies on lazy evaluation, which
  defers computation until necessary.

Lazy evaluation requires purity of functions
{: .notice--primary}

- **Parallel Execution**: Lazy evaluation and parallel execution depend on the
  immutability and purity of functions to ensure correctness and efficiency.

In contrast, an impure function might return different results for the same
arguments or modify external state.

> As Polymorphism is to object-oriented Programming,
`Functional Composition + Lazy Evaluation` is to functional programming

#### Avoid Shared Responsibility

```java
//Return the list of names of employees, in upper case, younger than 25
List<String> youngEmployees = new ArrayList<>();

employees.stream()
        .filter(employee -> employee.getAge() < 25)
        .map(EmployeeSimple::getName)//get the name
        .map(String::toUpperCase)//convert to upper case
        .forEach(upprCaseEmp -> youngEmployees.add(upprCaseEmp)); //Don't do this. Shared mutabilty is evil.
//This code can't ever be parallelized and it will misbehave.
```

the `filter` and `map` is pure function, but the `forEach` has shared mutability
and thus code wouldn't behave as expected on applying parallelStream

> It is programmers' responsibility to keep the function pure and if the
> function is impure, lazy evaluation would not be possible.

---------------------------------

# The Idea of Using Arguments in a Factory Method

In programming, particularly in Java, `factory methods` are often used to *
*_create objects_**
based on certain parameters or conditions.

Here, we explore how arguments can be utilized in a factory method
to influence the behavior of the created objects.

## Passing Behavior as Arguments

Previously, we have seen two key concepts:

- **Passing Behavior as Arguments**: We can pass behavior (such as functions or
  lambdas) as arguments to other functions.
- ```java
  // Define a predicate for checking if a car is red
  Predicate<Car> isRed = car -> "Red".equals(car.getColor());
  // Use the filterCars method with the predicate
  System.out.println(filterCars(new Car[]{car1, car2}, isRed)); // Output: [Red]
    
  // Method that takes a Predicate as an argument to filter cars
  public static String[] filterCars(Car[] cars, Predicate<Car> predicate) {
      return Arrays.stream(cars)
                   .filter(predicate)
                   .map(Car::getColor)
                   .toArray(String[]::new);
  }
  ```
- **Returning Behavior from Functions**: We can also return behavior from
  functions,
    - effectively creating factory methods that generate specific behaviors.
- ```java
  // Factory method that returns a Predicate based on the color
  public static Predicate<Car> getColorPredicate(String color) {
  return car -> color.equals(car.getColor());
  }
  ```

However, up until now, the behaviors returned by these functions have been fixed
and predefined.

## Example: Using a Single Argument

Consider a scenario where we want to create a criterion for evaluating the gas
level in a car.
The criterion depends on a threshold value that is provided as an argument.

### Example with a Constructor Argument

```java
// Factory method for creating GasLevelCarCriterion
public static Criteria<Car1> getGasLevelCarCriterion(int threshold) {
  return new GasLevelCarCriterion(threshold);
}

private static class GasLevelCarCriterion implements Criteria<Car1> {
  private final int threshold;

  public GasLevelCarCriterion(int threshold) {
    this.threshold = threshold;
  }

  @Override
  public boolean test(Car1 car1) {
    return car1.getGasLevel() >= threshold;
  }
}
```

```java
// Factory method creating GasLevelCarCriterion using a lambda expression
public static Criteria<Car1> getGasLevelCarCriterionLambda(int threshold) {
    return car1 -> car1.getGasLevel() >= threshold;
}
```

The lambda expression allows for concise syntax and still respects the
constraint that threshold must be final or effectively final.

### Using Variable Arguments

```java
// Factory method to return a criteria of Car based on multiple car colors
public static Criteria<Car1> getColorCriteria(String... colors) {
    Set<String> colorSet = new HashSet<>(Arrays.asList(colors));

    return c -> colorSet.contains(c.color);
}

```

# Closure and Immutability

When a function returns **behavior** that _depends on_ its **arguments**, it
introduces a **closure** effect.
This means that the returned behavior captures the values of the arguments used
within it.
However, for these values to be safely captured and used, they must be
constants (i.e., **final or effectively final**).

```java
// Factory method that returns a Predicate based on the threshold
public static Predicate<Integer> createThresholdPredicate(int threshold) {
  //threshold = threshold + 1;//Variable 'threshold' is accessed from within inner class (Lambda below), needs to be final or effectively final

  // 'threshold' is captured by the closure
  return number -> number > threshold;//Variable 'threshold' needs to be final or effectively final

}
```

In summary, using arguments in factory methods allows you to create flexible and
reusable criteria or behaviors, while ensuring that the values used within the
returned behavior are **immutable** to prevent unintended side effects.

------------------------------------

Java is a strongly statically typed language, and the lambda expressions lack
type information.

This is how it gets resolved

### **assignment to a variable**

- The first possibility is by **assignment to a variable**.

```java
private static final CarCriteria1 RED_CAR_CRITERION =  c ->  c.getColor().equals("Red");
```

### **lambda expression as an argument**

- **Passing a lambda expression as an argument** to another function call.

There is an implied assignment to the actual parameter of that method call, and
that parameter's type specifies what the
lambda expression has to be.

```java
showAll(getCarsByCriteria1(cars, c -> c.getPassengers().size() == 2));
```

### **Returning a lambda**

- Third, Returning a lambda expression directly from a function call.

The return type declared for that function specifies what the lambda expression
must be.

```java
  private static CarCriteria1 getFourPassengerCriterion(){
    return car -> car.getPassengers().size() == 4;
  }
```

### 4.Standalone Lambda using Type Casting.≥

- Fourth, the one that is significantly less common but completely legitimate,
  is to use a cast to specify what type of
  lambda we're trying to build.

Prior to the advent of lambda expressions in Java 8, there were two kinds of
places that you could use a cast.

- You could use a cast on a primitive value which would cause the bit pattern
  representation to change, perhaps from a
  32 bit integer into a 16 bit integer.

- Or you could use a **cast on an object reference expression** to say, _"Trust
  me, compiler, I know this looks like
  it's a reference to a car, but actually it's a special kind of car called a
  very fast car. And I know this, therefore
  I want you to trust that."_

Those two forms of casts are quite different from what's happening now.

```java
boolean b = ((CarCriteria1)(c -> c.getColor().equals("Red"))).test(Car1.withGasColorPassengers(0,"Red"));
```

This form of cast expression literally decides what will be created in the first
place. And is quite different.

Now, notice that a single lambda expression could potentially be compiled into
multiple different interfaces depending
on the context.

```java
boolean b2 = ((Strange)(c -> c.getColor().equals("Red"))).anotherTestStuff(Car1.withGasColorPassengers(0,"Red"));
```

Potentially confusing, and that's one of the reasons that we might choose to put
the argument types into the lambda's
formal parameter list. Because that could be sufficient in some cases to resolve
that ambiguity.

-------------------------------------------

As a general rule, you shouldn't be creating your own interfaces, just to work
with lambdas.

The vast majority of likely operations, whether they have zero, one, or two
arguments, including things dealing with
primitive return types, or primitive arguments, have been in-built in Java.

Use the features of the `java.util.function` package when you need to create
lambdas.

## Predefined Functional Interface

Defined in `java.util.function`

|                   |                                         |                                       |
|:------------------|:----------------------------------------|:--------------------------------------|
| Predicate <T>     | `test()`, takes T in, boolean out       | Used in `filter()` in Stream API      |
| Function<T,R>     | `apply(T k)`, T in R out(user defined ) | Used in `map()` in Stream API         |   
| Consumer<T>       | `accept()`, T in, void out              | Used in `forEach()` method            |
| Supplier<T>       | `get()`, nothing in, T out              | Used in `.collect` tereminal operator |
| BinaryOperator<T> | Two T’s in, T out                       |                                       |

--------------------

* Will be investigating the singleton, the factory and comparing those with
  constructors.