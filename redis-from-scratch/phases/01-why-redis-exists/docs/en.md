# Lesson 01.1: Why Redis Exists: Storage Hierarchy & Latency

## Motto
"RAM is fast not because it is magic, but because electrical capacitors have no mechanical or block-paging overhead."

## Problem
Relational databases write transactions to disk (WAL) for durability. When an application serves 50,000 requests/sec, disk seeks and OS page cache transitions become the primary throughput bottleneck.

## Prediction
How many times faster is reading an in-memory dictionary compared to querying an indexed SQLite or PostgreSQL table on disk over 10,000 iterations?

## Why this matters
Latency numbers every engineer should know: CPU L1 cache (~1 ns), RAM (~100 ns), NVMe SSD (~10-50 µs), Network within DC (~0.5 ms). Redis moves the data layer from SSD/disk speeds to RAM speeds.

## First principles
Physical storage latency hierarchy dictates database performance. Accessing dynamic RAM avoids kernel system calls, filesystem block allocation, and disk write barriers.

## Mental model
```text
CLIENT                     REDIS EVENT LOOP (ae.c)             MEMORY (dict.c)
  │                                   │                               │
  ├─ TCP Socket write() ─────────────►│                               │
  │                                   ├─ epoll/kqueue event fired     │
  │                                   ├─ readQueryFromClient()        │
  │                                   ├─ parse RESP command           │
  │                                   ├─ lookup & call() ────────────►├─ dictEntry insert
  │                                   ├─ addReply() buffer            │
  │◄─ TCP Socket read() ──────────────┤                               │
```

## Build it
See [code/measure_storage.py](../code/measure_storage.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/01-why-redis-exists/experiments/run_experiment.sh
```

## Inspect it
```bash
redis-cli INFO
```

## Measure it
Run quantitative benchmark and inspect execution latency.

## Break it
Stop the background Redis daemon or inject an invalid payload.

## Debug it
Observe error logs and connection socket diagnostic codes.

## Modify it
Adjust payload size or connection parameters and record shifts.

## Evidence
Record your findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. If RAM is ~1,000x faster than disk, why are all databases not in-memory?
2. What role does OS page caching play in closing the gap between disk and memory?

## When to use this
* Use Redis when sub-millisecond read/write latency is required for high-throughput hot data.

## When not to use this
* Do not use Redis for multi-terabyte cold datasets where RAM cost exceeds hardware budget.

## What comes next
Proceed to the next phase to build upon these systems primitives.
