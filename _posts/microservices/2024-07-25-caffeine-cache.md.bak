---
categories: Microservices
date: 2024-07-25 17:00:00
tags:
- Spring Boot
- Redis
- Microservices
title: Caffeine Cache
---

{% include toc title="Index" %}

[Project - https://github.com/nitinkc/springboot-caffeine-cachine](https://github.com/nitinkc/springboot-caffeine-cachine)
Enable the Cache config

```java
@Configuration
@EnableCaching
public class CacheConfig {

    @Bean
    public CaffeineCacheManager cacheManager() {
        CaffeineCacheManager cacheManager = new CaffeineCacheManager();
        cacheManager.setCaffeine(caffeineCacheBuilder());
        return cacheManager;
    }

    Caffeine<Object, Object> caffeineCacheBuilder() {
        return Caffeine.newBuilder()
                .initialCapacity(100)
                .maximumSize(500)
                .expireAfterAccess(1, TimeUnit.DAYS)
                .weakKeys()
                .recordStats();
    }
}
```

# View

View the values of the cache at the given point of time

```java
@Component
public class CacheViewer {
    private final CacheManager cacheManager;

    public CacheViewer(CacheManager cacheManager) {
        this.cacheManager = cacheManager;
    }

    public void viewCache(String cacheName) {
        Cache cache = cacheManager.getCache(cacheName);
        if (cache instanceof CaffeineCache caffeineCache) {
            Map<Object, Object> cacheMap = caffeineCache.getNativeCache().asMap();
            cacheMap.forEach((key, value) ->
                    System.out.println("Key: " + key + ", Value: " + value)
            );
        } else {
            System.out.println("Cache '" + cacheName + "' is not a Caffeine cache.");
        }
    }
}
```