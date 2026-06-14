---
title: Scalability Patterns & Distributed Systems
date: 2024-06-13 11:00:00
categories:
- System Design
tags:
- Scalability
- Distributed Systems
---

{% include toc title="Index" %}

Patterns and strategies for building scalable distributed systems.
{: .notice--primary}

# Scaling Strategies

## Vertical Scaling (Scale Up)
> **Executive Summary**: Add more resources (CPU, RAM, SSD) to existing machine. Simple but has hardware limits and creates single point of failure.

**Pros**:
- Simple, no code changes
- No distributed system complexity
- ACID compliance easier

**Cons**:
- Hardware limits
- Single point of failure
- Expensive at high end
- Downtime for upgrades

---

## Horizontal Scaling (Scale Out)
> **Executive Summary**: Add more machines to the pool. Better for handling load, but requires distributed system design. Preferred for web-scale.

**Pros**:
- Theoretically unlimited scaling
- Better fault tolerance
- Cost-effective (commodity hardware)
- No downtime for scaling

**Cons**:
- Distributed system complexity
- Data consistency challenges
- Network overhead
- Code changes may be required

---

# Distributed System Challenges

## The Eight Fallacies of Distributed Computing
> **Executive Summary**: Assumptions developers wrongly make about distributed systems. Understanding these prevents common mistakes.

1. **The network is reliable** → Handle failures, timeouts, retries
2. **Latency is zero** → Design for network delays
3. **Bandwidth is infinite** → Minimize data transfer
4. **The network is secure** → Encrypt, authenticate
5. **Topology doesn't change** → Handle dynamic infrastructure
6. **There is one administrator** → Plan for multi-team ownership
7. **Transport cost is zero** → Optimize serialization
8. **The network is homogeneous** → Handle different protocols/systems

---

## Split-Brain Problem
> **Executive Summary**: Network partition causes nodes to believe they're the only survivors. Multiple nodes may act as leader simultaneously.

**Solutions**:
- Quorum-based decisions
- Fencing tokens
- STONITH (Shoot The Other Node In The Head)
- Shared storage for state

---

## Byzantine Fault Tolerance
> **Executive Summary**: Handling nodes that may behave arbitrarily (malicious or buggy). More complex than crash-fault tolerance.

- Requires 3f+1 nodes to tolerate f Byzantine faults
- Practical Byzantine Fault Tolerance (PBFT) algorithm
- Used in blockchain systems

---

# Consensus Algorithms

## Paxos
> **Executive Summary**: Classic consensus algorithm. Guarantees agreement on a single value among distributed nodes. Complex to implement correctly.

**Roles**:
- **Proposers**: Suggest values
- **Acceptors**: Vote on proposals
- **Learners**: Learn chosen value

**Phases**:
1. **Prepare**: Proposer asks acceptors to promise not to accept older proposals
2. **Accept**: If majority promise, proposer sends accept request
3. **Learn**: Acceptors notify learners of chosen value

**Use Cases**: Chubby, Spanner, Zookeeper (ZAB is Paxos variant)

---

## Raft
> **Executive Summary**: Understandable consensus algorithm. Equivalent to Paxos but easier to implement. Leader-based approach.

**Key Concepts**:
- **Leader Election**: One leader at a time, elected by majority
- **Log Replication**: Leader replicates log entries to followers
- **Safety**: Only leader with most up-to-date log can win election

**Terms**: Logical time periods, new term for each election

```
States: Follower → Candidate → Leader
```

**Use Cases**: etcd, Consul, CockroachDB, TiKV

| Paxos | Raft |
|:------|:-----|
| Multi-decree complex | Simpler leader-based |
| Academic | Practical |
| Harder to implement | Well-documented |

---

## ZAB (Zookeeper Atomic Broadcast)
> **Executive Summary**: Paxos variant optimized for primary-backup systems. Used by Apache Zookeeper.

**Phases**:
1. Discovery
2. Synchronization
3. Broadcast

---

## Viewstamped Replication
> **Executive Summary**: Early consensus protocol, precursor to Raft. Uses view changes for leader election.

---

# Leader Election

> **Executive Summary**: Process of selecting a single coordinator node. Critical for primary-backup systems, distributed locks, coordination.

**Algorithms**:
- **Bully Algorithm**: Highest ID wins
- **Ring Algorithm**: Token passing
- **Raft/Paxos**: Consensus-based election

**Challenges**:
- Network partitions
- Split-brain
- Byzantine failures

**Tools**: Zookeeper, etcd, Consul

---

# Clock Synchronization

## Wall Clock vs Monotonic Clock
> **Executive Summary**: Wall clocks can jump (NTP sync), monotonic clocks only move forward. Use monotonic for measuring durations.

| Wall Clock | Monotonic Clock |
|:-----------|:----------------|
| Can go backwards | Always increases |
| NTP synchronized | Local to machine |
| For timestamps | For durations |

---

## Vector Clocks
> **Executive Summary**: Track causality in distributed systems. Each node maintains vector of counters. Detect concurrent events.

```
Node A: [A:1, B:0, C:0]
Node B: [A:1, B:1, C:0]  (after receiving from A)
```

**Comparison**:
- V1 < V2: V1 happened-before V2
- V1 || V2: Concurrent events

**Use Cases**: Conflict detection in eventual consistency (Dynamo, Riak)

---

## Lamport Timestamps
> **Executive Summary**: Simpler than vector clocks. Single counter per node. Provides partial ordering.

**Rules**:
1. Increment counter before each event
2. On send: include counter in message
3. On receive: counter = max(local, received) + 1

**Limitation**: Cannot detect concurrent events

---

## Hybrid Logical Clocks (HLC)
> **Executive Summary**: Combine physical time with logical counters. Causality + real-time proximity.

- Used by CockroachDB, Spanner
- Physical component for human-readable timestamps
- Logical component for ordering

---

# Failure Detection

## Heartbeat
> **Executive Summary**: Nodes periodically send "I'm alive" messages. Simple but can have false positives during network issues.

**Parameters**:
- Heartbeat interval
- Timeout threshold
- Number of missed heartbeats

---

## Phi Accrual Failure Detector
> **Executive Summary**: Probabilistic failure detection. Outputs suspicion level (φ) rather than binary up/down.

- Adapts to network conditions
- Used by Cassandra, Akka
- Higher φ = more suspicious of failure

---

## SWIM Protocol
> **Executive Summary**: Scalable Weakly-consistent Infection-style Membership. Efficient failure detection via random probing.

**How it works**:
1. Pick random node, send ping
2. If no response, ask k other nodes to probe
3. If still no response, mark suspected
4. Disseminate membership via piggybacked gossip

**Use Cases**: HashiCorp Memberlist, Serf

---

# Gossip Protocol
> **Executive Summary**: Epidemic-style information dissemination. Nodes randomly exchange information with peers. Eventually all nodes converge.

**Properties**:
- Scalable (O(log n) rounds to converge)
- Fault tolerant
- Decentralized
- Eventually consistent

**Use Cases**:
- Failure detection
- Membership management
- Data dissemination
- Aggregate computation

**Implementations**: Cassandra, Consul, Riak

---

# Data Replication

## Synchronous vs Asynchronous

| Synchronous | Asynchronous |
|:------------|:-------------|
| Wait for all replicas | Fire and forget |
| Stronger consistency | Higher availability |
| Higher latency | Lower latency |
| Simpler reasoning | Potential data loss |

---

## Semi-Synchronous
> **Executive Summary**: Wait for at least one replica acknowledgment. Balance between consistency and latency.

---

## Chain Replication
> **Executive Summary**: Replicas form a chain. Writes go to head, reads from tail. Strong consistency with good throughput.

```
Write → Head → Node2 → Node3 → Tail (Read)
```

**Properties**:
- Strong consistency
- High read throughput
- Write latency = chain length
- Tail handles all reads

---

## Quorum
> **Executive Summary**: Require majority agreement for operations. W + R > N ensures overlap between read and write sets.

**Common configurations**:
- W=N, R=1: Strong consistency, slow writes
- W=1, R=N: Fast writes, slow reads
- W=R=⌈(N+1)/2⌉: Balanced

**Sloppy Quorum**: Accept writes even if preferred nodes unavailable (with hinted handoff)

---

# Anti-Entropy Protocols

## Read Repair
> **Executive Summary**: Fix inconsistencies during normal reads. Compare versions from multiple replicas, update stale ones.

---

## Anti-Entropy (Merkle Trees)
> **Executive Summary**: Background process to detect and fix inconsistencies. Use Merkle trees to efficiently compare large datasets.

**Process**:
1. Build Merkle tree of data
2. Compare root hashes
3. If different, traverse to find divergent branches
4. Only transfer/fix differing data

---

## Hinted Handoff
> **Executive Summary**: When target node is down, store write hint on available node. Deliver when target recovers.

- Improves write availability
- Temporary inconsistency acceptable
- Used by Dynamo, Cassandra

---

# Conflict Resolution

## Last-Write-Wins (LWW)
> **Executive Summary**: Highest timestamp wins. Simple but can lose updates. Requires synchronized clocks.

**Problems**:
- Data loss
- Clock skew issues
- Not suitable for all use cases

---

## Vector Clocks
> **Executive Summary**: Track version history per replica. Detect conflicts by comparing vectors. Application resolves.

---

## CRDTs (Conflict-free Replicated Data Types)
> **Executive Summary**: Data structures that mathematically guarantee convergence. No coordination needed.

**Types**:
- **G-Counter**: Grow-only counter
- **PN-Counter**: Increment/decrement counter
- **G-Set**: Grow-only set
- **OR-Set**: Observed-Remove set
- **LWW-Register**: Last-writer-wins register

**Use Cases**: 
- Collaborative editing
- Shopping carts
- Distributed counters

**Implementations**: Redis CRDT, Riak

---

# Idempotency
> **Executive Summary**: Operation can be applied multiple times with same effect. Critical for safe retries in distributed systems.

**Techniques**:
- **Idempotency keys**: Client-generated unique ID per operation
- **Deduplication**: Track processed request IDs
- **Conditional updates**: Compare-and-swap

**Naturally idempotent**:
- GET, PUT, DELETE (if same parameters)
- Set value to X

**Not idempotent**:
- POST (create new resource)
- Increment counter

---

# Circuit Breaker
> **Executive Summary**: Prevent cascading failures by failing fast. Stop calling failing service, allow recovery time.

**States**:
1. **Closed**: Normal operation, track failures
2. **Open**: Fail immediately, don't call service
3. **Half-Open**: Test if service recovered

```
Closed → (failures exceed threshold) → Open
Open → (timeout expires) → Half-Open
Half-Open → (success) → Closed
Half-Open → (failure) → Open
```

**Implementation**: Hystrix, Resilience4j, Polly

---

# Bulkhead Pattern
> **Executive Summary**: Isolate components to contain failures. Like ship bulkheads preventing flooding.

**Types**:
- **Thread pool isolation**: Separate pools per service
- **Connection pool isolation**: Separate pools per dependency
- **Semaphore isolation**: Limit concurrent requests

---

# Backpressure
> **Executive Summary**: Mechanism for slow consumers to signal producers to slow down. Prevents buffer overflow and memory issues.

**Strategies**:
- **Drop**: Discard excess messages
- **Buffer**: Queue messages (limited)
- **Block**: Block producer
- **Rate limit**: Throttle producer

**Implementations**: Reactive Streams, TCP flow control

---

# Saga Pattern
> **Executive Summary**: Manage distributed transactions via sequence of local transactions. Each step has compensating action for rollback.

## Choreography
> **Executive Summary**: Services react to events, no central coordinator. Simpler but harder to track.

```
OrderService → Payment Event → PaymentService → Shipping Event → ...
```

## Orchestration
> **Executive Summary**: Central orchestrator directs the flow. Easier to understand but single point of failure.

```
Orchestrator → OrderService
Orchestrator → PaymentService
Orchestrator → ShippingService
```

**Compensation**: Each step defines undo action
- CreateOrder → CancelOrder
- ChargePayment → RefundPayment
- ReserveInventory → ReleaseInventory

---

# Event Sourcing
> **Executive Summary**: Store all changes as immutable events instead of current state. Derive state by replaying events.

**Benefits**:
- Complete audit trail
- Time travel (reconstruct any past state)
- Event replay for debugging
- Natural fit for CQRS

**Challenges**:
- Event schema evolution
- Large event stores
- Complexity

**Event Store**: Append-only log
- EventStoreDB
- Kafka as event store

---

# CQRS (Command Query Responsibility Segregation)
> **Executive Summary**: Separate read and write models. Optimize each independently. Often paired with Event Sourcing.

```
Write Path: Command → Aggregate → Event → Event Store
Read Path: Event Store → Projector → Read DB → Query
```

**Benefits**:
- Optimize reads and writes independently
- Different scaling strategies
- Simpler models

**Use Cases**:
- High read/write ratio difference
- Complex domain models
- Event-driven architectures

---

# Outbox Pattern
> **Executive Summary**: Ensure atomicity between database update and event publishing. Write event to outbox table in same transaction.

```
1. Begin Transaction
2. Update business data
3. Insert event into Outbox table
4. Commit Transaction
5. Background process publishes from Outbox
6. Delete from Outbox after publish confirmed
```

**Benefits**:
- Guaranteed delivery
- At-least-once semantics
- No two-phase commit needed

---

# Change Data Capture (CDC)
> **Executive Summary**: Capture database changes as events. Stream to message queue or other systems.

**Methods**:
- **Log-based**: Read database transaction log (preferred)
- **Trigger-based**: Database triggers capture changes
- **Timestamp-based**: Poll for changed rows

**Tools**: Debezium, Maxwell, AWS DMS

**Use Cases**:
- Event streaming from legacy systems
- Data replication
- Cache invalidation
- Audit logging

---

# Service Mesh
> **Executive Summary**: Infrastructure layer handling service-to-service communication. Provides observability, security, reliability without code changes.

**Features**:
- Load balancing
- Service discovery
- Circuit breaking
- Mutual TLS
- Observability
- Traffic management

**Components**:
- **Data Plane**: Sidecar proxies (Envoy)
- **Control Plane**: Configuration, policy

**Implementations**: Istio, Linkerd, Consul Connect

---

# Sidecar Pattern
> **Executive Summary**: Deploy helper container alongside main container. Handles cross-cutting concerns without modifying application.

**Use Cases**:
- Logging agents
- Service mesh proxy
- Configuration refresh
- Security

---

# Blue-Green Deployment
> **Executive Summary**: Run two identical production environments. Switch traffic after testing new version.

```
Blue (current) ←── Traffic
Green (new) ←── Test
After validation: Switch traffic to Green
```

**Benefits**: Instant rollback, zero downtime

---

# Canary Deployment
> **Executive Summary**: Gradually roll out to small percentage of users first. Monitor, then expand or rollback.

```
v1: 95% traffic
v2: 5% traffic (canary)
Monitor metrics...
v1: 50% → v2: 50%
v1: 0% → v2: 100%
```

---

# Feature Flags
> **Executive Summary**: Control feature availability without deployment. Enable/disable features dynamically.

**Use Cases**:
- Gradual rollout
- A/B testing
- Kill switches
- Beta features

**Tools**: LaunchDarkly, Split, Flagsmith

---

# Back-of-Envelope Calculations

## Common Numbers
```
L1 cache reference:                     0.5 ns
L2 cache reference:                     7 ns
Main memory reference:                  100 ns
SSD random read:                        150 μs
HDD seek:                               10 ms
Packet roundtrip (same datacenter):     500 μs
Packet roundtrip (CA to Netherlands):   150 ms
```

## Storage
```
1 byte = 8 bits
1 KB = 1,000 bytes
1 MB = 1,000 KB
1 GB = 1,000 MB
1 TB = 1,000 GB

ASCII char: 1 byte
Unicode char: 2-4 bytes
UUID: 16 bytes
Timestamp: 8 bytes
```

## Scale
```
1 million = 10^6
1 billion = 10^9
Seconds in day: 86,400 ≈ 10^5
Seconds in year: 31,536,000 ≈ 3 × 10^7
```

## QPS Estimates
```
Daily Active Users (DAU): X
Avg requests per user per day: Y
QPS = (X × Y) / 86400
Peak QPS ≈ 2-3 × average QPS
```

---

# System Design Interview Framework

## 1. Requirements Clarification (3-5 min)
- Functional requirements
- Non-functional requirements
- Scale estimates
- Constraints and assumptions

## 2. Back-of-Envelope Estimation (3-5 min)
- QPS
- Storage
- Bandwidth
- Memory (cache)

## 3. High-Level Design (10-15 min)
- Core components
- Data flow
- APIs
- Database schema

## 4. Deep Dive (15-20 min)
- Scaling bottlenecks
- Database choices
- Caching strategies
- Failure handling

## 5. Wrap Up (3-5 min)
- Trade-offs discussed
- Future improvements
- Edge cases

