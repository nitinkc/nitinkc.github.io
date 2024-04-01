---
title:  "Wrapper Classes - Parse & ValueOf"
date:   2023-01-03 02:30:00
categories: ['Java']
tags: ['Java']
---
{% include toc title="Index" %}

`parse` methods are more commonly used for parsing simple primitive values from strings.

`valueOf` methods are useful when 
- you need to handle cases where the **input can be `null`** or
- when you want to work with wrapper objects.

### Difference between `parse` and `valueOf` Methods

Both `parse` and `valueOf` methods are used to convert Strings (textual representations)
of primitive data types or objects into their respective Java types. 

However, there are some differences between the two methods:

1. **Usage**:
    - `parse` methods are usually static methods defined in primitive wrapper classes (`Integer`, `Double`, etc.) and
   the `java.time` classes for parsing date and time formats.
    - `valueOf` methods are usually static methods defined in primitive wrapper classes (`Integer`, `Double`, etc.), 
   and they return the respective wrapper object. They are also present in some other classes like `Boolean`, `BigInteger`, and `BigDecimal`.

2. **Return Type**:
    - `parse` methods return the primitive data type corresponding to the parsed value. 
   For example, `Integer.parseInt(String)` returns an `int`.
    - `valueOf` methods return an instance of the corresponding wrapper class. 
   For example, `Integer.valueOf(String)` returns an `Integer`.

3. **Exception Handling**:
    - `parse` methods may throw a `NumberFormatException` if the provided string cannot be parsed as the respective primitive type.
    - `valueOf` methods can return `null` if the provided string cannot be parsed, but they generally don't throw exceptions.

4. **Null Handling**:
    - `parse` methods do not handle null values; passing `null` to `parse` methods will result in a `NullPointerException`.
    - `valueOf` methods can handle `null` by returning `null`.

5. **Usages**:
    - `parse` methods are commonly used when you expect valid input and want the parsed primitive value directly. For example, `Integer.parseInt("123")` returns an `int`.
    - `valueOf` methods are often used when you want to handle possible null values or if you need to manipulate the parsed value further. For example, `Integer.valueOf("123")` returns an `Integer`, which can be assigned to an `Integer` reference and can handle null values.


Using `parse`:
```java
int intValue = Integer.parseInt("123");
double doubleValue = Double.parseDouble("3.14");
```

Using `valueOf`:
```java
Integer integerObject = Integer.valueOf("123");
Double doubleObject = Double.valueOf("3.14");
Boolean booleanObject = Boolean.valueOf("true");
```