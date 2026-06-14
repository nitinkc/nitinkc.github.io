---
title: Serialization & Externalization
date: 2022-08-03 18:16:00
categories:
- Java
tags:
- Java
---

{% include toc title="Index" %}

## Understanding Serialization and Deserialization in Java
Imagine you have a big balloon that you need to transport. To make it
manageable, you deflate it (serialize it) before sending and inflate it (
deserialize it) after receiving.

Think of serialization as **packing** an object into a byte stream, and deserialization as **unpacking** it back into a live object.
This lets you store or transmit object state and reconstruct it later.

## Serialization and Deserialization (Quick Summary)
- **Serialization:** Convert an object’s state to a byte stream (disk/network).
- **Deserialization:** Reconstruct the object from that byte stream.

## Serializable Interface (Marker)
To make a class serializable, implement `Serializable` (a **marker** interface with no methods).
It signals the JVM that instances can be serialized/deserialized.

### Key Points
- **Object References:** referenced objects must also implement `Serializable`.
- **Static Members:** not serialized (belong to the class, not the instance).
- **Transient Keyword:** excludes fields from serialization.

## Serial Version UID (SUID)
`serialVersionUID` verifies that the serialized data matches the current class definition.

- **Automatic SUID:** JVM generates it from class details (methods/fields). This can vary across JDKs/platforms.
- **Explicit SUID (recommended):** define it yourself for stable compatibility.

```java
public class Example implements Serializable {
    private static final long serialVersionUID = 1L; // Explicit SUID
}
```

By explicitly defining `serialVersionUID`, you control versioning and reduce `InvalidClassException` risk across environments.

## Field Behavior Summary
- **static:** not serialized.
- **transient:** not serialized; default value on deserialization.
- **static transient:** still not serialized.
- **final transient:** value stays constant, but still not serialized.

{% gist nitinkc/4207435e2c4b6d854ab7a7909556072c %}

# Incompatible Changes to a Serialized Class

When a serialized class changes, deserialization can fail with `InvalidClassException`
if the stored data no longer matches the class structure (or SUID).

Common incompatible changes:

## Incompatible Changes

1. **Adding a New Field**

- **Impact:** If you add a new field to a class, objects serialized with the old
  version of the class won’t have data for this new
  field. When deserialized, the new field will be initialized to its default
  value.

  ```java
  // Old Version
  public class Example implements Serializable {
    private static final long serialVersionUID = 1L;
    private int oldField;
  }
  
  // New Version with additional field
  public class Example implements Serializable {
    private static final long serialVersionUID = 2L; // Updated SUID
    private int oldField;
    private String newField; // Newly added field
  }
  ```

2. **Changing a Field from Static to Non-static**

- **Impact:** Changing a field from static to non-static will affect the
  serialization process because static fields are not serialized.
  The non-static field will be serialized and deserialized, but its value will
  be missing in older serialized data.

    ```java
    // Old Version
    public class Example implements Serializable {
      private static final long serialVersionUID = 1L;
      private static int staticField; // Not serialized
    }
    
    // New Version with non-static field
    public class Example implements Serializable {
      private static final long serialVersionUID = 2L; // Updated SUID
      private int nonStaticField; // Now serialized
    }
    ```

3. **Changing a Field from Transient to Non-transient**

- **Impact:** Changing a field from transient to non-transient means the field
  will now be serialized.
  During deserialization, the field will be restored with the value saved in the
  serialized data.

    ```java
    // Old Version
    public class Example implements Serializable {
      private static final long serialVersionUID = 1L;
      private transient int transientField; // Not serialized
    }
    
    // New Version with non-transient field
    public class Example implements Serializable {
      private static final long serialVersionUID = 2L; // Updated SUID
      private int nonTransientField; // Now serialized
    }
    ```

4. **Adding a Class to the Object Tree**

- **Impact:** Adding a new class to the object tree requires that the new class
  also implements `Serializable`.
  If it does not, deserialization may fail.

    ```java
    // Old Version
    public class Example implements Serializable {
      private static final long serialVersionUID = 1L;
      private String field;
    }
    
    // New Version with additional class
    public class Example implements Serializable {
      private static final long serialVersionUID = 2L; // Updated SUID
      private String field;
      private NewClass newClass; // New class added
    }
    
    public class NewClass implements Serializable {
      private static final long serialVersionUID = 1L;
      private int newField;
    }
    ```

# Saving Object State

Serialization allows you to persist object state beyond a JVM lifecycle:
- **Network transfer**
- **File system or database**
- **Note:** Only object state is saved (not class files or methods). The class must be available during deserialization.

# `Externalizable` Interface

The `Externalizable` interface extends `Serializable` and provides more control
over the serialization process.
Unlike `Serializable`, `Externalizable`  requires you to implement two methods:

- `writeExternal` and
- `readExternal`.

These methods allow you to define exactly how the object's data is serialized
and deserialized.

- When you serialize object using `Extenalizable` interface then while
  `deserilizing` it calls `constructor`(class must have public and default
  constructor).
- When you serialize object using `Serializable` interface then while
  deserializing it is not going to call constructor.
- when a class implements Serializable interface, default Serialization process
  gets kicked of and that takes responsibility of serializing super class state.
- When any class in Java implement `java.io.Externalizable` than its programmers
  responsibility to implement Serialization process.
- By using `java.io.Externalizable` interface you can create your own custom
  binary format for your object.

{% gist nitinkc/c4271b9841e6fcff023690be48c468d1 %}