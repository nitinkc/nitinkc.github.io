---
categories:
- System Design
date: 2024-07-06 16:02:00
tags:
- Distributed Systems
title: Zookeeper
---

{% include toc title="Index" %}

# ZooKeeper - Key Features

**Configuration Management**: Provides a centralized configuration repository
accessible to all nodes.

- **Use Case**: Need to manage and distribute configuration settings across a
  distributed system.
- **How ZooKeeper Helps**: Stores configuration data centrally and ensures
  consistency across all nodes.

**Synchronization**: Ensures synchronization and consistency among distributed
processes.

- **Use Case**: Coordination of access to shared resources among distributed
  processes.
- **How ZooKeeper Helps**: Provides primitives like locks and barriers to
  implement distributed synchronization.

**Naming Service**: Hierarchical namespace similar to a file system for storing
metadata.

- **Use Case**: Microservices need to locate and communicate with each other
  dynamically.
- **How ZooKeeper Helps**: Acts as a registry where services can register their
  locations and consumers can discover available services.
-

**High Availability**: Provides fault tolerance and high availability through
replication.

**Sequential Consistency**: Guarantees ordered updates across distributed nodes.

**Watch Mechanism**: Allows clients to register for notifications on changes to
data.

**Leader Election**

- **Use Case**: Selecting a leader among a group of distributed nodes for
  coordination tasks.
- **How ZooKeeper Helps**: Uses its consensus protocols to elect a leader node
  reliably.