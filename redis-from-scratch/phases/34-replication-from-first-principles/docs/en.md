# Lesson 34.1: Replication From First Principles: Asynchronous Streaming

## Motto
"Replication provides read scalability and data redundancy, but writes to the primary remain asynchronous."

## Problem
A single Redis server crashes due to a hardware failure. If all data lived only on that one machine, the application experiences total downtime.

## Prediction
When a client writes to the primary, does the primary wait for replicas to confirm receipt before returning '+OK' to the client?

## Why this matters
Replication is the foundation of high availability, failover, and geographical read scaling.

## First principles
Redis uses asynchronous primary-replica streaming. Writes are applied locally on the primary and queued to the replication backlog buffer to be streamed over TCP to replicas. Replicas are strictly read-only by default.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/replication_toy.py](../code/replication_toy.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/34-replication-from-first-principles/experiments/run_experiment.sh
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
1. How does the `WAIT` command allow clients to enforce semi-synchronous replication confirmation?
2. Why can a read from a replica return stale data?

## When to use this
* Use replicas to scale read-heavy traffic and provide hot-standby copies for disaster recovery.

## When not to use this
* Do not use standard Redis replication if your architecture requires strict linearizable ACID consensus.

## What comes next
Proceed to the next phase in the curriculum progression.
