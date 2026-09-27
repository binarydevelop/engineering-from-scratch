# Lesson 37.1: Flush and Durability

## Motto
"Refresh makes data searchable; Flush makes data durable by calling fsync and clearing the translog."

## Problem
If an operating system crashes or power fails, data residing only in the OS page cache is lost. How does Elasticsearch guarantee that acknowledged writes are not lost even if segments have not yet been written to physical disk?

## Prediction
What happens to the Translog (Transaction Log) when an explicit `_flush` is executed?

## Why this matters
Confusing **Refresh** with **Flush** is a fundamental architectural misunderstanding:
* **Refresh:** Memory Buffer $	o$ OS Page Cache (Searchable, but not durable).
* **Flush:** OS Page Cache $	o$ Physical Disk via `fsync`, and Translog is truncated (Durable).

## First principles
* **Translog (Transaction Log):** An append-only write-ahead log stored on disk. Every indexing write is appended here.
* **Flush Process:**
  1. Writes any memory buffer data to a new segment.
  2. Calls `fsync` on all Lucene segments in OS cache, persisting them physically to disk.
  3. Writes a Lucene Commit Point.
  4. Truncates the Translog (since all operations are now permanently on disk).
* Triggered automatically when translog reaches 512MB or every 30 minutes.

## Mental model
```text
           REFRESH                                     FLUSH
┌───────────────────────────┐               ┌───────────────────────────┐
│ Memory Buffer             │               │ OS Page Cache Segments    │
│            │              │               │            │              │
│            ▼              │               │            ▼ fsync()      │
│ OS Page Cache Segment     │               │ Physical Disk Storage     │
│ (Searchable! Not Durable!)│               │ + Truncate Translog       │
└───────────────────────────┘               └───────────────────────────┘
```

## Build it
See `code/flush_translog_sim.py` demonstrating write-ahead log lifecycle in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/37-flush-and-durability/experiments/run_experiment.sh
```

## Inspect it
Check translog stats before and after an explicit `_flush`:
```bash
curl -s http://localhost:9200/flush_demo/_stats/translog?pretty
curl -X POST http://localhost:9200/flush_demo/_flush
curl -s http://localhost:9200/flush_demo/_stats/translog?pretty
```
Notice `operations: 0` and `size_in_bytes: ~55b` after flush!

## Measure it
Measure disk I/O during a forced flush.

## Break it
Configure translog durability to `async` with a 60s interval and simulate an ungraceful container crash (`docker kill`).

## Recover it
Elasticsearch automatically replays the translog on node startup to reconstruct uncommitted segments.

## Modify it
Inspect `index.translog.flush_threshold_size` (default 512MB).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an Elasticsearch crash NOT cause data loss if a flush has not occurred for 10 minutes?
2. What is the physical role of the `fsync` system call?

## Guarantees
* Operations recorded in the translog will be fully recovered upon crash restart.

## Non-guarantees
* If `index.translog.durability: async` is configured, writes in the un-synced window can be lost on sudden power failure.

## When to use this
* Core understanding of storage engine crash resilience.

## When not to use this
* Do not call `_flush` manually on every write request (Elasticsearch manages flushes automatically).

## What comes next
In Phase 38, we examine Segment Merging: how Lucene consolidates small immutable segments.
