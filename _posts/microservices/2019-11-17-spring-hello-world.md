---
title:  "Spring Boot - Hello World"
date:   2019-11-17 13:54:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

### Hello World for Spring Boot

Download the demo package form https://start.spring.io/

* Spring Web
* H2 Database
* Spring Actuator


```java
package com.nitin.microservices.learning.limitservice;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HelloController {

    @RequestMapping("/")
    public String index() {
        return "Hello : Spring Boot is Up and Running";
    }
}
```
