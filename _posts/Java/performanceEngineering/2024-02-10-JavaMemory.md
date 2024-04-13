---
title:  "Java Memory"
date:   2024-02-10 01:23:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# The Stack, Heap and the Metaspace (Summary)

**Stack**

- JVM Argumenr - `Xss`
- stores method invocations and local variables.
- **Each thread in a Java program has its own stack**.
- When a method is called, a new frame is pushed onto the stack, which contains the method's parameters, local variables, and return address.
- last-in-first-out (LIFO)
- Stack memory is relatively small and fixed in size, typically around a few megabytes.
- Stack memory is efficient for managing method calls and local variables, but it's limited in size and can lead to stack overflow errors if exceeded.

**Heap**
- JVM Argumenr - `Xms Xmx`
- Stores objects and their instance variables
- The heap is a region of memory used for dynamic memory allocation.
- **shared among all threads** in a Java application.
- The heap is divided into two main regions: the young generation and the old generation.
  - Young generation is further divided into Eden space, and two survivor spaces (S0 and S1).

Objects are initially allocated in the Eden space. When Eden space fills up, **a minor garbage collection occurs**, 
and the surviving objects are moved to one of the survivor spaces.

Objects that survive several garbage collection cycles in the young generation are eventually promoted to the old generation.

The heap is larger and more flexible than the stack, but it's also more prone to fragmentation and garbage collection pauses.
  
**Metaspace**

- Metaspace, introduced in Java 8, replaces the older "permanent generation" (PermGen) for storing metadata related to classes and methods.
- It stores information such as class definitions, method information, and constant pool data.
- Unlike PermGen, metaspace is not part of the Java heap but is allocated from the native memory of the operating system.
- Metaspace automatically grows or shrinks based on the application's demand and the available native memory.
- The use of metaspace helps to avoid some of the limitations and issues associated with PermGen, such as memory leaks caused by classloader leaks.

Check [https://nitinkc.github.io/java/GarbageCollections/#generational-garbage-collection](https://nitinkc.github.io/java/GarbageCollections/#generational-garbage-collection)

# Stack
Every thread will have its own stack which is managed effectively by the Java virtual machine.

Java knows exactly when data on the stack can be destroyed (via [Automatic Garbage Collection Process](https://nitinkc.github.io/java/GarbageCollections))

```java
public static void main(String[] args) {
    int a = 10;//All nums are primitive
    int value = modify(a);
}

private static int modify(int data) {
    int temp = data + 2;
    int result = temp * 2;
    return result;
}
```

The Corrosponding Stack prior to `return result`
```log
|result = 24        | 
|temp = 12          |
|data = 10          | <-- Pass By Value Example in modify(int data)
|a=10               |
|args = empty array |

```

Stacks can only be used to store simple data types like primitives

For complex data types, Stack entry keeps a pointer to the object 

# The Heap

Objects and their instance variables are stored in heap

The data on a stack is restricted to ONE thread and can't be accessed by other threads in our application.

But data on the heap can be accessed by multiple threads.

* the stack is used for local primitives such as ints and doubles, but
* all objects such as Strings, Student,Customer or Integer objects will be stored on the heap

However, there will be a pointer to that object, which is the variable reference and that is stored on the stack.

# Java Memory - The Rules

* Objects are stored on the heap
* Variables are reference to that object
* Local variables (primitives) are stored on the stack

Passing variables into methods in Java is always done by making a copy of the variable.

For objects passed as a parameter into a method (let's say a List), 
  - the parameter value will be a copy of the list variable, which is 
a pointer to the object on the heap.

This means that a copy of the pointer to the object is created. The object itself is not copied (into the stack) and in fact it's not the
object that's passed into the method, but rather a pointer to the object.

![java-memory.png]({{ site.url }}/assets/images/java-memory.png)


# The immutable classes
Behaves like primitives

The Integer.String, Double, BigDecimal classes are immutable
* its value cannot be changed once it is assigned.

Therefore, an Integer/String object is passed into a method and it is modified it inside the method,
it actually creates a new integer object with the modified value.

![java-memory2.png]({{ site.url }}/assets/images/java-memory2.png)

# The final variables

In Java, when you declare a variable as final, it means that the reference to the object cannot be changed once it's 
initialized. However, it does not mean that the state of the object itself cannot be modified.

![java-memory3.png]({{ site.url }}/assets/images/java-memory3.png)

# Metaspace - Since Java 8

