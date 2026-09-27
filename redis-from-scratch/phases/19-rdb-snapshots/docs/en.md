# Lesson 19.1: RDB Snapshots: Point-in-Time Backups & Copy-on-Write

## Motto
"BGSAVE does not pause Redis; Linux fork() duplicates the process memory space virtually in microseconds using Copy-on-Write."

## Problem
Serializing a 20GB database to disk takes seconds or minutes. How does Redis continue serving 100,000 requests/sec during the snapshot without blocking or saving half-written state?

## Prediction
If a child process is writing `dump.rdb` and a client modifies 100,000 keys, what happens to memory usage on the host?

## Why this matters
RDB snapshots provide compact disaster-recovery backups that boot 10x faster than replaying huge logs, but fork() memory amplification can trigger OS OOM kills if unmonitored.

## First principles
Redis calls `fork()` to spawn a child process. The Linux kernel uses Copy-on-Write (COW): memory pages are shared between parent and child until written to. Only modified memory pages are copied.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/rdb_snapshots.py](../code/rdb_snapshots.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/19-rdb-snapshots/experiments/run_experiment.sh
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
1. Why is Linux `vm.overcommit_memory = 1` required when running Redis with background snapshots?
2. What data is lost if Redis crashes 14 minutes after a snapshot on a server configured with `save 900 1`?

## When to use this
* Use RDB for disaster recovery backups, remote cold storage (S3), and initial replica synchronization.

## When not to use this
* Do not rely solely on RDB if your business SLA cannot tolerate losing minutes of recent writes.

## What comes next
Proceed to the next phase in the curriculum progression.
