---
title:  "Spring Beans"
date:   2023-01-31 03:53:00
categories: [Microservices]
tags: [Microservices]
---

{% include toc title="Index" %}

a bean is simply a Spring-managed component or object. It is an instance of a Java class that is instantiated, configured, and managed by the Spring IoC (Inversion of Control) container. Beans are the fundamental building blocks of a Spring application.

Key characteristics of Spring beans include:

Managed by Spring Container: Beans are managed by the Spring IoC container, which handles their lifecycle, configuration, and dependencies.

Configurable: Beans can be configured using various mechanisms provided by Spring, such as XML-based configuration, Java-based configuration, or annotation-based configuration.

Singleton by Default: By default, beans are singletons in the Spring context, meaning that the Spring container creates only one instance of each bean and shares it throughout the application.

Dependency Injection: Beans can be injected with dependencies, either through constructor injection, setter injection, or field injection. This allows for loose coupling between components and facilitates easier testing and maintenance.

Scopes: Spring beans can have different scopes, such as singleton, prototype, request, session, etc., which define the lifecycle and visibility of bean instances.

Overall, beans in Spring provide a flexible and powerful way to manage components and their dependencies in a Spring application, promoting modularity, reusability, and maintainability.


1. **Singleton Scope**:
    - **Definition**: Singleton scope is the default scope in Spring, where only one instance of the bean is created and shared throughout the application context.
    - **Example**:
      ```java
      @Component
      public class SingletonBean {
          // Bean definition
      }
      ```

2. **Prototype Scope**:
    - **Definition**: Prototype scope instructs the Spring IoC container to create a new instance of the bean whenever it is requested.
    - **Example**:
      ```java
      @Component
      @Scope("prototype")
      public class PrototypeBean {
          // Bean definition
      }
      ```

3. **Request Scope**:
    - **Definition**: Request scope is used in web-based applications, where a new instance of the bean is created once per HTTP request.
    - **Example**:
      ```java
      @Component
      @Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
      public class RequestScopedBean {
          // Bean definition
      }
      ```

4. **Session Scope**:
    - **Definition**: Session scope is tied to the HTTP session lifecycle, with a new instance of the bean created once per HTTP session.
    - **Example**:
      ```java
      @Component
      @Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
      public class SessionScopedBean {
          // Bean definition
      }
      ```

5. **Application Scope**:
    - **Definition**: Application scope represents a single instance of the bean per servlet context, created once when the application starts up.
    - **Example**:
      ```java
      @Component
      @Scope(value = WebApplicationContext.SCOPE_APPLICATION, proxyMode = ScopedProxyMode.TARGET_CLASS)
      public class ApplicationScopedBean {
          // Bean definition
      }
      ```

