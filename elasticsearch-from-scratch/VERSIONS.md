# Elasticsearch Version Discipline and Reference Specifications

> **Motto:** Understand it. Build it. Index it. Search it. Measure it. Break it. Recover it. Scale it. Ship it.

This repository enforces strict version discipline. Systems programming and distributed systems education fails when instructors mix observable abstractions with outdated internal implementation details or vague generic descriptions.

---

## 1. Pinned Reference Release

| Component | Pinned Version | Docker Tag / Source Baseline | Notes |
| :--- | :--- | :--- | :--- |
| **Elasticsearch Server** | **8.17.0** | `docker.elastic.co/elasticsearch/elasticsearch:8.17.0` | Official Elastic container baseline |
| **Apache Lucene (Underlying Engine)** | **9.12.0** | Bundled inside ES 8.17.0 | Core inverted index & segment library |
| **Python Client** | **8.17.0+** (`elasticsearch>=8.17.0,<9.0.0`) | Official `elasticsearch` PyPI package | Modern typing and connection pooling |
| **Python Runtime** | **3.11+ / 3.12+ / 3.14** | `python3` | Native standard library + requests + pytest |
| **Docker Compose** | **v2.x+ / v5.x** | Compose specification | Single-node & 3-node multi-cluster labs |

---

## 2. Public Elasticsearch Abstractions vs. Lucene Core Internals

A central tenet of this curriculum is distinguishing **what the Elasticsearch client observes via HTTP REST APIs** from **how Apache Lucene implements data storage on disk**:

```text
+--------------------------------------------------------------------------+
|                        Elasticsearch Layer                               |
| - Distributed Cluster Coordination & State                               |
| - REST HTTP API (_search, _bulk, _cat, _cluster, _nodes)                 |
| - Index Sharding & Replication (Primary / Replica Routing)               |
| - Analysis Pipeline (Char Filters -> Tokenizer -> Token Filters)         |
| - Distributed Aggregations & Query Coordination                          |
+--------------------------------------------------------------------------+
                                     │
                                     ▼
+--------------------------------------------------------------------------+
|                         Apache Lucene Layer                              |
| - Shard == Independent Lucene Index directory                            |
| - Segments (Immutable inverted index files: .tim, .tip, .doc, .pos)      |
| - Columnar Doc Values (.dvd, .dvm) for sorting & aggregations            |
| - BKD Trees / Dimensional Points (.dii, .dim) for numeric/date/geo       |
| - Block Max WAND / BM25 Scoring Engine                                   |
+--------------------------------------------------------------------------+
```

### A. Document Types (`_type` removal)
* **Historical (< 7.0):** Indices could contain multiple mapping types (e.g. `twitter/tweet`, `twitter/user`), mimicking database tables.
* **Modern (7.x & 8.x):** Mapping types were completely removed. An Elasticsearch index contains a single uniform mapping schema. All operations operate directly on endpoints like `POST /<index>/_doc/<id>`.
* **Observable CLI:** Any query specifying `_type` or defining multiple types in mappings will be rejected with an `illegal_argument_exception`.

### B. Security Defaults (ES 8.x)
* In Elasticsearch 8.x, **X-Pack Security is enabled by default** when run without explicit configuration, requiring auto-generated TLS certificates and an `elastic` superuser password.
* In our local learning lab environments (`docker-compose.yml` and `docker-compose.cluster.yml`), security is explicitly set to `xpack.security.enabled=false` during early architectural phases (Phases 00–75) so learners focus on networking, distributed sharding, segments, and queries without TLS friction.
* **Phase 76 ("Elasticsearch Security Basics")** explicitly boots a secure cluster with mutual TLS, user roles, API keys, and RBAC to demonstrate production hardening.

### C. Default BM25 Relevance Scoring
* Since Elasticsearch 5.x and continuing in 8.17.0, **BM25 (Best Matching 25)** is the default similarity algorithm, replacing classic Lucene TF-IDF.
* Default parameters in 8.17.0:
  * $k_1 = 1.2$ (controls term frequency saturation limit)
  * $b = 0.75$ (controls field length normalization degree)

### D. Text vs. Keyword & Aggregation Data Structures
* `text` fields are analyzed, tokenized, and indexed into inverted indexes. By default, `fielddata` is **disabled** on `text` fields because loading unbounded analyzed terms into the JVM heap causes out-of-memory crashes.
* `keyword` fields are stored verbatim (untokenized) and automatically indexed into **Doc Values** (disk-based columnar storage) for fast aggregations and sorting.

### E. Vector & Lexical Hybrid Search (ES 8.x)
* Elasticsearch 8.x supports dense vector indexing via HNSW (`dense_vector` field type with cosine, dot-product, or euclidean similarity) and native hybrid search combining BM25 lexical scores with $k$-NN scores using Reciprocal Rank Fusion (RRF).

---

## 3. Verification Commands

Run these commands to verify your local runtime matches the course expectations:

```bash
# Verify Docker version
docker --version
docker compose version

# Verify Python version
python3 --version

# Verify Elasticsearch Cluster version via REST
curl -s http://localhost:9200/ | grep "number"
# Expected output sample:
# "number" : "8.17.0"
# "lucene_version" : "9.12.0"
```
