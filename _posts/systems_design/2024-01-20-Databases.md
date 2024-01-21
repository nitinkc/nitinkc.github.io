---
title:  "Databases"
date:   2024-01-20 11:00:00
categories: [System Design]
tags: [System Design]
---
{% include toc title="Index" %}

Relational Databases have **Structured Data** 
- Id to identify a row/tuple
- Well-defined data types
- Memory Management  (estimates can be done with query execution plan with approximate amount of data shuffled)

Algorithms used when sortinfg Data
- In Relational DB,
  - B+ trees are used (to create the index of the data)
  - Or Log Structured Merged Trees
- pages 
- hash tables 
- pointers

Query Optimizer optimizes the Query executed by a developer

# NoSQL DB
- these are key value stores

# Graph Database
- Stores Data internally as nodes adn edges
- Used to perform graph queries efficiently

# Time Series Database
- Stores Records that are part of time series
- Aggregate adn compress time-stamped data
- good for metric data, instrumentation data or monitor applicatiopn

# Object-Oriented Database
- Designed to work with complex data objects
- usually implemented using Relational DB

# Relational Database Management System (RDBMS)


## PostgreSQL:

General-purpose relational database.

Suitable for applications where **data consistency and ACID compliance are crucial**.
Commonly used for transactional systems, data warehousing, and applications requiring complex queries.

Offers strong ACID compliance.
Well-suited for complex queries and relational data modeling.
Not designed for horizontal scalability but excels in vertical scalability


## Cassandra
NoSQL Database, specifically a wide-column store.

Distributed, highly scalable systems requiring **high write and read throughput**.

Suitable for time-series data, sensor data, event logging, and other scenarios where scalability and fault tolerance are critical.
Widely used in large-scale, distributed environments.

Designed for high availability, fault tolerance, and scalability.
No single point of failure, making it suitable for distributed architectures.
Sacrifices some consistency (eventual consistency) for high availability and partition tolerance.



## Neo4j

Graph Database.

Applications with complex relationships and graph structures.

Suitable for scenarios where the relationships between data points are as important as the data itself.

Often used in social networks, recommendation engines, fraud detection, and any domain where relationships play a central role.

Optimized for traversing and querying graph structures.
Ideal for scenarios where relationships and connections between data points are crucial.
Well-suited for use cases involving complex graph-based queries.

Elastic Search don't support SQL. Have use a third party library that copvers the SQL queries into Elastic Search Queries
