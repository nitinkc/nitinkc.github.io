---
title:  "Database Replication & Migrations"
date:   2024-01-21 02:00:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

# Replication

##### Primary-Replica model
Write could be in Primary DB, but Reads can be in both Primary and Replica

- Fault Tolerance - If primary goes down, Replica can be elevated to Primary
- Improved Read Speeds - due to multiple read servers
- Simple
- Consistency could be a problem
  - as Primary propagates the write updates to Replica and Primary may fail with
  - When a new write operation occurs on the primary, it is sent to the replica for synchronization.

##### write ahead log
Operations are sequentially executed and can be rolled back, similar to transaction logs

The replica processes the write operation and ensures consistency by applying all previous operations in a sequential manner. 

**Drawbacks**
If the replica cannot catch up with the primary, consistency issues can arise. 

Timestamps (system_currentTimestamp()) and contextual values(eg: calculations based on # of existing rows or current timestamps)
can also lead to inconsistent when the replica and primary show different data values.

The solution for addressing these issues is introduced as "change data capture" (CDC). CDC involves sending events that indicate data changes and allow subscribers to process these events and make necessary transformations. This is particularly useful when you have different types of databases, some optimized for writes and others for reads. CDC can transform data and has built-in libraries for connecting to various databases, simplifying data replication.

##### Split brain problem

2 DBs can lead to inconsistencies and difficulties in reconciliation. 
This situation is referred to as "split brain." 

Manual reconciliation techniques like "last writer wins" is also used, but it has its own risks and complexities.

To avoid split brain scenarios, 
- have an odd number of primary nodes to ensure a majority consensus in case of network partitions. 
- The use of an even number of nodes can lead to reconciliation issues and require manual intervention.


##### write amplification
 "write amplification" and the potential for increased latency.

 Paxos or Raft to ensure that the entire cluster agrees on a value during data replication. This ensures strong consistency across the system.

consensus mechanisms and odd numbers of primary nodes to maintain data consistency and avoid split-brain scenarios.

# Migrations

Moving the Data from one Server into another. 

- ETL (Extract-Transform-Load) Tools can be used
- Brute force, when the DB is shutdown, data is exported (as SQL scripts or csv files or data dump), and loaded into new DB
- Optimized approach is to keep the data copying from running DB into new DB, while keeping track of the timestamps 
up to which the back up is taken. then repeat the process 