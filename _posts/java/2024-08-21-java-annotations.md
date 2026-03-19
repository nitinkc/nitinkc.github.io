---
title: Java annotations
date: 2024-08-21 00:17:00
categories:
- Java
tags:
- Java
---

{% include toc title="Index" %}

Before, JDK 1.5 XML was used to access metadata. Annotations have replaced it
since java 1.5

Spring 2.X was XML based and Spring 3 was Annotation based

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                           http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="myBean" class="com.example.MyBean">
        <property name="message" value="Hello, Spring!"/>
    </bean>

</beans>
```

With Spring 3.x and later, you can use annotations for configuration, which
simplifies the setup.

With just one line of Annotation, the xml document was eliminated

```java
@Component
public class MyBean {
    @Value("Hello, Spring!")
    private String message;

    public String getMessage() {
        return message;
    }
}
```

In Java, annotations have two main types of syntax:

- declaration and
- utilization.

### Declaration Syntax

Annotations are defined using the `@interface` keyword.

```java
@Retention(RetentionPolicy.RUNTIME) // Retention policy: available at runtime
@Target(ElementType.METHOD) // Target: can be applied to methods
public @interface MyCustomAnnotation {
    String description() default "No description"; // Default value for the annotation
}
```

#### **@Retention**
- Runtime level : `RetentionPolicy.RUNTIME`: Specifies that the annotation
  should be retained at runtime and be available for reflection.
- Source level - `RetentionPolicy.SOURCE`
- Classlevel - `RetentionPolicy.CLASS`

#### **@Target**
- Method level - `ElementType.METHOD` Specifies that this annotation can only be
  applied to methods.
- Class Level - `ElementType.TYPE`
- Field level - `ElementType.FIELD`
- Package level - `ElementType.PACKAGE`
- local variable level - `ElementType.LOCAL_VARIABLE`

**`description() default "No description"`**:

- An element of the annotation with a default value.

### Utilization Syntax

This is where annotation in the code is used.
Apply annotation to various Java elements (such as methods, classes, fields,
etc.) according to its `@Target` specification.

**Marker Annotation** : `@Override`

**Single Valued Annotation** : `@SuppressWarning("Unchecked")`

**Multivalued Annotation** : below custom code

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface MultiValueAnnotation {
    String name();
    int value();
    String[] tags() default {};  // Default empty array
}
```

**Usage**

```java
@MultiValueAnnotation(
    name = "SampleAnnotation",
    value = 100,
    tags = {"example", "annotation"}
)
public class MyClass {
    // Class implementation
}
```

---

# How Annotations Work Internally

Annotations are **metadata** — they don't change program logic directly. The magic
happens in three stages: compile time, class file storage, and runtime processing.

## Stage 1: Compile Time

The Java compiler (`javac`) processes annotations in two ways:

### Built-in compiler checks

Some annotations trigger compiler behavior directly:

| Annotation             | Compiler Action                                      |
|:-----------------------|:-----------------------------------------------------|
| `@Override`            | Verify method actually overrides a superclass method |
| `@Deprecated`          | Generate warning when deprecated element is used     |
| `@SuppressWarnings`    | Suppress specified compiler warnings                 |
| `@FunctionalInterface` | Verify interface has exactly one abstract method     |

### Annotation Processing (APT)

For custom compile-time processing, Java provides the **Annotation Processing Tool**.
Processors run during compilation and can:
- Generate new source files
- Generate new class files
- Report compiler errors/warnings

```java
// Annotation processor example (runs at compile time)
@SupportedAnnotationTypes("com.example.GenerateBuilder")
@SupportedSourceVersion(SourceVersion.RELEASE_17)
public class BuilderProcessor extends AbstractProcessor {
    @Override
    public boolean process(Set<? extends TypeElement> annotations, 
                          RoundEnvironment roundEnv) {
        for (Element element : roundEnv.getElementsAnnotatedWith(GenerateBuilder.class)) {
            // Generate a Builder class for this element
            generateBuilderClass(element);
        }
        return true;
    }
}
```

Examples using compile-time processing:
- **Lombok** — `@Getter`, `@Setter`, `@Builder` generate code at compile time
- **MapStruct** — generates mapper implementations
- **Dagger** — generates dependency injection code

## Stage 2: Storage in Class Files

After compilation, annotations are stored in the `.class` file based on `@Retention`:

| Retention  | Stored in .class?  | Available at Runtime? |
|:-----------|:-------------------|:----------------------|
| `SOURCE`   | ❌ No               | ❌ No                  |
| `CLASS`    | ✅ Yes              | ❌ No (default)        |
| `RUNTIME`  | ✅ Yes              | ✅ Yes                 |

You can inspect annotations in bytecode using `javap`:

```bash
javap -v MyClass.class | grep -A5 "RuntimeVisibleAnnotations"
```

Output shows annotations stored in the class file:

```
RuntimeVisibleAnnotations:
  0: #15(#16=s#17)
    com.example.MyAnnotation(
      value="example"
    )
```

## Stage 3: Runtime Processing (Reflection)
For `RUNTIME` retention annotations `@Retention(RetentionPolicy.RUNTIME)`, **@Retention(RetentionPolicy.RUNTIME)**:

### Core Reflection Methods

```java
// Check if annotation is present
boolean hasAnnotation = clazz.isAnnotationPresent(MyAnnotation.class);

// Get specific annotation
MyAnnotation annotation = clazz.getAnnotation(MyAnnotation.class);

// Get all annotations
Annotation[] all = clazz.getAnnotations();           // includes inherited
Annotation[] declared = clazz.getDeclaredAnnotations(); // only this class

// Read annotation values
String value = annotation.value();
```

### Complete Runtime Processing Example

```java
// 1. Define the annotation
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface Loggable {
    String level() default "INFO";
}

// 2. Use the annotation
public class UserService {
    @Loggable(level = "DEBUG")
    public void createUser(String name) {
        System.out.println("Creating user: " + name);
    }
    
    @Loggable
    public void deleteUser(String id) {
        System.out.println("Deleting user: " + id);
    }
}

// 3. Process at runtime
public class AnnotationProcessor {
    public static void processLoggable(Object obj) throws Exception {
        Class<?> clazz = obj.getClass();
        
        for (Method method : clazz.getDeclaredMethods()) {
            if (method.isAnnotationPresent(Loggable.class)) {
                Loggable loggable = method.getAnnotation(Loggable.class);
                System.out.println("Method: " + method.getName() 
                    + " has @Loggable with level: " + loggable.level());
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        processLoggable(new UserService());
    }
}
```

**Output:**
```
Method: createUser has @Loggable with level: DEBUG
Method: deleteUser has @Loggable with level: INFO
```

---

# How Frameworks Use Annotations

## The Processing Pattern

Most frameworks follow this pattern:

```
1. Scan classpath for classes
2. For each class, check for specific annotations
3. Based on annotation + values, take action (register, wrap, configure)
```

## Spring's Annotation Processing Flow

```java
// What you write:
@Service
public class OrderService {
    @Autowired
    private PaymentService paymentService;
    
    @Transactional
    public void placeOrder(Order order) { ... }
}
```

**What Spring does internally (simplified):**

```java
// 1. Classpath scanning finds OrderService.class
Class<?> clazz = Class.forName("com.example.OrderService");

// 2. Check for stereotype annotation
if (clazz.isAnnotationPresent(Service.class) || 
    clazz.isAnnotationPresent(Component.class)) {
    
    // 3. Create bean definition
    BeanDefinition bd = new BeanDefinition(clazz);
    
    // 4. Find injection points
    for (Field field : clazz.getDeclaredFields()) {
        if (field.isAnnotationPresent(Autowired.class)) {
            bd.addInjectionPoint(field);
        }
    }
    
    // 5. Check for AOP annotations
    for (Method method : clazz.getDeclaredMethods()) {
        if (method.isAnnotationPresent(Transactional.class)) {
            // Mark for proxy wrapping
            bd.requiresProxy(true);
        }
    }
    
    // 6. Register bean
    beanFactory.registerBeanDefinition("orderService", bd);
}
```

## JPA/Hibernate Example

```java
@Entity
@Table(name = "users")
public class User {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "user_name", nullable = false)
    private String username;
}
```

**Hibernate reads annotations to:**
1. Map class to table (`@Entity`, `@Table`)
2. Map fields to columns (`@Column`)
3. Configure primary key generation (`@Id`, `@GeneratedValue`)
4. Build SQL queries automatically

## JUnit Example

```java
public class CalculatorTest {
    @BeforeEach
    void setup() { /* runs before each test */ }
    
    @Test
    void testAddition() { /* test method */ }
    
    @Test
    @Disabled("Not implemented yet")
    void testDivision() { /* skipped */ }
}
```

**JUnit processes annotations to:**
1. Find test methods (`@Test`)
2. Run setup/teardown (`@BeforeEach`, `@AfterEach`)
3. Skip disabled tests (`@Disabled`)

---

# Annotation Internals: What's Really Happening

## Annotations are Interfaces

When you declare an annotation, Java creates an interface that extends
`java.lang.annotation.Annotation`:

```java
// What you write:
public @interface MyAnnotation {
    String value();
}

// What compiler generates (conceptually):
public interface MyAnnotation extends java.lang.annotation.Annotation {
    String value();
}
```

## Proxy Implementation at Runtime

When you call `getAnnotation()`, the JVM returns a **dynamic proxy** that
implements your annotation interface:

```java
MyAnnotation ann = clazz.getAnnotation(MyAnnotation.class);
System.out.println(ann.getClass().getName());
// Output: com.sun.proxy.$Proxy1 (or similar)
```

The proxy reads values from the class file's annotation data and returns them
when you call the annotation methods.

## Memory Layout

```
┌─────────────────────────────────────────────────────┐
│  .class file                                        │
├─────────────────────────────────────────────────────┤
│  RuntimeVisibleAnnotations attribute                │
│  ├── Annotation type: com.example.MyAnnotation      │
│  └── Element-value pairs:                           │
│      └── value = "example"                          │
└─────────────────────────────────────────────────────┘
          │
          │ Class.forName() / ClassLoader
          ▼
┌─────────────────────────────────────────────────────┐
│  java.lang.Class object (in memory)                 │
├─────────────────────────────────────────────────────┤
│  annotations: Map<Class, Annotation>                │
│  └── MyAnnotation.class -> Proxy instance           │
└─────────────────────────────────────────────────────┘
          │
          │ clazz.getAnnotation(MyAnnotation.class)
          ▼
┌─────────────────────────────────────────────────────┐
│  Dynamic Proxy implementing MyAnnotation            │
├─────────────────────────────────────────────────────┤
│  value() → returns "example"                        │
└─────────────────────────────────────────────────────┘
```

---

# Useful Custom Annotation

Annotation to mark code that is duplicated and be moved to a common place

```java
/**
 * Annotation to mark classes or methods that can be moved to a common library.
 */
@Retention(RetentionPolicy.SOURCE)//discarded by the compiler.
@Target({ElementType.TYPE, ElementType.METHOD})
public @interface MoveToCommonLibrary {
    String description() default "";
}
```

**`@ReviewRequired`** custom annotation for keepping a watch on the tech debt
items

```java
@Target({ElementType.LOCAL_VARIABLE, ElementType.FIELD,ElementType.TYPE, ElementType.METHOD, ElementType.PACKAGE})
@Retention(RetentionPolicy.SOURCE) //discarded by the compiler.
public @interface ReviewRequired {
    String description() default "";

    /**
     * The reviewers assigned to this class/method.
     * @return the list of reviewers
     */
    String[] reviewers() default {"nitin"}; // Using an array for compatibility
}
```