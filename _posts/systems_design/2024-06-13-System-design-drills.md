---
categories: System Design
date: 2024-06-13 11:02:00
tags:
- System Design
title: System Design Drills
---

{% include toc title="Index" %}

Engineering is all about Trade-off's
{: .notice--primary}

**Latency** -> 1ms (speed of transfer)

- refers to the time it takes for a single unit of data to travel from its
  source to its destination.
- It measures the delay or the time it takes for data to traverse a system.
- Typically measured in milliseconds (ms) or microseconds (μs).

**Throughput** -> quantity of transfer (bps,tps)

- Throughput refers to the rate at which data is transferred, processed, or
  handled by a system within a given period of time.
- It measures the quantity of data being transferred or processed over time.
- measured in bits per second (bps), packets per second (pps), or transactions
  per second (TPS)

Design for **Low Latency** & **High Throughput**
{: .notice--info}

> [system-design-101](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#http-status-codes)

# HTTP Status Codes

# Service Discovery

- **Zookeeper Service Discovery** Often used for distributed coordination,
  Zookeeper also serves as a service registry and can be used for service
  discovery.
- **Eureka**: Developed by Netflix, Eureka is a service registry and discovery
  server that is widely used in microservices architectures.
- **etcd**: A distributed key-value store that can be used for service discovery
  among other purposes. It's commonly used in Kubernetes clusters.

Helps find where the service is (IP & DNS name)

- Needed because in the cloud (GCP or AWS) services have dynamic IP's or DNS
  Name
- Service instances(VM or Container) register or write their IP or DNS name in a
  service registry
- Service Registry is a key-value pair storage

2 ways of service discovery

## Client-Side Service Discovery

- client is responsible for discovering the network location of the service and
- load balance across them.
- Services register their IP when they start up
- IP is remove using heart beat (if down)
- **Np Load balancer required**

## Server-Side Service Discovery

- Client connects to Service Registry via a Load Balancer
- Load balancer queries the service registry and
- routes the traffic to target microservice
- All Services register with the SERVICE REGISTRY

### Examples of Service registry

- etcd: A highly available, distributed service discovery system, used by
  Kubernetes
- Hashicorp consul: Offers fast service discovery, load balancing adn API's for
  registering and unregistering services
- Apache Zookeeper: Built for Hadoop, commonly used alongside Apache Kafka. Used
  to coordinate distributed systems

## Service Registration Pattern

- Self Registration
- Third Party Registration: Another system or microservice (Registrar) does the
  registration and de-registration.

# Load Balancing

Distribute incoming network traffic across multiple servers.(to ensure no single
server becomes overwhelmed)

Consistent hashing : distribute load among nodes

- Tools: HAProxy, NGINX, AWS ELB (Elastic Load Balancing)

# Distributed Rate Limiting

- **Rate Limiting**: Control the rate of requests sent or received by a system
  to prevent abuse.
    - Token Bucket
    - Leaky Bucket
    - Fixed Window Counter
    - Sliding Window log (improvement on Fixed Window Counter)
    - Sliding Window Counter (mixed of above 2)
    - [The Timer wheel](https://nitinkc.github.io/system%20design/Rate-limiting/#timer-wheel-algorithm)

# Fault Tolerance and Recovery

- **Replication**: Data is copied across multiple nodes to ensure availability.
- **Leader Election**: Determines the master node to coordinate tasks.
    - Algorithms: Paxos, Raft
- **Quorum-Based Decision-Making**: Ensures that a majority of nodes agree on a
  decision to maintain consistency.

# Failure Detection and Recovery

- **Gossip Protocol**: Nodes periodically exchange state information to detect
  failures.
- **Sloppy Quorum**: Allows temporary inconsistencies by accepting writes and
  reads from a subset of nodes.
- **Hinted Handoff**: Temporarily stores data on an available node if the target
  node is down.

### Metrics to detect failing/troubled nodes

1. Average Response Time
2. Age of messages in the message Queue
3. Increasing messages in Dead Letter Queue

Request Collapsing

Request cohorting/condensing

Client side rate limiting

# Storage and Databases

- **SQL Databases**: Traditional relational databases that provide ACID
  transactions.
    - Examples: PostgreSQL, MySQL
- **NoSQL Databases**: Handle large volumes of unstructured data and provide
  high availability.
    - Examples: Cassandra, MongoDB, Redis
- **Cassandra**: NoSQL database designed to handle write-heavy workloads.
- **SQLite**: File-based local relational database.

## Data Sharding

- **Sharding**: Distribute data across multiple servers (nodes) to improve
  scalability and performance.
    - Techniques: Range Sharding, Hash Sharding

## Key-Value Storage

- **Radis**
- **RocksDB**: Local file-based key-value store that uses an LSM tree.

## Storage Services

- **Amazon S3**: Scalable object storage service by Amazon.
- **GCS (Google Cloud Storage)**: Object storage service by Google.

# Distributed Databases

Problems with Distributed Databases Running in Multiple Nodes

#### 1. Problems with Writing Data

**Network Latency**:

- **Solution**: Optimize network protocols, use efficient data serialization
  formats, and place nodes in close-proximity to reduce latency.

**Write Conflicts**:

- **Solution**: Implement conflict resolution strategies such as
  last-write-wins, version vectors, or application-specific logic.

**Replication Lag**:

- **Solution**: Use faster replication mechanisms like asynchronous replication
  and ensure adequate network bandwidth.

**Partitioning and Sharding**:

- **Solution**: Use consistent hashing for efficient data distribution and
  rebalancing mechanisms to handle dynamic changes in data.

#### 2. Problems with Reading Data

**Data Consistency**:

- **Solution**: Choose the appropriate consistency model (e.g., linearizability,
  strong consistency, eventual consistency, causal consistency) based on the
  application needs and use quorum reads.
    - use protocols like Paxos or Raft for strong consistency

**Stale Data**:

- **Solution**: Implement mechanisms like read-repair, anti-entropy protocols,
  and tune replication factors to reduce staleness.

**Load Balancing**:
**Solution**: Use advanced load balancing techniques such as consistent hashing,
random sampling, and dynamic load adjustment.

**Partition Tolerance**:

- **Solution**: Design the system to degrade gracefully during partitions and
  use techniques like eventual consistency to ensure data convergence.

#### 3. Maintaining Consistency and Availability

- **Quorum Consensus**:
    - **Solution**: Adjust quorum sizes dynamically based on system state and
      use techniques like read/write quorums to balance consistency and
      availability.
- **Data Recovery and Fault Tolerance**:
    - **Solution**: Use replication, backups, and consensus algorithms (e.g.,
      Paxos, Raft) to ensure data is recoverable and the system is resilient to
      failures.
- **Coordination and Synchronization**:
    - **Solution**: Use coordination services (e.g., Zookeeper, etcd) for
      distributed locks and leader election, and design algorithms to minimize
      the need for coordination.


- **Consensus-Based Distributed Databases**: Ensure consistency across
  distributed nodes.
    - Examples: **YugabyteDB**, **CockroachDB**
- Keep copies of data (master-slave design)

## Consensus Algorithms

**Raft**: Consensus algorithm for managing a replicated log.

**Paxos**:

- Used by Apache Zookeeper (used for distributed locking)
- Google Chubby - for distributed locking and maintaining order in distributed
  logs

## Data Center and Transaction Processing

- **Typical Data Center Node**: Can support a few thousand transactions per
  second.
- **ZooKeeper**: Used to maintain sharding information in distributed databases.

# Data Synchronization

- **Anti-Entropy Protocol**: Nodes compare and reconcile their data to ensure
  consistency.
    - **Merkle Trees**: Used to detect inconsistencies efficiently.

### Handling Race Conditions in Distributed Environments

- Multiple nodes trying to update the same resource simultaneously.
- Concurrent transactions in a distributed database leading to inconsistent
  states.

**Prevention Techniques**:

- **Locks and Semaphores**: Ensure only one process can access a resource at a
  time.
- **Transactional Systems**: Use of ACID transactions to ensure consistency.
- **Versioning and Vector Clocks**: Track changes and resolve conflicts based on
  causality.
- **Idempotent Operations**: Design operations to be repeatable without causing
  different outcomes.

##### Inconsistency Resolution (Caused due to data replication)

- **Vector Clocks**: Track causality and versioning to resolve inconsistencies
  caused by concurrent updates.

**Tools**:

- **Zookeeper**: For coordination and distributed locking.
- **Etcd**: A distributed key-value store that provides coordination and
  consistency guarantees.

## Transaction Coordination (in distributed Env)

### Problems with Distributed Transactions

#### 1. Network Latency

Distributed transactions often involve communication across different nodes,
which can introduce significant network latency.

**Solution**:

- Optimize network protocols.
- Minimize data transfer.
- Use batching and parallelism.

#### 2. Two-Phase Commit (2PC) Limitations

The 2PC protocol is commonly used to **ensure atomicity** in distributed
transactions but can lead to bottlenecks and is vulnerable to coordinator
failures.

**Solution**:

- Use Three-Phase Commit (3PC).
- Employ consensus algorithms (e.g., Paxos, Raft) - for greater fault tolerance

#### 3. Resource Locking

Distributed transactions can lock resources across multiple nodes, leading to
contention and reduced system throughput.

**Solution**:

- Implement distributed locking mechanisms.
- Use timeout-based locks.
- Consider lock-free or optimistic concurrency control.

#### 4. Data Consistency

Ensuring consistency across distributed nodes is challenging, especially in the
presence of network partitions or node failures.

**Solution**:

- Use appropriate consistency models (e.g., eventual consistency, strong
  consistency).
- Employ conflict resolution strategies.

#### 5. Failure Handling

Handling failures (node crashes, network partitions) in distributed transactions
is complex and can lead to data inconsistency or transaction rollback issues.

**Solution**:

- Implement robust failure detection and recovery mechanisms.
- Use transaction logs for recovery.
- Design for graceful handling of partial failures.

#### 6. Scalability

As the number of nodes increases, coordinating transactions across them becomes
more complex and can impact performance.

**Solution**:

- Design with scalability in mind.
- Use sharding and partitioning.
- Minimize cross-node transactions.

#### 7. Distributed Deadlocks

Distributed transactions can lead to deadlocks where two or more transactions
are waiting for each other to release resources.

**Solution**:

- Implement deadlock detection and resolution mechanisms.
- Use timeout-based deadlock prevention.
- Consider deadlock-free protocols.

### 2-Phase Commit (2PC)

Either all nodes commit the transaction or all of them abort.

**Phase 1 (Prepare)**:

- The coordinator sends a `prepare` request to all participants.
- Participants execute the transaction up to the point of committing and vote to
  either commit or abort.
- Each participant writes the transaction to a log.

**Phase 2 (Commit)**:

- If all participants vote to commit, the coordinator sends a `commit` request.
- If any participant votes to abort, the coordinator sends an `abort` request.

**Use Cases**: Suitable for short-lived transactions requiring strong
consistency.

### Try-Confirm/Cancel (TCC)

A three-phase protocol used to achieve distributed transaction management with
compensating actions.

- **Try**: Reserve resources required for the transaction. Ensure that all
  preconditions are met.
- **Confirm**: Once all `Try` operations succeed, actually execute the
  transaction.
- **Cancel**: If any `Try` operation fails, roll back all reserved resources.

**Use Cases**: Suitable for business transactions that require reservation of
resources and eventual consistency.

### Saga Pattern

A sequence of local transactions where each transaction updates the database and
**publishes an event** or message triggering the next transaction step.

- If a transaction fails, the saga executes compensating transactions to undo
  the impact of the preceding transactions.

**Choreography**: Each service listens for events and decides if an action is
needed. There is no central coordination.

**Orchestration**: A central coordinator tells each participant what local
transaction to execute.

**Use Cases**: Long-lived transactions where each step is independently
recoverable and eventual consistency is acceptable.

# Consistency and Coordination (across all nodes)

- **Distributed Locks**: Ensure only one node accesses a resource at a time.
    - Tools: Zookeeper, Consul
- **Consensus Algorithms**: Ensure agreement among distributed nodes. Ensures
  all DB replicas are in sync.
    - Examples: Paxos, Raft
- **Distributed Data Structures**:
    - Distributed Counters: Used for counting operations across nodes.
    - Atomic Operations: Ensure operations are completed atomically across
      nodes.

# Caching

- **CDNs (Content Delivery Networks)**: Distribute content closer to users to
  reduce latency.
    - Examples: Akamai, Cloudflare
- **In-Memory Caches**: Store frequently accessed data to reduce database load.
    - Examples: Memcached, Redis

## Content Delivery Networks

- **CDN (Content Delivery Network)**: Uses edge servers located at points of
  presence (POPs) to deliver content closer to users.
  CDN : Edhge servers(server inside a POP)
  POP : Point of presense(Server Locations)

# Monitoring and Logging

- **Monitoring Tools**: Track system performance and health.
    - Examples: Prometheus, Grafana
- **Logging Tools**: Collect and analyze log data.
    - Examples: ELK Stack (Elasticsearch, Logstash, Kibana)

--------------------------------------------------------------------------------

# Video Containers and Codecs

- **Video Containers**: File formats that can contain different types of data,
  including video, audio, and subtitles.
    - `.avi`
    - `.mpeg`
    - `.mov`
    - `.mp4`
- **Codecs**: Compression and decompression algorithms used to encode and decode
  video files.
    - **HEVC (High-Efficiency Video Coding)**
    - **H.264 (Advanced Video Coding)**

## Streaming Protocols

- **DASH (Dynamic Adaptive Streaming Over HTTP)**: Adapts video quality based on
  network conditions.
- **MPEG (Moving Pictures Experts Group)**: Standards for audio and video
  compression.
- **Apple HLS (HTTP Live Streaming)**: Streaming protocol by Apple for
  delivering media content.
- **Adobe HDS (HTTP Dynamic Streaming)**: Protocol by Adobe for adaptive bitrate
  streaming.
- **Higher Bitrate**: Higher video quality.

# Communication Protocols

- **REST (Representational State Transfer)**: Web service communication protocol
  using HTTP.
- **gRPC**: High-performance RPC framework using HTTP/2 for communication
  between microservices.
- **WebSockets**: Full-duplex communication channel over a single TCP
  connection, useful for real-time applications.
- **HTTP2.0**
- **HTTP 3.0**

 ----------------------------------------------------------------

## Data Stores and Messaging

- **Redis**: In-memory key-value store.
    - **Pub/Sub**: Lightweight messaging bus for sending messages between
      services.
- **ZooKeeper**: Hierarchical key-value store.
    - **Distributed Config Service**
    - **Synchronization Service**
    - **Naming Service**
- **Prometheus / InfluxDB**: Time-series databases for monitoring and metrics.
- **Facebook's Gorilla**: In-memory time-series database for monitoring
  ingestion.
- **Flink**: Stream processing engine for real-time data processing.
- **Grafana**: Visualization tool for monitoring and observability.
- **Debezium**: Change data capture tool for tracking database changes.

# Queue and Messaging Systems

- **Message Queues**: Decouple components and handle asynchronous communication.
    - Examples: RabbitMQ, Apache Kafka
- **Kafka**: Low-latency, high-throughput data event streaming platform designed
  for real-time data feeds.

# Security

- **Authentication and Authorization**: Ensure secure access to services.
    - Examples: OAuth, JWT (JSON Web Tokens)
- **Encryption**: Protect data in transit and at rest using protocols like
  TLS/SSL.

# Deployment

- **CI/CD (Continuous Integration/Continuous Deployment)**: Automate the process
  of integrating and deploying code changes.
    - Tools: Jenkins, GitLab CI, CircleCI

# Email Protocols and Tools

- **SMTP (Simple Mail Transfer Protocol)**: Protocol for sending email from one
  mail server to another.
- **POP (Post Office Protocol)**: Protocol for retrieving email; mail clients
  download entire emails.
- **IMAP (Internet Mail Access Protocol)**: Protocol for email retrieval.
    - Only downloads emails when accessed, never deletes from the server.
    - Allows access from multiple devices.
- **MIME (Multipurpose Internet Mail Extensions)**: Allows attachments in base64
  encoding.
- **Apache James**: Implements JMAP (JSON Meta Application Protocol).

## Search and Indexing

- **Search Store**: Uses an inverted index data structure for efficient search
  queries.
- **Email Threads**: Implemented using the JWZ Algorithm.

## File System and Checksums

- **Unix**: Filenames are stored in a data structure called **inode**, while
  file data is stored separately.
- **Checksum Algorithms**: Ensure data integrity.
    - **MD5**
    - **SHA**
    - **HMAC**

## Payment Systems

- **Tipalti**: Third-party payout provider.
- **Stripe**: Payment processing platform.
- **PSP (Payment Service Provider)**: Facilitates electronic payments.
- **CVV (Card Verification Value)**: Security feature for credit and debit
  cards.

## Identifiers and Algorithms

- **UUID (Universally Unique Identifier)**: Used as a nonce.
- **Exponential Backoff**: Technique where the wait time between retries is
  doubled after each failure.

## Financial Protocols

- **FIX Protocol (Financial Information Exchange Protocol)**: Standard for
  electronic communication in the financial industry.

## Routing Algorithms

- **Dijkstra's Algorithm**: Finds the shortest path between nodes in a graph.
- **A\* Algorithm**: Pathfinding and graph traversal algorithm.

Roads as edges, intersections as nodes

## Software Design Patterns

- **Event Sourcing**: Domain-driven design pattern where state changes are
  stored as a sequence of events.
- **CQRS (Command Query Responsibility Segregation)**: Separates read and write
  operations into different models.

# Append Only Data structure

Supports adding new data (appending) without modifying or deleting existing
data.

- particularly useful when **sequential write operations** are crucial.

# mmap (memory-mapped file)

mmap is a feature that allows files or devices to be mapped into memory,
enabling applications to access files as if they were part of the main memory.
This can significantly improve performance when dealing with large files, as it
reduces the need for frequent read/write system calls.

- Can write to a disk, and cache recent content in memory at the same time

# Case Study Examples

### Netflix

- **Microservices Architecture**: Decomposes the application into small,
  independent services.
- **Eureka**: Service registry for service discovery.
- **Zuul**: Gateway for dynamic routing, monitoring, and resiliency.
- **Hystrix**: Latency and fault-tolerance library.

### GPS

- **Geospatial Databases**: Store and query location data.
    - Example: PostGIS (extension of PostgreSQL)
- **Real-Time Data Processing**: Stream processing frameworks.
    - Examples: Apache Kafka, Apache Flink

### Uber

- **Real-Time Matching**: Matching riders with drivers using algorithms.
- **Geospatial Indexing**: Efficiently handle location-based queries.
    - Data Structures: QuadTree, R-Tree
- **Load Balancing**: Distribute incoming requests across multiple servers.

### News Feed

- **Feed Generation**: Use of ranking algorithms to personalize content.
- **Graph Databases**: Manage relationships and interactions.
    - Example: Neo4j
- **Data Aggregation**: Collect data from various sources and aggregate it.
    - Example: Apache Storm

[//]: # (![]&#40;https://raw.githubusercontent.com/ByteByteGoHq/system-design-101/main/images/cloud-compare.jpg&#41;)