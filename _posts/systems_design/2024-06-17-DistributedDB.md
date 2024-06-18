---
title:  "Distributed Databases"
date:   2024-06-17 11:45:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}


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

Read [Consistent Hashing]()