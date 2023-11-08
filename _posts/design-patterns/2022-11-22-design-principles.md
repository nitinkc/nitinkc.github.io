---
title:  "Design Principles"
date:   2022-11-22 08:30:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

A good design reads like a story and not like a puzzle


DP #1 : take what varies and encapsulate it. It will not affect the rest of our code.

DP #2 : program to an interface/super type and not an implementation
the actual runtime object is not locked into the code
the type of variable should be supertype/interface

    Dog dog = new Dog();
    Animal dog = new Dog();
    List<String> str = new ArrayList<>();

what is behaviour of an object and whats is its state

DP #3 : Favor composition over inheritance. good to separate behaviour from implementation

composition : HAS-A relationship, whole-part relationship
you can encapsulate stuff into its own set of classes . HINT
you can CHANGE the behaviour at RUNTIME with interfaces

inheritance : IS-A relationship

aggregation : 

