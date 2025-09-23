---
categories: Java
date: 2023-11-24 23:23:00
tags:
- Java
title: Exceptions in Java
---

{% include toc title="Index" %}

Exception handling is fundamentally an **imperative style** of programming idea.

**Functional programming and Exception handling are mutually exclusive**

For Functional programming,

- Deal with the errors downstream and
- treat errors as another form of data.

##### The failed data vs success data.

Do not blow up the pipeline

In Reactive streams, errors are dealt in a separate channel

```java
reactiveStream
    .map()
    .filter(interfaceThatSupportsException)
    .map()
    .subscribe(
            data -> handleData(data),//Data Channel
            err -> handleErr(err), //error channel
            () -> done() //Complete channel
    )
```

Java exceptions are **objects** that represent abnormal conditions or error
situations during the execution of a program.

Exceptions are categorized into **two main types**:

### Checked Exceptions

- Checked exceptions represent exceptional conditions that an application *
  *should anticipate and recover from**.

- These are checked at compile-time, and the compiler forces you to handle them
  using a `try-catch block`
  or declare them in the `throws clause of the method`.

  **Examples: IOException, SQLException, FileNotFoundException.**

### Unchecked Exceptions (Runtime Exceptions)

Unchecked exceptions represent conditions that generally **reflect programming
bugs** and
are not expected to be recovered during normal program execution.

They are not required to be caught or declared explicitly.

* The program won’t give a compilation error.
* Handling is NOT verified during Compile time.
* These exceptions occur because of bad programming.
* All Unchecked exceptions are direct sub-class of `RuntimeException` class.

##### Common unchecked Exceptions

1. ArithmaticException : divide by zero
2. ArrayIndexOutOfBounds : illegal index access
3. ClassCastException : cast an object to a subclass which it is not an instance
4. IllegalArgumentException : method has been passed an illegal or inappropriate
   argument
4. NullPointerException : null reference where an object is required
1. NumberFormatException : when an attempt is made to convert a STRING to
   numeric type
1. IllegalStateException : attempting to run an invalid operation in collection
   adn Concurrency
1. UnsupportedOperationException : --do--

# Checked vs Unchecked Exceptions

| Property                             | Checked Exception                                                                 | Unchecked Exception                                                                      |
|--------------------------------------|-----------------------------------------------------------------------------------|------------------------------------------------------------------------------------------|
| **Also Known As**                    | Compile-time exceptions                                                           | Runtime exceptions                                                                       |
| **Should Be Solved At**              | Compile time                                                                      | Runtime                                                                                  |
| **Benefit/Advantage**                | Ensures issues are fixed at compile time to avoid runtime problems                | Handles interruptions at runtime and provides meaningful messages to users               |
| **Creating Custom Exceptions**       | `class UserException extends Exception { UserException(String s) { super(s); } }` | `class UserException extends RuntimeException { UserException(String s) { super(s); } }` |
| **Exception Propagation**            | Must use `throws` keyword                                                         | Automatically propagated                                                                 |
| **Handling in Subclass**             | Must handle or declare narrower checked exceptions                                | Can declare/throw any unchecked exception; cannot declare checked exceptions             |
| **Which Classes Are Which Type?**    | `Exception` and its subclasses (excluding `RuntimeException`) are checked         | `RuntimeException` and its subclasses are unchecked                                      |
| **Most Frequently Faced Exceptions** | `SQLException`, `IOException`, `ClassNotFoundException`                           | `NullPointerException`, `ArithmeticException`, `ArrayIndexOutOfBoundsException`          |

### Error

Errors represent more serious, unrecoverable problems that are not typically
handled by the application.

errors are not caught or handled by the application code.

**Examples: OutOfMemoryError, StackOverflowError, VirtualMachineError.**

### Custom Exceptions

Developers can create their own exceptions by

- extending the **Exception** class for **checked exceptions** or
- extending the **RuntimeException** class for **unchecked exceptions**.

Custom exceptions are handled in a similar way to built-in exceptions.

Handling exceptions in Java is typically done using try, catch, and finally
blocks.

# Try with resources

The `try-with-resources` syntax introduced in java 7,
automatically closes all resources opened in the try clause.

This feature is known as automatic resource management

Resources are automatically closed at the end of the try block with
`try-with-resources`.
This simplifies resource management and reduces the likelihood of resource
leaks.

Only try-with-resources statement is permitted to omit both the catch and
finally blocks
{: .notice--info}

The resources created in the try clause are **only in scope within the try block
**.

### AutoCloseable

Java Commits to closing any resource opened in the try-with-resource block.

For this reason the resource must be **closeable**.
Auto Closeable interface has only one method `close()`

Checked Exception thus have to give a catch block

### Basic File Reading

```java
try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
    String line;
    while ((line = reader.readLine()) != null) {
        System.out.println(line);
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

### HTTP Connection:

```java
 try {
    URL url = new URL(urlString);
    HttpURLConnection connection = (HttpURLConnection) url.openConnection();

    try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
        String line;
        while ((line = reader.readLine()) != null) {
            System.out.println(line);
        }
    }
} catch (IOException e) {
    e.printStackTrace();
}
```

### Database Connection :

```java
try (Connection connection = DriverManager.getConnection(jdbcUrl, username, password);
             Statement statement = connection.createStatement();
             ResultSet resultSet = statement.executeQuery("SELECT * FROM your_table")) {

    while (resultSet.next()) {
        System.out.println(resultSet.getString("column_name"));
    }
} catch (SQLException e) {
    e.printStackTrace();
}
```

# Multi-catch

- The exceptions caught in a multi-catch block must be **unrelated** in the
  class hierarchy.
- The final variable inside the catch block (in this case, e) is **implicitly
  final**, so you cannot reassign it within the block.

```java
// A method that may throw different exceptions
private static int divide(int dividend, int divisor) {
    // Potential division by zero and potential null pointer exceptions
    return dividend / divisor;
    }
    
// In the Calling Method    
try {
    // Code that may throw different exceptions
    int result = divide(10, 0);
    System.out.println("Result: " + result);
} catch (ArithmeticException | NullPointerException e) {
    // Multi-catch block handling ArithmeticException and NullPointerException
    System.out.println("An exception occurred: " + e.getMessage());
}
```

# Exception Chaining

```java
try {
    // Code that may throw different exceptions
    int result = divide(10, 0);
    System.out.println("Result: " + result);
} catch (ArithmeticException e) {
    // Handling ArithmeticException
    System.out.println("ArithmeticException occurred: " + e.getMessage());
} catch (NullPointerException e) {
    // Handling NullPointerException
    System.out.println("NullPointerException occurred: " + e.getMessage());
}
```

# Custom Exceptions

You can create your own custom exceptions by **extending the Exception class**
or one of its subclasses.

This allows you to define application-specific exception types.

```java
class CustomException extends Exception {
    // Custom exception code
}
```

# Finally Block

The `finally` block is used to execute code that should be run regardless of
whether an exception is thrown or not.

- often used for cleanup operations, such as closing resources.

```java
try {
    // Code that may throw an exception
} catch (Exception e) {
    // Exception handling
} finally {
    // Code to be executed whether an exception occurs or not
}
```

##### Try-Finally

Try with finally and without catch is allowed

```java
try{
   result = divident/divisor;
}finally {
   System.out.println("This will always run");
}
```

# ClassNotFoundException vs NoClassDefFoundError

Both `ClassNotFoundException` and `NoClassDefFoundError` indicate issues with
class loading, but they occur in different scenarios:

### ClassNotFoundException

| Property          | ClassNotFoundException                               | NoClassDefFoundError                                 |
|-------------------|------------------------------------------------------|------------------------------------------------------|
| **Type**          | Exception (`java.lang.Exception`)                    | Error (`java.lang.Error`)                            |
| **Occurs When**   | Class not found in classpath at runtime              | Class present at compile time but missing at runtime |
| **Thrown By**     | Application (e.g., `Class.forName()`, `loadClass()`) | Java Runtime System                                  |
| **Typical Cause** | Classpath not updated with required JAR files        | Required class definition missing at runtime         |

For more information, visit:

- [ClassNotFoundException vs NoClassDefFoundError](http://javaconceptoftheday.com/classnotfoundexception-vs-noclassdeffounderror-in-java/)
- [Stack Overflow Discussion](http://stackoverflow.com/questions/1457863/what-causes-and-what-are-the-differences-between-noclassdeffounderror-and-classn)