# Lesson 63.1: Heap and Memory

## Motto
"Never give all RAM to JVM heap: 50% belongs to heap (max 31GB), 50% belongs to OS page cache for Lucene."

## Problem
An administrator deploys an Elasticsearch node on a 64 GB RAM server and sets `-Xmx62g`, assuming more heap equals more performance. Within hours, search queries take 15 seconds and disk I/O thrashes!

## Prediction
Why does giving 62 GB of a 64 GB machine to JVM heap destroy search performance?

## Why this matters
Lucene is NOT a Java program that keeps everything in objects. Lucene relies on the **Operating System Page Cache** to memory-map immutable segment files.

## First principles
The Golden Memory Rule:
* **Max 50% to JVM Heap:** Leave at least 50% of physical RAM free for the OS page cache!
* **Max 31 GB Heap:** Never exceed ~31 GB (the threshold where JVM Compressed OOPs or Ordinary Object Pointers are disabled). Crossing 32 GB switches from 32-bit compressed pointers to 64-bit pointers, wasting gigabytes of RAM on pointer padding!

## Mental model
```text
64 GB RAM Machine:
┌───────────────────────────────────────┬───────────────────────────────────────┐
│ JVM Heap: 30 GB (-Xms30g -Xmx30g)     │ OS Page Cache: 34 GB                  │
├───────────────────────────────────────┼───────────────────────────────────────┤
│ - Cluster State                       │ - Lucene Segments (.doc, .tim)        │
│ - Index Buffers                       │ - Doc Values (.dvd) for sorting & aggs│
│ - Short-lived query aggregations      │ - Ultra-fast memory-mapped disk I/O   │
└───────────────────────────────────────┴───────────────────────────────────────┘
```

## Build it
See `code/compressed_oops_calc.py` calculating pointer overhead above 32GB in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/63-heap-and-memory/experiments/run_experiment.sh
```

## Inspect it
Check JVM heap usage and compressed pointers on your node:
```bash
curl -s "http://localhost:9200/_nodes/stats/jvm?pretty" | grep -A 10 "mem"
```

## Measure it
Inspect heap percent and garbage collector activity via `_cat/nodes?v&h=name,heap.percent,ram.percent`.

## Break it
Simulate high heap pressure by setting `-Xms128m -Xmx128m` and running an expensive query. Observe rapid GC pauses.

## Recover it
Configure balanced memory settings: `-Xms512m -Xmx512m` for lab, up to 30GB for production.

## Modify it
Inspect GC logs for Stop-The-World pause durations.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does allocating 33 GB of heap give you LESS usable memory than allocating 31 GB?
2. What role does the OS page cache play in Lucene search execution?

## Guarantees
* Compressed OOPs keep 64-bit JVM object references 32-bits wide below ~31 GB.

## Non-guarantees
* Having 31 GB of heap does not prevent OOM if unbounded queries load gigabytes into memory.

## When to use this
* Every node sizing and production deployment configuration.

## When not to use this
* Never violate the 50% RAM rule or 31GB heap ceiling.

## What comes next
In Phase 64, we investigate Disk Storage and Allocation Watermarks.
