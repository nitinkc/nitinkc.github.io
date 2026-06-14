---
title: Singleton Design Pattern
date: 2023-11-06 08:30:00
categories:
- Design Patterns
tags:
- Java
- OOP
---

{% include toc title="Index" %}

Singleton Pattern -> restricts the instantiation of a class to one object.

* Ensure a class only has **one instance** and provide a global point of access
  to it.
  * Eg: **DB Connection needs to be a singleton**
* It is used to control the number of objects created by preventing **external
  instantiation and modification**.
* This is useful when exactly one object is needed to coordinate actions across
  the system.

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
  private static SingletonDemo singletonDemo;//Lazy Evaluation
  ```

* public static method (get()/of()/getInstance() - convention) is the only place
  that can get an object.

## Eager Evaluation

```java
private static final SingletonDemo singletonDemo = new SingletonDemo();//Eager Evaluation
```

## Lazy Evaluation

```java
//Lazy mode
private static SingletonDemo singletonDemo;//Lazy Evaluation

public static SingletonDemo of(){
    if(null == singletonDemo){
        System.out.println("First time call");
        singletonDemo = new SingletonDemo();//Preventing from creating multiple instances
    }
    return singletonDemo;
}
```

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
