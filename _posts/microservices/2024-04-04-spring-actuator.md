---
title:  "Spring Actuator"
date:   2024-04-04 02:00:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---


```properties
## Actuator Settings
management.endpoints.web.exposure.include=health,info, metrics
management.endpoint.health.show-details=always
management.endpoint.health.enabled=true
```

## Custom Component for health checker

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




```json
"redis": {
"status": "UP",
"details": {
    "version": "7.2.4"
    }
},
"redis-health": {
"status": "UP",
"details": {
    "status": "OK",
    "message": "Redis connection successful",
    "version": "7.2.4",
    "os": "Linux 6.6.16-linuxkit x86_64",
    "tcp_port": "6379"
  }
}
```

The "redis" entry is provided by default by Spring Boot Actuator when it detects that Redis is available as a dependency 
It checks if the Redis connection is up by pinging the Redis server.

The "redis-health" entry is my custom health indicator RedisHealthIndicator. 
This indicator checks the health of the Redis connection in more detail, providing additional information 
such as the version of Redis and a custom message indicating that the connection to Redis was successful.

If you only want to see one entry, you can choose to use either the default health indicator provided by 
Spring Boot Actuator or your custom health indicator, depending on your requirements. 

If you prefer to use only your custom health indicator, you can disable the default health indicators provided by Spring Boot Actuator.