---
title: Factory Design Pattern
date: 2023-11-06 08:30:00
categories:
- Design Patterns
tags:
- Java
- OOP
---

{% include toc title="Index" %}

# Factory pattern

Polymorphism

extensibility

What is the worst keyword in Java from polymorphism angle

* final
* instanceof
* static

**new**

- new ClassName() //tight coupling
- So many patterns to fight with new, especially in Spring
- `new` introduces tight coupling. New is not polymorphic in Java, C++, .Net but it is in Ruby
- Python or Kotlin doesn't even have new

> Golden Rule : interfaces are better than abstract classes

Interfaces can have implementations (default methods) however they cannot have non-final fields

Interfaces cannot carry state but an abstract class carry a state.

# Abstract Factory vs. Factory Method

Class vs method

Factory Method : A class or an interface relies on a derived class to provide
the implementation whereas the base provides the common behavior

uses inheritance as design tool

uses factory METHOD

> Abstract Factory uses delegation as design tool