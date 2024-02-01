---
title:  "Swagger Documentations"
date:   2023-09-15 21:30:00
categories: Spring Microservices
tags: [CRUD]
---
{% include toc title="Index" %}

# Swagger Dcoumentation

Add Maven Dependencies

```sh
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.9.2</version>
</dependency>

<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.9.2</version>
</dependency>

```

Add a Swagger Config Class
```java
@Configuration
@EnableSwagger2
public class SwaggerConfig {

    @Bean
    public Docket api(){
        return new Docket(DocumentationType.SWAGGER_2)
    }
}
```

Access the Swagger Docs via

[http://localhost:8089/v2/api-docs]

Swagger UI
[http://localhost:8089/swagger-ui.html]

# TODO

* Configure further docs via swagger Annotations


