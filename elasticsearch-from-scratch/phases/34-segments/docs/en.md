# Lesson 34.1: Segments

## Motto
"A Lucene index is not a single file; it is a collection of immutable segments searched in parallel."

## Problem
In a mutable database, inserting or updating a record requires locking rows or disk pages to avoid concurrent write corruption. If search engines locked the inverted index during every insert, concurrent query throughput would collapse.

## Prediction
Why does Apache Lucene make segment files strictly immutable once written to disk?

## Why this matters
Segment immutability is the foundational design choice of Lucene and Elasticsearch. It unlocks lock-free concurrent reads, operating system page cache caching, and sequential write performance.

## First principles
* **Shard = Directory of Lucene Segments:** An index shard is composed of multiple independent segments.
* **Immutability:** Once a segment file (`_0.doc`, `_0.tim`) is written, it is never modified.
* **Search Across All Segments:** A query searches each segment in parallel and aggregates the results.
* **Deletions:** A delete writes the document ID to a separate `.del` bitset file. The original segment remains untouched!

## Mental model
```text
Shard 0 (Lucene Index Directory)
 ├── Segment _0 (100k docs) ──► Immutable (.doc, .tim, .dvd)
 ├── Segment _1 (50k docs)  ──► Immutable (.doc, .tim, .dvd)
 ├── Segment _2 (10k docs)  ──► Immutable (.doc, .tim, .dvd)
 └── _0.del (Bitset of deleted docs in Segment _0)

Query Execution: Searches _0, _1, and _2 concurrently; filters out deleted IDs from .del
```

## Build it
See `code/segment_engine_sim.py` implementing multi-segment indexing and search in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/34-segments/experiments/run_experiment.sh
```

## Inspect it
List all immutable segments for an index:
```bash
curl -s "http://localhost:9200/_cat/segments/products_phase06?v&h=index,shard,segment,generation,docs.count,docs.deleted,size"
```

## Measure it
Inspect the number of segments, active document count, and deleted document count.

## Break it
Notice that deleting a document increases segment disk usage slightly (due to appending to the `.del` file) rather than reducing it immediately.

## Recover it
Disk space is reclaimed during Segment Merging (Phase 38).

## Modify it
Index documents in separate batches with forced refreshes and count newly created segments.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does segment immutability eliminate the need for read locking in Lucene?
2. What are the negative consequences of accumulating too many tiny segments in a shard?

## Guarantees
* Search operations never experience lock contention against concurrent writes.

## Non-guarantees
* Deleting a document does not physically reclaim disk space immediately.

## When to use this
* Understanding all search, indexing, refresh, and merge behaviors.

## When not to use this
* Do not attempt to edit Lucene segment files directly in the filesystem.

## What comes next
In Phase 35, we examine why Elasticsearch is Near-Real-Time (NRT) rather than immediately searchable.
