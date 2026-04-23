## Copilot Context: MongoDB Learning Labs (consolidated)

### Project Overview
- **Goal**: Structured, incremental learning path to master MongoDB with shell labs and comprehensive theory documentation
- **Environment**: MongoDB 7.0 (Docker 3-node replica set in `docker/`), mongosh shell, Python MkDocs
- **Documentation**: Hosted via MkDocs with comprehensive theory, labs, and interview prep materials

### Key Project Structure
```
├── docs/
│   ├── index.md                              # Home page with quick start guide
│   ├── labs-overview.md                      # Lab exercises overview
│   ├── interview-prep.md                     # Interview Q&A and self-assessment
│   ├── theory/                               # 8 comprehensive theory modules
│   │   ├── 01-nosql-and-mongodb.md          # NoSQL concepts, CAP theorem, why MongoDB
│   │   ├── 02-core-concepts.md              # BSON, ObjectId, replica sets, oplog
│   │   ├── 03-data-modeling.md              # Embedding vs referencing, schema patterns
│   │   ├── 04-indexes-and-aggregation.md    # Index types, aggregation pipeline stages
│   │   ├── 05-transactions-and-consistency.md # ACID transactions, read/write concerns
│   │   ├── 06-ttl-and-change-streams.md     # TTL indexes, change streams, capped collections
│   │   ├── 07-aggregation-advanced.md       # $lookup, $facet, $bucket, $graphLookup, $setWindowFields
│   │   ├── 08-advanced.md                   # Sharding, security, monitoring, performance
│   ├── js/
│   │   └── mermaid-init.js                  # Mermaid diagram initializer
├── labs/                                    # 11 progressive MongoDB shell lab exercises
│   ├── 01_database_basics.js
│   ├── 02_document_modeling.js
│   ├── 03_indexes.js
│   ├── 04_aggregation_pipeline.js
│   ├── 05_transactions.js
│   ├── 06_ttl_and_capped.js
│   ├── 07_advanced_aggregation.js
│   ├── 08_schema_patterns.js
│   ├── 09_replica_set.js
│   ├── 10_security_basics.js
│   └── 11_monitoring_and_performance.js
├── docker/
│   ├── docker-compose.yml                   # 3-node MongoDB replica set + mongo-express
│   ├── init.js                              # Database initialization script
│   └── start.sh                             # Quick start script
├── mkdocs.yml                               # MkDocs configuration
├── requirements.txt                         # Python dependencies (MkDocs, plugins)
└── README.md                                # Project overview
```

### Theory Materials - What Each Module Covers
Each theory module includes:
- **Definitions**: Clear, precise definitions of core concepts
- **Explanations**: "What it means" sections with context and reasoning
- **Real-World Examples**: MongoDB shell code, scenarios, and use cases
- **Best Practices**: Do's and don'ts with justifications
- **Anti-Patterns**: Common mistakes and how to avoid them
- **Diagrams**: Mermaid diagrams showing relationships and workflows
- **Comparison Tables**: Quick reference guides (e.g., embedding vs referencing, write concerns)

### Key Learning Areas & Conventions

#### 1. **Document Model & Schema** (Theory 01-03, Labs 01-02, 08)
- Documents are flexible BSON objects (no fixed schema)
- Embed related data for co-accessed queries (reduce round-trips)
- Reference when data grows unboundedly or is shared across documents
- 16MB document size limit — use Outlier Pattern for exceptions
- Query-first design: structure data for your access patterns

#### 2. **Indexes** (Theory 04, Labs 03)
- Single-field, compound, multikey, text, geospatial, hashed, wildcard, partial, sparse, TTL
- ESR rule: **E**quality first, **S**ort second, **R**ange last (for compound indexes)
- IXSCAN = index scan (good), COLLSCAN = full collection scan (bad)
- Covered queries: all fields in filter + projection are in the index (fastest)
- Use `explain('executionStats')` to verify index usage

#### 3. **Aggregation Pipeline** (Theory 04, Labs 04, 07)
- Sequential stages: `$match`, `$group`, `$project`, `$unwind`, `$sort`, `$limit`, `$lookup`, `$facet`, etc.
- `$match` early to reduce data volume before expensive stages
- `$group` + accumulators (`$sum`, `$avg`, `$max`, `$push`) for analytics
- `$lookup` for runtime joins (slow — prefer embedding when possible)
- `$facet` for multi-faceted search results in one query

#### 4. **Transactions & Consistency** (Theory 05, Labs 05)
- Multi-document ACID transactions available on replica sets (4.0+) and sharded clusters (4.2+)
- `writeConcern: w: "majority"` ensures data survives primary failure
- `readConcern: "majority"` prevents reading uncommitted / rolled-back data
- Transactions have 3-5x overhead — prefer embedding to avoid them
- `retryWrites: true` (default) auto-retries writes on transient errors

#### 5. **Data Lifecycle** (Theory 06, Labs 06)
- TTL index: auto-delete documents after `expireAfterSeconds` (background thread ~60s)
- Capped collections: fixed-size ring buffers (auto-overwrite oldest docs)
- Change streams: real-time, resumable notifications on data changes
- Oplog: operations log that secondaries replay to stay in sync

#### 6. **Data Modeling Patterns** (Theory 03, Labs 08)
- **Bucket**: group time-series events into fixed-size buckets (IoT, metrics)
- **Computed**: pre-calculate expensive aggregations at write time (ratings, counts)
- **Polymorphic**: use type discriminator field to store different shapes in one collection
- **Outlier**: handle rare large documents with an overflow collection + flag
- **Subset**: embed only frequently-used fields, keep full data in separate collection
- **Embedding vs Referencing**: embed if always accessed together; reference if unbounded growth

#### 7. **Replica Sets & Consistency** (Theory 02, Labs 09)
- One PRIMARY (writes), N SECONDARies (read scaling + HA), optional ARBITERs (vote only)
- Read preferences: `primary`, `primaryPreferred`, `secondary`, `secondaryPreferred`, `nearest`
- Oplog: operations log that secondaries replay (idempotent, resumable)
- Auto-election on primary failure (~10 seconds), brief write outage during election
- Replication lag: monitor to ensure secondaries stay in sync

#### 8. **Sharding, Security & Monitoring** (Theory 08, Labs 10-11)
- Sharding: horizontal partitioning via shard key (enable linear scaling)
- Shard key: high cardinality, even distribution, matches query patterns
- Security: authentication (SCRAM-SHA-256), roles (built-in + custom), TLS encryption
- Monitoring: `explain()`, profiler, `$indexStats`, `serverStatus()`, `currentOp()`
- Performance: WiredTiger cache, index selectivity, tombstone ratio, GC pauses

### Important Files & Their Purposes
- **`docker/docker-compose.yml`**: 3-node MongoDB replica set (rs0), mongo-express UI
- **`docker/init.js`**: Base schema initialization; creates users, orders, products collections with seed data
- **`labs/` (11 files)**: Progressive MongoDB shell exercises, one `.js` file per lab
- **`docs/theory/` (8 files)**: Comprehensive learning modules with examples and diagrams
- **`mkdocs.yml`**: Site navigation and MkDocs configuration
- **`.github/copilot-instructions.md`**: This file; context for AI coding assistance

### Coding Standards & Practices
- **MongoDB Shell**: Use `mongosh` (modern shell, replaces legacy `mongo`)
- **BSON Types**: Use `Date` for timestamps, `Decimal128` for money, `ObjectId` for unique IDs
- **Collections**: Name in lowercase snake_case (e.g., `user_profiles`, `order_items`)
- **Schema**: Define validation via `$jsonSchema` for important collections
- **Indexes**: Name indexes with descriptive names (e.g., `idx_users_email_unique`)
- **Query Patterns**: Design collections for your access patterns (query-first, not normalization-first)
- **Comments**: Explain "why" not just "what" — MongoDB has different mental model than SQL

### Common Development Tasks

#### Running Labs
```bash
# Start 3-node replica set
cd docker && docker compose up -d

# Run individual lab exercise
docker exec -it mongo1 mongosh --file /labs/03_indexes.js

# Connect to interactive shell
docker exec -it mongo1 mongosh

# Or from host (requires mongosh installed locally)
mongosh "mongodb://localhost:27017/mongo_labs?replicaSet=rs0"
```

#### Common Queries
```js
// Switch database
db = db.getSiblingDB("mongo_labs");

// View collection schema
db.getCollectionInfos();

// Check indexes
db.collection_name.getIndexes();

// Replica set status
rs.status();
rs.conf();
```

#### Debugging Performance Issues
- **Slow query**: Use `explain('executionStats')` to check IXSCAN vs COLLSCAN
- **Missing index**: Look for COLLSCAN in explain() output
- **High replication lag**: Check secondaries with `rs.status()`, monitor oplog window
- **Hot shard**: Monitor shard stats, ensure shard key is high-cardinality
- **Large documents**: Monitor `$bsonSize` in aggregation, consider decomposing
- **OOM errors**: Increase WiredTiger cache, reduce batch sizes

### Interview Prep Notes
- Focus on trade-offs: embedding vs referencing, consistency vs performance, sharding vs single-node
- Explain document model advantages: flexible schema, nested data, query-first design
- Understand CAP theorem and why MongoDB is CP (strongly consistent on primary)
- Know when NOT to use MongoDB: complex relational joins, small data, strict ACID everywhere
- Be ready to design a schema for a given business requirement (query-first modeling)
- Explain replica sets: primary/secondary roles, oplog replication, auto-election, replication lag
- Understand indexes deeply: ESR rule, covered queries, multikey behavior, index intersection

### Update History
- **Latest**: Complete MongoDB Learning Labs project created with 11 progressive labs, 8 theory modules, 3-node Docker setup
- **Labs**: All executable mongosh scripts with inline comments explaining concepts
- **Docs**: Comprehensive theory with definitions, examples, best practices, anti-patterns, and Mermaid diagrams
- **Docker**: Replica set + mongo-express UI for hands-on practice
- **Copilot**: This instruction file for AI agent context and guidance

