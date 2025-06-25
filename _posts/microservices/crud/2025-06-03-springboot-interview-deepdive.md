---
title:  "SpringBoot Interview - Deep Dive"
date:   2025-06-03 11:50:00
categories: Spring Microservices
tags: [Spring Microservices, CRUD]
---

{% include toc title="Index" %}


### 1. What is Spring Boot and how does it differ from Spring Framework?
Spring Boot is an extension of the Spring Framework that simplifies application development by providing:
-   Auto-configuration
-   Embedded servers (Tomcat, Jetty)
-   Production-ready features (Actuator)
-   Opinionated defaults

Unlike Spring Framework, Spring Boot **eliminates the need for extensive XML configuration** and boilerplate code.

### 2. What does `@SpringBootApplication` do?
It is a convenience annotation that combines:
-   `@Configuration`
-   `@EnableAutoConfiguration`
-   `@ComponentScan`

It marks 
- the main class of a Spring Boot application 
- triggers component scanning and 
- auto-configuration.

### 3. How does Spring Boot manage dependencies?
Spring Boot uses **Spring Boot Starters**, which are curated dependency descriptors.
It also uses a **parent POM** that manages versions, reducing the need for manual dependency management.

### 4. What is auto-configuration in Spring Boot?
 
Auto-configuration automatically configures Spring beans based on classpath settings,
property values, and other factors.

It uses `@Conditional` annotations and is enabled by `@EnableAutoConfiguration`.

----------

### 5. How do you use `@ConfigurationProperties`?

**Answer:**

```java
@ConfigurationProperties(prefix = "app")
public class AppProperties {
    private String name;
    private int timeout;
    // getters and setters
}

```

You must annotate the class with `@Component` or register it as a bean.

----------

## 🔸 Round 2: Advanced Spring Boot

### 6. How does Spring Boot’s auto-configuration work internally?

**Answer:**  
It scans `META-INF/spring.factories` for `EnableAutoConfiguration` classes and applies them conditionally using `@ConditionalOnClass`, `@ConditionalOnMissingBean`, etc.

----------

### 7. How do you create a custom Spring Boot starter?

**Answer:**

1.  Create a library module.
2.  Add auto-configuration class with `@Configuration`.
3.  Register it in `META-INF/spring.factories`.
4.  Package and publish the starter.

----------

### 8. What is Spring Boot Actuator?

**Answer:**  
Actuator provides production-ready features like:

-   Health checks (`/actuator/health`)
-   Metrics (`/actuator/metrics`)
-   Environment info (`/actuator/env`)

----------

### 9. How do you secure Actuator endpoints?

**Answer:**

-   Use Spring Security to restrict access.
-   Configure `management.endpoints.web.exposure.include` and `management.endpoint.health.show-details`.

----------

## 🔹 Round 3: Spring Security

### 10. What is the difference between authentication and authorization?

**Answer:**

-   **Authentication**: Verifying identity (e.g., login).
-   **Authorization**: Granting access to resources based on roles/permissions.

----------

### 11. How do you implement JWT authentication?

**Answer:**

-   Generate JWT on login.
-   Validate JWT in a custom filter.
-   Use `UsernamePasswordAuthenticationToken` to set authentication in the security context.

----------

### 12. What is the Spring Security filter chain?

**Answer:**  
A chain of filters that intercepts HTTP requests. Key filters include:

-   `UsernamePasswordAuthenticationFilter`
-   `BasicAuthenticationFilter`
-   `ExceptionTranslationFilter`

----------

### 13. How do you secure REST APIs?

**Answer:**

-   Use stateless JWT authentication.
-   Disable CSRF.
-   Use `@PreAuthorize` or `@Secured` for method-level security.

----------

### 14. How do you implement role-based access control?

**Answer:**

-   Assign roles to users.
-   Use annotations like `@PreAuthorize("hasRole('ADMIN')")`.

----------

## 🔸 Round 4: Architecture & Design

### 15. How do you design microservices with Spring Boot?

**Answer:**

-   Use Spring Cloud for service discovery, config, and gateway.
-   Use REST or messaging (Kafka/RabbitMQ) for communication.
-   Implement resilience with Resilience4j.

----------

### 16. How do you implement circuit breaking?

**Answer:** Use Resilience4j:

```java
@CircuitBreaker(name = "myService", fallbackMethod = "fallback")
public String callExternalService() {
    // logic
}

```

----------

### 17. How do you ensure observability?

**Answer:**

-   Use Spring Boot Actuator.
-   Integrate with Prometheus + Grafana.
-   Use distributed tracing (Zipkin, Sleuth).

----------

## 🔸 Round 5: Scenario-Based

### 18. A REST API is slow. How do you debug it?

**Answer:**

-   Use Actuator metrics.
-   Profile with tools like JProfiler.
-   Check DB queries, thread pools, GC logs.

----------

### 19. How do you implement a custom authentication provider?

**Answer:** Implement `AuthenticationProvider`:

```java
public class CustomAuthProvider implements AuthenticationProvider {
    public Authentication authenticate(...) {
        // custom logic
    }
}

```

----------

### 20. How do you handle multi-tenancy?

**Answer:**

-   Use a tenant identifier (header, subdomain).
-   Use Hibernate multi-tenancy support.
-   Isolate data per tenant using schemas or databases.

----------

Would you like me to generate a downloadable **Markdown file** or convert this into a **PDF** for your blog?