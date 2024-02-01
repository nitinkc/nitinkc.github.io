---
# layout: static
title:  "Dependency Injection"
date:   2022-02-10 20:55:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

# Dependency Injection Concepts using Spring 5

**IOC(Inversion Of Control)**

Giving control to the container to get instance of object is called Inversion of Control. 
* instead of you are creating object using new operator, let the container do that for you.

**DI(Dependency Injection)**:  Way of injecting properties to an object is called Dependency injection.

We have three types of Dependency injection
* Constructor Injection
* Setter/Getter Injection
* Interface Injection

Spring support only Constructor Injection and Setter/Getter Injection.

### Dependency Injection is done in 3 ways

1. By class properties - least preferred 
  * Using private properties is <span style="color:red">**EVIL**</span>
2. By Setters - Area of much debate
	
```java
private GreetingService greetingService;
@Autowired
//@Qualifier("setterGreetingService")
public void setGreetingService(@Qualifier("setterGreetingService") GreetingService greetingService) {
    this.greetingService = greetingService;
}
```

3. By Constructor - Most Preferred
```java
private GreetingService greetingService;
//Constructor, With Spring 5 no need to explicitly mention @Autowired, but its a good practice
public A3ConstructorInjectedController(GreetingService greetingService) {
    this.greetingService = greetingService;
}
```


#### DI via Interfaces is highly preferred
* Allows runtime to decide implementation to inject
* Follows Interface Segregation Principle of SOLID
* Also, makes your code more testable

`@Primary` - Multiple beans of the same type and one is intended to go in by default 
           
`@Profile` - making a profile active from the application.properties

default profile is added 

`@Profile({"en","default"})`

**Component Scan** : 

By default, the package containing the main method is scanned. In addition to it, to scan other
packages, following annotation is used.

```java
@ComponentScan(basePackages = {"com.spring5.concepts","com.spring5.services"})
``` 


