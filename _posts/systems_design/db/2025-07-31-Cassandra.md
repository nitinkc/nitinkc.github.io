---
title: Cassandra - Column-Oriented Database
date: 2025-05-08 11:02:00
categories:
- System Design
tags:
- Database
- NoSQL
- Distributed
---

{% include toc title="Index" %}

Apache Cassandra is a distributed, wide-column store designed for high availability and linear scalability.
Cassandra is designed for **high write throughput**, predictable low-latency reads, and scalable distribution across many nodes. To achieve this:
- You model your tables around the queries your application needs to run (query-first).
  - Data is modeled around partitions and clustering columns, optimized for fast writes and predictable reads when queries are modeled correctly.
- You often store the same logical data multiple times in different tables (denormalization) so each read can be served by a single, efficient partition lookup (no cluster-wide scan or server-side join).
  - Best for time-series, event logging, multi-region writes, and high-throughput workloads.

> In short: **design for reads (access patterns) first**, accept data duplication to keep reads fast and simple.

# Key Concepts
- **Keyspace**: top-level namespace (similar to database).
- **Table**: collection of rows grouped by a partition key.
- **Partition key**: determines which node stores the row; must be part of queries that read data efficiently.
- **Clustering columns**: order rows within a partition and support range queries.
- **Primary key** = (partition_key, clustering_columns...)
- Replication strategy and consistency levels control durability and read/write behavior.

# Basic CQL examples
Create a keyspace with SimpleStrategy (single DC) or NetworkTopologyStrategy (multi-DC):

```sql
CREATE KEYSPACE IF NOT EXISTS ks_demo
WITH replication = {
  'class': 'NetworkTopologyStrategy',
  'dc1': 3,
  'dc2': 2
};
```

Create a table (wide-column):

```sql
CREATE TABLE ks_demo.user_events (
  user_id uuid,
  event_time timestamp,
  event_type text,
  payload text,
  PRIMARY KEY (user_id, event_time)
) WITH CLUSTERING ORDER BY (event_time DESC);
```

Insert data:

```sql
INSERT INTO ks_demo.user_events (user_id, event_time, event_type, payload)
VALUES (uuid(), toTimestamp(now()), 'login', '{"ip":"1.2.3.4"}');
```

Select within a partition (must specify partition key):

```sql
-- get last 10 events for a user
SELECT event_time, event_type, payload
FROM ks_demo.user_events
WHERE user_id = 123e4567-e89b-12d3-a456-426614174000
LIMIT 10;
```

Important: queries must include the partition key (or a token() based approach) for efficient reads. Avoid full table scans.

# Primary key and modeling patterns
- Single-column partition key: PRIMARY KEY (user_id)
- Composite partition key: PRIMARY KEY ((year, month), id) — grouping by multiple columns in parentheses forms the partition key.
- Partition key + clustering columns: PRIMARY KEY (user_id, event_time) — partitioned by user, ordered by time.

Design for queries: Cassandra data modeling is query-driven. Denormalize and duplicate data to serve each query pattern efficiently.

Example: time-series rollup table vs raw events table

```sql
-- raw events (store for fast writes)
CREATE TABLE ks_demo.events_raw (
  device_id text,
  ts timestamp,
  metric_name text,
  value double,
  PRIMARY KEY (device_id, ts)
) WITH CLUSTERING ORDER BY (ts DESC);

-- daily rollup for query by date
CREATE TABLE ks_demo.events_daily (
  device_id text,
  day date,
  metric_name text,
  sum_value double,
  count_value bigint,
  PRIMARY KEY ((device_id, day), metric_name)
);
```

# Consistency and replication
- Replication factor (RF) determines how many nodes store a copy.
- Consistency levels: ANY, ONE, TWO, THREE, QUORUM, LOCAL_QUORUM, EACH_QUORUM, ALL, SERIAL, LOCAL_SERIAL.
- Typical pattern: write at QUORUM and read at QUORUM for strong-ish consistency.

# Writes, deletes, TTLs
- Cassandra is optimized for writes: writes are appended to the commit log and SSTables; memtable holds in-memory before flush.
- Deletes are tombstones — tombstones are later removed by compaction. Careful with deletes on many rows (can affect performance during reads/compaction).
- TTL support:

```sql
INSERT INTO ks_demo.events_raw (device_id, ts, metric_name, value)
VALUES ('dev-1', toTimestamp(now()), 'temp', 22.5)
USING TTL 86400; -- expires in 1 day
```

# Batches and counters
- BATCH is not a transaction across partitions — use BATCH only for atomicity within the same partition or to reduce network round trips.
- Counters are a special column type with their own caveats (eventual consistency and limited operations):

```sql
CREATE TABLE ks_demo.page_views (
  page text,
  day date,
  views counter,
  PRIMARY KEY (page, day)
);

UPDATE ks_demo.page_views SET views = views + 1 WHERE page = 'home' AND day = '2025-07-31';
```

# Lightweight transactions (LWT)
- Use `IF NOT EXISTS` or `IF <cond>` which uses Paxos for linearizable consistency on a per-partition basis.

```sql
INSERT INTO ks_demo.users (user_id, email)
VALUES (uuid(), 'alice@example.com') IF NOT EXISTS;
```

LWTs are slower and should be used sparingly for coordination needs like uniqueness checks.

# Secondary indexes, materialized views
- Secondary indexes: useful for low-cardinality fields or small partitions; avoid on high-cardinality values.
- Materialized views (MV): can help maintain alternate query patterns but have known issues historically; use with caution and understand repair/consistency implications.

# Compaction and performance settings
- Compaction strategies: SizeTieredCompactionStrategy (STCS), LeveledCompactionStrategy (LCS), TimeWindowCompactionStrategy (TWCS) — choose based on workload (e.g., TWCS for time-series).
- Bloom filters, compression, and memtable settings affect IO and memory trade-offs.

# Read/write path (high level)
- Write: coordinator node -> commit log + memtable -> replica nodes persist memtable -> flush -> SSTable files.
- Read: coordinator queries replicas; depending on CL it may read from one replica and then perform read repair or merge results from multiple replicas.

# Use cases and comparison to MongoDB
- Cassandra excels at linear write scaling, multi-region replication, and predictable latency for modeled queries.
- MongoDB (document DB) offers richer ad-hoc querying and flexible document shapes. Cassandra requires query-driven modeling and often denormalization.

When to choose Cassandra:
- High ingest rates with predictable query patterns.
- Multi-region deployments requiring high availability and no single-master.
- Time-series, IoT, logs, events, and counter use cases.

# Example modeling walkthrough
Problem: store sensor readings and support queries:
- Latest N readings for a sensor
- Aggregate by day per sensor

Design:
- Table `sensor_latest` with PRIMARY KEY (sensor_id, ts) clustering DESC for latest reads.
- Table `sensor_daily_agg` with PRIMARY KEY ((sensor_id, day), metric) for daily rollups.

# Administration notes
- Repair is required for anti-entropy across replicas (nodetool repair) — schedule repairs according to RF and workload.
- Backup: snapshot SSTables; incremental repairs can be used.
- Monitor compaction, tombstones, and disk usage to avoid read spikes.

# Quick CQL cheat sheet
```sql
-- create keyspace
CREATE KEYSPACE ks WITH replication = {'class':'SimpleStrategy','replication_factor':3};

-- create table
CREATE TABLE ks.users (id uuid PRIMARY KEY, name text, email text);

-- insert
INSERT INTO ks.users (id, name, email) VALUES (uuid(), 'Bob', 'bob@example.com');

-- lightweight transaction
INSERT INTO ks.users (id, email) VALUES (uuid(), 'x@x.com') IF NOT EXISTS;
```

# Further reading and tools
- Apache Cassandra documentation: https://cassandra.apache.org/
- cqlsh: interactive CQL shell
- Reaper / Netflix Priam: repair and management tools

---

If you'd like, I can also:
- Rename the file to `2025-07-31-MongoDb.md` if you prefer the existing MongoDB content to live in a correctly named file (note: I didn't rename files to avoid changing URLs).
- Create a short redirect page if you want to preserve the old filename but serve a different title.
- Add diagrams or a small example app (CQL scripts) under `scripts/` for the modeling walkthrough.
