---
title:  "Spring Bean Scope"
date:   2023-01-31 03:53:00
categories: [Microservices]
tags: [Microservices]
---

{% include toc title="Index" %}

A bean is simply a Spring-managed component or object.

It is an instance of a Java class that is instantiated, configured, and managed
by the **Spring IoC (Inversion of Control) container**.

Beans are the fundamental building blocks of a Spring application.

# Bean Scope

## **Singleton Scope**:
Singleton scope is the **default scope** in Spring, where only one instance of the
bean is created and shared throughout the application context.

- The singleton scope is the **default** scope in Spring.
- The `Gang of Four` defines Singleton as having one **instance per ClassLoader**.
    - in their book **Design Patterns: Elements of Reusable Object-Oriented Software**-,
      ensures that a class has only one instance and provides a global point of
      access to it.

- However, Spring singleton is defined as one instance of bean definition per
  container.
    - In the Spring Framework, a singleton bean is defined as a bean that is
      instantiated only once per Spring IoC container.
    - This means that within a single container, there will be only one instance
      of a bean definition.

```java
   @Component
   public class SingletonBean {
       // Bean definition
   }
```
### **Use Cases**:
1. **Stateless Services**:
    - Beans that don’t hold any client-specific or mutable data.
    - Example: Service classes, DAOs.

2. **Configuration Beans**:
    - Classes used for setting up application-wide configurations.
    - Example: `@Configuration` annotated beans.

3. **Shared Utilities**:
    - Beans providing reusable functionality, like logging or caching utilities.

### **Advantages**:
- Efficient memory usage.
- Shared state across the application.

## **Prototype Scope**:
Prototype scope instructs the Spring IoC container to create a new instance of
the bean whenever it is requested.

```java
@Component
@Scope("prototype")
public class PrototypeBean {
   // Bean definition
}
```
### **Description**:
- A new instance of the bean is created every time it is requested.

### **Use Cases**:
1. **Stateful Components**:
    - Beans holding temporary or client-specific data.
    - Example: Objects with user session details.

2. **Expensive Objects**:
    - Large objects that need different configurations for each use.
    - Example: Heavy object initialization with variable parameters.

3. **Multi-threaded Applications**:
    - Beans where thread-safety requires separate instances per thread.

### **Advantages**:
- Isolation between instances.
- Ideal for beans with mutable state.

## **Request Scope**:
Request scope is used in web-based applications, where a new instance of the
bean is created once per HTTP request.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestScopedBean {
   // Bean definition
}
```

### **Description**:
- A new instance of the bean is created for each HTTP request in a web application.

### **Use Cases**:
1. **Request-Specific Data Processing**:
    - Beans holding data that is specific to a single HTTP request.
    - Example: Request validation or processing logic.

2. **Controllers and Form Handlers**:
    - Beans to manage user input and request processing in MVC applications.

3. **Temporary Attributes**:
    - Beans required to calculate data for a single view or response.

### **Advantages**:
- Scoped to a single HTTP request lifecycle.
- Avoids memory leaks from request-specific data in global beans.


## **Session Scope**:
Session scope is tied to the HTTP session lifecycle, with a new instance of the
bean created once per HTTP session.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionScopedBean {
   // Bean definition
}
```
### **Description**:
- A new instance of the bean is created for each HTTP session in a web application.

### **Use Cases**:
1. **User-Specific Session Data**:
    - Beans holding user preferences, shopping cart data, or session-specific attributes.

2. **Authentication and Authorization**:
    - Beans to store user credentials or session tokens during the session lifecycle.

3. **Stateful Web Applications**:
    - Applications requiring user-specific state across multiple requests.

### **Advantages**:
- Isolated state per user session.
- Useful for managing user-specific resources.

## **Application Scope**:
Application scope represents a single instance of the bean per servlet context,
created once when the application starts up.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_APPLICATION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ApplicationScopedBean {
   // Bean definition
}
```

### **Description**:
- A single instance of the bean is created for the entire servlet context.

### **Use Cases**:
1. **Application-Wide Resources**:
    - Beans managing shared resources, like global settings or configuration.

2. **Servlet Context Attributes**:
    - Beans wrapping context-level attributes or data.

3. **Cache or Resource Pools**:
    - Objects reused by all users, such as database connections or thread pools.

### **Advantages**:
- Shared across the entire application lifecycle.
- Suitable for long-lived resources.


# **Comparison of Scopes**

| Scope           | Instance Per              | Typical Use Case                | Lifetime                  |
|:----------------|:--------------------------|:--------------------------------|:--------------------------|
| **Singleton**   | Application               | Stateless services, utilities   | Application lifecycle     |
| **Prototype**   | Each request or injection | Stateful or temporary objects   | Per request/injection     |
| **Request**     | HTTP request              | Request-specific logic          | HTTP request lifecycle    |
| **Session**     | HTTP session              | User-specific data              | HTTP session lifecycle    |
| **Application** | Servlet context           | Global settings, resource pools | Servlet context lifecycle |
