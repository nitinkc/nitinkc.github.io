---
title:  "Data Consistency Levels"
date:   2024-01-20 11:20:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

Measure of how **up-to-date* a piece of data is in a distributed systems.

**Consistency Levels**

### Linearizable/Serializable Consistency 
- EveryRead operation results in the **MOST up-to-date** data
- To achieve this a single-threaded single server may be used.So every read and write request will always be ordered
- Every request is processed linearly one by one
  - Others wait while one request gets processed
  - If the processing request fails or takes a long time or sleeps, every other request has to wait (**Head-of-line Blocking**)
  - Single point of failure
  - High Latency - Time taken to process the request successfully. 
  - Low Availability - Chance of a system to be able to respond to a request
  - High Consistency - 

### Eventual Consistency
- we can send stale data for a read request,but eventually,return the latest data after updates are done
- Until we are returning the stale data our system is not consideredconsistent but we can guarantee that after some time it will be consistent
- To achieve this we can process read and write requests parallelly (using multiple servers) or concurrently (using multiple threads)
- Multiple servers can send requests to a DB at the same time
  - If `WRITE (then)-> READ` is expected and both requests went from 2 different instances of a service, 
    - may be possible that Read goes in first and reads the data before writing it
- Same with email - if the mail is in the outbox, eventually it will be sent


### Causal Consistency
- if a previous operation is related to the current operation then the previous operation has to be executed before the current operation
- Extracts the requests based on the keys and order sequentially and perform operation
- Causal consistency is stronger and slower than eventual consistency because operations for the same key are processed sequentially.
- **Fails on Aggregation**
  - causal consistency orders query based on IDs but aggregation operations use all IDs

### Quorum
- At this consistency level, we have multiple replicas of the database and these replicas may or may not be in sync.
- For a read query, we get the data from all the replicas and return the mostappropriate values (Majority value, Latest updated value etc). 
- It works on some kind of consensus in the distributed system.
- Eventually consistent
- Distributed Consensus
- It provides fault tolerance and depending upon the values R, W and N we can either have an
  - eventually consistent system (R + W <= N) or
  - a strongly consistent system (R + W > N)

A system can be strongly consistent by specifying the **minimum number of replicas** 
it needs to read the data from. 

R + W > N where,
- R = Minimum Number of replicas to read the data from
- W = Number of replicas data is written to
- N = Total Number of replicas


| Consistency Level         | Consistency                          | Efficiency                           |
|:--------------------------|:-------------------------------------|:-------------------------------------|
| Linearizable/Serializable | Highest                              | Lowest                               |
| Causal Consistency        | Linealizable > **Causal** > Eventual | Linealizable < **Causal** < Eventual |
| Quorun                    | Configurable                         | Configurable                         |
| Eventual Consistency      | Lowest                               | Highest                              |

Check [Transaction Isolation Level](https://nitinkc.github.io/system%20design/Transaction-Isolation-levels/)
