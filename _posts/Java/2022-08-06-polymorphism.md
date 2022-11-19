---
title:  "Polymorphism"
date:   2022-08-06 15:45:00
categories: ['Java']
tags: ['Java']
---

## Overriding in Inheritance

Overriding => same signature, child and parent but different implementation

* private and final methods cannot be overridden

* Static methods cannot be overridden BUT no contribution in Polymorphism
(no dynamic binding)

* Static method in subclass is hidden (if extended) by static method of parent class

* Cannot reduce visibility

* Covariant return type

After java 5 return type may vary i.e possible to override method by changing return type

## Dynamic Binding

```java
Parent p = new Child();
List<String> list = new ArrayList();

p.m1();// dynamic binding, at run time, it invokes childs m1()
```

---
* Methods signature does not involve return Type => method name + Argument/Parameters (type and order)
```java
public List<BusinessDto> myMethod(String a, Integer b);
// Method Signature = myMethod(String a, Integer b);
```
* Overloading is when method is loaded with different argument
```java
//Overloaded methods
public List<BusinessDto> myMethod(String a);
public List<BusinessDto> myMethod(String a, Integer b);
public List<BusinessDto> myMethod(String a, Integer b, Float c);
```
# Abstract Class

* Can't be instantiated
* public because need to be given out
* Still define its constructors => invoked in constructors of subclass.
* 0 to 100% abstraction
* java.lang.Number class

> You Program for Interfaces rather than implementation

* Abstraction is applied in the process of identifying s/w artifacts to model the problem domain

* The Chef analogy : `{Customer -> Waiter}` -> {Head chef -> {Indian, Chinese, Italian, Mexican} ->> multiple chefs/cooks} . 
Anyone can leave (deprecated) from the junior chefs and new can come. Customers need not be worried

REAL AIM : 
* FLEXIBILITY (code can be changed but the abstraction remains the same) and not hiding
* Segregation of code, free to change without affecting the business

Constructor chaining <=> for inheritance

> IT IS POLYMORPHISM WHICH LINKS ABSTRACT CODE TO CONCRETE IMPLEMENTATION.

### Binding 

Binding : Relating a method call to a method

```java
// Object of same class (List) but behave differently and behaviour depends on object being invoked

List<String> linkedListObj = new LinkedList()<>;
List<String> arrayListObj = new ArrayList()<>;
```

// Always occurs with Inheritence with a special case.

// Child behaviour is changed hiding parent.

// Treat an object of any subclass as if it were an object of parent class.

### Dynamic Binding

**Binding is done at runtime**

Dynamic binding makes polymorphism possible. Compiler is not able to resolve the call. 

* Dynamic polymorphism in Java is achieved by **method overriding**
* Dynamic Binding : all instance methods
* **Virtual methods** are bounded during runtume object
* No concept of compile time polymorphism.
* Because the method to call gets determined at runtime, this is called dynamic binding or late binding.

### Static Binding

* Static Binding or **Method Overloading**
* Happens in **compile time**
* Uses type information (class in Java) for binding.
* private, static, final, static variables methods, not participate in polymorphism.