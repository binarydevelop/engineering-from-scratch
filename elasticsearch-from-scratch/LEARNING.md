# The Learning Methodology of `elasticsearch-from-scratch`

> **Motto:** Understand it. Build it. Index it. Search it. Measure it. Break it. Recover it. Scale it. Ship it.

Most engineers learn Elasticsearch backward: they read high-level REST API documentation, issue a few HTTP `POST` requests, treat it as "a MongoDB or Postgres table with a free-text search box", and then suffer catastrophic cluster outages in production when high-cardinality aggregations cause JVM Out-Of-Memory crashes, unmerged segments exhaust file handles, or oversharding grinds query coordination to a halt.

This repository exists to replace that superficial API memorization with deep, intuitive systems mastery.

---

## 1. The Core Learning Loop

Every phase in this curriculum demands active, experimental engagement. You will never merely read text and nod along. You will execute this iterative loop:

```text
       Read Problem & Motivation
                  │
                  ▼
         PREDICT The Outcome
      (Write down expected behavior)
                  │
                  ▼
         BUILD From Scratch
      (Pure Python simulation)
                  │
                  ▼
         INDEX Test Data
      (Push real documents to ES)
                  │
                  ▼
         SEARCH & Query
      (Execute queries & aggregations)
                  │
                  ▼
         INSPECT State
      (Segments, Mappings, Postings, Explain)
                  │
                  ▼
         MEASURE Metrics
      (Latency p95, Disk bytes, JVM heap)
                  │
                  ▼
         EXPLAIN Trade-offs
      (Write in your own words)
                  │
                  ▼
         MODIFY Parameters
      (Vary settings & measure shift)
                  │
                  ▼
         BREAK The System
      (Inject deliberate failures)
                  │
                  ▼
         RECOVER The Node/Cluster
      (Diagnose logs & heal state)
                  │
                  ▼
         REBUILD From Memory
      (Internalize the mental model)
```

---

## 2. The Nine Rules of Mastery

### Rule 1: Always Predict Before You Execute
Never hit `Enter` on a curl command or run a Python script without writing down your hypothesis.
* *Example:* "If I issue a `match` query for `running`, will it match a document containing `run`? Why or why not?"
* If your prediction was wrong, celebrate: you just identified a boundary where your mental model diverged from reality.

### Rule 2: Build the Primitive Before Calling the API
Before relying on Elasticsearch's `match_phrase` query, build a positional inverted index in 40 lines of Python. Before relying on BM25, write the term frequency saturation curve by hand. When you understand how the underlying data structure works, the Elasticsearch API becomes an obvious convenience, not a black box.

### Rule 3: Inspect Internal State, Not Just Query Responses
A query returning `{ "hits": { "total": 1 } }` tells you almost nothing about how the engine executed your request.
* Look at `_explain` to see the exact BM25 breakdown.
* Look at `_cat/segments` to see immutable Lucene segment files on disk.
* Look at `_cluster/allocation/explain` to see why a replica shard refused to assign.

### Rule 4: Measure Everything
"Elasticsearch is fast" is an unscientific statement.
Measure:
* Ingestion throughput in documents/second.
* Query latency at the 50th, 95th, and 99th percentiles.
* Segment count and file size before and after an explicit `_forcemerge`.
* JVM heap memory before and after loading high-cardinality terms into fielddata.

### Rule 5: Break It Intentionally
You do not truly understand a distributed database until you have broken it, watched it fail, read its cryptic error messages, and brought it back to life.
* Kill the primary shard holder while ingestion is active.
* Trigger a mapping explosion with 2,000 dynamically generated field names.
* Run an unindexed prefix regex query across 500,000 documents and observe coordinator CPU spike.

### Rule 6: Relevance Is a Science, Not Magic
Search relevance is not "good vibes." Relevance can be quantified, decomposed into mathematical components (Term Frequency, Inverse Document Frequency, Field-Length Normalization, Slop Distance), and tuned through systematic evaluation sets (Precision@K, Mean Reciprocal Rank).

### Rule 7: Never Proceed While Something Feels Magical
If a query produces a result and you cannot explain the step-by-step path that took the query string through the character filters, tokenizer, token filters, dictionary lookup, posting list intersection, and BM25 scoring accumulator, **stop**. Re-read the first principles, inspect the explain output, and trace it.

### Rule 8: Maintain Evidence Logs
Every lesson folder contains an `outputs/evidence-template.md`. When you complete an experiment, record your actual terminal output, latencies, and diagnostic reasoning. Your evidence folder is your personal engineering laboratory notebook.

### Rule 9: Rebuild From Memory
At the end of each major milestone (e.g., Phase 02 Inverted Index, Phase 15 BM25 Scorer, Phase 44 Distributed Scatter-Gather, Phase 80 Mini Search Engine), close the tutorial and write the implementation from scratch on a blank editor. If you can build it from scratch, you own the concept forever.
