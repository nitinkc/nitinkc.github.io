## Copilot Context: Cassandra Learning Labs (consolidated)

### Project Overview
- **Goal**: Structured, incremental learning path to master Cassandra with CQL labs and a Spring Boot application
- **Environment**: Cassandra 5.0.6 (Docker in `docker/`), Java 21, Maven, Spring Boot 3.x app in `spring-boot-app/`
- **Documentation**: Hosted via MkDocs with comprehensive theory, labs, and interview prep materials

### Key Project Structure
```
├── docs/
│   ├── index.md                              # Home page with GitHub repo link
│   ├── theory/                               # 8 comprehensive theory modules
│   │   ├── 01-nosql-and-cassandra.md        # NoSQL concepts, CAP theorem, why Cassandra
│   │   ├── 02-core-concepts.md              # Cluster, nodes, partition keys, RF, consistency
│   │   ├── 03-data-modeling.md              # Query-first design, denormalization, time-series
│   │   ├── 04-indexes-and-mv.md             # Secondary indexes, materialized views, dual-writes
│   │   ├── 05-consistency-lwt-batch.md      # Consistency levels, Paxos, atomic writes
│   │   ├── 06-ttl-tombstones.md             # Data expiration, tombstone management, compaction
│   │   ├── 07-aggregation-counters.md       # Aggregation limits, counters, filtering
│   │   ├── 08-advanced.md                   # Hot partitions, multi-DC, security, monitoring
│   ├── interview-prep.md                    # Interview preparation guide
│   ├── interview-questions.md               # Q&A for interviews and self-study
│   └── labs-overview.md                     # Lab exercises overview
├── labs/                                    # 11 progressive CQL lab exercises
│   ├── 01_keyspace_basics.cql
│   ├── 02_partitioning_clustering.cql
│   ├── 03_modeling_by_query.cql
│   ├── 04_indexes_and_mv.cql
│   ├── 05_consistency_lwt_batch.cql
│   ├── 06_ttl_tombstones.cql
│   ├── 07_aggregation_filtering.cql
│   ├── 08_relational_to_query_first.cql
│   ├── 09_multi_dc_replication.cql
│   ├── 10_security_basics.cql
│   └── 11_monitoring_and_repair.cql
├── docker/
│   ├── docker-compose.yml                   # 2-node Cassandra cluster setup
│   ├── init.cql                             # Schema initialization
│   └── start-2node.sh                       # Quick start script
└── spring-boot-app/                         # Spring Boot 3.x application
    ├── pom.xml                              # Maven dependencies
    └── src/main/                            # Application source code
```

### Theory Materials - What Each Module Covers
Each theory module now includes:
- **Definitions**: Clear, precise definitions of core concepts
- **Explanations**: "What it means" sections with context and reasoning
- **Real-World Examples**: CQL code, scenarios, and use cases
- **Best Practices**: Do's and don'ts with justifications
- **Anti-Patterns**: Common mistakes and how to avoid them
- **Diagrams**: Mermaid diagrams showing relationships and workflows
- **Comparison Tables**: Quick reference guides (e.g., SI vs. MV vs. Dual-Write)

### Key Learning Areas & Conventions

#### 1. **Primary Key Design** (Theory 02, Labs 02-03)
- Partition key determines data distribution (hash-based)
- Clustering columns define sort order within partition
- Hot partitions = most common performance issue
- Solutions: salting (composite keys), time-buckets, high-cardinality distribution

#### 2. **Query-First Denormalized Modeling** (Theory 03, Labs 03, 08)
- Design tables for specific queries, NOT for normalization
- Duplicate data across tables (denormalization)
- No joins supported (query multiple tables in application)
- Time-series: always use time-bucket in partition key

#### 3. **Consistency & Transactions** (Theory 05, Labs 05)
- Tunable consistency: ONE, QUORUM, ALL, LOCAL_QUORUM
- Lightweight Transactions (LWT): Paxos-based, IF conditions
- Batching: logged (atomic) vs unlogged (parallel)
- QUORUM + QUORUM recommended for balanced consistency
- LWT has 2-5x latency overhead; use sparingly

#### 4. **Data Lifecycle Management** (Theory 06, Labs 06)
- TTL: automatic expiration (recommended for sessions, tokens)
- Tombstones: deletion markers, prevent data resurrection
- gc_grace_seconds: window for tombstone removal (default 10 days)
- Monitor tombstone ratio; use TTL for mass expiration

#### 5. **Indexes & Materialized Views** (Theory 04, Labs 04)
- Secondary indexes: only for low-cardinality columns + small result sets
- Materialized views: automatic denormalization (consistency risks)
- Dual-writes: explicit application-controlled updates (safest for critical data)
- High-cardinality index queries unpredictable; fix with better schema

#### 6. **Aggregation & Filtering** (Theory 07, Labs 07)
- Aggregation: only efficient within single partition
- ALLOW FILTERING: symptom of schema mismatch; avoid in production
- Counters: distributed, eventually consistent (accept approximation)
- Use denormalization or batch processing for cross-partition aggregation

#### 7. **Data Distribution & Hot Partitions** (Theory 08, Labs 02)
- Monitor for balanced load across nodes
- Salting: add random component to partition key
- Time-buckets: rotate partitions daily/hourly
- Prevent: high-cardinality PK, avoid low-cardinality PK alone

#### 8. **Security & Monitoring** (Theory 08, Labs 10-11)
- Authentication: enable in production, strong passwords
- Encryption: in-transit for sensitive data, at-rest for compliance
- nodetool: monitor status, repair, compaction, GC
- Metrics: latency, GC pauses, tombstone ratio, disk usage, CPU
- Repair: weekly/monthly anti-entropy repair (merkle trees)

### Important Files & Their Purposes
- **`docker/docker-compose.yml`**: Two-node Cassandra cluster, quick testing
- **`docker/init.cql`**: Base schema; lab exercises build on top
- **`labs/README.md`**: Lab exercise descriptions and learning objectives
- **`labs/interview-questions.md`**: Interview Q&A and self-assessment
- **`docs/index.md`**: Documentation home with GitHub repo link
- **`mkdocs.yml`**: Site navigation and MkDocs configuration
- **`.github/copilot-instructions.md`**: This file; context for AI coding assistance

### Coding Standards & Practices
- **CQL Style**: Use UPPERCASE for keywords, snake_case for identifiers
- **Schema Design**: Always define PRIMARY KEY explicitly; consider RF and consistency
- **Query Patterns**: Design tables for access patterns; avoid ad-hoc queries
- **Testing**: Test with docker-compose locally; use labs as test cases
- **Documentation**: Code comments explain "why" not just "what"

### Common Development Tasks

#### Running Labs
```bash
# Start Cassandra cluster
cd docker && docker-compose up -d

# Run individual lab exercise
cqlsh localhost 9042 < labs/02_partitioning_clustering.cql

# Connect to cqlsh for interactive testing
cqlsh localhost 9042
```

#### Common Queries
```cql
-- Check keyspace
DESC KEYSPACE keyspace_name;

-- View table schema
DESC TABLE table_name;

-- Check replication settings
SELECT * FROM system.local;
```

#### Debugging Cassandra Issues
- **High latency**: Check for hot partitions, tombstone ratio, GC pauses
- **Out of memory**: Increase heap, reduce cache sizes
- **Repair failures**: Run during low-traffic window, check network
- **Data inconsistency**: Use nodetool repair, check consistency levels

### Interview Prep Notes
- Focus on trade-offs: consistency vs. performance, denormalization vs. storage
- Explain partition key importance: distribution, hot partitions, scalability
- Understand CAP theorem and why Cassandra chose AP
- Know when NOT to use Cassandra (ACID, ad-hoc queries, small data)
- Be ready to design a schema for a given business requirement (query-first)

### Update History
- **Latest**: Expanded all 8 theory modules with detailed definitions, explanations, examples, and best practices
- **Added**: GitHub repo link in index.md
- **Updated**: Copilot instructions with comprehensive project structure and learning areas

