---
categories: System Design
date: 2024-06-14 08:02:00
tags:
- Consistent Hashing
- Load Balancing
- Distributed Systems
- Partitioning
title: Consistent Hashing
---

{% include toc title="Index" %}

Distribute Data/Connections across all servers evenly using a good hash
function (like MD5 or Murmur hash)

Simple hashing, when the number of servers are fixed.

$ serverIndex = hash(key) % N $
N = # of servers

If any server goes down, then N changes and the impact is drastic as most of the
keys will have to be redistributed

# Consistent Hashing

We map both servers and objects onto the hash ring, using a uniformly
distributed hash function

In addition to hashing the object keys, we also hash the server **names** and
come with range of values called **hash space**

The concept of Ring

Place the servers onto the ring by hashing its Id.

then we hash each object by its keys (sessionId, transactionId etc.) using the
same hashing function, and use the hash directly to map the key onto the ring

To locate the server for a particular object, we go clockwise from the location
of the object key on the ring until a server is found.

if a new server is added into the ring(with its new hash based on its id), only
the keys left to it will get affected

- with simple hashing, when a new key is added, almost all the keys need to be
  remapped
- with consistent hashing, adding a new server only requires redistributing of a
  fraction of the keys

## Potential Issue

With hash functions, achieving a perfect distribution & equally sized segments
on the rings is very unlikely. Conceptually, random points are picked on the
ring

Situation might occur that a lot of objects map to a single server unevenly,
leaving other servers free.
the problem is exacerbated if the servers are frequently added or removed.

This problem is resolved with the usage of the **virtual nodes**

We can have `x` servers with `y` virtual nodes for each. More virtual server
implies more distribution over the ring

But, maintaining the metadata for the virtual nodes take up more space, so a
trade-off to tune the number of virtual nodes to fit our system requirements

### To be used to distribute Data evenly

Cassandra and Dynamo DB uses consistent hashing for Data Partitioning

Data is distributed across multiple servers (horizontal scaling) in a
distributed DB environment.

for predictable performance, Evenly distributed data accross all servers is what
is aimed

### To bve used for load balancing

Taking the requests and evenly balance the load among N servers

Distribute persistent connection evenly. this limits the number of connections
that needs to be restablished when a **backend server goes down**

Hash the serverId along with the requestId

| --                         | --                                                                    |
|:---------------------------|:----------------------------------------------------------------------|
| Amazon DynamoDB            | Data Partitioning. Helps DB minimize data movement during rebalancing | 
| Apache Cassandra           | ^^                                                                    |
| Content Delivery Networks  | Distributes Web Content Evenly among the edge servers                 |
| like Acamai                | ^^                                                                    |
| Load Balancers             | Distribute persistent connection evenly across backend servers        |
| like Google Load Balancers | ^^                                                                    |

# Guaranteed Strong Consistency

$$ R + W > N  $$
𝑅 : is the number of replicas that agreed on read,
𝑊 : is the number of replicas that successfully take a write, and
𝑁 : is the total number of replicas,