---
categories: Microservices
date: 2024-07-28 17:00:00
tags:
- Spring Boot
- Microservices
title: SpringBoot with Virtual Threads
---

{% include toc title="Index" %}

The size of the thread pool that is used in Spring Boot

- by default, Tomcat uses a threadpool size of 200.
- It means that If 250 concurrent users hit spring boot application, 50 of them
  are going to wait for a platform thread to process their request

```yaml
spring.threads.virtual.enabled=true
```