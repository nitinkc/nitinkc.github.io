---
title: Records & Sealed Classes
date: 2026-01-20 23:17:00
categories:
- Java
tags:
- Best Practices
---

{% include toc title="Index" %}


Data Oriented Programming with Records and Sealed Classes
## Records
- Low signal to Noise Ratio (no explicit boilerplate code - constructor, getter-setters, toString(), hashCode(), equals())
- Immutable Data Carriers (Record is a **FINAL** Class)
- Auto-generated methods: equals(), hashCode(), toString(), getters

```java
record Person(String name, int age) {}
```

```shell
javac Person.java
javap Person.class

Compiled from "Person.java"
final class Person extends java.lang.Record {
  Person(java.lang.String, int);
  public final java.lang.String toString();
  public final int hashCode();
  public final boolean equals(java.lang.Object);
  public java.lang.String name();
  public int age();
}
```

## Record Features
- is a final class
- Can't have any subclasses
- can't have any base classes as it implicitly extends `java.lang.Record`
  - meaning can put any extends or implements clause
- can have static fields and methods
- can have instance methods
- can have a compact constructor for validation
- May **implement** interfaces
  - record implementing Comparable<T> 
    ```java
    record Person(String name, int age) implements Comparable<Person> {
        @Override
        public int compareTo(Person other) {
            return Integer.compare(this.age(), other.age());
        }
    }
    ```
- record implementing a custom interface
    ```java
    // 
    interface Greeter {
        String greet();
    }
  
    record User(String name) implements Greeter {
        @Override
        public String greet() {
            return "Hello, " + name();
        }
    }
    ```

We should prefer composition over inheritance. Records are great for data carriers but not for complex hierarchies.
- Records enforce composition by being final and not allowing subclassing.

Records are immutable data carriers that promote composition over inheritance, making them ideal for simple data structures without complex behavior.

MAke sure to create record using Strings, primitives other immutable classes/instances and other well created records

Do NOT write constructurot unless you have a scenario for it

When do we need to write constructor in record?
1) Data Clensing or data transformation
2) Validation
- To add validation logic for the fields.


#### List.copyOf()
- Creates an unmodifiable copy of the given collection.
- If the input collection is already unmodifiable, it may return the same instance.
- whats immutable is safe to **SHARE & COPY**

### Compact Constructor
- compact constructor is kind of an interceptor between your call and canonical constructor 
- compact constructor is a middle agent that transform the data and validates as necessary


Do not write canonical constructor(which takes all the arguments) 
- Canonical constructor (All arguments)
  ```java
  record Location(double latitude, double longitude) {
      public Location(double latitude, double longitude) {//Canonical constructor, forces bioler plate
          if (latitude < -90 || latitude > 90) {
              throw new IllegalArgumentException("Invalid latitude: " + latitude);
          }
          if (longitude < -180 || longitude > 180) {
              throw new IllegalArgumentException("Invalid longitude: " + longitude);
          }
          this.latitude = latitude;
          this.longitude = longitude;
  ```
- instead write compact constructor (No argument)
  ```java
  record Location(double latitude, double longitude) {
      public Location {// Compact constructor
          if (latitude < -90 || latitude > 90) {//DATA VALIDATION
              throw new IllegalArgumentException("Invalid latitude: " + latitude);
          }
          if (longitude < -180 || longitude > 180) {
              throw new IllegalArgumentException("Invalid longitude: " + longitude);
          }
      }
  }
  ```
  

# Where can i change final field
1. At the point of declaration'
2. In the constructor (**excluding** compact constructor for records)
3. In an instance initializer block.

Recurds can used to simulate the Tuples

## Sealed Classes & Interfaces
- Restrict which other classes or interfaces may extend or implement them.
- Use `permits` clause to specify allowed subclasses.
- Can be `abstract`, `interface`, or `enum`.
```java
sealed class Shape permits Circle, Rectangle {}  
```   

If not using modules, all the permitted subclasses must be in the **same package** as the sealed class.
- Subclasses must be declared as `final`, `sealed`, or `non-sealed`.
- `final`: No further subclassing allowed. (Records can be a good candidate for final subclasses)
- `sealed`: If you want it to serve as Base. Further restrict subclassing
- `non-sealed`: Remove restrictions, allowing unrestricted subclassing. Anyone can inherit from it
  - mark it non-sealed very carefully as it breaks the sealed class hierarchy
    - if you want to create some experimental classes and not have to keep hacking
```java
final class Circle extends Shape {}     
```

Recommendations:
If you decide to use non sealed, please keep that class or interface as non public (package-private)
- This way you can control who can extend it within the package
- can create experimental classes without exposing them to the entire world.
