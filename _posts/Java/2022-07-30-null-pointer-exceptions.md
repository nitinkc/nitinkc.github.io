---
# layout: static
title:  "Null pointer Exceptions"
date:   2022-07-30 21:55:00
categories: ['Java']
tags: ['Java']
---

# Handling Null pointer Exceptions

Try with resources -> Closable Interface

## Boolean Variables

Prefer primitive boolean types over Wrapper class to avoid creating objects & NPE.


If a String, intended to carry boolean values, is to be tested,

```java
String isBooleanFlag = 'true';//'undefined', 'false', 'anyStringValue '
Boolean.getBoolean(isBooleanFlag)
```


```java
// if any object in a list is NULL
list.stream()
        .filter(object -> object != null) //Removing potential objects that might create exception
        .map(str -> str.toLowerCase())
        .collect(Collectors.toList())
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

## Use of Optionals

[Optional Use Cases]({% post_url /Java/2021-10-13-Optionals %})