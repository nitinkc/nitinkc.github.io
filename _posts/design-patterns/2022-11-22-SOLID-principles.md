---
categories: Design Patterns
date: 2022-11-22 08:30:00
tags:
- SOLID
- OOP
- Principles
- Best Practices
title: SOLID Principles
---

{% include toc title="Index" %}

# **S -> single responsibility principle**

* a class or an entity should have **only one reason** to change
* loosely coupled or low-coupled design

In Java, adhere to SRP by **creating classes** that are **focused on a single
purpose**.
For example, separate the business logic from the presentation logic, database
access, and other concerns.

- Controllers
- Service
- Repository or DAO classes

# **O -> Open closed principle**

* Open **to Extension**
* Closed **for modification**

- you should be able to add new functionality to a class without changing its
  existing code.

In Java, follow OCP by **using interfaces and abstract classes** (to define
behavior that can be extended by subclasses).

- This allows introducing new functionality through **implementing new classes**
  without altering the existing ones.

**Extend vs implement**

* Eg : Strategy design pattern, Template design pattern

# **L -> Liskov substitution principle**

Same as **POLYMORPHISM**.

* subclasses should be able to be used interchangeably with their base class
* in-short, objects of a superclass should be replaceable with objects of a
  subclass (without affecting the correctness of the program)
* Overriding methods should not violate the behavior expected from the
  superclass

In Java, uphold LSP, by ensuring that **subclasses adhere to the contract
defined by their superclass**.

* Overriding methods should not violate the behavior expected from the
  superclass.

We can substitute derived objects (Circle and Rectangle) for the base object (
Shape) without affecting the correctness of the program.

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

# **I -> Interface Segregation principle**

* clients **should not be forced to depend** on interfaces they do not use
* it's better to have **many specific interfaces rather than a single** large,
  monolithic interface.

In Java, follow ISP by creating **smaller, focused interfaces** that cater to
specific sets of behaviors.

* This way, classes can implement only the interfaces they need, reducing
  unnecessary dependencies.

# **D -> Dependency Inversion Principle (Inversion of control)**

* The DIP states that **high-level modules should not depend on low-level
  modules**.
    * Both should depend on abstractions.
    * Furthermore, abstractions should not depend on details; details should
      depend on abstractions.

In Java, practice DIP by using **dependency injection**.

* This involves passing dependencies (e.g., other objects, services) to a class
  through
    * constructors (constructor injection) or
    * setter methods, rather than having the class create its dependencies
      directly.

By doing so, the class becomes more flexible and easier to test.

@startuml
' Define the EmailSender class with its method
class EmailSender {

+ sendEmail(message: String)
  }

' Define the NotificationService class with its dependency on EmailSender
class NotificationService {

- emailSender: EmailSender

+ NotificationService(emailSender: EmailSender)
+ sendNotification(message: String)
  }

' Show that NotificationService directly depends on EmailSender
NotificationService --> EmailSender : uses

' Add annotation to explain the dependency
note right of NotificationService
**High-level module**
Directly depends on
EmailSender for sending
notifications.
end note

' Add annotation to explain the EmailSender class
note right of EmailSender
**Low-level module**
Provides the concrete
implementation for sending
emails.
end note

@enduml

### Problems with this approach:

- **Tight coupling**: NotificationService is tightly coupled to EmailSender.
  Changing the email sending logic requires modifying NotificationService.
- **Hard to test**: It’s difficult to test NotificationService in isolation
  because it directly creates EmailSender.

@startuml

' Define the MessageSender interface
interface MessageSender {

+ send(message: String)
  }

' Define the EmailSender class implementing MessageSender
class EmailSender {

+ send(message: String)
  }

MessageSender <|-- EmailSender

' Define the NotificationService class which depends on MessageSender
class NotificationService {

- messageSender: MessageSender

+ NotificationService(messageSender: MessageSender)
+ sendNotification(message: String)
  }

' Draw dependencies
NotificationService --> MessageSender : depends on

' Add annotation to explain the dependency
note right of NotificationService
**High-level module**
Directly depends on
MessageSender for sending
notifications.
end note

' Add annotation to explain the EmailSender class
note right of EmailSender
**Low-level module**
Implements MessageSender
and provides a concrete
implementation for sending
messages.
end note

' Add annotation to explain the MessageSender class
note right of MessageSender
**Abstraction** (MessageSender interface).

The high-level module (**NotificationService**)
depend on this abstraction.

specific implementation in
**Low-level module(EmailSender)**

* The DIP states that **high-level modules
  should not depend on low-level modules**.
* Both should depend on abstractions
  end note
  @enduml

### Benefits of this approach:

- **Loose coupling**: NotificationService is not dependent on EmailSender but
  rather on the MessageSender interface. It can work with any implementation of
  MessageSender.
- **Easier testing**: You can now inject mock implementations of MessageSender
  for testing purposes.
- **Flexibility**: Changing the implementation of MessageSender (e.g., using a
  SMSSender instead of EmailSender) requires minimal changes in the
  NotificationService.

By applying the SOLID principles in your Java code, you can create more
maintainable, flexible, and scalable software that is easier to understand,
modify, and extend.
Based on the above principles, we have

# Three types of design Patterns

1. **Creational** - Singleton, Builder, Factory (Static Factory)
2. **Behavioral** - Strategy Design Pattern (already part of Java Language
   Design)
3. **Structural** - Decorator, Facade

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