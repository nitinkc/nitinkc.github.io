---
title:  "Polymorphism"
date:   2022-08-06 15:45:00
categories: ['Java']
tags: ['Java']
---


Overriding => same signature, child and parent but different implementation

private and final cannot be overridden

static methods cannot be overridden BUT no contribution in Polymorphism
(no dynamic binding)

also static method in subclass is hidden (if extended) by static method of parent class

Cannot reduce visibility

Covariant return type

After java 5 return type may vary i.e possible to override method by changing return type

## Dynamic Binding

```java
Parent p = new Child();

        p.m1();// dynamic binding, at run time, it invokes childs m1()
```


-------------------------------------
methods signature => name + Argument (type and order)

Overloading is => load a method with diff. argument



# Abstract Class

* Can't be instantiated
* public because need to be given out
* still define its constructors => invoked in constructors of subclass.
* 0 to 100% abstraction
* java.lang.Number class

You Program for Interfaces rather than implementation

Abstraction is applied in the process of identifying s/w artifacts to model the problem domain

The Chef analogy : customer -> Head chef -> {indian, chinese, Italian, Mexican} ->> multiple chefs

anyone can leave from the junior chefs and new can come. Customers need not be worried

REAL AIM : FLEXIBILITY (code can be changed but the abstraction remains the same) and not hiding

Segregation of code, free to change without affecting the business

Constructor chaining <=> for inheritance

IT IS POLYMORPHISM WHICH LINKS ABSTRACT CODE TO CONCRETE IMPLEMENTATION.



 /* Object of same class (List) but behave differently and behaviour depends on object being invoked */
        List linkedList = new LinkedList();
        List arrayList = new ArrayList();

        // Always occurs with Inheritence with a special case
        //child behaviour is changed hiding parent

        // Treat an object of any subclass as if it were an object of parent class

        // Dynamic binding makes polymorphism possible. Compiler is not able to resolve the call. Binding
        // id done at runtime

        // Binding : Relating a method call to a method

        /* Static Binding or Overloading: Happens in compile time
         * uses type information (class in Java) for binding, binding -> relating methods to methods calls
         * private, static, final, static variables } methods, not participation in polymorphism
         */

        /* Dynamic Binding : all instance methods
         * Virtual methods are bounded during runtume object
         * No concept of compiletime polymorphism.
         */


         * Dynamic polymorphism in Java is achieved by method overriding
 * As the method to call is determined at runtime, this is called dynamic binding or late binding.
 */


 