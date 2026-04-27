---
title: Data Structures for System Design
date: 2024-06-13 10:30:00
categories:
- System Design
tags:
- Data Structures
- Algorithms
---

{% include toc title="Index" %}

Essential data structures for building scalable distributed systems.
{: .notice--primary}

# Probabilistic Data Structures

Probabilistic data structures trade perfect accuracy for massive space and time savings. They provide approximate answers that are "good enough" for many use cases.
{: .notice--info}

## Bloom Filter
> **Executive Summary**: Space-efficient probabilistic structure to test set membership. May return false positives but NEVER false negatives. Perfect for "definitely not in set" queries.

**How it works**:
1. Bit array of m bits, initialized to 0
2. k independent hash functions
3. To add: hash element k times, set those bits to 1
4. To query: hash element k times, check if ALL bits are 1

```
False Positive Rate: (1 - e^(-kn/m))^k
where: n = elements, m = bits, k = hash functions
```

**Use Cases**:
- Database query optimization (check before disk access)
- Web browsers checking malicious URLs
- CDN cache existence checks
- Preventing one-hit-wonders in cache
- Email spam detection

**Variants**:
- **Counting Bloom Filter**: Counters instead of bits, supports deletion
- **Scalable Bloom Filter**: Grows dynamically
- **Cuckoo Filter**: Supports deletion, often more space-efficient

| Operation | Time Complexity | Space |
|:----------|:----------------|:------|
| Insert | O(k) | O(m) bits |
| Query | O(k) | - |
| Delete | Not supported | - |

---

## Count-Min Sketch
> **Executive Summary**: Estimates frequency of elements in a stream. Like Bloom filter but counts occurrences instead of membership. Always overestimates, never underestimates.

**How it works**:
1. 2D array of d rows × w columns
2. d independent hash functions
3. To add: increment counters at d positions
4. To query: return minimum of d counters

```
Error bound: ε = e/w (error rate)
Failure probability: δ = e^(-d)
```

**Use Cases**:
- Finding heavy hitters (top-k elements)
- Network traffic analysis
- Natural language processing (word frequencies)
- Database query optimization
- Click stream analysis

| Operation | Time Complexity | Space |
|:----------|:----------------|:------|
| Update | O(d) | O(d × w) |
| Query | O(d) | - |

---

## HyperLogLog
> **Executive Summary**: Estimates cardinality (count of distinct elements) with very low memory. Uses ~12KB for billions of elements with ~2% error.

**How it works**:
1. Hash each element
2. Count leading zeros in hash
3. Track maximum leading zeros per bucket
4. Estimate cardinality from statistics

```
Memory: ~12KB for 2^64 distinct elements
Standard Error: 1.04/√m where m = number of buckets
```

**Use Cases**:
- Unique visitor counting
- Database DISTINCT approximation
- Real-time analytics dashboards
- Network monitoring (unique IPs)
- Redis PFCOUNT command

| Operation | Time | Space |
|:----------|:-----|:------|
| Add | O(1) | O(m) |
| Count | O(m) | - |
| Merge | O(m) | - |

---

## MinHash / SimHash
> **Executive Summary**: Estimate similarity between sets. MinHash for Jaccard similarity, SimHash for cosine similarity on text.

### MinHash
**Use Cases**:
- Near-duplicate detection
- Document clustering
- Recommendation systems
- Plagiarism detection

**How it works**:
1. Apply k hash functions to each set
2. Take minimum hash value for each function
3. Signature = vector of k minimums
4. Jaccard similarity ≈ fraction of matching signature values

### SimHash
**Use Cases**:
- Near-duplicate web page detection (Google)
- Similar text finding
- Clustering similar items

---

## Skip List
> **Executive Summary**: Probabilistic alternative to balanced trees. Simpler to implement, supports efficient range queries. Expected O(log n) operations.

**Structure**:
```
Level 3:    1 ─────────────────────────→ 9
Level 2:    1 ──────────→ 5 ────────────→ 9
Level 1:    1 ───→ 3 ───→ 5 ───→ 7 ───→ 9
Level 0:    1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9
```

**Use Cases**:
- Redis sorted sets (ZSET)
- LevelDB / RocksDB memtables
- In-memory indexes
- Lock-free concurrent data structures

| Operation | Average | Worst |
|:----------|:--------|:------|
| Search | O(log n) | O(n) |
| Insert | O(log n) | O(n) |
| Delete | O(log n) | O(n) |

---

## T-Digest
> **Executive Summary**: Estimates percentiles/quantiles in streaming data with high accuracy at tails. Used for latency tracking (p99, p95).

**Use Cases**:
- Latency percentile tracking
- Real-time analytics
- Monitoring systems
- SLA compliance tracking

---

# Tree Structures

## B-Tree
> **Executive Summary**: Self-balancing tree optimized for disk I/O. Wide branching factor minimizes tree height. Standard for database indexes.

**Properties**:
- Each node can have m children (order m)
- Non-leaf nodes store up to m-1 keys
- All leaves at same depth
- Designed for systems that read/write large blocks

| Operation | Time |
|:----------|:-----|
| Search | O(log n) |
| Insert | O(log n) |
| Delete | O(log n) |

**Use Cases**:
- Database indexes (PostgreSQL, MySQL)
- File systems (NTFS, HFS+, ext4)

---

## B+ Tree
> **Executive Summary**: Variant of B-Tree where ALL data stored in leaves. Internal nodes only store keys. Leaves linked for efficient range scans.

**Advantages over B-Tree**:
- More keys per internal node (higher fanout)
- Sequential access via leaf links
- All data at leaf level (simpler caching)

**Use Cases**:
- Database indexes (most common)
- File systems

---

## LSM Tree (Log-Structured Merge Tree)
> **Executive Summary**: Write-optimized structure. Writes go to memory (memtable), then flush to immutable sorted files. Background compaction merges files.

**Architecture**:
```
Write → Memtable (Memory) → SSTable (Disk L0) → Compact → L1 → L2 ...
```

**Characteristics**:
- Sequential writes (fast)
- Read amplification (may check multiple levels)
- Write amplification (compaction rewrites data)
- Space amplification (temporary duplicates)

**Use Cases**:
- Write-heavy workloads
- Time-series databases
- Log storage

**Implementations**: LevelDB, RocksDB, Cassandra, HBase

---

## Merkle Tree
> **Executive Summary**: Hash tree where leaves are hashes of data blocks, parents are hashes of children. Efficient verification of data integrity and consistency.

**Structure**:
```
        Root Hash
       /         \
    H(H1+H2)   H(H3+H4)
    /     \    /     \
  H(D1) H(D2) H(D3) H(D4)
   |     |     |     |
  D1    D2    D3    D4
```

**Use Cases**:
- Bitcoin/Blockchain transaction verification
- Git (content-addressed storage)
- Anti-entropy in distributed databases (Cassandra, DynamoDB)
- File synchronization (rsync)
- Certificate transparency logs

**Key Benefit**: Identify differences between replicas by comparing only O(log n) hashes.

---

## Trie (Prefix Tree)
> **Executive Summary**: Tree for storing strings where each node represents a character. Shared prefixes share nodes. Fast prefix lookups.

| Operation | Time |
|:----------|:-----|
| Search | O(m) where m = key length |
| Insert | O(m) |
| Prefix search | O(m) |

**Use Cases**:
- Autocomplete
- Spell checkers
- IP routing tables (CIDR)
- Phone directories

**Variants**:
- **Radix Tree (Compact Trie)**: Merge single-child chains
- **Patricia Trie**: Space-optimized radix tree

---

## Segment Tree
> **Executive Summary**: Tree for range queries and updates. Each node stores aggregate for a segment. O(log n) queries and updates.

**Use Cases**:
- Range sum/min/max queries
- Range updates
- Computational geometry
- Database aggregations

---

## Fenwick Tree (Binary Indexed Tree)
> **Executive Summary**: Space-efficient structure for prefix sums and point updates. Simpler than segment tree with same complexity.

| Operation | Time |
|:----------|:-----|
| Prefix sum | O(log n) |
| Point update | O(log n) |
| Range sum | O(log n) |

---

# Geospatial Data Structures

## QuadTree
> **Executive Summary**: 2D space partitioning tree. Each node divides region into 4 quadrants. Efficient for point location and range queries.

**Use Cases**:
- Geographic information systems
- Image processing
- Collision detection in games
- Spatial indexing

---

## R-Tree
> **Executive Summary**: Tree for indexing multi-dimensional data (rectangles, polygons). Nodes represent bounding rectangles.

**Use Cases**:
- Geographic databases (PostGIS)
- Spatial queries (nearest neighbor, intersection)
- CAD systems
- Video game collision detection

---

## Geohash
> **Executive Summary**: Encode latitude/longitude into a string. Nearby locations share common prefixes. Easy proximity queries.

```
Example: 37.7749, -122.4194 → "9q8yyk"
```

**Properties**:
- Hierarchical (longer = more precise)
- Prefix sharing = nearby points
- Simple string comparison for proximity
- Edge case: points across boundaries may not share prefix

**Use Cases**:
- Location-based services
- Proximity searches
- Database indexing of locations
- Redis geospatial commands

---

## S2 Geometry
> **Executive Summary**: Google's spherical geometry library. Projects Earth onto cube faces, subdivides hierarchically. Handles edges better than Geohash.

**Use Cases**:
- Google Maps
- Uber surge pricing regions
- Ride matching
- Geographic region coverage

---

# Concurrency Data Structures

## Lock-Free Data Structures
> **Executive Summary**: Use atomic operations (CAS) instead of locks. Better performance under contention, no deadlock risk.

- **CAS (Compare-And-Swap)**: Atomic conditional update
- **ABA Problem**: Value changed A→B→A, CAS may not detect
- **Solution**: Add version counter

## Concurrent Hash Map
> **Executive Summary**: Thread-safe hash map using fine-grained locking or lock-free techniques. Segments/buckets locked independently.

- Java ConcurrentHashMap: Segment-based locking
- Lock-free versions use CAS operations

## Disruptor (Ring Buffer)
> **Executive Summary**: High-performance inter-thread messaging. Lock-free, cache-friendly ring buffer. Used by LMAX Exchange.

**Features**:
- Pre-allocated entries (no GC)
- Single producer optimization
- Batching consumers
- Mechanical sympathy (cache-line aware)

---

# Inverted Index
> **Executive Summary**: Maps content (words) to locations (documents). Foundation of full-text search. Posting lists store document IDs per term.

**Structure**:
```
"database" → [doc1, doc5, doc23, doc45]
"index"    → [doc1, doc12, doc45]
"search"   → [doc5, doc23, doc99]
```

**Use Cases**:
- Search engines (Google, Elasticsearch)
- Full-text search in databases
- Log analysis

**Features**:
- Term frequency (TF)
- Inverse document frequency (IDF)
- Positional information for phrase queries

---

# Time-Series Data Structures

## Ring Buffer (Circular Buffer)
> **Executive Summary**: Fixed-size buffer that wraps around. Old data automatically overwritten. Perfect for streaming data with fixed memory.

**Use Cases**:
- Recent N events
- Moving averages
- Audio/video buffering
- Rate limiting (sliding window)

---

## Time-Wheel
> **Executive Summary**: Circular buffer for scheduling events at future times. Constant time insert/delete for near-future events.

**Structure**:
```
Slot 0  → [timer at t+0]
Slot 1  → [timer at t+1]
...
Slot 59 → [timer at t+59]
(wraps around)
```

**Use Cases**:
- Timer management (Kafka, Netty)
- Rate limiting
- Connection timeouts
- Scheduled tasks

---

# Graph Data Structures

## Adjacency List vs Matrix

| Aspect | Adjacency List | Adjacency Matrix |
|:-------|:---------------|:-----------------|
| Space | O(V + E) | O(V²) |
| Add edge | O(1) | O(1) |
| Check edge | O(degree) | O(1) |
| Find neighbors | O(degree) | O(V) |
| Best for | Sparse graphs | Dense graphs |

---

## Union-Find (Disjoint Set)
> **Executive Summary**: Track elements partitioned into disjoint sets. Near O(1) union and find with path compression.

**Operations**:
- **Find**: Determine which set an element belongs to
- **Union**: Merge two sets

**Use Cases**:
- Kruskal's MST algorithm
- Detecting cycles in graphs
- Network connectivity
- Image segmentation

| Operation | Time (with optimizations) |
|:----------|:--------------------------|
| Find | O(α(n)) ≈ O(1) |
| Union | O(α(n)) ≈ O(1) |

---

# Summary Table

| Data Structure | Primary Use | Space | Key Operations |
|:---------------|:------------|:------|:---------------|
| Bloom Filter | Set membership | O(m) bits | Insert O(k), Query O(k) |
| Count-Min Sketch | Frequency estimation | O(d×w) | Update O(d), Query O(d) |
| HyperLogLog | Cardinality | O(m) | Add O(1), Count O(m) |
| Skip List | Sorted data | O(n) | All O(log n) |
| B+ Tree | Disk-based index | O(n) | All O(log n) |
| LSM Tree | Write-heavy storage | O(n) | Write O(1)*, Read O(log n) |
| Merkle Tree | Data verification | O(n) | Verify O(log n) |
| Trie | String operations | O(nm) | All O(m) |
| QuadTree | 2D spatial | O(n) | Query O(log n) |
| R-Tree | Multi-D spatial | O(n) | Query O(log n) |
| Inverted Index | Text search | O(n) | Search O(1) |

