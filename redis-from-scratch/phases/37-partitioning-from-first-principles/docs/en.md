# Lesson 37.1: Partitioning From First Principles: Modulo vs. Hash Slots

## Motto
"Naive modulo hashing creates a nightmare: adding one node forces 80% of all keys to relocate."

## Problem
A dataset exceeds the RAM capacity of a single physical server (e.g. 500GB dataset on 64GB machines). We must partition keys across multiple nodes.

## Prediction
In a 4-node cluster using naive `hash(key) % 4`, what fraction of keys must move when node 5 is added?

## Why this matters
Understanding hash slot mechanics is essential for reasoning about Redis Cluster, DynamoDB, and distributed systems partitioning.

## First principles
Naive modulo partitioning reshuffles almost all keys on node membership changes. Redis Cluster solves this by introducing **16,384 virtual Hash Slots**. Nodes own ranges of slots, so scaling only requires moving specific slots without recalculating key hashes.

## Mental model
```text
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/partitioning_modulo.py](../code/partitioning_modulo.py).

## Use Redis
Execute the lesson experiment:
```bash
./phases/37-partitioning-from-first-principles/experiments/run_experiment.sh
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
1. Why did Redis Cluster choose exactly 16,384 ($2^{14}$) hash slots instead of 65,536?
2. How does consistent hashing differ from fixed hash slot assignment?

## When to use this
* Partition data when dataset size or write throughput exceeds the hardware limits of a single node.

## When not to use this
* Avoid partitioning if your queries rely heavily on multi-key cross-slot transactions.

## What comes next
Proceed to the next phase in the curriculum progression.
