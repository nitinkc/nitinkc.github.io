---
title:  "Spring Actuator"
date:   2024-04-04 02:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---



```shell
management.endpoints.web.exposure.include=health,info, metrics
management.endpoint.health.show-details=always
```


```java
@Component("redis-health")
@Slf4j
public class RedisHealthIndicator implements HealthIndicator {
    @Override
    public Health health() {
        try (Jedis jedis = new Jedis("redis-server", 6379)) { // Update with your Redis host and port
            // Attempt to connect to Redis
            log.info("Ping redis-server on 6379 :: {}",jedis.ping());
            return Health.up()
                    .withDetail("status", "OK")
                    .withDetail("message", "Redis connection successful")
                    .build(); // Redis connection successful
        } catch (Exception e) {
            return Health.down().withDetail("error", e.getMessage()).build(); // Redis connection failed
        }
    }
}
```

[http://localhost:8080/actuator](http://localhost:8080/actuator)


## Check Health for Redis custom-url
http://localhost:8080/actuator/health/redis-health](http://localhost:8080/actuator/health/redis-health)


```json5
{
"status": "UP",
"details": {
    "status": "OK",
    "message": "Redis connection successful"
    }
}
```