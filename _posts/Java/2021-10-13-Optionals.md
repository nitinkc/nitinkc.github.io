---
# layout: static
title:  "Optional Use cases"
date:   2021-10-13 21:55:00
categories: ['Java']
tags: ['Java']
---

### Keeping an object in case it is null, avoiding ternary operator

Use of if statement can be avoided using declarative functional way. 

```java
null != student.getFirstName() ? student.getFirstName() : ""
```
can be re-written as 
```java
Optional.of(student.getFirstName()).orElse("")
```

Optional of Nullable - If present then set else keep a default value
{% gist nitinkc/48b38c0c6ffab602a38dc305179d42f4 %}

```java
//Another Example, in a loop, adding city name from the Object obj and appending a comma if the city exist, else leaving the city name.
String test1 = Optional.ofNullable(obj.getCityName()).isPresent() ? "," + obj.getCityName():"");

// Using Map, avoiding ternary operator
String str2 = Optional.ofNullable(obj.getCityName()))
                            .map(obj -> ","+ obj )
                            .orElse("");
```

### Applying conterters with Optional

{% gist nitinkc/3b6166b2b2825dad85bea8dd9cf7812a %}

### Returning Optional from a mehtod to make it failsafe

In the given method, instead of returning a Map, returning an Optional of Map
```java
 public Optional<Map<String, Object >> getInfoByCode(String code){
    Map<String, String> queryParams = new HashMap<>();
    queryParams.put("excludeSensitiveInfo", "true");

    //Get URL from config file
    List<Map<String, Object>> codes = restTemplate.getForObject(appConfig.getUrl()+"code/"+code, List.class, queryParams);
    //Returniung a valid response even if the service fails.
    return Optional.ofNullable(Optional.of(codes.stream().findFirst().get())
                        .orElse(Collections.emptyMap()));
}
```