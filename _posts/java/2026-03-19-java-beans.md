---
title: "Java Beans: What, Why, and How"
date: 2026-03-19 09:17:00
categories:
- Java
tags:
- Microservices
---

{% include toc title="Index" %}

## What is a Java Bean?
A **Java Bean** is simply a Java class that follows specific conventions:

| Convention         | Requirement                                                        |
|:-------------------|:-------------------------------------------------------------------|
| No-arg constructor | Must have a public default constructor                             |
| Private fields     | Properties are private                                             |
| Getters/Setters    | Public accessor methods (`getX()`, `setX()`, `isX()` for booleans) |
| Serializable       | Often implements `Serializable` (optional in Spring)               |

```java
// A simple Java Bean
@Getter
@Setter
public class Person {
    private String name;
    private int age;
    
    public Person() {}  // no-arg constructor
}
```

## Spring Bean vs Java Bean

| Java Bean                         | Spring Bean                                                   |
|:----------------------------------|:--------------------------------------------------------------|
| Follows getter/setter conventions | Any object managed by Spring IoC container                    |
| Created by you with `new`         | Created and managed by Spring                                 |
| No lifecycle management           | Has lifecycle (creation → initialization → use → destruction) |
| No dependency injection           | Dependencies injected automatically                           |

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

---

## Why Register Beans?
Registration tells Spring: *"This object exists, manage it for me."*

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

---

## Bean Scopes: Why They Matter

**Scope** determines how many instances of a bean exist and how long they live.

### Available Scopes

| Scope         | Instances                | Lifetime                | Use Case                     |
|:--------------|:-------------------------|:------------------------|:-----------------------------|
| `singleton`   | 1 per container          | Application lifetime    | Stateless services (default) |
| `prototype`   | New instance per request | Until garbage collected | Stateful objects             |
| `request`     | 1 per HTTP request       | Single HTTP request     | Request-specific data        |
| `session`     | 1 per HTTP session       | User session            | User session data            |
| `application` | 1 per ServletContext     | Application lifetime    | Shared across servlets       |
| `websocket`   | 1 per WebSocket          | WebSocket session       | WebSocket-specific data      |

### Singleton (Default) — One Instance

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

### Prototype — New Instance Each Time

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

```java
@Component
@Scope(value = WebApplicationContext.SCOPE_REQUEST, proxyMode = ScopedProxyMode.TARGET_CLASS)
public class RequestContext {
    private String correlationId;
    private long startTime;
    // Fresh instance for each HTTP request
}
```

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