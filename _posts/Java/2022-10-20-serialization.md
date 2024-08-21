---
title:  "Serialization & Externalization"
date:   2022-08-03 18:16:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}


Imagine you have a big balloon that you need to transport. To make it manageable, you deflate it (serialize it) before sending and inflate it (deserialize it) after receiving.
This analogy helps to understand that serialization makes objects fit for transportation or storage,
and deserialization restores them to their original state.

# Understanding Serialization and Deserialization in Java

## Serialization

Serialization is the process of converting an object's state into a byte stream. 
This byte stream can be saved to disk or transmitted over a network. 
In simpler terms, serialization means turning an object into a format that can be stored or sent.

To make a class serializable, implement the `Serializable` interface, which is a marker interface. 
This interface doesn’t have any methods but signals to the Java runtime that instances of the 
class can be serialized and deserialized.

> Serializable interface is a marker interface

### Key Points:
- **Serializable Interface:** A marker interface that allows Java objects to be serialized. Classes implementing this interface can be converted into a byte stream.
- **Object References:** Any object reference contained within a serializable class must also implement the `Serializable` interface.
- **Static Members:** Static fields are **ignored** during serialization as they belong to the class rather than to any specific object instance.
- **Transient Keyword:** Use the `transient` keyword to **exclude variables** from serialization. This prevents sensitive or unnecessary data from being serialized.

## Deserialization
Deserialization is the reverse process of serialization. It involves reading the byte stream from disk or network and converting it back into a Java object (POJO). Essentially, it reconstructs the object from the byte stream.


### Summary:
- **Serialization:** Writing an object's state to a byte stream for storage or transmission.
- **Deserialization:** Reconstructing the object from the byte stream.


# Serial Version UID (SUID)

**Serial Version UID (SUID)** is a unique identifier used during the serialization process to ensure that a loaded class corresponds to the serialized object. The SUID helps the Java Virtual Machine (JVM) verify that the serialized data is compatible with the current version of the class.

## Automatic vs. Custom SUID
By default, if you don't explicitly define a `serialVersionUID`, the JVM automatically 
generates one based on the class's details, such as its methods and fields. 

However, relying on automatic SUID generation can be risky because:
- **Inconsistencies Across Platforms:** Different Java Development Kit (JDK) versions or platforms (e.g., JDK 8 on Windows vs. OpenJDK 6 on Linux) may generate different SUIDs, leading to compatibility issues.

To avoid these issues, it’s recommended to explicitly define a `serialVersionUID` in your class.

By explicitly defining a serialVersionUID, you maintain control over the versioning of your serialized objects, 
making your code more robust and less prone to compatibility issues across different Java environments.

## Key Points:
- **Static Variables**: Static fields are not part of the serialized object and thus their values are not saved or restored during the serialization process.
- **transient Variables**: These variables are not serialized, so their values are not saved or restored. 
  - They are initialized to their default values upon deserialization.
- **static transient Variables**: Static fields are associated with the class, not with any particular object instance,
  - so they are not serialized.
- **final transient Variables**: The final modifier overrides the transient modifier, meaning the variable's value remains constant, 
  - but it still won't be serialized.

{% gist nitinkc/4207435e2c4b6d854ab7a7909556072c %}

# Incompatible Changes to a Serialized Class

When modifying a class that has already been serialized, certain changes can lead to compatibility issues. 
Specifically, these changes can result in an `InvalidClassException` during deserialization if the Serial Version UID (SUID)
does not match between the serialized data and the current class definition. 

This exception occurs because the JVM detects that the serialized object does not match the class structure expected during 
deserialization. Here are some common scenarios that can cause such issues:

When using RESTful APIs, the data exchanged between the client and server is often serialized into formats such as JSON or XML. 
These serialized formats are then deserialized on the receiving end to reconstruct the original objects. 

If you modify a class that has already been serialized and sent over the network, it can lead to compatibility issues. 
Specifically, these issues can arise if the Serial Version UID (SUID) does not match between the serialized data and 
the current class definition.


## Incompatible Changes

1. **Adding a New Field**
- **Impact:** If you add a new field to a class, objects serialized with the old version of the class won’t have data for this new 
field. When deserialized, the new field will be initialized to its default value.

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
- **Impact:** Changing a field from static to non-static will affect the serialization process because static fields are not serialized. 
The non-static field will be serialized and deserialized, but its value will be missing in older serialized data.

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
- **Impact:** Changing a field from transient to non-transient means the field will now be serialized. 
During deserialization, the field will be restored with the value saved in the serialized data.

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
- **Impact:** Adding a new class to the object tree requires that the new class also implements `Serializable`.
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

## Serial Version UID (SUID)

- **Automatic SUID:** Java generates an SUID automatically based on the class’s structure. If the class structure changes, the SUID may differ, causing deserialization issues.
- **Manual SUID:** Define a static final `serialVersionUID` to maintain compatibility. 
It helps ensure that deserialization only occurs if the SUID matches.

  ```java
      public class Example implements Serializable {
          private static final long serialVersionUID = 1L; // Explicit SUID
      }
    ```

# Saving Object State
Serialization allows you to save an object’s state beyond the lifecycle of the JVM. This includes:

**Network Transfer**: Objects can be serialized and sent over a network.

**File System or Database**: Objects can be saved to files or databases.

**Note**: Only the object’s state is saved, not the class file or methods.
When deserializing, the class definition must be available to reconstruct the object properly.

# `Externalizable` Interface
The `Externalizable` interface extends `Serializable` and provides more control over the serialization process. 
Unlike `Serializable`, `Externalizable`  requires you to implement two methods: 
- `writeExternal` and 
- `readExternal`.

These methods allow you to define exactly how the object's data is serialized and deserialized.

- When you serialize object using `Extenalizable` interface then while `deserilizing` it calls `constructor`(class must have public and default constructor).
- When you serialize object using `Serializable` interface then while deserializing it is not going to call constructor. 
- when a class implements Serializable interface, default Serialization process gets kicked of and that takes responsibility of serializing super class state. 
- When any class in Java implement `java.io.Externalizable` than its programmers responsibility to implement Serialization process.
- By using `java.io.Externalizable` interface you can create your own custom binary format for your object.

{% gist nitinkc/c4271b9841e6fcff023690be48c468d1 %}