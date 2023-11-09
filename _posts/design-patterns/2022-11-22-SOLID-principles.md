---
title:  "SOLID Principles"
date:   2022-11-22 08:30:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}


### Supplier
```java
public interface Supplier<T> {
    T get();
}
```

```java
//Static method Reference
Supplier<LocalDate> s1 = LocalDate::now;
//Lambda Expression
Supplier<LocalDate> s2 = () -> LocalDate.now();
```

# SOLID Principles

**S -> single responsibility principle**
* a class or an entity, should have only one reason to change
* loosely coupled or low coupled design

**O -> Open closed principle**
* Open to Extension
* Closed for modification
* Extend vs implement
* Eg : Strategy design pattern, Template design pattern

**L -> Liskov substitution principle**
* subclasses should be able to be used interchangeably with their base class
* Overriding methods should not violate the behavior expected from the superclass
```java
class Shape {
    public double area() {
        return 0.0; // Default area for a generic shape
    }
}

class Circle extends Shape {
    @Override
    public double area() {
        return Math.PI * radius * radius;
    }
}

class Rectangle extends Shape {
    @Override
    public double area() {
        return width * height;
    }
}
  
Shape circle = new Circle(5.0);
Shape rectangle = new Rectangle(4.0, 3.0);
```
We can substitute derived objects (Circle and Rectangle) for the base object (Shape) without affecting the correctness of the program.

**I -> Interface Segregation principle**
* clients should not be forced to depend on interfaces they do not use
* it's better to have **many specific interfaces rather than a single** large, monolithic interface.

**D -> Dependency Inversion Principle (Inversion of control)**



## SOLID Principles in Detail

### 1. Single Responsibility Principle (SRP)

The SRP states that a class should have only one reason to change. In other words, a class should have only one responsibility or job to do. This ensures that changes to one part of the software do not affect other unrelated parts.

In Java, adhere to SRP by creating classes that are focused on a single purpose. For example, separate the business logic from the presentation logic, database access, and other concerns.

### 2. Open/Closed Principle (OCP)

The OCP states that classes should be open for extension but closed for modification. This means that you should be able to add new functionality to a class without changing its existing code.

In Java, follow OCP by using interfaces and abstract classes to define behavior that can be extended by subclasses. This allows you to introduce new functionality through implementing new classes without altering the existing ones.

### 3. Liskov Substitution Principle (LSP)

The LSP states that
* objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program.
* In other words, **subclasses should be able to be used interchangeably with their base class**.

In Java, uphold LSP by ensuring that subclasses adhere to the contract defined by their superclass.
* Overriding methods should not violate the behavior expected from the superclass.

### 4. Interface Segregation Principle (ISP)
* The ISP states that clients should not be forced to depend on interfaces they do not use.
* In other words, it's better to have **many specific interfaces rather than a single** large, monolithic interface.

* In Java, follow ISP by creating smaller, focused interfaces that cater to specific sets of behaviors.
* This way, classes can implement only the interfaces they need, reducing unnecessary dependencies.

### 5. Dependency Inversion Principle (DIP)

* The DIP states that **high-level modules should not depend on low-level modules**.
    * Both should depend on abstractions.
    * Furthermore, abstractions should not depend on details; details should depend on abstractions.

In Java, practice DIP by using dependency injection.
* This involves passing dependencies (e.g., other objects, services) to a class through
    * constructors or
    * setter methods, rather than having the class create its dependencies directly.
      By doing so, the class becomes more flexible and easier to test.

By applying the SOLID principles in your Java code, you can create more maintainable, flexible, and scalable software that is easier to understand, modify, and extend.

Based on the above principles, we have

# Three types of design Patterns

1. Creational Design Patterns - Singleton, Builder, Factory (Static Factory)
2. Behavioral Design pattern - Strategy Design Pattern (already part of Java Language Design)
3. Structural Design pattern