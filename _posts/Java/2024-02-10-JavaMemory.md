---
title:  "Java Memory"
date:   2024-02-10 01:23:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# The Stack, Heap and the Metastack

Every thread will have its own stack which is managed effectively by the Java virtual machine.
Java knows exactly when data on the stack can be destroyed.

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
|result = 24       | 
|temp = 12         |
|data = 10         | <-- Pass By Value Example in modify(int data)
|a=10              |
|args = empty aray |

```

Stacks can only be used to store simple data types like primitives


# The Heap
Complex objects are stored in heap

The data on a stack is restricted to ONE thread and can't be accessed by other threads in our application.

But data on the heap can be accessed by multiple threads.

* the stack is used for local primitives such as ints and doubles, but
* all objects such as Strings, Student,Customer or Integer objects will be stored on the heap

However, there will be a pointer to that object, which is the variable reference and that is stored on the stack.

# Java Memory - The Rules

* Objects are stored on the heap
* Variables are reference to that object
* Local variables (primitives) are stored on the stack

passing variables into methods in Java is always done by making a copy of the variable.

For objects passed as a parameter into a method, then the parameter value will be a copy of the list variable, which is 
a pointer to the object on the heap.

This means that a copy of the pointer to the object is created. The object itself is not copied and in fact it's not the
object that's passed into the method, but rather a pointer to the object.

![java-memory.png](..%2F..%2Fassets%2Fimages%2Fjava-memory.png)


# The immutable classes
Behaves like primitives

The Integer.String, Double, BigDecimal classes are immutable
* its value cannot be changed once it is assigned.

Therefore, an Integer/String object is passed into a method and it is modified it inside the method,
it actually creates a new integer object with the modified value.

![java-memory2.png](..%2F..%2Fassets%2Fimages%2Fjava-memory2.png)

# The final variables

In Java, when you declare a variable as final, it means that the reference to the object cannot be changed once it's 
initialized. However, it does not mean that the state of the object itself cannot be modified.

![java-memory3.png](..%2F..%2Fassets%2Fimages%2Fjava-memory3.png)

# Metaspace - Since Java 8

