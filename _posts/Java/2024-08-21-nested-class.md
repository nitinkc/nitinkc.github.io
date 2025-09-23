---
categories: Java
date: 2024-08-21 00:17:00
tags:
- Java
title: Nested Classes in Java
---

{% include toc title="Index" %}

**Logical Grouping**: If a class is useful only to one other class, embedding it
within that class makes the code more
logically organized.

- For example, if an inner class is only used by its outer class, it is sensible
  to define it within the outer class
  to group related functionalities together.

**Increased Encapsulation**: By embedding classes within another class, you can
restrict access to them, enhancing encapsulation.

- This is particularly useful when you want to hide implementation details from
  other parts of your application.

**Readability and Maintainability**: Using inner classes can make your code more
readable and maintainable by keeping
related classes together and reducing the scope of access.

In Java, a class can be defined within another class, which is known as a nested
class.
The outer class is the class containing the nested class, and the nested class
is the class defined within the outer class.
Nested classes are categorized into two main types:

- static and
- non-static.

## Types of Nested Classes

> Map.Entry is an example of inner class

```
Nested Class
|
├── Static Nested Class
|
└── Inner Class
    |
    ├── Instance Inner Class
    |
    ├── Method-local Inner Class
    |
    └── Anonymous Inner Class
```

### **Static Nested Class**

- A static class defined within another class.
- **Characteristics:**
    - Can be instantiated without an instance of the outer class.
    - Can only access static members of the outer class.
    - Useful for logically grouping classes that do not need to access
      instance-specific data.

  ```java
  public class Outer {
     private static final String staticOuterField = "Static Outer Field";
  
     static class StaticNested {
         void display() {
             System.out.println("Accessing static outer field: " + staticOuterField);
         }
     }
  
     public static void main(String[] args) {
         Outer.StaticNested nested = new Outer.StaticNested();
         nested.display();
     }
  }
```

### **Non-static Nested Classes (Inner Classes)**

- **Instance Inner Class**
    - A class defined within another class but outside any method.
    - **Characteristics:**
        - Each instance of an instance inner class is associated with an
          instance of the outer class.
        - Can access all members (including private members) of the outer class.
        - Requires an instance of the outer class for instantiation.

  ```java
  public class Outer {
    private final String outerField = "Outer Field";
  
    class Inner {
        void display() {
            System.out.println("Accessing outer field: " + outerField);
        }
    }
  
    public static void main(String[] args) {
        Outer outer = new Outer();
        Outer.Inner inner = outer.new Inner();
        inner.display();
    }
  }
```

### **Method-local Inner Class**

- A class defined within a method of the outer class.
- **Characteristics:**
    - Scope is restricted to the method where it is defined.
    - Cannot have access modifiers or static members.
    - Can access final or effectively final local variables of the enclosing
      method.

    ```java
    public class Outer {
      void myMethod() {
          final int num = 23;
    
          class MethodLocalInner {
              void print() {
                  System.out.println("This is method-local inner class: " + num);
              }
          }
    
          MethodLocalInner inner = new MethodLocalInner();
          inner.print();
      }
    
      public static void main(String[] args) {
          Outer outer = new Outer();
          outer.myMethod();
      }
    }
    ```

### **Anonymous Inner Class**

- A class defined and instantiated in a single expression.
- **Characteristics:**
    - No name assigned to the class.
    - Commonly used(prior to Java 1.8) for quick implementations of interfaces
      or abstract classes.

    ```java
    public class Outer {
      interface Test {//Functional Interface, SAM
          void testing();
      }
    
      public static void main(String[] args) {
          Test test = new Test() {
              @Override
              public void testing() {
                  System.out.println("Hello from anonymous inner class!");
              }
          };
    
          test.testing();
      }
    }
    ```

##### Anonymous Inner Class vs Lambda

Anonymous class was the only way to implement functional idiom prior to Java 8

> Lambda can replace Anonymous

```java
public class Outer {
  interface Test {//Functional Interface, SAM
      void testing();
  }

  public static void main(String[] args) {
    //Providing the implementation of the testing() method
      Test test = () -> System.out.println("Hello from anonymous inner class!");
      test.testing();
  }
}
```