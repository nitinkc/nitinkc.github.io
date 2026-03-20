---
title: "Java Beans & Spring Beans — what, why, scopes and lifecycle"
date: 2026-03-19 11:00:00
categories:
  - Java
tags:
  - Java
  - Spring Boot
layout: post
---

{% include toc title="Index" %}

This post explains what a Java Bean is, how Spring treats "beans", why registering
beans with the container is useful, the different bean scopes, common pitfalls, and
the Spring bean lifecycle with code examples you can copy.

## What is a Java Bean?

A Java Bean is a simple Java class that follows these common conventions:

- A public no-argument constructor (so tools/frameworks can create instances).
- Private properties accessed via public getters/setters (property accessors).
- Optionally implements `Serializable` (historical convention for some frameworks).

Example:

```java
public class Person {
    private String name;
    private int age;

    public Person() {}

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
}
```

JavaBean conventions make a class easy to introspect, serialize, and manipulate by
IDE tools, frameworks, and libraries (e.g., JSP, JSF, older frameworks, and some
serialization libraries).

## Spring Bean vs Java Bean

- Java Bean: a POJO following getter/setter conventions.
- Spring Bean: any object created and managed by the Spring IoC container. It
  doesn't have to follow JavaBean conventions (can use constructor injection,
  final fields, etc.).

Example of Spring-managed bean via stereotype:

```java
@Service
public class OrderService {
    private final PaymentService paymentService;

    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```

Example of Spring-managed bean via Java configuration:

```java
@Configuration
public class AppConfig {
    @Bean
    public PaymentService paymentService() {
        return new PaymentService();
    }

    @Bean
    public OrderService orderService(PaymentService paymentService) {
        return new OrderService(paymentService);
    }
}
```

## Why register beans with the container?

Registration tells Spring to create, configure, and manage an object for you.
Benefits:

- Dependency Injection: the container automatically wires dependencies.
- Lifecycle management: initialization and destruction callbacks are handled.
- Scope control: singleton/prototype/request/session lifecycles.
- A central place for configuration, cross-cutting concerns, and testing.
- Easier swapping of implementations (for testing or different runtime profiles).

Manual wiring quickly becomes unmanageable for medium/large apps — Spring
registration reduces boilerplate and centralizes object creation.

## How to register beans

1. Stereotype annotations (@Component, @Service, @Repository, @Controller)
   + Use `@ComponentScan` or `@SpringBootApplication` to auto-discover.

```java
@Component
public class EmailService { }
```

2. Java `@Configuration` classes with `@Bean` methods (explicit registration):

```java
@Configuration
public class AppConfig {
    @Bean
    public CacheService cacheService() {
        return new CacheService();
    }
}
```

3. XML configuration (legacy):

```xml
<bean id="emailService" class="com.example.EmailService" />
```

## Bean scopes — what they mean and when to use them

Scope controls how many instances of a bean are created and how long they live.

Common scopes (Spring Core + Web):

- singleton — one instance per Spring container (default). Good for stateless services.
- prototype — a new instance each time the bean is requested from the container.
- request — one instance per HTTP request (Spring Web).
- session — one instance per HTTP session (Spring Web).
- application — one instance per ServletContext (Web application-wide).
- websocket — one instance per WebSocket session.

Example: prototype scope

```java
@Component
@Scope("prototype")
public class ShoppingCart {
    private final List<String> items = new ArrayList<>();
    public void add(String item) { items.add(item); }
}
```

Request scope example (web):

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestContext {
    private final String requestId = UUID.randomUUID().toString();
    public String getRequestId() { return requestId; }
}
```

### Singleton vs Prototype gotcha

If a `singleton` bean depends on a `prototype` bean and the prototype is injected directly,
that prototype instance is created once at container startup and reused — defeating
`prototype` semantics.

Bad (unexpected behavior):

```java
@Service  // singleton
public class OrderService {
    @Autowired
    private ShoppingCart cart; // injected once → reused across requests
}
```

Solutions:

- Inject `ObjectProvider<ShoppingCart>` or `Provider<ShoppingCart>` and call `get()` when needed.
- Use scoped proxies for web scopes (`proxyMode = ScopedProxyMode.TARGET_CLASS`).

Example with provider:

```java
@Service
public class OrderService {
    @Autowired
    private ObjectProvider<ShoppingCart> cartProvider;

    public void process() {
        ShoppingCart cart = cartProvider.getIfAvailable(); // new instance each time
    }
}
```

## Thread-safety and scope

- Singleton beans must be thread-safe (no mutable shared state) or must guard mutable
  state properly (synchronization, thread-local, or use stateless design).
- Prototype/request/session beans can safely hold state for their intended lifetime
  (but be careful when exposing prototype-scoped instances to multiple threads).

## Bean lifecycle (creation → destruction)

Spring manages a bean's lifecycle with well-defined callbacks and extension points.
The following flow applies to singleton beans (prototype has different destruction semantics):

1. Instantiation — container creates the bean instance (calls constructor).
2. Populate properties — dependency injection (`@Autowired`, setter injection).
3. Aware callbacks — `BeanNameAware#setBeanName`, `BeanFactoryAware#setBeanFactory`, etc.
4. BeanPostProcessor#postProcessBeforeInitialization — pre-init hooks.
5. Initialization — `@PostConstruct` methods, `InitializingBean.afterPropertiesSet()`, or custom `init-method`.
6. BeanPostProcessor#postProcessAfterInitialization — post-init hooks (where proxies are often created).
7. Bean ready to use.
8. Destruction — on context close: `@PreDestroy`, `DisposableBean.destroy()`, or custom `destroy-method`.

### Example with lifecycle callbacks

```java
@Component
public class DatabaseConnectionPool implements InitializingBean, DisposableBean {

    @Autowired private DataSourceConfig config;
    private List<Connection> connections;

    @PostConstruct
    public void init() {
        // runs after dependencies are injected
        connections = new ArrayList<>();
    }

    @Override
    public void afterPropertiesSet() {
        // final init step — safe to create connections
        for (int i = 0; i < config.getPoolSize(); i++) {
            connections.add(createConnection());
        }
    }

    @PreDestroy
    public void cleanup() {
        // runs before destruction
        connections.forEach(c -> closeQuietly(c));
    }

    @Override
    public void destroy() {
        // final cleanup
    }
}
```

Notes:
- `@PostConstruct` runs before `afterPropertiesSet()`.
- `BeanPostProcessor` implementations get called before/after initialization and are
  the right place to implement cross-cutting behaviors (AOP proxies, property modification).
- Prototype-scoped beans are not destroyed by the container — you must clean up resources manually
  if required.

## Common best practices

- Prefer constructor injection for required dependencies (makes immutability and testing easier).
- Keep singleton beans stateless. If state is required, prefer narrower scopes.
- Use `@Configuration` + `@Bean` for explicit wiring when you need control over construction logic.
- Avoid circular dependencies; if unavoidable, prefer setter injection for one side.
- Use `ObjectProvider`/`Provider` for injection of beans that should be created per-use.
- Use `@PostConstruct` / `@PreDestroy` for lifecycle work and avoid `InitializingBean` unless necessary.

## Quick checklist for migrating code to Spring-managed beans

- Identify hard `new` calls – consider making those beans.
- Convert factory wiring to `@Configuration` + `@Bean` or `@Component` + constructor injection.
- Decide appropriate scope (default singleton unless state or request/session semantics required).
- Add `@PostConstruct`/`@PreDestroy` for resource management.
- Add unit tests by creating Spring test slices or mocking injected beans.

---


