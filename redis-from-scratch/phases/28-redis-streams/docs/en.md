# Lesson 28.1: Redis Streams: Consumer Groups, PEL, and Crash Recovery

## Motto
"Redis Streams provide Kafka-like log semantics directly inside Redis, with persistent offsets and crash recovery."

## Problem
A worker pulls a task from a queue and begins executing it. 100ms later, the worker's power cord is unplugged. How do you recover the unacknowledged job without losing it?

## Prediction
What command inspects tasks that have been assigned to workers but have not yet been acknowledged with XACK?

## Why this matters
Redis Streams combine durability, multi-consumer partitioning, and failure recovery into a single high-performance engine.

## First principles
Streams are append-only logs indexed by `<timestamp>-<sequence>`. Consumer Groups partition streams across workers. Unacknowledged messages reside in the Pending Entries List (PEL). If a worker crashes, supervisor workers claim them via `XCLAIM`.

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/streams_lab.py](../code/streams_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/28-redis-streams/experiments/run_experiment.sh
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
1. What does `>` mean as the ID parameter in `XREADGROUP`?
2. How does `XCLAIM` allow a healthy worker to steal an abandoned job from a crashed worker?

## When to use this
* Use Redis Streams for mission-critical background jobs, audit trails, and multi-consumer event processing.

## When not to use this
* Do not use Redis Streams if message retention must span years across petabytes (use Apache Kafka or AWS Kinesis).

## What comes next
Proceed to the next phase in the curriculum progression.
