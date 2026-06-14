---
title: "From XML Hell to Annotations: How Spring Cleaned Up Java Configuration"
date: 2026-03-22
categories: [java, spring, backend]
tags: [spring, annotations, xml, dependency-injection, ioc, reflection, spring-boot]
---

Early Spring applications were infamous for one thing: **mountains of XML**. If you've only ever used Spring Boot, you may have never seen it. But understanding why annotations replaced XML — and *how Java makes that possible internally* — gives you a much deeper understanding of how Spring actually works.

---

## The Old Way: XML-Based Configuration

Before Spring 2.5 (circa 2007), everything was configured in XML files. You had to explicitly declare every bean, every dependency, and every wiring by hand.

### Defining Beans in XML

```xml
<!-- applicationContext.xml -->
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="...">

    <bean id="userRepository" class="com.example.UserRepository" />

    <bean id="userService" class="com.example.UserService">
        <property name="userRepository" ref="userRepository" />
    </bean>

    <bean id="userController" class="com.example.UserController">
        <constructor-arg ref="userService" />
    </bean>

</beans>
```

And then the corresponding Java classes were just plain classes with no Spring-specific code:

```java
public class UserService {
    private UserRepository userRepository;

    // Spring calls this setter based on the XML <property> tag
    public void setUserRepository(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

### Why This Was Painful

- **Verbose**: Hundreds of lines of XML for even a medium-sized app
- **Error-prone**: Typos in class names or bean IDs only failed at runtime, not compile time
- **No IDE support**: Renaming a class didn't update the XML — you found out at startup
- **Split context**: Business logic lived in `.java`, configuration lived in `.xml` — always two places to look
- **Boilerplate setters**: Every injected dependency needed a public setter just for Spring to call

A real project could have `applicationContext.xml`, `security-context.xml`, `datasource-context.xml`, `mvc-context.xml` — each hundreds of lines long.

---

## The Shift: Annotation-Based Configuration

Spring 2.5 introduced annotations, and Spring 3.0 completed the picture with Java-based `@Configuration` classes. XML became optional, then effectively obsolete for most use cases.

### The Same App, Annotated

```java
@Repository
public class UserRepository {
    // Spring detects this class and registers it as a bean
}

@Service
public class UserService {

    private final UserRepository userRepository;

    @Autowired  // Spring injects UserRepository automatically
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

@RestController
public class UserController {

    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping("/users")
    public List<User> getUsers() {
        return userService.findAll();
    }
}
```

No XML. No setter boilerplate. Spring discovers, creates, and wires everything automatically.

### Common Stereotype Annotations

| Annotation | Meaning | Typical Use |
| --- | --- | --- |
| `@Component` | Generic Spring-managed bean | Utility classes |
| `@Service` | Business logic layer | Service classes |
| `@Repository` | Data access layer | DAO / JPA repositories |
| `@Controller` | Web layer (MVC) | MVC controllers |
| `@RestController` | `@Controller` + `@ResponseBody` | REST API controllers |
| `@Configuration` | Bean definition class | Replaces XML config files |
| `@Bean` | Factory method producing a bean | Inside `@Configuration` classes |

---

## Java-Based Config: Replacing XML Files Entirely

Even for third-party classes you can't annotate, you can use `@Configuration` + `@Bean` instead of XML:

**Old XML way:**

```xml
<bean id="dataSource" class="com.zaxxer.hikari.HikariDataSource">
    <property name="jdbcUrl" value="jdbc:postgresql://localhost/mydb" />
    <property name="username" value="admin" />
</bean>
```

**New Java way:**

```java
@Configuration
public class DataSourceConfig {

    @Bean
    public DataSource dataSource() {
        HikariDataSource ds = new HikariDataSource();
        ds.setJdbcUrl("jdbc:postgresql://localhost/mydb");
        ds.setUsername("admin");
        return ds;
    }
}
```

Type-safe, refactor-friendly, and your IDE understands it fully.

---

## How Java Makes This Possible Internally

This is the important part. Annotations don't *do* anything by themselves — they are just **metadata markers**. The real magic is in how Spring reads them at runtime using **Java Reflection**.

### Step 1 — Annotations Are Just Metadata

When you write `@Service` on a class, the Java compiler stores that annotation in the `.class` file's bytecode as metadata. At runtime, the annotation is still there, attached to the class, waiting to be read.

```java
// This is all @Service really is — a marker interface with metadata
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)  // ← critical: keeps the annotation available at runtime
@Component
public @interface Service {
    String value() default "";
}
```

`@Retention(RetentionPolicy.RUNTIME)` is the key — it tells the compiler to keep the annotation in the bytecode so it can be read via reflection at runtime.

### Step 2 — Classpath Scanning

When your Spring application starts, the `ApplicationContext` performs **classpath scanning**. It:

1. Finds all `.class` files under the base package
2. Loads each class using the `ClassLoader`
3. Uses reflection to check: *does this class have `@Component` or any meta-annotation of `@Component`?*

```java
// Simplified version of what Spring does internally
for (Class<?> clazz : allClassesInBasePackage) {
    if (clazz.isAnnotationPresent(Component.class)) {
        registerAsBean(clazz);
    }
}
```

`@Service`, `@Repository`, `@Controller` are all themselves annotated with `@Component` — so Spring treats them all the same way under the hood. This is called **meta-annotation composition**.

### Step 3 — Reflection-Based Dependency Injection

Once Spring knows which classes are beans, it needs to wire them together. It uses reflection to inspect constructors, fields, and methods for `@Autowired`:

```java
// Spring inspects constructors
Constructor<?>[] constructors = clazz.getDeclaredConstructors();
for (Constructor<?> constructor : constructors) {
    if (constructor.isAnnotationPresent(Autowired.class)) {
        // resolve each parameter type from the ApplicationContext
        // then call constructor.newInstance(resolvedArgs...)
    }
}
```

For field injection (`@Autowired` directly on a field), Spring uses:

```java
field.setAccessible(true);  // bypass private access
field.set(beanInstance, resolvedDependency);
```

This is why field injection works even on `private` fields — reflection can bypass Java's visibility rules with `setAccessible(true)`.

### Step 4 — Proxy Generation (AOP)

For features like `@Transactional` or `@Cacheable`, Spring can't just set a field — it needs to *wrap* your bean with behaviour. It does this by generating a **proxy class** at runtime using either:

- **JDK Dynamic Proxies** — if your bean implements an interface
- **CGLIB** — if your bean is a concrete class (subclasses it at runtime)

```java
// What you write
@Service
public class OrderService {
    @Transactional
    public void placeOrder(Order order) { ... }
}

// What Spring actually puts in the ApplicationContext at runtime
// (a CGLIB-generated subclass, roughly):
public class OrderService$$SpringCGLIB extends OrderService {
    @Override
    public void placeOrder(Order order) {
        beginTransaction();
        try {
            super.placeOrder(order);  // your actual code
            commitTransaction();
        } catch (Exception e) {
            rollbackTransaction();
            throw e;
        }
    }
}
```

You never write this class. Spring generates it at startup using bytecode manipulation, then injects this proxy wherever `OrderService` is needed — so `@Transactional` just works.

### The Full Internal Pipeline

```text
Application starts
    → @SpringBootApplication triggers component scan
        → ClassLoader loads all .class files in package
            → Reflection checks each class for @Component meta-annotation
                → Matching classes registered as BeanDefinitions
                    → Spring instantiates beans (via reflection / constructor)
                        → @Autowired dependencies resolved and injected
                            → @Transactional / @Cacheable beans wrapped in proxies
                                → ApplicationContext ready
                                    → DispatcherServlet maps @RequestMapping → handler beans
```

---

## XML vs. Annotations: Side-by-Side

| Concern | XML Config | Annotation Config |
| --- | --- | --- |
| Bean declaration | `<bean class="...">` | `@Component` / `@Service` / etc. |
| Dependency injection | `<property ref="...">` | `@Autowired` |
| Request mapping | XML MVC config | `@GetMapping`, `@PostMapping` |
| Third-party beans | `<bean>` blocks | `@Bean` in `@Configuration` |
| Type safety | None (strings) | Full (compiler checks) |
| Refactor safety | Manual XML updates | IDE handles it |
| Startup error detection | Runtime only | Mostly compile time |
| Readability | Config split from code | Config lives with code |

---

## A Note on Spring Boot

Spring Boot takes annotations one step further with **auto-configuration**. It ships with hundreds of `@Configuration` classes that activate conditionally — e.g., if `HikariCP` is on the classpath, it auto-configures a `DataSource` bean for you.

This is driven by `@ConditionalOnClass`, `@ConditionalOnMissingBean`, and the `spring.factories` / `AutoConfiguration.imports` mechanism — all powered by the same reflection machinery described above.

The result: you add a dependency to `pom.xml`, and Spring Boot figures out the configuration automatically. Zero XML, often zero `@Bean` methods.

---

## Summary

XML configuration wasn't wrong — it was a reasonable solution for its time, keeping Spring-specific config out of business logic. But it didn't scale well as applications grew.

Annotations solved this by:

1. **Co-locating** configuration with the code it configures
2. **Leveraging Java's reflection API** to read metadata at runtime
3. **Enabling classpath scanning** so beans are discovered, not declared
4. **Using proxy generation** to layer cross-cutting concerns (transactions, caching) transparently

Under the hood, annotations are just metadata. Spring's power comes entirely from reading that metadata via reflection and acting on it — creating objects, injecting dependencies, and generating proxies — all before your first HTTP request arrives.
