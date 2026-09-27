# Lesson 79.1: Failure Scenarios

## Motto
"Chaos engineering for search: predict, break, observe, diagnose, recover, and explain 7 real distributed failures."

## Problem
Engineers who have only experienced healthy green clusters freeze when production incidents occur. Mastery requires having broken and recovered every distributed component in a safe lab environment.

## Prediction
What happens to active indexing and queries when you kill a node, fill a write queue, or inject a disk watermark block?

## Why this matters
This phase runs through the 7 canonical failure modes of distributed search clusters:
1. Primary Shard Node Crash
2. Unassigned Replica Shard
3. Write Queue Overflow (HTTP 429)
4. Disk Flood Stage Lock (Read-Only)
5. Mapping Explosion Rejection
6. High-Cardinality Heap Saturation
7. Split-Brain Prevention / Master Failover

## First principles
The Failure-Recovery Loop:
$$	ext{Predict} \longrightarrow 	ext{Break} \longrightarrow 	ext{Observe} \longrightarrow 	ext{Diagnose} \longrightarrow 	ext{Recover} \longrightarrow 	ext{Explain}$$

## Mental model
```text
           THE 7 CONTROLLED FAILURE DRILLS
┌──────────────────────────────────────────────────────────────┐
│ 1. Node Loss        ──► Inspect promotion & recovery         │
│ 2. Unassigned Shard ──► Diagnose with allocation explain     │
│ 3. HTTP 429 Reject  ──► Observe backoff & write queue        │
│ 4. Read-Only Block  ──► Clear flood-stage lock               │
│ 5. Mapping Limit    ──► Fix schema design                    │
│ 6. Slow Wildcard    ──► Audit slow logs                      │
│ 7. Hot Shard Skew   ──► Rebalance routing partition          │
└──────────────────────────────────────────────────────────────┘
```

## Build it
See `code/chaos_runner.py` automating failure injections in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/79-failure-scenarios/experiments/run_experiment.sh
```

## Inspect it
Observe error logs and recovery steps for each simulated failure mode.

## Measure it
Measure Mean Time To Recovery (MTTR) for each scenario.

## Break it
Run the complete automated failure suite.

## Recover it
Follow the diagnostic procedures in `docs/troubleshooting.md`.

## Modify it
Add network packet latency simulation between data nodes.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How does practicing failure injection prevent panic during real production outages?
2. Which failure mode is easiest to prevent with upfront schema design? (Mapping explosion).

## Guarantees
* Controlled failure drills build operational muscle memory.

## Non-guarantees
* Lab failure simulations do not encompass every bizarre hardware failure mode.

## When to use this
* Operational onboarding, disaster readiness testing, and game days.

## When not to use this
* Production environments during business hours.

## What comes next
In Phase 80, we construct Capstone 3: Building a Mini Search Engine from Scratch.
