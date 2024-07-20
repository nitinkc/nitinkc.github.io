---
title:  "CommandLineRunner - Spring Boot"
date:   2024-07-15 20:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---
{% include toc title="Index" %}

**@Order**: Specifies the execution order of this CommandLineRunner bean among others. 
- Lower values for Order execute before higher values or those without an Order specified.

**@ConditionalOnExpression**: Ensures that this CommandLineRunner bean is registered only if the SpEL 
expression `${runner1:false}` evaluates to true. 
- This allows conditional registration based on application configuration.

# CommandLineRunner Interface
CommandLineRunner is a functional interface provided by Spring Boot. It contains a single method:

```java
void run(String... args) throws Exception;
```
When a class implements CommandLineRunner, it must provide an implementation for this run method.
- This method is automatically invoked by Spring Boot after the application context has been loaded and before the application starts running.
- This is useful for performing initialization tasks, setting up configurations, or executing any necessary operations that should occur at the beginning of the application lifecycle.

```java
@Component
@Slf4j
@RequiredArgsConstructor
@Order(value = 1) //Sequence of runner
@ConditionalOnExpression("${runner1:false}") //Can be controlled from App yml 
public class Runner1 implements CommandLineRunner {
    //Make fine to be used with Required Args Constructor
    private final AnyServiceDependency anyServiceDependency;

    @Override
    public void run(String... args) throws Exception {
        log.info("Starting Runner 1");
        //Do processing
        doProcessing();
    }

    private void doProcessing() {
        //Write business logic
    }
}
```