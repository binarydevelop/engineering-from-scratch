# Lesson 39.1: Cluster Failure and Resharding: Slot Migration

## Motto
"Online resharding moves slots key by key while the cluster continues serving traffic."

## Problem
Your business grows 5x. You need to add 3 new nodes to a running Redis Cluster without taking the application offline.

## Prediction
What happens during slot migration if a client requests a key that has not yet been migrated to the new node?

## Why this matters
Online elasticity (resharding without downtime) is the hallmark of modern distributed data infrastructure.

## First principles
During slot migration: 1. Target node is set to `IMPORTING`. 2. Source node is set to `MIGRATING`. 3. Keys are moved via `DUMP`/`RESTORE`. 4. If a client queries source, source returns `-ASK <slot> <target>` redirecting client to check target.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/cluster_reshard.py](../code/cluster_reshard.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/39-cluster-failure-and-resharding/experiments/run_experiment.sh
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
1. What happens if a primary node fails and its replica has also crashed? What does `cluster-require-full-coverage` control?
2. How do cluster nodes discover failures among themselves via the Gossip protocol?

## When to use this
* Perform cluster resharding during off-peak windows with rate-limited slot migrations.

## When not to use this
* Never forcefully kill nodes during an active incomplete slot migration.

## What comes next
Proceed to the next phase in the curriculum progression.
