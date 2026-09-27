# Lesson 38.1: Redis Cluster: 16,384 Hash Slots & -MOVED Redirects

## Motto
"Redis Cluster nodes do not proxy requests; they return -MOVED redirects and force smart clients to route packets directly."

## Problem
How does a client find which of 100 cluster nodes owns the key `user:994` without querying a centralized coordinator?

## Prediction
What happens if a client issues `MGET key_a key_b` when `key_a` and `key_b` hash to different slots on different nodes?

## Why this matters
Redis Cluster enables multi-terabyte horizontal scaling while maintaining sub-millisecond execution.

## First principles
Every key is mapped via `CRC16(key) mod 16384`. If a client sends a command to the wrong node, the node replies with `-MOVED <slot> <ip>:<port>`. Smart clients cache this slot map. Hash tags (`{user:123}:profile`, `{user:123}:orders`) force keys to the same slot for atomic multi-key operations.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/cluster_slots.py](../code/cluster_slots.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/38-redis-cluster/experiments/run_experiment.sh
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
1. What is the difference between a `-MOVED` redirection and an `-ASK` redirection?
2. Why does executing `KEYS *` on a Redis Cluster node only return keys from slots owned by that specific node?

## When to use this
* Use Redis Cluster for massive horizontal write scaling and datasets larger than single-machine RAM.

## When not to use this
* Do not use Redis Cluster if your application depends extensively on multi-key operations across arbitrary un-tagged keys.

## What comes next
Proceed to the next phase in the curriculum progression.
