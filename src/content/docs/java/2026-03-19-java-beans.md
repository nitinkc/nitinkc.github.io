---
title: "Spring Bean : Scopes, Lifecycle, and Best Practices"
date: 2026-03-19 09:17:00
categories:
- Java
tags:
- Java
- Spring Boot
---

{% include toc title="Index" %}

## What is a Java Bean?
A **Java Bean** is simply a Java class that follows specific conventions:

| Convention         | Requirement                                                        |
|:-------------------|:-------------------------------------------------------------------|
| No-arg constructor | Must have a **public** default constructor                         |
| Private fields     | Properties are **private**                                         |
| Getters/Setters    | Public accessor methods (`getX()`, `setX()`, `isX()` for booleans) |
| Serializable       | Often implements `Serializable` (optional in Spring)               |

```java
// A simple Java Bean
@Getter @Setter @NoArgsConstructor
public class Person {
    private String name;
    private int age;
    
    public Person() {}  // no-arg constructor
}
```

## Spring Bean vs Java Bean

| Java Bean                         | Spring Bean                                                    |
|:----------------------------------|:---------------------------------------------------------------|
| Follows getter/setter conventions | Any object **managed** by Spring **IoC container**             |
| Created by you with `new`         | Created and managed by Spring                                  |
| No lifecycle management           | Has lifecycle (creation → initialization → use → destruction)  |
| No dependency injection           | Dependencies injected automatically                            |

> **Spring Bean** = Any object that Spring creates, configures, and manages.

```java
// This is a Spring Bean (managed by Spring)
@Component
public class OrderService {
    private final PaymentService paymentService;  // injected by Spring
    
    public OrderService(PaymentService paymentService) {
        this.paymentService = paymentService;
    }
}
```

# @Bean Annotation

The `@Bean` annotation is used on **methods/constructor** (not classes) to explicitly declare a bean and register it with the Spring container.

## Why Use `@Bean` on a Method?

While `@Component` (and its stereotypes like `@Service`, `@Repository`) are used on **classes** to let Spring auto-detect and register beans via component scanning,
`@Bean` is used when:

1. **You don't own the class** - The class comes from a third-party library, so you can't add `@Component` to it.
2. **You need custom instantiation logic** - The bean requires specific constructor arguments or configuration.
3. **You want explicit control** - You prefer programmatic bean definition over auto-detection.

## How It Works

```java
@Configuration
public class AppConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        return mapper;
    }
}
```

- The **method name** (`restTemplate`, `objectMapper`) becomes the **bean name** by default.
- The **return type** is the bean type that Spring will manage.
- Spring calls this method and registers the returned object as a bean in the ApplicationContext.

## @Bean vs @Component

| Aspect          | `@Bean`                                   | `@Component`                              |
|:----------------|:------------------------------------------|:------------------------------------------|
| **Applied to**  | Methods (inside `@Configuration` class)   | Classes                                   |
| **Use case**    | Third-party classes, custom instantiation | Your own classes                          |
| **Discovery**   | Explicit declaration                      | Auto-detected via component scan          |
| **Flexibility** | Full control over instantiation           | Limited to default/autowired constructors |

## Example: Third-Party Library Bean

You cannot modify `RestTemplate` source code to add `@Component`, so you use `@Bean`:

```java
@Configuration
public class HttpClientConfig {

    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) {
        return builder
            .setConnectTimeout(Duration.ofSeconds(5))
            .setReadTimeout(Duration.ofSeconds(10))
            .build();
    }
}
```

## Bean Naming

```java
@Bean // Bean name: "myService" (method name)
public MyService myService() { ... }

@Bean("customName") // Bean name: "customName"
public MyService myService() { ... }

@Bean(name = {"name1", "alias1"}) // Multiple names/aliases
public MyService myService() { ... }
```

## Dependency Injection in @Bean Methods

Spring automatically injects dependencies as method parameters:

```java
@Bean
public UserService userService(UserRepository userRepository, EmailService emailService) {
    return new UserService(userRepository, emailService);
}
```

Spring resolves `UserRepository` and `EmailService` from the container and passes them to the method.

## Why Register Beans in Spring?
Registration tells Spring: **"This object exists, manage it for me."**

### Without Registration (Manual Wiring)

```java
// You must create and wire everything manually
public class Application {
    public static void main(String[] args) {
        // Create dependencies manually
        DatabaseConnection db = new DatabaseConnection("jdbc:mysql://...");
        UserRepository userRepo = new UserRepository(db);
        EmailService emailService = new EmailService();
        UserService userService = new UserService(userRepo, emailService);
        OrderService orderService = new OrderService(userService);
        
        // 😩 Painful for large applications with 100+ classes
    }
}
```

### With Registration (Spring Manages It)

```java
@Component
public class DatabaseConnection { }

@Repository
public class UserRepository {
    @Autowired private DatabaseConnection db;
}

@Service
public class UserService {
    @Autowired private UserRepository userRepo;
    @Autowired private EmailService emailService;
}

// Spring automatically:
// 1. Finds all @Component classes
// 2. Creates instances in correct order
// 3. Injects dependencies
// 4. Manages lifecycle
```

### Benefits of Bean Registration

| Benefit                  | Description                                           |
|:-------------------------|:------------------------------------------------------|
| **Dependency Injection** | Spring injects dependencies automatically             |
| **Lifecycle Management** | Spring handles creation, initialization, destruction  |
| **Singleton by Default** | One instance shared across application (saves memory) |
| **Loose Coupling**       | Classes don't create their own dependencies           |
| **Easy Testing**         | Swap real beans with mocks easily                     |
| **Configuration**        | Change behavior via properties without code changes   |

## How to Register Beans

1. **Stereotype Annotations** (@Component, @Service, @Repository, @Controller)
- Use `@ComponentScan` or `@SpringBootApplication` to auto-discover.
    ```java
    @Component
    public class EmailService { }
    ```

2. **Java `@Configuration` Classes** with `@Bean` methods (explicit registration):
    ```java
    @Configuration
    public class AppConfig {
        @Bean
        public CacheService cacheService() {
            return new CacheService();
        }
    }
    ```

3. **XML Configuration** (legacy):
    ```xml
    <bean id="emailService" class="com.example.EmailService" />
    ```

## Bean Scopes: Why They Matter

**Scope** determines how many **instances** of a bean exist and how long they live.

### Available Scopes

| Scope         | Instances                    | Lifetime                 | Use Case                     |
|:--------------|:-----------------------------|:-------------------------|:-----------------------------|
| `singleton`   | 1 per container              | Application lifetime     | Stateless services (default) |
| `prototype`   | New instance per **request** | Until garbage collected  | Stateful objects             |
| `request`     | 1 per HTTP request           | Single HTTP request      | Request-specific data        |
| `session`     | 1 per HTTP session           | User session             | User session data            |
| `application` | 1 per ServletContext         | Application lifetime     | Shared across servlets       |
| `websocket`   | 1 per WebSocket              | WebSocket session        | WebSocket-specific data      |

### Singleton Scope (Default) — One Instance

Singleton scope is the **default scope** in Spring, where only one instance of the
bean is created and shared throughout the application context.

- The singleton scope is the **default** scope in Spring.
- The `Gang of Four` defines Singleton as having one **instance per ClassLoader**.
    - in their book **Design Patterns: Elements of Reusable Object-Oriented Software**-,
      ensures that a class has only one instance and provides a global point of
      access to it.

- However, Spring singleton is defined as **one instance of bean definition per
  container**.
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

#### Use Cases:
1. **Stateless Services**:
    - Beans that don’t hold any client-specific or mutable data.
    - Example: Service classes, DAOs.

2. **Configuration Beans**:
    - Classes used for setting up application-wide configurations.
    - Example: `@Configuration` annotated beans.

3. **Shared Utilities**:
    - Beans providing reusable functionality, like logging or caching utilities.

#### Advantages:
- Efficient memory usage.
- Shared state across the application.

```java
@Service  // singleton by default
public class PaymentService {
    // Same instance injected everywhere
    // ⚠️ Must be thread-safe (no mutable instance state)
}
```

```
┌─────────────────────────────────────────────────┐
│  Spring Container                               │
│  ┌─────────────────────────────────────────┐   │
│  │  PaymentService (single instance)       │   │
│  └─────────────────────────────────────────┘   │
│         ▲              ▲              ▲        │
│         │              │              │        │
│  ┌──────┴──┐    ┌──────┴──┐    ┌──────┴──┐    │
│  │ OrderA  │    │ OrderB  │    │ OrderC  │    │
│  └─────────┘    └─────────┘    └─────────┘    │
└─────────────────────────────────────────────────┘
All orders share the SAME PaymentService instance
```

### Prototype Scope — New Instance Each Time

Prototype scope instructs the Spring IoC container to create **a new instance of
the bean** whenever it is requested.

```java
@Component
@Scope("prototype")
public class PrototypeBean {
   // Bean definition
}
```

#### Use Cases:
1. **Stateful Components**:
    - Beans holding temporary or client-specific data.
    - Example: Objects with user session details.

2. **Expensive Objects**:
    - Large objects that need different configurations for each use.
    - Example: Heavy object initialization with variable parameters.

3. **Multi-threaded Applications**:
    - Beans where thread-safety requires separate instances per thread.

#### Advantages:
- Isolation between instances.
- Ideal for beans with mutable state.

```java
@Component
@Scope("prototype")
public class ShoppingCart {
    private List<Item> items = new ArrayList<>();
    // Each user gets their own cart instance
}
```

```
┌─────────────────────────────────────────────────┐
│  Spring Container                               │
│                                                 │
│  getBean(ShoppingCart.class) → new instance     │
│  getBean(ShoppingCart.class) → new instance     │
│  getBean(ShoppingCart.class) → new instance     │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Cart 1  │  │  Cart 2  │  │  Cart 3  │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
Each request gets a NEW ShoppingCart instance
```

### Request Scope — Per HTTP Request

A new instance of the bean is created **for each HTTP request** in a web application.
Request scope is used in web-based applications, where a new instance of the
bean is **created once per HTTP request**.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestScopedBean {
   // Bean definition
}
```

#### Use Cases:
1. **Request-Specific Data Processing**:
    - Beans holding data that is specific to a single HTTP request.
    - Example: Request validation or processing logic.

2. **Controllers and Form Handlers**:
    - Beans to manage user input and request processing in MVC applications.

3. **Temporary Attributes**:
    - Beans required to calculate data for a single view or response.

#### Advantages:
- Scoped to a single HTTP request lifecycle.
- Avoids memory leaks from request-specific data in global beans.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestContext {
    private String correlationId;
    private long startTime;
    // Fresh instance for each HTTP request
}
```

### Session Scope — Per HTTP Session

A new instance of the bean is created for **each HTTP session** in a web application.
Session scope is tied to the HTTP session lifecycle, 

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_SESSION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class SessionScopedBean {
   // Bean definition
}
```

#### Use Cases:
1. **User-Specific Session Data**:
    - Beans holding user preferences, shopping cart data, or session-specific attributes.
    - Collaborative Web Applications
2. **Authentication and Authorization**:
    - Beans to store user credentials or session tokens during the session lifecycle.

3. **Stateful Web Applications**:
    - Applications requiring user-specific state across multiple requests.

#### Advantages:
- Isolated state per user session.
- Useful for managing user-specific resources.

#### Why Use Session Beans in Multithreading?
##### State Isolation:
Each user’s session has its own instance of the bean.
Even when multiple threads handle requests concurrently, the state remains tied to the specific session.
##### Simplified State Management:
The bean eliminates the need to manually pass session attributes or manage synchronization across requests.

##### Real-World Examples:
Shopping Carts: Multiple requests for adding/removing items in a single session.
Collaborative Workflows: Multiple operations (e.g., saving drafts, updating settings) performed concurrently by a user.

### Application Scope — Per Servlet Context

A single instance of the bean is created for the entire servlet context.
created once when the application starts up.

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_APPLICATION, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class ApplicationScopedBean {
   // Bean definition
}
```

#### Use Cases:
1. **Application-Wide Resources**:
    - Beans managing shared resources, like global settings or configuration.

2. **Servlet Context Attributes**:
    - Beans wrapping context-level attributes or data.

3. **Cache or Resource Pools**:
    - Objects reused by all users, such as database connections or thread pools.

#### Advantages:
- Shared across the entire application lifecycle.
- Suitable for long-lived resources.

### Why Scope Matters: The Singleton + Prototype Problem

```java
@Service  // singleton
public class OrderService {
    @Autowired
    private ShoppingCart cart;  // prototype
    
    // ⚠️ PROBLEM: cart is injected ONCE at startup
    // All requests share the same cart!
}

// Solution: Use Provider or ObjectFactory
@Service
public class OrderService {
    @Autowired
    private Provider<ShoppingCart> cartProvider;
    
    public void processOrder() {
        ShoppingCart cart = cartProvider.get();  // new instance each time
    }
}
```

---

## Thread-safety and Scope

- **Singleton beans** must be thread-safe (no mutable shared state) or must guard mutable
  state properly (synchronization, thread-local, or use stateless design).
- **Prototype/request/session beans** can safely hold state for their intended lifetime
  (but be careful when exposing prototype-scoped instances to multiple threads).

---

## Bean Lifecycle

Spring beans go through a well-defined lifecycle with hooks for custom logic.

### Lifecycle Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                     BEAN LIFECYCLE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. INSTANTIATION                                               │
│     └── Spring calls constructor                                │
│              │                                                  │
│              ▼                                                  │
│  2. POPULATE PROPERTIES                                         │
│     └── @Autowired fields/setters injected                      │
│              │                                                  │
│              ▼                                                  │
│  3. BEAN NAME AWARE                                             │
│     └── setBeanName() if BeanNameAware                          │
│              │                                                  │
│              ▼                                                  │
│  4. BEAN FACTORY AWARE                                          │
│     └── setBeanFactory() if BeanFactoryAware                    │
│              │                                                  │
│              ▼                                                  │
│  5. PRE-INITIALIZATION (BeanPostProcessor)                      │
│     └── postProcessBeforeInitialization()                       │
│              │                                                  │
│              ▼                                                  │
│  6. INITIALIZATION                                              │
│     ├── @PostConstruct method                                   │
│     ├── InitializingBean.afterPropertiesSet()                   │
│     └── Custom init-method                                      │
│              │                                                  │
│              ▼                                                  │
│  7. POST-INITIALIZATION (BeanPostProcessor)                     │
│     └── postProcessAfterInitialization()                        │
│              │                                                  │
│              ▼                                                  │
│  8. BEAN READY FOR USE ✓                                        │
│              │                                                  │
│              ▼                                                  │
│  9. DESTRUCTION (on container shutdown)                         │
│     ├── @PreDestroy method                                      │
│     ├── DisposableBean.destroy()                                │
│     └── Custom destroy-method                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Lifecycle Callbacks Example

```java
@Component
public class DatabaseConnectionPool implements InitializingBean, DisposableBean {
    
    private List<Connection> connections;
    
    @Autowired
    private DataSourceConfig config;  // injected before @PostConstruct
    
    // Called after dependency injection
    @PostConstruct
    public void init() {
        System.out.println("1. @PostConstruct: Initializing pool");
        connections = new ArrayList<>();
    }
    
    // InitializingBean interface method
    @Override
    public void afterPropertiesSet() {
        System.out.println("2. afterPropertiesSet: Creating connections");
        for (int i = 0; i < config.getPoolSize(); i++) {
            connections.add(createConnection());
        }
    }
    
    // Called before bean destruction
    @PreDestroy
    public void cleanup() {
        System.out.println("3. @PreDestroy: Closing connections");
        connections.forEach(Connection::close);
    }
    
    // DisposableBean interface method
    @Override
    public void destroy() {
        System.out.println("4. destroy: Final cleanup");
    }
}
```

**Output on startup:**
```
1. @PostConstruct: Initializing pool
2. afterPropertiesSet: Creating connections
```

**Output on shutdown:**
```
3. @PreDestroy: Closing connections
4. destroy: Final cleanup
```

### Preferred Approach: Use Annotations

```java
@Service
public class CacheService {
    
    private Cache cache;
    
    @PostConstruct
    public void initializeCache() {
        // Called once after all dependencies are injected
        cache = CacheBuilder.newBuilder()
            .maximumSize(1000)
            .expireAfterWrite(10, TimeUnit.MINUTES)
            .build();
        System.out.println("Cache initialized");
    }
    
    @PreDestroy
    public void clearCache() {
        // Called before bean is destroyed (app shutdown)
        cache.invalidateAll();
        System.out.println("Cache cleared");
    }
}
```

### Lifecycle Summary Table

| Callback               | When                   | Use Case                             |
|:-----------------------|:-----------------------|:-------------------------------------|
| Constructor            | First                  | Basic instantiation                  |
| `@Autowired`           | After constructor      | Dependency injection                 |
| `@PostConstruct`       | After injection        | Initialize resources, validate state |
| `afterPropertiesSet()` | After `@PostConstruct` | Alternative to `@PostConstruct`      |
| `@PreDestroy`          | Before destruction     | Release resources, cleanup           |
| `destroy()`            | After `@PreDestroy`    | Alternative to `@PreDestroy`         |

### Why Lifecycle Matters

| Scenario                             | Lifecycle Hook   |
|:-------------------------------------|:-----------------|
| Open database connections on startup | `@PostConstruct` |
| Start background thread/scheduler    | `@PostConstruct` |
| Validate required configuration      | `@PostConstruct` |
| Close connections on shutdown        | `@PreDestroy`    |
| Stop background threads gracefully   | `@PreDestroy`    |
| Flush caches/buffers                 | `@PreDestroy`    |

---

## Common Best Practices

- Prefer constructor injection for required dependencies (makes immutability and testing easier).
- Keep singleton beans stateless. If state is required, prefer narrower scopes.
- Use `@Configuration` + `@Bean` for explicit wiring when you need control over construction logic.
- Avoid circular dependencies; if unavoidable, prefer setter injection for one side.
- Use `ObjectProvider`/`Provider` for injection of beans that should be created per-use.
- Use `@PostConstruct` / `@PreDestroy` for lifecycle work and avoid `InitializingBean` unless necessary.

## Quick Checklist for Migrating Code to Spring-Managed Beans

- Identify hard `new` calls – consider making those beans.
- Convert factory wiring to `@Configuration` + `@Bean` or `@Component` + constructor injection.
- Decide appropriate scope (default singleton unless state or request/session semantics required).
- Add `@PostConstruct`/`@PreDestroy` for resource management.
- Add unit tests by creating Spring test slices or mocking injected beans.

# Comparison of Scopes

| Scope           | Instance Per              | Typical Use Case                | Lifetime                  |
|:----------------|:--------------------------|:--------------------------------|:--------------------------|
| **Singleton**   | Application               | Stateless services, utilities   | Application lifecycle     |
| **Prototype**   | Each request or injection | Stateful or temporary objects   | Per request/injection     |
| **Request**     | HTTP request              | Request-specific logic          | HTTP request lifecycle    |
| **Session**     | HTTP session              | User-specific data              | HTTP session lifecycle    |
| **Application** | Servlet context           | Global settings, resource pools | Servlet context lifecycle |

