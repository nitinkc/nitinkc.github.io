---
title:  "Composition"
date:   2023-11-06 08:30:00
categories: ['Java','Design Patterns', "Object Oriented Design"]
tags: ['Java']
---

{% include toc title="Index" %}

# Composition

* Also known as whole-part relationship
* has - a relationship
* primarily for code re-use (both state and behaviour) - for inheritache
* Composition is about delegating. Delegating certain aspects of its functional behaviour of A to B
```java
class A{
    public void foo(){
        
    }
}

class B{
    public void bar(){
        
    }
}
```

A -> B

Runtime time instance of A has a reference to a run time instance of B