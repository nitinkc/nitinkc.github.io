---
title:  "Strategy Pattern"
date:   2023-11-06 08:30:00
categories: ['Java','Design Patterns']
tags: ['Java']
---
{% include toc title="Index" %}


# Strategy pattern

We want to vary a small part of an algorithm while
keeping the rest of the algorithm the same.

Language design is program design : Programming language influences our design. 
Language restricts what we can do

Design patterns often kick in to fill-in the gaps of a programming language.

Design Patterns can compensate the powerlessness of a language

A more power a language is, the less we talk about  design patterns as these naturally become the features
of the language.

In the past, how did we use strategy

We created an interface and then a bunch of classes
Then wire them together often using factories. Quite an effort.

Lambdas are lightweight strategies


Strategies are often a single method or function.
So, functional interfaces and lambdas work really well


Strategies are Stateless. So its easier to pull them as a **Static method** and thus instance reference

```java
//Bringing in some Business Strategy
totalValuesUsingStreams(numbers, BusinessLogic::someStrategy)

```

With the introduction is Lambdas, Strategy pattern has become feature of the Language 
thus instead of Design patterns its design practise in Java now.

No need to put efforts to create interfaces and classes


