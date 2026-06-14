---
layout: post
title: "Java Servlets, Servlet Containers, and How to Build HTTP APIs Without Them"
date: 2026-03-21
categories: [java, web, backend]
tags: [servlet, spring-boot, reactive]
---


## What Is a Servlet?

A **servlet** is a Java class that handles HTTP requests and produces responses. It follows the `javax.servlet.HttpServlet` (or `jakarta.servlet.HttpServlet`) API, where you override methods like `doGet()`, `doPost()`, etc.

```java
public class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        res.setContentType("text/plain");
        res.getWriter().write("Hello, World!");
    }
}
```

Crucially, a servlet **has no `main` method**. It is just a class — it cannot run on its own. Something else needs to host it.

---

## What Is a Servlet Container?

A **servlet container** (also called a *web container*) is the runtime environment that actually does the heavy lifting:

- **Listens** on a TCP port (e.g. 8080)
- **Parses** raw HTTP bytes into `HttpServletRequest` objects
- **Manages** the servlet lifecycle — `init()`, `service()`, `destroy()`
- **Routes** incoming requests to the correct servlet
- **Writes** the `HttpServletResponse` back to the client socket

Well-known servlet containers include **Apache Tomcat**, **Eclipse Jetty**, **JBoss Undertow**, and **GlassFish**.

The key value proposition: they implement the **Servlet Specification** (part of Jakarta EE), so your servlet code is portable across all compliant containers.

---

## Do You Need a Servlet Container?

**No.** The servlet API is just one abstraction over raw HTTP. There are several other approaches, ranging from low-level to high-level.

### 1. Raw `ServerSocket` (Pure JDK)

You can handle HTTP at the socket level with nothing but the JDK. You're responsible for parsing the HTTP protocol yourself — practical for learning, painful in production.

### 2. JDK Built-in HTTP Server

Since Java 6, the JDK ships with `com.sun.net.httpserver` — a lightweight HTTP server with no external dependencies:

```java
HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
server.createContext("/hello", exchange -> {
    byte[] body = "Hello!".getBytes();
    exchange.sendResponseHeaders(200, body.length);
    exchange.getResponseBody().write(body);
    exchange.close();
});
server.start();
```

Good for tooling, internal services, or quick prototypes. Not recommended for high-traffic production use.

### 3. Netty

[Netty](https://netty.io/) is an asynchronous, event-driven network framework. It works at the channel/buffer level — no servlet API involved. It's the backbone of many modern Java frameworks and offers very high throughput.

### 4. Modern Frameworks with Embedded Servers

Most modern Java frameworks embed their own server and bypass (or wrap) the servlet API entirely:

| Framework | Underlying Server | Uses Servlet API? |
|:----|:------|:-------|
| Spring Boot (MVC) | Embedded Tomcat | Yes |
| Spring Boot (WebFlux) | Embedded Netty | No |
| Micronaut | Netty | No |
| Quarkus | Vert.x / Netty | No |
| Vert.x | Netty | No |
| Javalin | Embedded Jetty | Thin wrapper |

Reactive frameworks like **Spring WebFlux**, **Micronaut**, and **Vert.x** go fully non-blocking and have no dependency on the servlet spec at all.

### 5. Java 21+ Virtual Threads (Project Loom)

With **virtual threads** introduced in Java 21, the traditional argument against blocking I/O (that it doesn't scale) largely disappears. You can write straightforward, blocking-style code using a simple `ServerSocket` or the JDK HTTP server and get excellent concurrency — without a servlet container, and without going reactive.

---

## Beans vs. Servlets — What's the Difference?

If you've used Spring, you've heard the word **bean** constantly. It has nothing to do with the Servlet API — here's how to keep them straight.

### Java Bean

A **Java Bean** is just a plain Java class following a few conventions:

- A public no-argument constructor
- Private fields
- Public getters and setters

The word "bean" simply means *a managed, reusable object*. Nothing HTTP-specific about it.

### Spring Bean

A **Spring Bean** is any object whose lifecycle is managed by the **Spring IoC (Inversion of Control) container**, also called the `ApplicationContext`. Spring:

1. **Creates** the object for you (you don't call `new`)
2. **Injects** its dependencies automatically
3. **Destroys** it when the context shuts down

You declare a Spring Bean using annotations like `@Component`, `@Service`, `@Repository`, or `@Bean` inside a `@Configuration` class.

```java
@Service
public class UserService {
    // Spring creates this, manages it, injects it wherever needed
}
```

### So Where Do Servlets Fit?

A servlet is managed by the **servlet container** (e.g. Tomcat) — not by Spring. These are two separate container systems:

| | Managed By | Examples |
| --- | --- | --- |
| **Spring Beans** | Spring `ApplicationContext` | `@Service`, `@Controller`, `@Repository` |
| **Servlets** | Servlet Container | `HttpServlet` subclasses |

### How Spring Boot Bridges the Two

When you use Spring Boot with Spring MVC, Spring registers a single servlet called **`DispatcherServlet`** with Tomcat. That servlet is the *bridge*:

```text
HTTP Request
    → Tomcat (servlet container)
        → DispatcherServlet (the one servlet)
            → Spring ApplicationContext
                → your @RestController bean
```

Your `@RestController` classes are **Spring Beans** — Spring manages them. They are **not** servlets. The `DispatcherServlet` is the only actual servlet, and it delegates everything to Spring's bean world.

> **Rule of thumb:** In a Spring Boot app, you almost never write a servlet. You write beans (`@RestController`, `@Service`, etc.) and let Spring + `DispatcherServlet` handle the plumbing.

---

## Summary

| Approach | Dependencies | Servlet API | Use Case |
| --- | --- | --- | --- |
| Raw `ServerSocket` | None | No | Learning / custom protocols |
| `com.sun.net.httpserver` | None (JDK) | No | Tooling, internal services |
| Netty | Netty only | No | High-performance, async |
| Spring Boot MVC | Spring + Tomcat | Yes (embedded) | Standard REST APIs |
| Spring WebFlux | Spring + Netty | No | Reactive / streaming APIs |
| Micronaut / Quarkus | Framework | No | Cloud-native microservices |

Servlets and servlet containers are the *traditional* Java web model — solid, portable, and well-understood. But modern frameworks, reactive runtimes, and Project Loom have made it entirely practical to build production HTTP APIs in Java without ever touching the servlet API.
