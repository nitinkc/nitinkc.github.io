---
title:  "Singleton Design Pattern"
date:   2023-11-06 08:30:00
categories: ['Java','Design Patterns']
tags: ['Java']
---

{% include toc title="Index" %}

Singleton Pattern -> restricts the instantiation of a class to one object.
* Ensure a class only has **one instance** and provide a global point of access to it.Eg: **DB Connection needs to be a singleton**
* It is used to control the number of objects created by preventing **external instantiation and modification**.
* This is useful when exactly one object is needed to coordinate actions across the system.

# How ?

* private constructor - so that no other class can instantiate a new object.

```java
class SingletonDemo {
    ....
    private SingletonDemo() {
    }
}
```
* private reference or instance - no external modification.

```java
    //private static SingletonDemo singletonDemo = new SingletonDemo();//Eager Evaluation
    private static SingletonDemo singletonDemo;//Eager Evaluation
```

* public static method (get()/of()/getInstance() - convention) is the only place that can get an object.

## Eager Evaluation
```java
//Lazy mode
public static SingletonDemo of(){
    if(null == singletonDemo){
        System.out.println("First time call");
        singletonDemo = new SingletonDemo();//Preventing from creating multiple instances
    }
    return singletonDemo;
}
```

## Lazy Evaluation
```java
private static SingletonDemo singletonDemo = new SingletonDemo();//Eager Evaluation
```

There are four different ways to create objects in java:
1.     Using new keyword
2.     Using Class.forName()://reflection
3.     Using clone():
4.     Using Object Deserialization: Using new Intance() method


Private constructor **doesn't protect** from instantiation via **reflection**.

Joshua Bloch (Effective Java) proposes a better implementation of Singleton

```java
//This ENUM acts as a singleton bean
public enum SingletonDemoEnum {
    //INSTANCE;
    INSTANCE();

    public String doSomething(){
        return "Do something inside Enum";
    }
}

```

Access thew singleton object via
```java
SingletonDemoEnum object = SingletonDemoEnum.INSTANCE;//TODO: Whats is INSTANCE
```

# What does Spring use