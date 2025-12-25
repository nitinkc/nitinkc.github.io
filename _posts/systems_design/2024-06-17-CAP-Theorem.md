---
categories:
- System Design
date: 2024-06-17 11:45:00
tags:
- CAP Theorem
- Consistency
- Distributed Systems
title: CAP Theorem
---

{% include toc title="Index" %}

[https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#cap-theorem](https://github.com/ByteByteGoHq/system-design-101?tab=readme-ov-file#cap-theorem)

The CAP theorem, also known as Brewer's theorem, states that it is impossible
for a distributed data system to simultaneously
provide more than two out of the following three guarantees:

**Consistency (C)**: Every read receives the most recent write or an error.
In other words, all nodes in the system have the same data at any given time.

**Availability (A)**: Every request receives a response, without guarantee that
it contains the most recent write.
This means the system is always operational and responsive, even if some nodes
are down or partitioned (network partition).

**Partition tolerance (P)**: The system continues to operate despite network
partitions (communication failures)
that may cause some messages to be lost or delayed between nodes

CP systems prioritize Consistency and Partition tolerance over Availability.
They sacrifice availability when there is a network partition to ensure that
data remains consistent across all nodes.

AP systems prioritize Availability and Partition tolerance over Consistency.
They provide high availability even in the event of a network partition,
accepting that there might be temporary inconsistencies between nodes.

![](https://www.youtube.com/watch?v=BHqjEjzAicA)