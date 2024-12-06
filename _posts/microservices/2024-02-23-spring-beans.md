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

# Key characteristics of Spring beans:

**Managed by Spring Container**: Beans are managed by the Spring IoC container,
which handles their lifecycle, configuration, and dependencies.

**Configurable**: Beans can be configured using various mechanisms provided by
Spring, such as XML-based configuration, Java-based configuration, or
annotation-based configuration.

**Singleton by Default**: By default, beans are singletons in the Spring
context,
meaning that the Spring container creates only one instance of each bean and
shares it throughout the application.

**Dependency Injection**: Beans can be injected with dependencies, either
through
constructor injection, setter injection, or field injection. This allows for
loose coupling between components and facilitates easier testing and
maintenance.

**Scopes**: Spring beans can have different scopes, such as singleton,
prototype,
request, session, etc., which define the lifecycle and visibility of bean
instances.

Overall, beans in Spring provide a flexible and powerful way to manage
components
and their dependencies in a Spring application, promoting modularity,
reusability, and maintainability.

# Bean Scope

## **Singleton Scope**:

Singleton scope is the default scope in Spring, where only one instance of the
bean
is created and shared throughout the application context.

   ```java
   @Component
   public class SingletonBean {
       // Bean definition
   }
   ```

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


# **Comparison of Scopes**

| Scope           | Instance Per              | Typical Use Case                | Lifetime                  |
|:----------------|:--------------------------|:--------------------------------|:--------------------------|
| **Singleton**   | Application               | Stateless services, utilities   | Application lifecycle     |
| **Prototype**   | Each request or injection | Stateful or temporary objects   | Per request/injection     |
| **Request**     | HTTP request              | Request-specific logic          | HTTP request lifecycle    |
| **Session**     | HTTP session              | User-specific data              | HTTP session lifecycle    |
| **Application** | Servlet context           | Global settings, resource pools | Servlet context lifecycle |
