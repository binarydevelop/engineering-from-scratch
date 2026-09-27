# Lesson 36.1: Redis Sentinel: Quorum, Health Checks, and Failover

## Motto
"Sentinel is the supervisor that watches the primary, agrees on death via quorum, and automatically promotes a replica."

## Problem
When a primary server crashes at 3 AM, a human operator cannot manually log in, reconfigure replicas with `REPLICAOF NO ONE`, and update application DNS without hours of downtime.

## Prediction
Why does a robust Sentinel deployment require at least 3 Sentinel nodes rather than 2?

## Why this matters
Redis Sentinel provides automated High Availability (HA) for standalone primary-replica setups.

## First principles
Sentinels run as independent processes monitoring Redis nodes. When a primary misses heartbeats (`PING`), a Sentinel flags it `sdown` (subjectively down). When a quorum of Sentinels agree, it becomes `odown` (objectively down). Sentinels elect a leader via Raft-like consensus to execute failover.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/sentinel_lab.py](../code/sentinel_lab.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/36-sentinel/experiments/run_experiment.sh
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
1. What is split-brain and how does `min-replicas-to-write` help mitigate it?
2. Why must client applications connect to Sentinel instances rather than hardcoding the primary IP address?

## When to use this
* Use Sentinel for automated failover on single-primary systems where dataset fits on one machine.

## When not to use this
* Do not use Sentinel if you need horizontal write partitioning across multiple shards (use Redis Cluster).

## What comes next
Proceed to the next phase in the curriculum progression.
