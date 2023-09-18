---
title:  "Spring Config Client"
date:   2019-11-22 21:15:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

Test Microservice for Spring Cloud Config. This is a client Application 

Provide Git Repo for the config server 

[Set property](https://github.com/nitinkc/spring-cloud-config-server/blob/master/src/main/resources/application.
properties#L8)

```yaml
spring.cloud.config.server.git.uri=https://github.com/spring-microservices-learning/config-repo.git
```

[Config Repo](https://github.com/nitinkc/config-repo)

[Another Central Config](https://github.com/nitinkc/CentralizedConfiguration)