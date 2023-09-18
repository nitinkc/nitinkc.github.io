---
title:  "Spring Boot - Basics"
date:   2019-11-17 13:54:00
categories: 'Spring Microservices'
tags: [Spring Microservices, Spring Boot]
---

# Hello World for Spring Boot

Download the demo package form https://start.spring.io/

* Spring Web
* H2 Database
* Spring Actuator

## Config

{% gist nitinkc/5dd5f552cc1033347f2868ea6e6b7ad7 %}

## Banner 

[Spring Boot banner generator](https://springhow.com/spring-boot-banner-generator/)

For Ascii banner, put the ASCII Art in banner.txt in and it will be taken
[Sample file](https://github.com/nitinkc/spring-5-restful-web/blob/master/src/main/resources/banner.txt)

to turn off the banner
```yaml
spring:
  main:
    banner-mode: "off"
```
For image banner, put the logo.png file and 

```yaml
spring:
  banner:
    image:
      location: logo.png
```

## Initial Data Setup

keep the sql script in the resources folder by the name `data.sql`

[Sample Data file](https://github.com/nitinkc/spring-data-jpa/blob/master/src/main/resources/data.sql)


## Controller for Hello World

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
