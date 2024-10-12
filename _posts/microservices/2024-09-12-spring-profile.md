---
title:  "SpringBoot Profile"
date:   2024-09-12 15:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

{% include toc title="Index" %}

# Setting a profile

- Using `-Dspring.profiles.active=prod` in VM Arguments
- In application.properties, `spring.profiles.active=prod`

# `@Profile`

- making a profile active from the application.properties
- **default** profile is added with the argument
    - `@Profile({"qa","default"})` on a bean

```java
@Profile({"qa","default"})
@Bean
public String beanQa() {
return "Qa";
}

@Profile("prod")
@Bean
public String beanProd() {
return "profile prod";
}
```