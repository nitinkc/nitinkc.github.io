---
title:  "Distributed Databases"
date:   2024-06-17 11:45:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

# How Distributes DB Works

A distributed database (DB) works by distributing data across multiple nodes (servers) in a network. 
This distribution enables the database to scale horizontally, handle large volumes of data, and provide high availability and fault tolerance.

## Architecture
##### Nodes (Servers):
A distributed database consists of multiple nodes, each hosting a part of the database (data partitions).
Nodes can be geographically distributed across different locations, data centers, or regions.

##### Data Partitioning:
- The database partitions (splits) the data into smaller chunks or shards.
- Each node is responsible for storing and managing one or more partitions of the database.
- Partitioning can be done based on various strategies such as range partitioning, hash partitioning, or key-based partitioning.

##### Replication:
- To ensure fault tolerance and availability, data can be replicated across multiple nodes.

Replication involves maintaining multiple copies (replicas) of data on different nodes.

Replicas can be synchronized asynchronously (eventual consistency) or synchronously (strong consistency) depending on the system's requirements.

## Coordination and Consistency

##### Consistency Models:

Distributed databases can operate under different consistency models, such as eventual consistency or strong consistency.

- Eventual consistency allows replicas to diverge temporarily and then converge over time.
- Strong consistency ensures that all replicas are always synchronized and provide the latest committed data.

##### Coordination Protocols:

Distributed databases use coordination protocols like distributed consensus algorithms (e.g., Paxos, Raft, or variants like ZAB in ZooKeeper) to ensure consistency and coordination among nodes.

These protocols help nodes agree on the order of operations (transactions) and maintain data integrity across the distributed system.

## Query Processing and Communication
##### Query Distribution:
Queries can be distributed across nodes to leverage parallel processing and improve performance.

The distributed database’s **query optimizer** determines how to distribute and execute queries across nodes efficiently.

##### Communication Protocols:

Nodes communicate with each other using network protocols to exchange data, coordinate transactions, and synchronize replicas.

Communication protocols ensure reliable data transmission, error handling, and network partition handling (e.g., detecting and recovering from network splits).

## Benefits
Scalability: Distributed databases can scale horizontally by adding more nodes to handle increased data volume and user traffic.

Fault Tolerance: By replicating data and using distributed consensus protocols, distributed databases can tolerate node failures, network partitions, and other faults without losing data or availability.

High Availability: Data replicas and decentralized architecture ensure that distributed databases can provide high availability by serving read and write requests from multiple nodes.

## Challenges
Complexity: Designing, deploying, and maintaining distributed databases requires dealing with complex issues such as data consistency, concurrency control, and fault tolerance.

Consistency vs. Performance Trade-offs: Choosing an appropriate consistency model involves trade-offs between consistency guarantees and system performance (e.g., latency and throughput).

Network Overhead: Distributed databases rely heavily on network communication, which can introduce latency and require efficient management of network resources.



# Read Replication

Read replication solves read problems than write problems. If read most work loads is there, then its good.

one master DB and multiple slave DB's. Master used for writes, and slave for reads. Multiple slaes so if one fails others can be used for reading.


# Sharding 

Horizontal partitioning : taking an ID/Key to break data into pieces and allocate it to diff DB servers is caklled Horizontal partitioning

Vertical Partitioning : partitioning based on columns to partition

Sharding : taking one attribute in data and partition the data in such a way that each DB server gets one chunk of data

## Sharding when read replication runs out of gas
Split up the DB based on certain key, for ex, names from A to F in one db, F to N  in another and so on.

- separate overhead of identifying a shard

### Problems with Sharding

- joins accross shards
- can't do further - memcached
  - partitioning uses consistent hashing
- Failing shards
  - keep master slave architecture

Read [Consistent Hashing](https://nitinkc.github.io/system%20design/ConsistentHashing/)


# Responses to Failures
When we can't just roll it back
- Write-off
- Retry
- Compensating Actions

# BASE Properties for NoSQL DB's

Basically Available: The system guarantees availability—typically sacrificing consistency—in the presence of network partitions or node failures.
This means that the system will respond to read and write requests even if some nodes are not reachable or if there's a network issue.

Soft state: The state of the system may change over time even without input.
This reflects the idea that data in a NoSQL system can exist in various states (e.g., replicas might be inconsistent for a period).

Eventual consistency: The system will eventually become consistent once it stops receiving input. 
In practice, this means that given enough time (and no further updates), all replicas of a piece of data will eventually 
converge to the same value.


# Focus on AP 
Compromise on eventual consistency/weak consistency
```markdown
      +----------------------+
      |        Master        |
      |   [Database Server]  |
      +----------------------+
                |
                |------------------> If this link goes down, and still the 2 machines 
                v                    are in consistent state, this both are partition tolerant
      +----------------------+
      |        Slave         |
      |   [Database Server]  |
      +----------------------+

```

