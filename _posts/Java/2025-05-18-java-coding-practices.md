---
categories: Java
date: 2025-05-18 23:17:00
tags:
- Best Practices
- Clean Code
title: Java Coding Practices
---

{% include toc title="Index" %}

### **1. Embrace Immutability**

✅ **Good**: Use `final` and immutable classes
❌ **Bad**: Mutable fields and public setters

##### `final` Fields
- To clearly express intent that a field is constant **after construction**
- For immutable objects (e.g., User, Car, Config).
- To guarantee thread safety for shared data.
```java
// ✅ Good
public final class User {
    private final String name;// ✅ Immutable

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

##### `final` Method Parameters
Use final to prevent accidental reassignment of method arguments.

- In large methods where reassignment might cause confusion.
- When passing parameters to inner classes or lambdas (required to be effectively final).

```java
public void printUser(final String name) {
    System.out.println(name);
    name = "New Name"; // ❌ Compilation error
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
{% gist nitinkc/456cae4080354d855553419b5f09a82d %}

---

### **4. Master Exception Handling**

✅ **Good**: Catch specific exceptions  
❌ **Bad**: Catch `Exception` or ignore/swallow it

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

#### ✅ **Why Use `ConcurrentHashMap`?**

- **Thread Safety Without Synchronization Bottlenecks**: Unlike `HashMap`, which is not thread-safe, or `Collections.synchronizedMap()`, which locks the entire map, `ConcurrentHashMap` uses **fine-grained locking** (bucket-level or segment-level), allowing better concurrency.
- **No `ConcurrentModificationException`**: Iterators are **weakly consistent**, meaning they reflect some, but not necessarily all, updates made after the iterator was created.
- **Atomic Operations**: Methods like `putIfAbsent`, `computeIfAbsent`, and `compute` allow atomic updates, which are crucial in concurrent environments.


**Scenarios Where `ConcurrentHashMap` Is Useful**

#### 1. **Caching Frequently Accessed Data**
```java
ConcurrentHashMap<String, Object> cache = new ConcurrentHashMap<>();
cache.putIfAbsent("user_123", fetchUserFromDB("user_123"));
```
- Multiple threads can read/write to the cache without blocking each other.

#### 2. **Counting Word Frequencies in Parallel**
```java
Map<String, Integer> wordCounts = new ConcurrentHashMap<>();
words.parallelStream().forEach(word ->
    wordCounts.merge(word, 1, Integer::sum)
    wordCounts.merge(word, 1, (oldVal,newVal) -> oldVal + newVal)
);
// key: The key with which the resulting value is to be associated.
// value: The non-null value to be merged with the existing value.
// remappingFunction: A function that takes the existing value and the new value, 
    // and returns the value to be associated with the key.
```
- Efficiently aggregates counts without race conditions.

#### 3. **Storing Session Data in a Web Server**
```java
Map<String, Session> sessions = new ConcurrentHashMap<>();
```
- Each thread handling a request can safely read/write session data.

#### 4. **Tracking Active Users in a Chat App**
```java
Map<String, UserConnection> activeUsers = new ConcurrentHashMap<>();
```
- Threads can add/remove users as they join/leave without locking the whole map.

#### 5. **Implementing a Thread-Safe Singleton Registry**
```java
Map<String, Object> registry = new ConcurrentHashMap<>();
registry.computeIfAbsent("serviceA", k -> new ServiceA());
```
- Ensures only one instance is created even under concurrent access.

---

### **6. Favor Composition Over Inheritance**

✅ **Good**: Use interfaces and delegate  
❌ **Bad**: Deep inheritance trees

{% gist nitinkc/f6dae5e1acae8ecbda28efb79515141f %}

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

{% gist nitinkc/fe84f4f5b4621919ab0927347922c83d %}

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

### **11. Use Optional to Avoid Nulls**
- Optional<T> is a powerful tool to avoid NullPointerException.
- Use it in return types, not in fields or parameters.