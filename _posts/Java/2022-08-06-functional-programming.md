---
title:  "Functional Concepts"
date:   2022-08-06 08:30:00
categories: ['Java']
tags: ['Java']
---
# Functional Concepts Agenda

* How to get behavior out of a method and
* Passing behavior into a method.
* Will be investigating the singleton, the factory and comparing those with constructors.

### A Question of Ownership

Good Design Principle
``` keep together what belongs together ```

Tight relationship between the car and the means of selecting a particular car, the criteria, should actually be in the
car class.


A pure function is essentially one where the return value, the result of that function, depends only on its arguments.
There are no variations and there are no side effects.

So, if we had a pure function and we call it, let's say, three and seven as arguments, the mechanism of the pure
function always produces the **same result** for the **same arguments**; 
so, perhaps 10 in this case, if it were adding them
together.

Further, a pure function does not do anything else.

By contrast, a regular function, or an impure one, if we call it with three and seven, the mechanism might return
different values for different invocations, even with the same arguments.

It might for example look something up in a database; it might look up three and get 99 as a result (from the db call)
and then produce a result of 106.

It might also write things to the database.

Pure functions are idempotent. Can be run many times without any effect.

Improves concurrency as multiple pure functions can be executed in parellel wihout any side effects.


---------------------------------

# The idea of using arguments to a factory method

- Previously, we've seen the ability to pass behavior as an argument to a function (often as a lambda, but not
  necessarily,)

- and we've been returning behavior back from a function, those have been our factories

But so far the behavior we've been returning out of functions has essentially been fixed.

- get gas level car criterion, creates an object, a new gas level criterion, which is actually parametrized with a
  threshold. The gas level criterion class internally has a threshold.

That value is set as the argument to the constructor

So the test method that we created here actually behaves in a way that depends on the threshold value that is passed in
to the constructor

### Single Argument

  ```java
// Factory for creating GasLevelCarCriterion
public static Criteria<Car1> getGasLevelCarCriterion(int threshold){
    return new GasLevelCarCriterion(threshold);
  }

  private static class GasLevelCarCriterion implements Criteria<Car1> {
    private int threshold;
    public GasLevelCarCriterion(int threshold) {
      this.threshold = threshold;
    }  
```

The value of threshold is shared. It gets copied from the method stack to the object memory stack of the Lambda

the object that the lambda represents is created, is that the code is copied in there. But also, the value of threshold
is duplicated into the object.

```java
// Factory for creating GasLevelCarCriterion using anonymous inner class. Variable is shared between lambda.
  // Its effectively final. Can be used, but cannot be modified
  public static Criteria<Car1> getGasLevelCarCriterion(int threshold){

    //threshold = threshold + 1;//Variable 'threshold' is accessed from within inner class, needs to be final or effectively final
    return new Criteria<Car1>(){
      @Override
      public boolean test(Car1 car1) {
        return car1.getGasLevel() >= threshold;
      }
    };
  }
```

OR, The same can be written as

```java
 public static Criteria<Car1> getGasLevelCarCriterionLambda(int threshold){
        return car1 ->  car1.getGasLevel() >= threshold;
  }
```

### Variable Argument

```java
// Factory method to return a criteria of Car based on multiple car color
  
  public static Criteria<Car1> getColorCriteria(String ...colors){
    Set<String> colorSet = new HashSet<>(Arrays.asList(colors));

    return c -> colorSet.contains(c.color);
  }
```

when a function returns another behavior that depends on the arguments to the factory, then we have that closure effect,
and the values that are used inside the generated behavior must be constants (final or effectively final). 


------------------------------------

Java is a strongly statically typed language, and the lambda expression seems to lack type information.

This is how it gets resolved

- The first possibility is by **assignment to a variable**.

```java
private static final CarCriteria1 RED_CAR_CRITERION =  c ->  c.getColor().equals("Red");
```

- **Passing a lambda expression as an argument** to another function call.

There is an implied assignment to the actual parameter of that method call, and that parameter's type specifies what the
lambda expression has to be.

```java
    showAll(getCarsByCriteria1(cars, c -> c.getPassengers().size() == 2));
```

- Third, Returning a lambda expression directly from a function call.

The return type declared for that function specifies what the lambda expression must be.

```java
  private static CarCriteria1 getFourPassengerCriterion(){
    return car -> car.getPassengers().size() == 4;
  }
```

- Fouth, the one that is significantly less common but completely legitimate, is to use a cast to specify what type of
  lambda we're trying to build.

## Standalone Lamdba using Type Casting.≥

So, prior to the advent of lambda expressions in Java 8, there were two kinds of places that you could use a cast.

- You could use a cast on a primitive value which would cause the bit pattern representation to change, perhaps from a
  32 bit integer into a 16 bit integer.

- Or you could use a **cast on an object reference expression** to say, _"Trust me, compiler, I know this looks like
  it's a reference to a car, but actually it's a special kind of car called a very fast car. And I know this, therefore
  I want you to trust that."_

Those two forms of casts are quite different from what's happening now.

``` java
boolean b = ((CarCriteria1)(c -> c.getColor().equals("Red"))).test(Car1.withGasColorPassengers(0,"Red"));
```

This form of cast expression literally decides what will be created in the first place. And is quite different.

Now, notice that a single lambda expression could potentially be compiled into multiple different interfaces depending
on the context.

```java
    boolean b2 = ((Strange)(c -> c.getColor().equals("Red"))).anotherTestStuff(Car1.withGasColorPassengers(0,"Red"));

```

Potentially confusing, and that's one of the reasons that we might choose to put the argument types into the lambda's
formal parameter list. Because that could be sufficient in some cases to resolve that ambiguity. 

-------------------------------------------

As a general rule, you shouldn't expect to be creating your own interfaces, just to work with lambdas. T

The vast majority of likely operations, whether they have zero, one, or two arguments, including things dealing with
primitive return types, or primitive arguments, have probably been built for you.

And you should use the features of the java.util.function package when you need to create lambdas.


Generically typed interfaces
– Predicate<T> —T in, boolean out
– Function<T,R> —T in, R out
– Consumer<T> —T in, nothing (void) out
– Supplier<T> —Nothing in, T out
– BinaryOperator<T> —Two T’s in, T out



## Predefined Functional Interface

Defined in java.util.function

|1.| Predicate &lt;T> | test(), takes T in, returns boolean | Used with filter() in Stream API|
|2.| Function<T,R> |apply(T k), T in return user defined TYPE R | Used with map() in Stream API
|3.| Consumer&lt;T> |accept(), T in, void out |Used with forEach() method |
|4.| Supplier&lt;T> |get(), nothing in, T out |Used with .collect tereminal operator|

