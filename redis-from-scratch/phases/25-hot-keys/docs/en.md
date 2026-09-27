# Lesson 25.1: Hot Keys: Workload Skew & Thread Saturation

## Motto
"Adding more cluster nodes does not fix a hot key; a single key can only ever live on a single node."

## Problem
In a cluster of 50 Redis nodes, 90% of all application queries request the exact same key (`trending:world_cup`). Node 12 runs at 100% CPU while nodes 1-11 and 13-50 sit idle at 2% CPU.

## Prediction
What happens if a hot key receives 150,000 requests/sec on a single Redis thread?

## Why this matters
Hot keys are a leading cause of outages in distributed architectures, defeating horizontal sharding.

## First principles
Because Redis assigns each key to exactly one hash slot on one node, horizontal scaling cannot partition a single key. Mitigations include client-side in-memory caching and key replication (`key:shard_{1..N}`).

## Mental model
```text
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/hot_key_lab.py](../code/hot_key_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/25-hot-keys/experiments/run_experiment.sh
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
1. How does Redis 6.0+ Client-Side Caching (Tracking / RESP3) solve the hot key problem?
2. What tool can you run in production to detect hot keys (`redis-cli --hotkeys`)?

## When to use this
* Use client-side caching or key replication for read-heavy global configurations and top celebrity profiles.

## When not to use this
* Do not replicate hot keys that are frequently written to, as synchronization complexity escalates.

## What comes next
Proceed to the next phase in the curriculum progression.
