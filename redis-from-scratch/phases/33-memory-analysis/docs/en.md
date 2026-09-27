# Lesson 33.1: Memory Analysis: Fragmentation, RSS, and jemalloc

## Motto
"Storing 100 bytes of data in Redis does not mean Redis consumes 100 bytes of physical RAM."

## Problem
An engineer calculates that 10,000,000 keys of 20 bytes each should take 200MB. When loaded, Redis consumes over 1.2GB of RAM and crashes with OOM!

## Prediction
What overhead does each key in Redis carry before including the actual string bytes?

## Why this matters
Memory is the primary financial and operational constraint of Redis. Understanding memory layout prevents costly sizing errors.

## First principles
Every key requires a `dictEntry` (24-32 bytes), an SDS header for the key, a `robj` header (16 bytes), an SDS header for the value, plus memory allocator (jemalloc) bucket alignment padding.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/memory_audit.py](../code/memory_audit.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/33-memory-analysis/experiments/run_experiment.sh
```

## Inspect it
Inspect server status, telemetry counters, and internal diagnostic logs.

## Measure it
Quantify latency percentiles, throughput, memory allocation, and failure impact.

## Break it
Inject network partitions, process terminations, or invalid commands.

## Debug it
Diagnose the failure using evidence from diagnostic tools.

## Modify it
Tune configuration thresholds and measure behavioral changes.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What causes a high `mem_fragmentation_ratio` (> 1.5) and how does `activedefrag` solve it?
2. Why does storing fields inside a Hash consume significantly less memory per item than storing individual standalone keys?

## When to use this
* Use `MEMORY USAGE <key>` and `MEMORY STATS` to audit data schemas before loading billions of records.

## When not to use this
* Do not store millions of 1-byte standalone keys; group them into hashes or packed buffers.

## What comes next
Proceed to the next phase in the curriculum progression.
