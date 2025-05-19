---
title:  "Java Coding Practices"
date:   2025-05-18 23:17:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

### **1. Embrace Immutability**

✅ **Good**: Use `final` and immutable classes  
❌ **Bad**: Mutable fields and public setters

```java
// ✅ Good
public final class User {
    private final String name;

    public User(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }
}

// ❌ Bad
public class MutableUser {
    public String name;

    public void setName(String name) {
        this.name = name;
    }
}
```

---

### **2. Leverage Streams and Functional Programming**

✅ **Good**: Use `Stream` for clean data processing  
❌ **Bad**: Manual loops for everything

```java
// ✅ Good
List<String> names = people.stream()
    .filter(p -> p.getAge() > 30)
    .map(Person::getName)
    .collect(Collectors.toList());

// ❌ Bad
List<String> names = new ArrayList<>();
for (Person p : people) {
    if (p.getAge() > 30) {
        names.add(p.getName());
    }
}
```

---

### **3. Use Design Patterns Thoughtfully**

✅ **Good**: Use Builder for complex object creation  
❌ **Bad**: Telescoping constructors

```java
// ✅ Good - Builder Pattern
public class Car {
    private final String engine;
    private final int wheels;

    private Car(Builder builder) {
        this.engine = builder.engine;
        this.wheels = builder.wheels;
    }

    public static class Builder {
        private String engine;
        private int wheels;

        public Builder engine(String engine) {
            this.engine = engine;
            return this;
        }

        public Builder wheels(int wheels) {
            this.wheels = wheels;
            return this;
        }

        public Car build() {
            return new Car(this);
        }
    }
}

// ❌ Bad - Telescoping Constructor
public class Car {
    private String engine;
    private int wheels;

    public Car(String engine) {
        this(engine, 4);
    }

    public Car(String engine, int wheels) {
        this.engine = engine;
        this.wheels = wheels;
    }
}
```

---

### **4. Master Exception Handling**

✅ **Good**: Catch specific exceptions  
❌ **Bad**: Catch `Exception` or ignore it

```java
// ✅ Good
try {
    Files.readAllLines(Path.of("file.txt"));
} catch (IOException e) {
    System.err.println("File read error: " + e.getMessage());
}

// ❌ Bad
try {
    // risky code
} catch (Exception e) {
    // silently ignore
}
```

---

### **5. Write Thread-Safe Code**

✅ **Good**: Use `ConcurrentHashMap`  
❌ **Bad**: Use unsynchronized shared data

```java
// ✅ Good
Map<String, Integer> map = new ConcurrentHashMap<>();
map.put("key", 1);

// ❌ Bad
Map<String, Integer> map = new HashMap<>();
map.put("key", 1); // Not thread-safe
```

---

### **6. Favor Composition Over Inheritance**

✅ **Good**: Use interfaces and delegate  
❌ **Bad**: Deep inheritance trees

```java
// ✅ Good
interface Engine {
    void start();
}

class Car {
    private final Engine engine;

    public Car(Engine engine) {
        this.engine = engine;
    }

    public void start() {
        engine.start();
    }
}

// ❌ Bad
class Vehicle {
    void start() {}
}

class Car extends Vehicle {
    // tightly coupled
}
```

---

### **7. Apply SOLID Principles**

✅ **Good**: One class = one responsibility  
❌ **Bad**: God classes

```java
// ✅ Good
class InvoicePrinter {
    void print(Invoice invoice) {}
}

class InvoiceSaver {
    void save(Invoice invoice) {}
}

// ❌ Bad
class InvoiceManager {
    void print(Invoice invoice) {}
    void save(Invoice invoice) {}
}
```

---

### **8. Use Dependency Injection**

✅ **Good**: Inject via constructor  
❌ **Bad**: Instantiate dependencies inside class

```java
// ✅ Good
class Service {
    private final Repository repo;

    public Service(Repository repo) {
        this.repo = repo;
    }
}

// ❌ Bad
class Service {
    private final Repository repo = new Repository(); // hard to test
}
```

---

### **9. Optimize with Profiling, Not Guesswork**

✅ **Good**: Use profilers  
❌ **Bad**: Premature optimization

```java
// ✅ Good
// Use JVisualVM or Flight Recorder to identify slow methods

// ❌ Bad
// Rewriting code for performance without knowing if it's a bottleneck
```

---

### **10. Write Tests Like a Pro**

✅ **Good**: Use JUnit and Mockito  
❌ **Bad**: No tests or untestable code

```java
// ✅ Good
@Test
void testAddition() {
    Calculator calc = new Calculator();
    assertEquals(5, calc.add(2, 3));
}

// ❌ Bad
// No tests or tests that rely on external systems
```

---

Use Optional to Avoid Nulls
Optional<T> is a powerful tool to avoid NullPointerException.
Use it in return types, not in fields or parameters.


