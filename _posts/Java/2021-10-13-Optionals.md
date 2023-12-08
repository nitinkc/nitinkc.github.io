---
layout: page
title:  "Optional Use cases"
date:   2021-10-13 21:55:00
categories: ['Java']
tags: ['Java']
---

{% include toc title="Index" %}

# Optional 
* New class in java.util package.
* It is a Container to hold at most one value, like Collections and Arrays.
* To represent a value if its present or absent.
* Avoids any runtime NullPointerExceptions

##### In Streams API, Optional is returned

* value.get() – returns value if present or throws exception
* value.orElse(other) – returns value if present or returns other
* value.orElseGet(Supplier) – returns value if present or calls function
* value.isPresent() – returns true if value is present

### Avoid ternary operator with Optional

Use of if statement can be avoided using declarative functional way. 

```java
String str = (null != student.getFirstName()) ? student.getFirstName() : StringUtils.EMPTY;

//is Equivalent to
String str = Optional.of(student.getFirstName()).orElse(StringUtils.EMPTY);
```

### Optional of Nullable
- If present then set else keep a default value
{% gist nitinkc/48b38c0c6ffab602a38dc305179d42f4 %}

- With Optional, we get advantage of applying map as well.

```java
//Another Example, in a loop, adding city name from the Object obj and appending a comma if the city exist, else leaving the city name.
String test1 = Optional.ofNullable(obj.getCityName()).isPresent() ? "," + obj.getCityName():"");

// Using Map, avoiding ternary operator
String str2 = Optional.ofNullable(obj.getCityName()))
                            .map(obj -> ","+ obj )//Advantage of using map
                            .orElse("");
```

### Applying converters with Optional

{% gist nitinkc/3b6166b2b2825dad85bea8dd9cf7812a %}

### Returning Optional from a method to make it failsafe
Also check [Do's and Donts of Optionals](https://nitinkc.github.io/java/design%20patterns/optional-design-patterns/#dos-and-donts)

In the given method, instead of returning a Map, returning an Optional of Map provides more flexibility
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

### IfPresent Or else

Considering a scenario where we need to return the first element, if present, else return an empty response.

{% gist nitinkc/1c8d47211a5b373292620dce79dbc36b %}


# The null == object comparison

Using `null == object` is a defensive programming practice, especially in languages like Java, 
where **accidental assignment in conditionals** can cause bugs. 

Writing `null == object` instead of `object == null` prevents accidental assignment if a developer mistakenly use a single `=` instead of `==`. 

For example, `if(object = null)`, the expression object = null will always evaluate to null, and the **if condition will always be false**, even if object is not null.

However, object == null to be more natural to read and understand. 
Modern IDEs often help prevent such mistakes by showing a warning when an assignment is used inside a conditional expression. 
So, whether to use null == object or object == null is largely a matter of personal preference and coding standards within a team. 
Both forms are correct and serve the same purpose.

## Optional ofNullable
Instead of using then else statement, use of optional can be handy

```java
Optional.ofNullable(str1).orElse(str2)
```