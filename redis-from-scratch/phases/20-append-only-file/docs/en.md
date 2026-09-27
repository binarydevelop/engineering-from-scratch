# Lesson 20.1: Append-Only File: Write-Ahead Logging & fsync Tradeoffs

## Motto
"The Append-Only File turns every mutation into a permanent audit trail written before acknowledgment."

## Problem
RDB snapshots have a durability window of minutes. If a server loses power between snapshots, all writes in that window vanish.

## Prediction
What is the maximum amount of data lost during a power outage if `appendfsync` is set to `everysec`?

## Why this matters
AOF is the primary persistence mechanism that makes Redis viable as an authoritative transactional store.

## First principles
Every state-modifying command is logged to disk in standard RESP format. Redis supports three fsync policies: `always` (maximum durability, lowest throughput), `everysec` (1-second data loss window, excellent throughput), and `no` (delegated to OS kernel flush).

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/aof_fsync.py](../code/aof_fsync.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/20-append-only-file/experiments/run_experiment.sh
```

## Inspect it
Inspect command return codes, internal data structures, and memory.

## Measure it
Quantify latency, concurrency race conditions, and throughput.

## Break it
Inject network delays, TTL expirations, or ungraceful client terminations.

## Debug it
Diagnose the failure using logs and atomic status returns.

## Modify it
Tune timeouts, concurrency levels, or batch sizes and observe shifts.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `appendfsync always` drop Redis throughput from 100,000 ops/sec to ~2,000 ops/sec?
2. What does the `redis-check-aof --fix` CLI utility do when an AOF file ends with a corrupted half-written command?

## When to use this
* Use AOF with `everysec` as the default persistence policy for production systems needing high durability.

## When not to use this
* Do not set `appendfsync always` unless your hardware uses enterprise battery-backed NVRAM or PCIe SSDs designed for write barriers.

## What comes next
Proceed to the next phase in the curriculum progression.
