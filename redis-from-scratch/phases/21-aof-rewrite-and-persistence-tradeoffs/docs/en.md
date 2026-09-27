# Lesson 21.1: AOF Rewrite & Compaction: Log Compaction Mechanics

## Motto
"If a counter is incremented 1,000,000 times, AOF rewrite replaces 1,000,000 log lines with a single SET command."

## Problem
An append-only log grows indefinitely. Over months, a 50MB dataset could generate a 100GB AOF log file, filling disks and taking hours to replay on startup.

## Prediction
Does `BGREWRITEAOF` read the existing historical AOF log file on disk to compact it?

## Why this matters
AOF rewrite keeps log storage bounded and predictable, enabling rapid server reboots.

## First principles
`BGREWRITEAOF` does NOT read the old file. It forks a child process that scans the live dataset in RAM, writing the minimal sequence of commands necessary to recreate the current dataset directly into a new temporary file.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/aof_rewrite.py](../code/aof_rewrite.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/21-aof-rewrite-and-persistence-tradeoffs/experiments/run_experiment.sh
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
1. How does Redis handle new client writes that occur while the child process is actively rewriting the AOF?
2. What are the advantages of combining RDB snapshots and AOF into a hybrid persistence file (Redis 5.0+)?

## When to use this
* Configure automated AOF rewriting (`auto-aof-rewrite-percentage 100`) to keep log sizes bounded.

## When not to use this
* Do not trigger manual AOF rewrites during peak traffic spikes, as `fork()` introduces latency.

## What comes next
Proceed to the next phase in the curriculum progression.
