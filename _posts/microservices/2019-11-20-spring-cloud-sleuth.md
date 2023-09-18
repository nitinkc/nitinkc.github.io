---
title:  "Spring Cloud Sleuth"
date:   2019-11-17 23:21:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

## Assigning Trace id to all the Microservices 

All Microservices Projects are hosted on different servers on different ports.

Provides a unique id to all the requests for distributed tracing

Place the dependency to all the projects needed a unique request id

[Spring Cloud Sleuth](https://cloud.spring.io/spring-cloud-sleuth/reference/html/)

```maven
<!-- Spring Cloud Sleuth -->
		<dependency>
			<groupId>org.springframework.cloud</groupId>
			<artifactId>spring-cloud-starter-sleuth</artifactId>
		</dependency>
```

private Logger logger = LoggerFactory.getLogger(this.getClass());

# Sleuth with Zipkin over RabbitMQ or Kafka

Messaging queue is utilized to keep all the logs from different servers into a central location.

[https://nitinkc.github.io/spring/microservices/zipkin-distributed-tracing/](https://nitinkc.github.io/spring/microservices/zipkin-distributed-tracing/)
