---
title: System Design Interview Cheatsheet
date: 2024-06-13 12:00:00
categories:
- System Design
tags:
- Interview
- Cheatsheet
---

{% include toc title="Index" %}

Quick reference for system design interviews - executive summaries only.
{: .notice--primary}

# Core Concepts Quick Reference

| Concept | One-Liner | When to Use |
|:--------|:----------|:------------|
| **Horizontal Scaling** | Add more machines | When vertical limits reached |
| **Vertical Scaling** | Add more resources to machine | Simple cases, quick fix |
| **Load Balancer** | Distribute traffic across servers | Multiple servers |
| **CDN** | Cache content at edge locations | Static content, global users |
| **Cache** | Store frequently accessed data in memory | Read-heavy workloads |
| **Message Queue** | Async communication buffer | Decouple services |
| **Database Replication** | Copy data across nodes | High availability, read scaling |
| **Database Sharding** | Split data across nodes | Write scaling, large datasets |

---

# Database Selection Guide

| Use Case | Recommended | Why |
|:---------|:------------|:----|
| Transactions, ACID | PostgreSQL, MySQL | ACID compliance |
| Document storage | MongoDB | Flexible schema |
| Wide-column, time-series | Cassandra, HBase | Write-heavy, scale |
| Key-Value cache | Redis, Memcached | Fast lookups |
| Graph relationships | Neo4j | Complex relationships |
| Search | Elasticsearch | Full-text search |
| Analytics (OLAP) | ClickHouse, BigQuery | Columnar, aggregations |
| Blob storage | S3, GCS | Large files |

---

# Consistency vs Availability

| Choose Consistency When | Choose Availability When |
|:------------------------|:------------------------|
| Financial transactions | Social media feeds |
| Inventory management | User preferences |
| Booking systems | Analytics dashboards |
| Leader election | Metrics collection |
| Distributed locks | Shopping cart |

---

# Common Patterns Quick Reference

## Caching Patterns

| Pattern | Write | Read | Best For |
|:--------|:------|:-----|:---------|
| Cache-Aside | App writes to DB | Check cache, fallback to DB | General purpose |
| Read-Through | N/A | Cache fetches from DB | Simple reads |
| Write-Through | Write cache + DB sync | From cache | Consistency needed |
| Write-Behind | Write cache, async DB | From cache | Write-heavy |

---

## Rate Limiting Algorithms

| Algorithm | Description | Pros/Cons |
|:----------|:------------|:----------|
| Token Bucket | Tokens refill at rate, requests consume tokens | Allows bursts |
| Leaky Bucket | Fixed outflow rate | Smooth output |
| Fixed Window | Counter per time window | Simple, edge spikes |
| Sliding Window | Moving window counter | Accurate, more memory |

---

## ID Generation

| Method | Size | Sortable | Coordination |
|:-------|:-----|:---------|:-------------|
| UUID v4 | 128 bit | No | None |
| Snowflake | 64 bit | Yes | Machine ID |
| ULID | 128 bit | Yes | None |
| Auto-increment | Variable | Yes | Required |

---

# Data Structures for Scale

| Structure | Purpose | Use Case |
|:----------|:--------|:---------|
| **Bloom Filter** | Probably in set | Cache lookup, spam filter |
| **HyperLogLog** | Count unique items | Unique visitors |
| **Count-Min Sketch** | Frequency estimation | Top-K, heavy hitters |
| **Consistent Hash** | Distribute across nodes | Distributed cache |
| **Merkle Tree** | Detect data differences | Anti-entropy sync |
| **LSM Tree** | Write-optimized storage | Write-heavy DBs |
| **B+ Tree** | Read-optimized index | Database indexes |
| **Skip List** | Sorted data structure | Redis sorted sets |
| **Trie** | Prefix lookups | Autocomplete |
| **Geohash/S2** | Location encoding | Proximity search |
| **Inverted Index** | Text to documents | Full-text search |

---

# Communication Patterns

| Protocol | Use When | Latency | Complexity |
|:---------|:---------|:--------|:-----------|
| REST/HTTP | Standard APIs | Medium | Low |
| gRPC | Microservices | Low | Medium |
| WebSocket | Real-time bidirectional | Low | Medium |
| SSE | Server push | Low | Low |
| Message Queue | Async, decoupling | Variable | Medium |
| GraphQL | Flexible queries | Medium | High |

---

# Scaling Numbers

## QPS Guidelines

| Service Type | Typical QPS/Server |
|:-------------|:-------------------|
| Web server | 1K-10K |
| Database (simple) | 1K-5K |
| Cache (Redis) | 100K+ |
| Load Balancer | 100K+ |

## Storage Rules of Thumb
- Text tweet (140 chars): ~280 bytes
- User record: ~1 KB
- Image thumbnail: ~20 KB
- HD Image: ~2 MB
- 1 minute video (compressed): ~10 MB

## Time Estimates
- Seconds in day: 86,400 ≈ 100K
- Seconds in month: 2.6M ≈ 3M
- Seconds in year: 31.5M ≈ 30M

---

# Reliability Patterns

| Pattern | Purpose | Implementation |
|:--------|:--------|:---------------|
| **Circuit Breaker** | Fail fast, prevent cascade | Hystrix, Resilience4j |
| **Retry with Backoff** | Handle transient failures | Exponential backoff |
| **Bulkhead** | Isolate failures | Thread/connection pools |
| **Timeout** | Don't wait forever | Set aggressive timeouts |
| **Fallback** | Graceful degradation | Default/cached values |
| **Health Check** | Detect failures | /health endpoint |
| **Idempotency** | Safe retries | Idempotency keys |

---

# Distributed Transactions

| Pattern | Consistency | Complexity | Use Case |
|:--------|:------------|:-----------|:---------|
| **2PC** | Strong | High | Short transactions |
| **Saga** | Eventual | Medium | Long transactions |
| **Outbox** | At-least-once | Low | DB + Events |
| **TCC** | Strong | High | Reservations |

---

# Consensus & Coordination

| Tool | Use For |
|:-----|:--------|
| **Zookeeper** | Leader election, config, locks |
| **etcd** | Kubernetes, config, service discovery |
| **Consul** | Service mesh, discovery, config |
| **Redis** | Distributed locks (Redlock) |

---

# Observability Stack

| Layer | Tools |
|:------|:------|
| **Metrics** | Prometheus, Grafana, Datadog |
| **Logging** | ELK Stack, Loki, Splunk |
| **Tracing** | Jaeger, Zipkin, X-Ray |
| **Alerting** | PagerDuty, OpsGenie |

---

# Security Checklist

- [ ] HTTPS everywhere (TLS 1.3)
- [ ] Authentication (OAuth 2.0, JWT)
- [ ] Authorization (RBAC, ABAC)
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Secrets management (Vault)
- [ ] Encryption at rest
- [ ] Audit logging

---

# Interview Questions Mapped to Concepts

| Question | Key Concepts |
|:---------|:-------------|
| Design URL Shortener | Hash, Base62, Cache, Database |
| Design Twitter | Feed fanout, Timeline, Sharding |
| Design Chat System | WebSocket, Presence, Message Queue |
| Design YouTube | CDN, Transcoding, Adaptive Streaming |
| Design Instagram | Object Storage, CDN, Feed |
| Design Uber | Geospatial Index, Matching, Real-time |
| Design Rate Limiter | Token Bucket, Distributed Counter |
| Design Notification | Push, Queue, Priority |
| Design Search | Inverted Index, Ranking, Sharding |
| Design File Storage | Chunks, Replication, Metadata |

---

# High-Level Design Template

```
┌─────────────────────────────────────────────────────────────┐
│                         Clients                              │
│                  (Web, Mobile, API)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                           CDN                                │
│                   (Static content)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     Load Balancer                            │
│                  (L7, Health checks)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Gateway                             │
│        (Auth, Rate limit, Routing, SSL termination)        │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Service A   │    │   Service B   │    │   Service C   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│     Cache     │    │   Database    │    │ Message Queue │
│    (Redis)    │    │  (Primary)    │    │   (Kafka)     │
└───────────────┘    └───────────────┘    └───────────────┘
                              │
                              ▼
                    ┌───────────────┐
                    │   Replicas    │
                    └───────────────┘
```

---

# Estimation Formulas

## QPS
```
QPS = (DAU × actions_per_user) / seconds_in_day
Peak QPS ≈ 2-3 × average QPS
```

## Storage
```
Storage = users × data_per_user × retention_period
Growth = new_users_per_day × data_per_user
```

## Bandwidth
```
Bandwidth = QPS × request_size (inbound)
Bandwidth = QPS × response_size (outbound)
```

## Cache Size
```
Cache = QPS × cache_entry_size × cache_duration
Cache hit ratio target: 80-95%
```

## Servers Needed
```
Servers = Peak_QPS / QPS_per_server
Add 20-30% for headroom
```

---

# Tradeoff Discussions

| Decision | Option A | Option B |
|:---------|:---------|:---------|
| Consistency vs Availability | CP (consistency) | AP (availability) |
| SQL vs NoSQL | ACID, joins, schema | Scale, flexibility |
| Sync vs Async | Immediate feedback | Decoupling, scale |
| Push vs Pull | Real-time, more connections | Polling, simpler |
| Cache vs Fresh | Speed | Accuracy |
| Monolith vs Microservices | Simple, fast | Scale, teams |
| Embedded vs Managed | Control, cost | Ease, reliability |

---

# Red Flags to Avoid

❌ Single point of failure
❌ No caching strategy
❌ Ignoring data growth
❌ No backup/recovery plan
❌ Tight coupling between services
❌ No rate limiting
❌ Synchronous calls for everything
❌ Not considering peak load
❌ Ignoring security
❌ No monitoring/alerting

---

# Related Articles

- [System Design Fundamentals]({% post_url /systems_design/2024-06-13-System-design-fundamentals %})
- [Data Structures for System Design]({% post_url /systems_design/2024-06-13-System-design-data-structures %})
- [Scalability Patterns]({% post_url /systems_design/2024-06-13-Scalability-patterns %})
- [System Design Drills]({% post_url /systems_design/2024-06-13-System-design-drills %})

