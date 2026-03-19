---
title: Spring Component Scanning, AOT & Native-Image Reflection
date: 2026-03-19 00:30:00
categories:
  - Microservices
tags:
  - Java
  - Spring Boot
---

{% include toc title="Index" %}

This post dives into how Spring uses reflection under the hood for component scanning,
how Ahead-of-Time (AOT) compilation changes that, and how to configure reflection for
GraalVM native images.

## Spring Component Scanning

Component scanning is the mechanism by which Spring automatically discovers and registers
beans without explicit XML or Java configuration for each one.

### How it works (reflection-based)

1. **Classpath scanning**: Spring scans packages (starting from `@ComponentScan` base packages
   or Spring Boot's main class package) looking for classes annotated with stereotype annotations.

2. **Stereotype annotations detected**:
   - `@Component` — generic Spring-managed component
   - `@Service` — business/service layer
   - `@Repository` — data access layer (also adds exception translation)
   - `@Controller` / `@RestController` — web layer

3. **Reflection usage**:
   - Spring uses `ClassLoader` and ASM (bytecode reading) to find candidate classes
   - For each candidate, reflection checks for annotations: `Class.isAnnotationPresent(...)`
   - Reflection discovers constructors for instantiation: `Class.getDeclaredConstructors()`
   - Reflection finds `@Autowired` fields/setters for dependency injection

### Minimal example

```java
@SpringBootApplication // includes @ComponentScan
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}

@Service
public class GreetingService {
    public String greet(String name) {
        return "Hello, " + name;
    }
}

@RestController
public class GreetingController {
    private final GreetingService greetingService;

    // Constructor injection — Spring uses reflection to find this constructor
    public GreetingController(GreetingService greetingService) {
        this.greetingService = greetingService;
    }

    @GetMapping("/greet/{name}")
    public String greet(@PathVariable String name) {
        return greetingService.greet(name);
    }
}
```

### What Spring does at startup (simplified)

| Step | Reflection involved |
|:-----|:--------------------|
| Scan packages for `@Component` etc. | `ClassLoader.loadClass()`, ASM bytecode reading |
| Check for annotations | `Class.isAnnotationPresent()`, `Class.getAnnotations()` |
| Find constructors | `Class.getDeclaredConstructors()` |
| Instantiate beans | `Constructor.newInstance()` |
| Inject dependencies | `Field.set()`, `Method.invoke()` for setters |
| Create proxies (AOP) | CGLIB subclassing or JDK dynamic proxies |

### Customizing component scanning

```java
@ComponentScan(
    basePackages = "com.example.services",
    includeFilters = @ComponentScan.Filter(type = FilterType.ANNOTATION, classes = MyCustomAnnotation.class),
    excludeFilters = @ComponentScan.Filter(type = FilterType.REGEX, pattern = ".*Test.*")
)
```

---

## Spring AOT (Ahead-of-Time) Processing

Spring 6 / Spring Boot 3 introduced AOT processing to reduce startup time and memory,
and to support GraalVM native images.

### Why AOT?

| JIT (traditional) | AOT |
|:------------------|:----|
| Classpath scanning at runtime | Pre-computed bean definitions at build time |
| Reflection to discover beans | Generated code replaces reflection |
| Slower startup, higher memory | Faster startup, lower memory |
| Works everywhere | Requires build-time processing |

### How AOT works in Spring

1. **Build-time bean discovery**: During `mvn spring-boot:aot-generate` or Gradle equivalent,
   Spring scans and processes all beans.

2. **Code generation**: Instead of runtime reflection, Spring generates:
   - `BeanDefinition` supplier classes
   - Reflection hints for unavoidable reflection
   - Proxy classes

3. **Runtime uses generated code**: At startup, Spring loads pre-generated metadata
   instead of scanning and reflecting.

### Enabling AOT in Spring Boot 3

```xml
<!-- pom.xml -->
<plugin>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-maven-plugin</artifactId>
    <executions>
        <execution>
            <id>aot</id>
            <goals>
                <goal>process-aot</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

```bash
# Generate AOT artifacts
mvn spring-boot:process-aot

# Run with AOT
java -Dspring.aot.enabled=true -jar myapp.jar
```

### What gets generated

After AOT processing, you'll find generated classes under `target/spring-aot/main/sources/`:

```
target/spring-aot/main/sources/
├── com/example/
│   ├── MyApp__BeanDefinitions.java
│   ├── GreetingService__BeanDefinitions.java
│   └── GreetingController__BeanDefinitions.java
└── org/springframework/aot/
    └── RuntimeHints.java
```

Example generated bean definition (simplified):

```java
// Generated — replaces runtime reflection
public class GreetingService__BeanDefinitions {
    public static BeanDefinition getGreetingServiceBeanDefinition() {
        return BeanDefinitionBuilder
            .rootBeanDefinition(GreetingService.class)
            .setInstanceSupplier(GreetingService::new)
            .getBeanDefinition();
    }
}
```

---

## Native-Image Reflection Configuration

GraalVM native-image performs aggressive dead-code elimination and closed-world analysis.
Reflection breaks this because the compiler cannot know at build time which classes/methods
will be accessed reflectively.

### The problem

```java
// This works in JIT but may fail in native image
Class<?> clazz = Class.forName("com.example.MyService");
Object instance = clazz.getDeclaredConstructor().newInstance();
```

Native-image doesn't see the string `"com.example.MyService"` as a class reference,
so it may not include `MyService` in the final binary.

### Solution: reflection configuration

You must tell native-image which classes, methods, and fields need reflection access.

#### Option 1: `reflect-config.json`

Create `src/main/resources/META-INF/native-image/reflect-config.json`:

```json
[
  {
    "name": "com.example.MyService",
    "allDeclaredConstructors": true,
    "allDeclaredMethods": true,
    "allDeclaredFields": true
  },
  {
    "name": "com.example.Person",
    "methods": [
      { "name": "getName", "parameterTypes": [] },
      { "name": "setName", "parameterTypes": ["java.lang.String"] }
    ],
    "fields": [
      { "name": "name", "allowWrite": true }
    ]
  }
]
```

#### Option 2: Spring's `RuntimeHints` (preferred for Spring apps)

```java
@Configuration
@ImportRuntimeHints(MyRuntimeHints.class)
public class MyConfig { }

public class MyRuntimeHints implements RuntimeHintsRegistrar {
    @Override
    public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
        // Register class for reflection
        hints.reflection().registerType(MyService.class, 
            MemberCategory.INVOKE_DECLARED_CONSTRUCTORS,
            MemberCategory.INVOKE_DECLARED_METHODS);
        
        // Register resource
        hints.resources().registerPattern("config/*.properties");
        
        // Register for serialization
        hints.serialization().registerType(MyDto.class);
    }
}
```

#### Option 3: `@RegisterReflectionForBinding`

For DTOs and data classes used with Jackson/serialization:

```java
@RegisterReflectionForBinding({Person.class, Address.class})
@RestController
public class PersonController {
    // ...
}
```

#### Option 4: GraalVM tracing agent

Run your app with the tracing agent to auto-generate config:

```bash
# Run with agent
java -agentlib:native-image-agent=config-output-dir=src/main/resources/META-INF/native-image \
     -jar myapp.jar

# Exercise your application (hit all endpoints, trigger all code paths)

# Agent writes: reflect-config.json, resource-config.json, etc.
```

### Building a native image

```bash
# With Spring Boot 3 + GraalVM
mvn -Pnative native:compile

# Or with Gradle
./gradlew nativeCompile
```

### Common reflection-related native-image errors

| Error | Cause | Fix |
|:------|:------|:----|
| `ClassNotFoundException` | Class not included in image | Add to `reflect-config.json` |
| `NoSuchMethodException` | Method not registered for reflection | Register method in hints |
| `IllegalAccessException` | Private access not allowed | Use `allowWrite: true` or register field |
| `InstantiationException` | No-arg constructor not found | Register `allDeclaredConstructors` |

---

## Putting it together: complete native Spring Boot app

### pom.xml (key parts)

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.graalvm.buildtools</groupId>
            <artifactId>native-maven-plugin</artifactId>
        </plugin>
        <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
        </plugin>
    </plugins>
</build>

<profiles>
    <profile>
        <id>native</id>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.graalvm.buildtools</groupId>
                    <artifactId>native-maven-plugin</artifactId>
                    <executions>
                        <execution>
                            <id>build-native</id>
                            <goals>
                                <goal>compile-no-fork</goal>
                            </goals>
                            <phase>package</phase>
                        </execution>
                    </executions>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

### RuntimeHints for custom reflection

```java
public class AppRuntimeHints implements RuntimeHintsRegistrar {
    @Override
    public void registerHints(RuntimeHints hints, ClassLoader classLoader) {
        // If you use Class.forName() anywhere
        hints.reflection().registerType(
            TypeReference.of("com.example.DynamicallyLoadedClass"),
            MemberCategory.INVOKE_DECLARED_CONSTRUCTORS
        );
    }
}

@SpringBootApplication
@ImportRuntimeHints(AppRuntimeHints.class)
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}
```

### Build and run

```bash
# JIT mode (normal)
mvn spring-boot:run

# Native image
mvn -Pnative native:compile
./target/myapp   # starts in ~50ms instead of ~2s
```

---

## Summary

| Concept | Traditional (JIT) | Modern (AOT/Native) |
|:--------|:------------------|:--------------------|
| Bean discovery | Runtime classpath scan | Build-time code generation |
| Reflection | Heavy use everywhere | Minimized, explicit hints |
| Startup time | 1-10 seconds | 50-200 ms |
| Memory | Higher (JIT, metadata) | Lower (no JIT, pre-computed) |
| Flexibility | Can load any class dynamically | Must declare reflective access |

**Key takeaways**:
- Spring's component scanning historically relied heavily on reflection
- Spring 6 / Boot 3 AOT shifts work to build time, generating code instead of reflecting
- For native images, you must explicitly declare reflection needs via `RuntimeHints` or config files
- Use the GraalVM tracing agent to discover reflection usage in existing apps

## References

- [Spring Framework AOT documentation](https://docs.spring.io/spring-framework/reference/core/aot.html)
- [Spring Boot Native Image Guide](https://docs.spring.io/spring-boot/docs/current/reference/html/native-image.html)
- [GraalVM Native Image Reflection](https://www.graalvm.org/latest/reference-manual/native-image/metadata/)
- [Spring RuntimeHints API](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/aot/hint/RuntimeHints.html)

