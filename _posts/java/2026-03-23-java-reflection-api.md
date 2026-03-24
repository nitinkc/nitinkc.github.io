---
layout: post
title: "Java Reflection API: Class Objects, Metadata, and Instantiation"
date: 2026-03-23
categories: [java, reflection]
tags: [class, metadata, constructors, methods, fields]
---

[Reflection API test code](https://github.com/nitinkc/JavaConcepts/tree/main/src/main/java/nitin/reflectionAPI)

## 1) The `Class` object: the entry point to reflection

For every loaded type, the JVM keeps exactly one `Class` object. 
The first learning milestone is to obtain that `Class` instance in three common ways:

```java
// 1) .class literal
Class<?> c1 = ReflectionTestClass.class;

// 2) Object instance
ReflectionTestClass obj = new ReflectionTestClass();
Class<?> c2 = obj.getClass();

// 3) Fully-qualified class name
Class<?> c3 = Class.forName("nitin.reflectionAPI.ReflectionTestClass");
```

This is the idea behind `R1BasicRefAPITest`: you can navigate from a name, an object, or a literal to the same `Class` instance.

## 2) Class identity and equality

Once you hold `Class` references, you can compare them directly. The `R2ReflectionEquality` example shows they are identical for the same loaded type:

```java
Class<?> c1 = ReflectionTestClass.class;
Class<?> c2 = Class.forName("nitin.reflectionAPI.ReflectionTestClass");
Class<?> c3 = new ReflectionTestClass().getClass();

System.out.println(c1 == c2); // true
System.out.println(c1 == c3); // true
```

This confirms there is exactly one `Class` object per loaded type (per class loader).

## 3) Inspect class metadata: methods, fields, constructors

Reflection is powerful because you can discover structure at runtime. `R3ReflectionProbeMethods` demonstrates:

- Declared methods vs. public methods (including inherited ones)
- Declared fields vs. public fields
- Constructors
- Implemented interfaces
- Superclass

A condensed version:

```java
Class<?> c = Class.forName("nitin.reflectionAPI.ReflectionTestClass");

for (Method m : c.getDeclaredMethods()) {
    System.out.println(m);
}

for (Field f : c.getDeclaredFields()) {
    System.out.println(f);
}

for (Constructor<?> ctor : c.getDeclaredConstructors()) {
    System.out.println(ctor);
}

System.out.println("Superclass: " + c.getSuperclass());
```

This is the core reflection toolkit: you can discover the shape of a class even if you never compiled against it.

## 4) Object creation patterns (including reflection)

There are four different ways to create objects in java:

1. Using `new` keyword
2. Using `Class.forName()`://reflection
3. Using `clone()`:
4. Using Object Deserialization: Using `new Instance()` method

A clarifying note: `Class.forName()` loads the class. To instantiate, use `getDeclaredConstructor().newInstance()` (preferred) or the older `Class.newInstance()` (deprecated). Object deserialization uses `ObjectInputStream.readObject()` to create a new instance from bytes.

### Example: practical instantiation styles

```java
// 1) new keyword
Student student = new Student();

// 2) reflection + no-args constructor
Class<?> c = Class.forName("nitin.reflectionAPI.Student");
Student byReflection = (Student) c.getDeclaredConstructor().newInstance();

// 3) clone (requires Cloneable + proper override)
// Student cloned = (Student) student.clone();

// 4) deserialization (requires Serializable)
// Student deserialized = (Student) new ObjectInputStream(in).readObject();
```

## 5) Reflection can bypass access checks

Private constructor **doesn't protect** from instantiation via **reflection**. Reflection can make non-public constructors accessible:

```java
class Secret {
    private Secret() {}
}

Constructor<Secret> ctor = Secret.class.getDeclaredConstructor();
ctor.setAccessible(true); // bypass access checks
Secret secret = ctor.newInstance();
```

This is why frameworks can still create instances of classes that are not publicly instantiable. In production, you should combine reflection with validation and be cautious about security assumptions.

## 6) Putting it together: a small, cohesive reflection walkthrough

Here is a compact, runnable example aligned to `nitin.reflectionAPI` types:

```java
Class<?> type = Class.forName("nitin.reflectionAPI.ReflectionTestClass");
System.out.println("Class name: " + type.getName());

for (Field field : type.getDeclaredFields()) {
    System.out.println("Field: " + field.getName());
}

Constructor<?> ctor = type.getDeclaredConstructor();
Object instance = ctor.newInstance();
System.out.println("Instance type: " + instance.getClass().getSimpleName());
```
