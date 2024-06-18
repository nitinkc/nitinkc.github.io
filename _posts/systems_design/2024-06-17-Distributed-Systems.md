---
title:  "Distributed Systems"
date:   2024-06-17 11:45:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

Tim Burgland - Distributed Systems in one Lecture

Distributed Systems is a collection of independent computers that appear to its users as one computer.
- Computers that operate concurrently
- computers can fail independently
- computers do-not share global clock.
  - Asynchronous with respect to other machine.


|            |                             |  |
|:----------------|:-------------------------------------------|:----------------|
| Storage         | Database                                   | Relational DB/Mongo |
| ^^              | File Systems                               | Cassandra, (HDFS) |
| Computations    | Hadoop, Spark, Storm                       ||
| Synchronization | NTP (Network Time Protocol), Vector Clocks ||
| Concensus       | Paxos, Zookeeper                           ||
| Messaging       | KAfka, RabbitMq, Google PubSub             ||


# Lambda Architecture
Wrong Answers fast

Right answers slow


# Synchronization

Network time protocols

Vector clocks

