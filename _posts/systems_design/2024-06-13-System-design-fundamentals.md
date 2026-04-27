---
title: System Design Fundamentals
date: 2024-06-13 10:00:00
categories:
- System Design
tags:
- Fundamentals
- Architecture
---

{% include toc title="Index" %}

Executive summaries and core concepts for system design interviews.
{: .notice--primary}

# Core Metrics

## Latency
> **Executive Summary**: Time for a single request to travel from source to destination. Measured in milliseconds (ms). Lower is better.

| Type | Typical Values |
|:-----|:---------------|
| L1 Cache Reference | 0.5 ns |
| L2 Cache Reference | 7 ns |
| Main Memory Reference | 100 ns |
| SSD Random Read | 150 μs |
| HDD Seek | 10 ms |
| Round trip within same datacenter | 500 μs |
| Round trip CA to Netherlands | 150 ms |

## Throughput
> **Executive Summary**: Rate of data transfer or requests processed per unit time. Measured in requests/second (RPS) or transactions/second (TPS). Higher is better.

- **Network**: Measured in bits per second (bps), Mbps, Gbps
- **Application**: Requests per second (RPS), Queries per second (QPS)
- **Database**: Transactions per second (TPS)

## Availability
> **Executive Summary**: Percentage of time a system is operational. Expressed as "nines" (99.9% = three nines).

| Availability | Downtime/Year | Downtime/Month | Downtime/Week |
|:-------------|:--------------|:---------------|:--------------|
| 99% (two 9s) | 3.65 days | 7.31 hours | 1.68 hours |
| 99.9% (three 9s) | 8.77 hours | 43.83 min | 10.08 min |
| 99.99% (four 9s) | 52.60 min | 4.38 min | 1.01 min |
| 99.999% (five 9s) | 5.26 min | 26.30 sec | 6.05 sec |

**Formula**: `Availability = Uptime / (Uptime + Downtime)`

## Reliability
> **Executive Summary**: Probability that a system will perform its intended function without failure for a specified period. MTBF (Mean Time Between Failures) is key metric.

- **MTBF**: Mean Time Between Failures
- **MTTR**: Mean Time To Recovery
- **Availability** = MTBF / (MTBF + MTTR)

## Durability
> **Executive Summary**: Guarantee that data, once written, will not be lost. Expressed as probability (e.g., 99.999999999% = 11 nines).

- **S3 Standard**: 99.999999999% (11 nines) durability
- Achieved through: Replication, Checksums, Error correction codes

---

# CAP Theorem

> **Executive Summary**: In a distributed system, you can only guarantee 2 of 3 properties: Consistency, Availability, Partition Tolerance. Since network partitions are inevitable, choose between CP (consistent but may be unavailable) or AP (available but may be inconsistent).

**Consistency**: Every read receives the most recent write or an error.

**Availability**: Every request receives a response (without guarantee it's the most recent).

**Partition Tolerance**: System continues to operate despite network partitions.

| Choice | Behavior | Examples |
|:-------|:---------|:---------|
| CP | Consistent, may reject requests during partition | MongoDB, HBase, Redis |
| AP | Available, may return stale data | Cassandra, DynamoDB, CouchDB |

## PACELC Extension
> **Executive Summary**: Extends CAP - even when there's no Partition, there's a tradeoff between Latency and Consistency.

- **PA/EL**: Sacrifice consistency for availability and lower latency (Cassandra, DynamoDB)
- **PC/EC**: Prefer consistency over availability and latency (VoltDB, H-Store)
- **PA/EC**: Availability during partition, consistency otherwise (MongoDB)

---

# Consistency Models

## Strong Consistency
> **Executive Summary**: All nodes see the same data at the same time. Every read returns the most recent write. Higher latency, simpler programming model.

- Implemented via: Synchronous replication, Consensus protocols (Paxos, Raft)
- Use when: Financial transactions, inventory management

## Eventual Consistency
> **Executive Summary**: Given enough time without new updates, all replicas will converge to the same value. Lower latency, higher availability.

- Implemented via: Asynchronous replication, Conflict resolution
- Use when: Social media feeds, DNS, Shopping cart

## Causal Consistency
> **Executive Summary**: Operations that are causally related are seen by all nodes in the same order. Concurrent operations may be seen in different orders.

- If A causes B, everyone sees A before B
- Stronger than eventual, weaker than strong
- Use when: Collaborative editing, Comment threads

## Read-Your-Writes Consistency
> **Executive Summary**: A user always sees their own writes immediately. Other users may see stale data.

- Session consistency
- Implemented via: Sticky sessions, Version vectors

## Linearizability
> **Executive Summary**: Strongest consistency model. Operations appear to happen instantaneously at some point between invocation and response.

- Real-time ordering guaranteed
- Expensive to implement at scale
- Use when: Distributed locks, Leader election

---

# Replication Strategies

## Single Leader (Master-Slave)
> **Executive Summary**: One node handles all writes; replicas handle reads. Simple, but leader is a bottleneck and single point of failure.

```
Client → Leader (Write) → Replicas (Async/Sync)
Client → Replicas (Read)
```

**Pros**: Simple, consistent writes, easy conflict resolution
**Cons**: Leader bottleneck, failover complexity, write latency

## Multi-Leader (Master-Master)
> **Executive Summary**: Multiple nodes accept writes. Better write performance and availability, but complex conflict resolution required.

- Use cases: Multi-datacenter, Offline-capable apps
- Conflict resolution: Last-write-wins, Custom merge logic, CRDTs

## Leaderless (Dynamo-style)
> **Executive Summary**: Any node can accept reads/writes. Uses quorum to ensure consistency. Highly available, no single point of failure.

- **Quorum**: W + R > N (Write nodes + Read nodes > Total replicas)
- **Read Repair**: Fix inconsistencies on read
- **Anti-entropy**: Background process to sync replicas
- Examples: Cassandra, DynamoDB, Riak

---

# Partitioning / Sharding

> **Executive Summary**: Split data across multiple nodes to scale horizontally. Each shard contains a subset of data. Key challenge: choosing the right partition key.

## Range Partitioning
> **Executive Summary**: Data divided by key ranges (A-M, N-Z). Good for range queries, but can lead to hot spots.

- Pros: Efficient range queries, sorted data
- Cons: Hot spots, uneven distribution
- Use when: Time-series data, alphabetical lookups

## Hash Partitioning
> **Executive Summary**: Hash function determines partition. Even distribution, but loses ordering and range query efficiency.

- Pros: Even distribution, no hot spots
- Cons: Inefficient range queries
- Use when: Random access patterns, user data by ID

## Consistent Hashing
> **Executive Summary**: Nodes and keys mapped to a ring. Data moves only between adjacent nodes when topology changes. Minimizes data movement during scaling.

- Virtual nodes improve load distribution
- Use when: Distributed caches, DHTs
- Examples: Cassandra, DynamoDB, Memcached

## Directory-Based Partitioning
> **Executive Summary**: Lookup service maintains mapping of keys to partitions. Flexible but lookup service is potential bottleneck.

---

# Load Balancing

> **Executive Summary**: Distribute traffic across multiple servers to improve performance, reliability, and scalability. Can operate at L4 (transport) or L7 (application).

## Algorithms

| Algorithm | Description | Use Case |
|:----------|:------------|:---------|
| Round Robin | Requests distributed sequentially | Equal capacity servers |
| Weighted Round Robin | Servers assigned weights | Different capacity servers |
| Least Connections | Route to server with fewest connections | Long-lived connections |
| IP Hash | Hash client IP to determine server | Session affinity |
| Least Response Time | Route to fastest responding server | Performance optimization |
| Random | Random server selection | Simple, stateless |

## Layer 4 vs Layer 7

| Layer 4 (Transport) | Layer 7 (Application) |
|:--------------------|:----------------------|
| Faster (no content inspection) | Content-based routing |
| TCP/UDP level | HTTP headers, cookies |
| Limited routing options | URL, method-based routing |
| Examples: HAProxy, AWS NLB | Examples: NGINX, AWS ALB |

## Health Checks
- **Active**: Load balancer periodically checks endpoints
- **Passive**: Monitor response from real traffic
- **Criteria**: HTTP status, response time, custom checks

---

# Caching

> **Executive Summary**: Store frequently accessed data in fast storage (memory) to reduce latency and database load. Key decisions: what to cache, where to cache, when to invalidate.

## Cache Strategies

### Cache-Aside (Lazy Loading)
> **Executive Summary**: Application checks cache first, fetches from DB on miss, then populates cache. Simple but can have cache stampede issues.

```
1. Check cache
2. If miss → Read from DB → Write to cache
3. Return data
```

### Read-Through
> **Executive Summary**: Cache sits between app and DB. Cache handles misses by fetching from DB automatically.

### Write-Through
> **Executive Summary**: Data written to cache and DB synchronously. Consistent but higher write latency.

### Write-Behind (Write-Back)
> **Executive Summary**: Data written to cache immediately, DB updated asynchronously. Lower latency but risk of data loss.

### Write-Around
> **Executive Summary**: Data written directly to DB, bypassing cache. Good for write-heavy workloads where data isn't immediately read.

## Cache Invalidation
- **TTL (Time-To-Live)**: Expire after fixed duration
- **Event-based**: Invalidate on data change
- **Version-based**: Cache key includes version number

## Eviction Policies

| Policy | Description |
|:-------|:------------|
| LRU (Least Recently Used) | Evict least recently accessed |
| LFU (Least Frequently Used) | Evict least frequently accessed |
| FIFO | Evict oldest entries first |
| Random | Random eviction |
| TTL | Evict expired entries |

## Cache Levels
1. **Browser Cache**: Client-side, HTTP headers (Cache-Control, ETag)
2. **CDN Cache**: Edge servers close to users
3. **Application Cache**: In-memory (Redis, Memcached)
4. **Database Cache**: Query cache, buffer pool

---

# Message Queues

> **Executive Summary**: Asynchronous communication between services. Decouple producers and consumers. Provides buffering, load leveling, and guaranteed delivery.

## Point-to-Point vs Pub/Sub

| Point-to-Point | Pub/Sub |
|:---------------|:--------|
| One consumer per message | Multiple subscribers |
| Message deleted after consumption | Message delivered to all subscribers |
| Work distribution | Event notification |
| Examples: SQS, RabbitMQ | Examples: Kafka, SNS, Redis Pub/Sub |

## Delivery Guarantees

| Guarantee | Description | Trade-off |
|:----------|:------------|:----------|
| At-most-once | Fire and forget | May lose messages |
| At-least-once | Retry until acked | May have duplicates |
| Exactly-once | Deduplication + at-least-once | Complex, expensive |

## Message Ordering
- **FIFO**: Strict ordering (higher latency)
- **Best effort**: No ordering guarantee (higher throughput)
- **Partition ordering**: Order within partition only (Kafka)

## Dead Letter Queue (DLQ)
> **Executive Summary**: Queue for messages that failed processing after max retries. Enables debugging and manual intervention.

---

# Proxies

## Forward Proxy
> **Executive Summary**: Sits in front of clients. Hides client identity, caches responses, filters content.

- Use cases: Corporate firewalls, Anonymity, Content filtering

## Reverse Proxy
> **Executive Summary**: Sits in front of servers. Load balancing, SSL termination, caching, compression.

- Examples: NGINX, HAProxy, Cloudflare
- Use cases: Load balancing, Security, Caching

## API Gateway
> **Executive Summary**: Single entry point for microservices. Handles routing, authentication, rate limiting, protocol translation.

- Examples: Kong, AWS API Gateway, Apigee
- Features: Auth, Rate limiting, Logging, Transformation

---

# Database Indexing

> **Executive Summary**: Data structures that improve query speed at the cost of write performance and storage. Choose indexes based on query patterns.

## B-Tree Index
> **Executive Summary**: Balanced tree structure. Good for range queries and equality. Most common index type.

- O(log n) lookups, inserts, deletes
- Supports range queries
- Use for: Primary keys, Foreign keys, Range queries

## Hash Index
> **Executive Summary**: Hash table for O(1) lookups. Only supports equality queries.

- No range query support
- Use for: Exact match queries

## Composite Index
> **Executive Summary**: Index on multiple columns. Order matters (leftmost prefix rule).

```sql
INDEX (a, b, c)
-- Supports: WHERE a, WHERE a AND b, WHERE a AND b AND c
-- Does NOT support: WHERE b, WHERE c, WHERE b AND c
```

## Full-Text Index
> **Executive Summary**: Inverted index for text search. Supports natural language queries.

- Examples: Elasticsearch, PostgreSQL tsvector
- Use for: Search functionality

## Covering Index
> **Executive Summary**: Index contains all columns needed for query. No table lookup required.

---

# Unique ID Generation

> **Executive Summary**: Generate globally unique identifiers in distributed systems. Trade-offs between sortability, size, and coordination requirements.

## UUID
> **Executive Summary**: 128-bit universally unique identifier. No coordination required, but not sortable and large.

- V1: Timestamp + MAC address
- V4: Random (most common)
- Pros: No coordination, globally unique
- Cons: Not sortable, 128 bits, no locality

## Snowflake ID
> **Executive Summary**: 64-bit ID with timestamp, machine ID, sequence. Time-sortable, no coordination between machines.

```
| Timestamp (41 bits) | Machine ID (10 bits) | Sequence (12 bits) |
```
- ~69 years of IDs per machine
- 4096 IDs per millisecond per machine
- Used by: Twitter, Discord

## ULID
> **Executive Summary**: 128-bit Universally Unique Lexicographically Sortable Identifier. Sortable, URL-safe.

- First 48 bits: timestamp
- Last 80 bits: randomness
- Lexicographically sortable

## Database Auto-Increment
> **Executive Summary**: Simple sequential IDs. Requires coordination, single point of failure.

- Pros: Simple, small, sortable
- Cons: Coordination required, reveals information

---

# API Design

## REST
> **Executive Summary**: Stateless, resource-oriented API using HTTP methods. Simple, cacheable, widely adopted.

| Method | Action | Idempotent |
|:-------|:-------|:-----------|
| GET | Read | Yes |
| POST | Create | No |
| PUT | Update (full) | Yes |
| PATCH | Update (partial) | No |
| DELETE | Delete | Yes |

## GraphQL
> **Executive Summary**: Query language for APIs. Client specifies exact data needed. Reduces over/under-fetching.

- Pros: Flexible queries, strong typing, single endpoint
- Cons: Complexity, caching challenges, N+1 queries

## gRPC
> **Executive Summary**: High-performance RPC using Protocol Buffers. Strongly typed, supports streaming.

- Uses HTTP/2 (multiplexing, header compression)
- Binary format (smaller, faster)
- Use for: Microservices, low-latency requirements

---

# Serialization Formats

| Format | Type | Human Readable | Size | Speed |
|:-------|:-----|:---------------|:-----|:------|
| JSON | Text | Yes | Large | Slow |
| XML | Text | Yes | Very Large | Slow |
| Protocol Buffers | Binary | No | Small | Fast |
| Avro | Binary | No | Small | Fast |
| Thrift | Binary | No | Small | Fast |
| MessagePack | Binary | No | Medium | Fast |

---

# Time Synchronization

## NTP (Network Time Protocol)
> **Executive Summary**: Synchronizes clocks over network. Accuracy: 1-50ms over internet, <1ms on LAN.

- Hierarchical system of time sources (strata)
- Stratum 0: Atomic clocks, GPS
- Stratum 1: Directly connected to Stratum 0

## Logical Clocks

### Lamport Timestamps
> **Executive Summary**: Partial ordering of events. If A happened-before B, then L(A) < L(B). Converse not guaranteed.

### Vector Clocks
> **Executive Summary**: Track causality between events. Can determine if events are concurrent or causally related.

- Each node maintains vector of counters
- Expensive in large systems

### Hybrid Logical Clocks (HLC)
> **Executive Summary**: Combines physical and logical time. Provides causality while staying close to real time.

---

# Distributed Tracing

> **Executive Summary**: Track requests across microservices. Essential for debugging and performance analysis in distributed systems.

- **Trace**: End-to-end journey of a request
- **Span**: Individual operation within a trace
- **Context Propagation**: Pass trace ID between services

Tools: Jaeger, Zipkin, AWS X-Ray, OpenTelemetry

