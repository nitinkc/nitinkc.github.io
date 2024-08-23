---
title:  "Java annotations"
date:   2024-08-21 00:17:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

Before, JDK 1.5 XML was used to access metadata. Annotations have replaced it since java 1.5
Spring 2.X was XML based and Spring 3 was Annotation based

```xml
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="http://www.springframework.org/schema/beans
                           http://www.springframework.org/schema/beans/spring-beans.xsd">

    <bean id="myBean" class="com.example.MyBean">
        <property name="message" value="Hello, Spring!"/>
    </bean>

</beans>
```

With Spring 3.x and later, you can use annotations for configuration, which simplifies the setup.

With just one line of Annotation, the xml document is not needed
```java
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class MyBean {
    @Value("Hello, Spring!")
    private String message;

    public String getMessage() {
        return message;
    }
}
```

In Java, annotations have two main types of syntax: declaration and utilization. 

### Declaration Syntax

Declaring a Custom Annotation

Annotations are defined using the `@interface` keyword. Here’s how you can define a simple custom annotation:

```java
@Retention(RetentionPolicy.RUNTIME) // Retention policy: available at runtime
@Target(ElementType.METHOD) // Target: can be applied to methods
public @interface MyCustomAnnotation {
    String description() default "No description"; // Default value for the annotation
}
```
- `@Retention(RetentionPolicy.RUNTIME)`: Specifies that the annotation should be retained at runtime and be available for reflection.
  - Source level
  - Classlevel
- `@Target(ElementType.METHOD)`: Specifies that this annotation can only be applied to methods.
  - Class Level - `ElementType.TYPE`
  - Field leve : `ElementType.FIELD`
  - Similarly for package lever 
- `description() default "No description"`: An element of the annotation with a default value.

### Utilization Syntax
This is where annotation in the code is used. 
Apply annotation to various Java elements (such as methods, classes, fields, etc.) according to its `@Target` specification.


Marker Annotation : @Override

Single Valued Annotation : @SuppressWarning("Unchecked")

Multivalued Annotation : 

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.TYPE)
public @interface MultiValueAnnotation {
    String name();
    int value();
    String[] tags() default {};  // Default empty array
}
```

Usage

```java
@MultiValueAnnotation(
    name = "SampleAnnotation",
    value = 100,
    tags = {"example", "annotation"}
)
public class MyClass {
    // Class implementation
}
```

# Useful Custom Annotation

```java
/**
 * Annotation to mark classes or methods that can be moved to a common library.
 */
@Retention(RetentionPolicy.SOURCE)//discarded by the compiler.
@Target({ElementType.TYPE, ElementType.METHOD})
public @interface MoveToCommonLibrary {
    String description() default "";
}
```



```java
@Target({ElementType.LOCAL_VARIABLE, ElementType.FIELD,ElementType.TYPE, ElementType.METHOD, ElementType.PACKAGE})
@Retention(RetentionPolicy.SOURCE) //discarded by the compiler.
public @interface ReviewRequired {
    String description() default "";

    /**
     * The reviewers assigned to this class/method.
     * @return the list of reviewers
     */
    String[] reviewers() default {"nitin"}; // Using an array for compatibility
}
```