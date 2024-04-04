---
title:  "Caching with Redis"
date:   2024-03-06 00:45:00
categories: [Microservices]
tags: [Spring Microservices, CRUD]
---

{% include toc title="Index" %}

**Redis**

Run Docker

```shell
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
```
Access the Redis UI

[http://localhost:8001/redis-stack/browser](http://localhost:8001/redis-stack/browser)

# Redis Caching Dependency

```properties
// Redis for caching
implementation 'org.springframework.boot:spring-boot-starter-data-redis'
```

@EnableCaching is from org.springframework.cache.annotation.EnableCaching;

```java
@EnableCaching
public class SpringBootReferenceApplication {

	public static void main(String[] args) {
		SpringApplication.run(SpringBootReferenceApplication.class, args);
	}
}

```

app yml

```properties
## Redis
spring.redis.host=localhost
spring.redis.port=6379
```

### @Cacheable

enable caching at method level

```java
@Service
@AllArgsConstructor
@Slf4j
public class RefTableService {
   private RefTableRepository refTableRepository;

    @Cacheable(value = "refTableCache - findById", key = "#id")
    public RefTableDTO findById(Integer id) {
        log.info("Fetching RefTable with id {} from the cache...", id);
        ...
    }

    @Cacheable("RefTable-findByIds")
    public List<RefTableDTO> findByIds(List<Integer> refIds) {
        ''''
        return refTableDTOList;
    }
}
```

## Caching with Service Class Methods:

Using @Cacheable in service class methods is common when you want to cache the results of business logic operations or 
data retrieval operations performed by your service layer.

Service methods often encapsulate complex logic, including data retrieval from repositories, manipulation, and processing of data.

By caching the results of service methods, you can improve the performance of your application by avoiding redundant
computations or database queries for frequently accessed data.

## Caching with Repository Methods:

While repository methods are primarily responsible for interacting with the database, you can still use `@Cacheable` 
in repository methods to cache the results of database queries.

Caching repository methods can be beneficial if the queries are frequently executed and the data doesn't change frequently.
- Example : Ref Data for UI drop-downs, dynamic radio buttons.
- 
However, caching repository methods might not be suitable for complex queries or queries that involve dynamic parameters,
as it can lead to cache key management complexities and cache pollution.
