---
categories: Java
date: 2021-10-13 21:55:00
tags:
- Optional
- Null Safety
- Java 8
- Best Practices
title: Optional Use cases
---

{% include toc title="Index" %}

**Null is a smell**

* New class in `java.util package`
* optional provides a means for a function returning a value to indicate the
  value could possibly be null.
* Optional is a box that **hold at most one value**, like Collections and
  Arrays, in it
* Optional is of **16 bytes**, and is an `Object`.
* creates a separate memory, excessive use should be avoided, as it can create
  performance issues.
* Optional is **immutable**. Once assigned, it cannot be reassigned.

# Creating Optional - .of() vs .ofNullable()

**`Optional.of()`**

- Creates an Optional with a non-null value.
- If you pass **null** to this method, it throws a **NullPointerException**.
- Use Case: Use `Optional.of()` when you are certain that the value you are
  wrapping is not null.

**`Optional.ofNullable()`**

- Creates an Optional that can hold **either a non-null value or null**.
- If you pass null to this method, it creates an Optional that is empty (
  `**Optional.empty()**`).
- Use Case: Use Optional.ofNullable() when the value you are wrapping might be
  null and you want to handle that gracefully.

# Optional methods

| **Category**   | **Methods of Optional**               | **Description**                                            |
|:---------------|:--------------------------------------|:-----------------------------------------------------------|
| Creating       | `Optional.of()`                       | Optional with a **non-null** value                         |
| ^^Optional     | `Optional.ofNullable`                 | Optional that can hold **either a non-null value or null** |
| Unwrapping     | `optional.get()`                      | returns value if present or throws                         |        
| ^^Optionals    | ^^                                    | ^^**`NoSuchElementException: No value present`**           |
| ^^             | `optional.orElse(other)`              | returns value if present or returns other                  |
| ^^             | `optional.orElseGet(Supplier)`        | returns value if present or returns Supplier               |
| apply function | `optional.map(Function)`              | returns an Option with function applied                    |
|                | `optional.isPresent()`                | returns true if value is present                           |
| ^^             | `optional.ifPresentOrElse(`           | Beware of the **Shared Mutability**                        |
| ^^             | ^^ `value -> actionIfPresent(value),` | ^^                                                         |
| ^^             | ^^ `() -> actionIfEmpty()`            | ^^                                                         |
| ^^             | ^^ `);`                               | ^^                                                         |

```java
String str = null;
// Create an Optional that may or may not have a value
Optional<String> optional = Optional.ofNullable(str);//Value expecting a String

System.out.println(optional.get());//NoSuchElementException: No value present
System.out.println(optional.orElse("other"));//other
System.out.println(optional.orElseGet(String::new));//EMPTY String
System.out.println(optional.isPresent());//false
```

### IfPresentOrElse

- If present then set else keep a default value
  {% gist nitinkc/48b38c0c6ffab602a38dc305179d42f4 %}

- Considering a scenario where we need to return the first element, if present,
  else return an empty response.
  {% gist nitinkc/1c8d47211a5b373292620dce79dbc36b %}

### Avoid ternary operator with Optional

Use of `if` statement can be avoided using declarative functional style.

```java
String str = (null != student.getFirstName()) ? student.getFirstName().toUpperCase() : StringUtils.EMPTY;

//is Equivalent to
String str = Optional.of(student.getFirstName().toUpperCase).orElse(StringUtils.EMPTY);
```

### Optional with map() - Applying converters

With Optional, we get the advantage of applying function(map) as well.

```java
//adding city name from the list obj and appending a comma if the city exist, else "NO_CITY"
String[] cities = {("New York"), (null), ("Los Angeles"), ("Chicago")};

for (String city : cities) {
  // Using Map, avoiding ternary operator
  String str2 = Optional.ofNullable(city)
          .map(obj -> obj.toUpperCase() + ",")//Advantage of using map
          .orElse("NO_CITY");
  
  System.out.println(str2);
}
```

- More elaborate example
- {% gist nitinkc/3b6166b2b2825dad85bea8dd9cf7812a %}

# Patterns & Anti-patterns - Do's and Dont's

**var has strict type checking**. Reassignment has to match the `type` initially
set.

```java
var a = SampleData.getSimpleEmployees();
//a = "Nitin";//Strict type checking
```

### Receive an optional

**Use `var` to obtain an optional from a service or a method**

```java
var result = getName();//returns an Optional
String str = result.orElse("not found");//Default Value
//Or str = result.orElseGet(String::new);//Empty String
//Or str = result.orElseThrow();//if at all you need to use get, then use orThrow instead

//str = result.get();//DO NOT USE THIS due to the danger on NPE
```

### Fields

- There is **no reason to use Optional as a field**.
- use `optional.orElse()` instead of `optional.get()` to retrieve a value into a
  field.
    - If there is really a need to use `get()`, use `optional.orElseThrow()` to
      know the real reason of blowing up

### Method parameter

- **Do not** use Optional<T> as a parameter to methods. If needed, use
  overloading instead.
  ```java 
  public static void methodName(Optional<String> name); //Anti-pattern - DO NOT DO THIS
  ```
- Optional in the argument will force/punish the programmers when the method is
  invoked
  ```java
  methodName(Optional.empty());//Not Good
  //OR
  methodName(Optional.of(str));//Not Good
  ```
    - Instead, use overloading
      ```java
      //A good design has empathy
      public static void methodName() {
        //use the default value
      }
    
      public static void methodName(String name) {
        //use the given name
      }
      ```

### Method

Return Optional from a method to make it failsafe.

**When we have a single value to return**

* Instead of returning `null` (from method) return `Optional<T>`
* If a method *always has a single value* as a result, **do not use** Optional.

- In the given method, instead of returning a Map, returning an Optional of Map
  provides more flexibility
  ```java
  public Optional<Map<String, Object >> getInfoByCode(String code){
      Map<String, String> queryParams = new HashMap<>();
      queryParams.put("excludeSensitiveInfo", "true");
  
      //Get URL from config file
      List<Map<String, Object>> codes = restTemplate.getForObject(appConfig.getUrl()+"code/"+code, List.class, queryParams);
      
      //Returning a valid response even if the service fails.
      return Optional.ofNullable(Optional.of(codes.stream().findFirst().get())
                          .orElse(Collections.emptyMap()));
  }
  ```

- If a method may or may not have a single value as a result, **then use
  Optional**.
  ```java
  public static Optional<String> getName() {
      if(fakeService.getRandNumber() < 3) {
        return Optional.of("Name");
      }
  
      //return null; //ABSOLUTELY NO. it works but it's NASTY CODE
      return Optional.empty();
    }
  ```

- If the result is a **collection**, then **don't use Optional**, instead return
  an empty collection

> With collections, Do not return a null, instead return an empty *collection* -
> Effective Java

# The `null == object` comparison

Using `null == object` is a defensive programming practice,
where **accidental assignment in conditionals** can cause bugs.

Writing `null == object` instead of `object == null` prevents accidental
assignment if mistakenly use a single `=` instead of `==`.

For example, `if(object = null)`, the expression `object = null` will always
evaluate to null,
and the **if condition will always be false**, even if the object is not null.

# Handling Null pointer Exceptions (NPE)

### Boolean Variables

Prefer **primitive boolean** types over Wrapper class to avoid creating
objects & NPE.

If a String, intended to carry boolean values, you should use the
`Boolean.parseBoolean(String)` method.

```java
String trueString = "true";

// Parsing strings to boolean
boolean isTrue = Boolean.parseBoolean(trueString);
```

**Misinterpretation of Argument**: The argument for `Boolean.getBoolean` should
be the name of a system property,
not a boolean value.

```java
String isBooleanFlag = "true";//'undefined', 'false', 'anyStringValue '
//isBooleanFlag is intended to be a boolean value, this usage is incorrect
boolean aBoolean = Boolean.getBoolean(isBooleanFlag);
```

### Removing 'null' values

```java
// if any object in a list is NULL
list.stream()
        .filter(object -> null != object) //Removing potential objects that might create exception
        .map(str -> str.toLowerCase())
        .collect(Collectors.toList());
```

Ensuring, in case there is a null return, the exception is handled properly

```java
Order specificOrders = orders.stream()
				.filter(order -> order.getOrderNumber().equals(electronicOrder.getOrderNumber()))
				.findFirst()
                .orElse(null);
	
if(null != specificOrders) {
    ...
    ...
    ...
}
```

Or same code optimized

```java
orders.stream()
    .filter(order -> order.getOrderNumber().equals(electronicOrder.getOrderNumber()))
    .findFirst()
    .ifPresent(specificOrders -> {
        // Perform actions on specificOrders
        ...
        ...
        ...
        });
```