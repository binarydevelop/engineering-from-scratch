# Pinned Versions & Environment Matrix

This document records the exact database versions, query specifications, container tags, and environment specifications used across **NoSQL Databases and Query Languages From Scratch**.

---

## 1. Primary Database Versions

| Database | Version / Tag | Query Language / Spec | Container Image | Port(s) | Primary Purpose |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **MongoDB** | `7.0.12-jammy` / `8.0-rc` | MQL (MongoDB Query Language) & Aggregation Pipeline v7.0+ | `mongo:7.0-jammy` | `27017` | Document Database & Aggregation Language |
| **Apache Cassandra** | `5.0.0` (LTS) | CQL (Cassandra Query Language) v3.4.7 | `cassandra:5.0.0` | `9042` | Wide-Column & LSM Tree Distributed Storage |
| **Amazon DynamoDB** | `2.5.3` (DynamoDB Local) | Native Query/Update Expressions & PartiQL v1.0 Subset | `amazon/dynamodb-local:2.5.3` | `8000` | Cloud Key-Value, Single-Table Design, PartiQL |
| **Redis** | `7.4.0-alpine` | Redis Command Model & RedisSearch / RedisJSON | `redis:7.4-alpine` | `6379` | In-Memory Data Structures, Sorted Sets, Streams |
| **Neo4j** | `5.24.0-community` | Cypher Query Language v5 & ISO/IEC 39075:2024 (GQL) | `neo4j:5.24.0-community` | `7474`, `7687` | Property Graph & Pattern Traversal |
| **Elasticsearch** | `8.17.0` | Elasticsearch JSON Query DSL & Aggregations | `docker.elastic.co/elasticsearch/elasticsearch:8.17.0` | `9200`, `9300` | Inverted Index, Full-Text, Vector & Faceted Search |

---

## 2. Host Runtimes & Tooling

| Component | Tested Version | Minimum Supported | Notes |
| :--- | :--- | :--- | :--- |
| **Python** | `3.14.7` / `3.11.9` | `3.10.0+` | Core simulators, graders, and seeds run on pure Python standard library |
| **Docker Engine** | `29.7.2` | `24.0.0+` | Container execution environment |
| **Docker Compose**| `v5.4.0` | `v2.20.0+` | Profile-based container management (`--profile mongo`, etc.) |
| **mongosh** | `2.9.2` | `2.0.0+` | Modern MongoDB interactive shell |
| **redis-cli** | `8.4.0` / `7.4.0` | `6.2.0+` | Redis command line interface |
| **cqlsh** | `6.2.0` | `5.0.0+` | Bundled within the Cassandra container; access via `docker exec -it nosql-cassandra cqlsh` |
| **curl / httpie**| `8.7.1` | `7.68.0+` | REST testing for Elasticsearch and DynamoDB Local |

---

## 3. Disciplinary Taxonomy: Portable Concept vs Database-Specific vs Version-Specific

To maintain rigorous architectural clarity, every lesson and query exercise explicitly categorizes behavior into one of three tiers:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 1. PORTABLE CONCEPTS                                                   │
│    Hash partitioning, consistent hashing rings, LSM tree compaction,   │
│    SSTables, Bloom filters, inverted indexes, quorums (N, R, W),      │
│    vector clocks, eventual consistency, CAP / PACELC, fan-out costs.  │
├────────────────────────────────────────────────────────────────────────┤
│ 2. DATABASE-SPECIFIC BEHAVIOR                                          │
│    - MongoDB: $elemMatch, $unwind cardinality explosion, $lookup costs │
│    - Cassandra: Clustering column physical sort order, ALLOW FILTERING  │
│    - DynamoDB: Begins_with sort key expressions, GSI sparse indexes     │
│    - Redis: O(1) hash field lookup vs O(log N) sorted set range zrange │
│    - Neo4j: Pattern matching (A)-[:REL]->(B), OPTIONAL MATCH           │
│    - Elasticsearch: bool query (must, filter, should, must_not)        │
├────────────────────────────────────────────────────────────────────────┤
│ 3. VERSION-SPECIFIC CAPABILITIES                                       │
│    - Cassandra 5.0+: Storage Attached Indexing (SAI) vs legacy 2i      │
│    - Neo4j 5.x: Cypher 5 semantics and alignment with ISO GQL standard │
│    - MongoDB 7.0+: Enhanced compound wildcard indexing and $lookup     │
│    - DynamoDB: PartiQL subset limitations (no JOINs, no transactions)  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Graph Query Evolution: Cypher and ISO GQL

In 2024, the International Organization for Standardization published **ISO/IEC 39075:2024 (Database languages — GQL)**, the first new ISO standard database language since SQL in 1987.
- **Cypher (openCypher)** is the primary dialect used in this course via Neo4j 5.24.
- Neo4j 5 Cypher actively incorporates GQL-conforming features: pattern expressions, label expressions (`:Person&Employee`), and normalized result projections.
- In this repository, we teach **Cypher 5** as the primary concrete query language while explicitly highlighting its direct correspondence to ISO GQL keywords and graph pattern structures.

---

## 5. DynamoDB: Native Expressions vs PartiQL

Amazon DynamoDB supports two query paradigms:
1. **Native API / Key Condition Expressions:** Uses `KeyConditionExpression`, `FilterExpression`, and `ProjectionExpression`. This is the native, canonical, and highest-efficiency mechanism.
2. **PartiQL:** A SQL-compatible query language supported by DynamoDB since late 2020.
   - *Critical Rule:* DynamoDB executes PartiQL queries using the exact same underlying partition engine. Writing `SELECT * FROM Orders WHERE status = 'PENDING'` will execute a full table scan if `status` is not part of the primary key or a GSI!
   - In this course, we contrast native expressions with PartiQL side-by-side to expose the illusion of SQL syntax over non-relational storage engines.
