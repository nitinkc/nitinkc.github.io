---
title:  "Spring Scheduler"
date:   2024-03-13 22:50:00
categories: Spring Microservices
tags: [Spring Microservices, Spring Boot]
---

# Scheduling with Cron

using `@Scheduled` annotation on the method
```java
@Component
@Slf4j
@AllArgsConstructor
public class ChronService {
    private final MyService myService;

    @Scheduled(cron="${report.cron-expr}", zone="GMT")
    public void runReport(){
        ...
        myService.callMyServiceAtScheduledTime();
    }
}
```

# Application yml file
create cron expression using [https://crontab.guru/](https://crontab.guru/#0_1_*_*_1-7)

```yaml
report:
    cron-expr:  0 0/2 * * * ? #run every 2 min
    #0 1 * * 1-7  #At 01:00 AM GMT or 8 PM Central Time on every day-of-week from Monday through Sunday.
```

# Async Scheduling

use the two annotations `@EnableAsync` and `@EnableScheduling` at the application level

```java
import org.springframework.scheduling.annotation.EnableAsync;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableAsync
@EnableScheduling
public class MemoryIssuesApplication {
    public static void main(String[] args) {
        SpringApplication.run(MemoryIssuesApplication.class, args);
    }
}
```

Method scheduled to run periodically
```java
//@Scheduled(fixedDelay = 1000)
public void runTask() {
CompletableFuture.runAsync(this::myScheduledMethod);
}
```