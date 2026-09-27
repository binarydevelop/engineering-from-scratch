# Elasticsearch Mental Models and Architecture Diagrams

> **Core Axiom:** Elasticsearch is a distributed document-oriented search and analytics engine built around Lucene indexes, immutable segments, sharding, replication, and query coordination.

---

## 1. Relational B-Tree vs. Inverted Index

Why do standard relational databases struggle with arbitrary full-text queries?

### Relational B-Tree (Prefix & Range Optimized)
```text
B-Tree Key: "Distributed Systems in Practice"
┌─────────────────────────────────────────────────────────┐
│ Root Node: ["A..." to "M..."]  |  ["N..." to "Z..."]    │
└────────────┬────────────────────────────────────────────┘
             ▼
        Leaf Node: ["Distributed Systems in Practice"] ──► Row ID 42
```
* **Failure mode:** Querying `WHERE title LIKE '%Systems%'` cannot use the B-Tree index prefix. It forces a complete $O(N)$ sequential table scan across millions of disk blocks.

### Inverted Index (Term-Centric Lookup)
```text
Documents:
  Doc 1: "Distributed Systems in Practice"
  Doc 2: "Principles of Distributed Computing"
  Doc 3: "Database Systems"

                    INVERTED INDEX
Term Dictionary (Sorted)     Postings List (Doc IDs + Positions + Frequencies)
┌──────────────┐            ┌──────────────────────────────────────────────┐
│ computing    │ ──────────►│ [Doc 2 (pos: 3, freq: 1)]                    │
│ database     │ ──────────►│ [Doc 3 (pos: 0, freq: 1)]                    │
│ distributed  │ ──────────►│ [Doc 1 (pos: 0, freq: 1), Doc 2 (pos: 2)]    │
│ practice     │ ──────────►│ [Doc 1 (pos: 3, freq: 1)]                    │
│ principles   │ ──────────►│ [Doc 2 (pos: 0, freq: 1)]                    │
│ systems      │ ──────────►│ [Doc 1 (pos: 1, freq: 1), Doc 3 (pos: 1)]    │
└──────────────┘            └──────────────────────────────────────────────┘
```
* **Search efficiency:** Querying `"systems"` does a binary search or FST (Finite State Transducer) lookup on the sorted dictionary ($O(\log M)$ terms) and immediately retrieves `Doc 1` and `Doc 3`.

---

## 2. Text Analysis Pipeline

Every analyzed string passes through three sequential filters before becoming inverted index terms:

```text
Raw Text Input:
  "<p>The QUICK Brown Fox jumps over 12 lazy dogs! Visit https://elastic.co</p>"
                               │
                               ▼
 1. CHARACTER FILTERS (Operate on raw characters)
    - html_strip: removes `<p>` and `</p>`
    - mapping:    replaces "&" with "and"
                               │
                               ▼
    "The QUICK Brown Fox jumps over 12 lazy dogs! Visit https://elastic.co"
                               │
                               ▼
 2. TOKENIZER (Splits into discrete tokens and records offsets)
    - standard tokenizer: divides on word boundaries
                               │
                               ▼
    ["The", "QUICK", "Brown", "Fox", "jumps", "over", "12", "lazy", "dogs", "Visit", "https", "elastic.co"]
                               │
                               ▼
 3. TOKEN FILTERS (Transform, filter, or inject tokens)
    - lowercase:  "QUICK" -> "quick", "Fox" -> "fox"
    - stop:       removes ["the", "over"]
    - stemmer:    "jumps" -> "jump", "dogs" -> "dog"
                               │
                               ▼
 Final Index Terms:
    ["quick", "brown", "fox", "jump", "12", "lazi", "dog", "visit", "https", "elastic.co"]
```

---

## 3. Lucene Immutable Segments, Refresh, Flush, and Merge

Understanding how data moves from memory to disk explains the Near-Real-Time (NRT) nature and write performance of Elasticsearch.

```text
                     IN-MEMORY BUFFER                       OS FILESYSTEM CACHE                 PERSISTENT DISK (LUCENE)
               ┌──────────────────────────┐               ┌───────────────────────┐           ┌───────────────────────────┐
Write Doc ────►│ Indexing Buffer (RAM)    │               │                       │           │                           │
               │ Doc 1, Doc 2, Doc 3...   │               │                       │           │                           │
               └────────────┬─────────────┘               │                       │           │                           │
                            │                             │                       │           │                           │
                   REFRESH  │ (Every 1s by default)       │                       │           │                           │
                            ▼                             │                       │           │                           │
               ┌──────────────────────────┐               ▼                       │           │                           │
               │ Generates new searchable ├──────────────►│ Searchable Segment A  │           │                           │
               │ Lucene Segment in Cache  │               │ (Immutable in RAM)    │           │                           │
               └──────────────────────────┘               └───────────┬───────────┘           │                           │
                                                                      │                       │                           │
                                                               FLUSH  │ (fsync every 30m      │                           │
                                                                      │  or translog 512MB)   ▼                           │
                                                                      └──────────────────────►│ Segment A (Synced to Disk)│
                                                                                              │ Segment B (Synced to Disk)│
                                                                                              │ Segment C (Synced to Disk)│
                                                                                              └─────────────┬─────────────┘
                                                                                                            │
                                                                                                BACKGROUND  │ MERGE
                                                                                                            ▼
                                                                                              ┌───────────────────────────┐
                                                                                              │ Consolidated Segment AB   │
                                                                                              │ (Deleted docs purged)     │
                                                                                              └───────────────────────────┘
```

### Key Differences: Refresh vs. Flush
| Property | Refresh | Flush |
| :--- | :--- | :--- |
| **Target Destination** | OS Page Cache (Memory) | Physical Disk Storage (`fsync`) |
| **Result** | New segment is **Searchable** (NRT) | Data is **Durable** across crashes |
| **Default Frequency**| Every `1s` (`index.refresh_interval`)| Every 30 mins or Translog > 512MB |
| **I/O Cost** | Low (memory buffer copy) | High (physical disk I/O barrier) |

---

## 4. Inverted Index vs. Doc Values vs. `_source`

Why does Elasticsearch store the same document multiple times in different formats?

```text
Incoming Document:
{ "id": 1, "title": "Elasticsearch in Action", "price": 45, "tag": "tech" }

                    ┌──────────────────────────────────────────────────────────┐
                    │                      DOCUMENT CHANNELS                   │
                    └──────────────────────────────────────────────────────────┘
                                 │                      │                    │
          ┌──────────────────────┘                      │                    └──────────────────────┐
          ▼                                             ▼                                           ▼
1. INVERTED INDEX                             2. DOC VALUES                               3. _SOURCE STORE
(Row -> Column Inversion)                     (Columnar On-Disk Format)                   (Raw JSON Archive)
"action"        -> [Doc 1]                    Doc 1 -> price: 45                          Original JSON compressed
"elasticsearch" -> [Doc 1]                    Doc 1 -> tag: "tech"                        block for retrieving fields
                                                                                          on search hit response.
Use Case: Full-text Search                    Use Case: Sorts & Aggregations              Use Case: Display & Reindexing
```

---

## 5. Distributed Search: Two-Phase Query-Then-Fetch

How a multi-shard search executes without saturating the network:

```text
               CLIENT
                 │
                 │ 1. GET /products/_search?q=systems&size=10
                 ▼
          COORDINATING NODE
          ┌───────────────┐
          │ Parse Query   │
          └───────┬───────┘
                  │
        ┌─────────┴─────────┐  PHASE 1: QUERY PHASE (Scatter)
        │                   │  Sends query without doc bodies;
        ▼                   ▼  Requests only top 10 (DocID, BM25 Score)
     SHARD 0             SHARD 1
   ┌─────────┐         ┌─────────┐
   │ BM25    │         │ BM25    │
   │ Scoring │         │ Scoring │
   └────┬────┘         └────┬────┘
        │                   │
        └─────────┬─────────┘  Gathers top 10 candidates from each shard:
                  ▼            (Shard 0: 10 hits, Shard 1: 10 hits = 20 total)
          COORDINATING NODE
          ┌──────────────────────────────────────────────────┐
          │ Merge & Sort Top 20 hits to find overall Top 10  │
          └───────┬──────────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐  PHASE 2: FETCH PHASE (Gather)
        │                   │  Requests full `_source` only for the
        ▼                   ▼  winning 10 document IDs
     SHARD 0             SHARD 1
  (Fetch doc 4, 9)    (Fetch doc 1, 3)
        │                   │
        └─────────┬─────────┘
                  ▼
          COORDINATING NODE
          ┌──────────────────────────────────────┐
          │ Assemble JSON search hits response   │
          └───────┬──────────────────────────────┘
                  │
                  ▼
               CLIENT (Receives Top 10 documents)
```

---

## 6. JVM Memory vs. OS Page Cache Split

Why allocating 100% of machine RAM to Elasticsearch JVM heap destroys performance:

```text
TOTAL PHYSICAL HOST RAM (e.g. 64 GB)
┌───────────────────────────────────────┬───────────────────────────────────────┐
│        JVM HEAP MEMORY (Max 31 GB)    │         OS PAGE CACHE (33 GB)         │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ - Cluster State metadata              │ - Lucene Segments (.doc, .tim, .pos)  │
│ - Shard & Segment routing tables      │ - Columnar Doc Values (.dvd, .dvm)    │
│ - In-flight indexing buffers          │ - Term Dictionary FST index           │
│ - Query Cache & Aggregation state     │ - Fast memory-mapped disk I/O         │
└───────────────────────────────────────┴───────────────────────────────────────┘
```
> [!IMPORTANT]
> Lucene relies heavily on the **OS Page Cache** for ultra-fast memory-mapped inverted index reading. If you allocate all system RAM to the JVM heap, Lucene segment reads will trigger physical disk I/O, causing dramatic search latency spikes. Never set `-Xmx` greater than 50% of physical RAM or beyond 31 GB (to preserve Compressed Ordinary Object Pointers).
