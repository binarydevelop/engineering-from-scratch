# Lesson 51.1: Shard Allocation

## Motto
"The cluster allocator evaluates deciders: disk thresholds, node filters, shard limits, and replica anti-affinity."

## Problem
A replica shard remains persistently `UNASSIGNED`. Why did the master node refuse to place it? Guessing the cause leads to fruitless node restarts.

## Prediction
Can Elasticsearch tell you the exact algorithmic reason why a specific shard cannot be placed on any node in the cluster?

## Why this matters
The `_cluster/allocation/explain` API is the single most powerful diagnostic tool for fixing unassigned shards and cluster health issues.

## First principles
The Allocation Process & Deciders:
1. **`same_shard` decider:** Rejects allocating primary and replica of the same shard on the same physical node.
2. **`disk_threshold` decider:** Rejects allocation if node disk usage exceeds low watermark (85%).
3. **`shards_limit` decider:** Rejects if node already holds max shards per node.
4. **`awareness` decider:** Distributes shards across availability zones or racks.

## Mental model
```text
Allocator: "Can I put Replica Shard 0 on Node A?"
  ├── Decider 'same_shard': NO (Node A already has Primary Shard 0!)
Allocator: "Can I put Replica Shard 0 on Node B?"
  ├── Decider 'same_shard': YES
  ├── Decider 'disk_threshold': NO (Node B is at 89% disk usage!)
Result: Shard remains UNASSIGNED.
```

## Build it
See `code/allocation_decider_sim.py` simulating allocation rules in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/51-shard-allocation/experiments/run_experiment.sh
```

## Inspect it
Run `_cluster/allocation/explain` to diagnose why an unassigned shard cannot allocate:
```bash
curl -X POST http://localhost:9200/_cluster/allocation/explain?pretty -H "Content-Type: application/json" -d '{
  "index": "yellow_demo",
  "shard": 0,
  "primary": false
}'
```
Read the exact `decider` output in the JSON response!

## Measure it
Inspect shard movement events using `_cat/shards?v&s=state`.

## Break it
Set `cluster.routing.allocation.enable: "none"` and create an index. All shards remain stuck in unassigned state!

## Recover it
Reset allocation: `PUT /_cluster/settings {"transient": {"cluster.routing.allocation.enable": "all"}}`.

## Modify it
Configure allocation filtering to route indices to specific hardware tiers (e.g. `index.routing.allocation.include._tier: "data_hot"`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What does the `same_shard` allocation decider enforce?
2. How does `_cluster/allocation/explain` help on-call engineers resolve unassigned shards?

## Guarantees
* Shard allocation deciders prevent data loss and prevent overloading stressed nodes.

## Non-guarantees
* The allocator cannot place shards if hardware resources (disk/nodes) are physically insufficient.

## When to use this
* Investigating any yellow or red cluster status.

## When not to use this
* Routine operations when cluster health is green.

## What comes next
In Phase 52, we study Cluster State: the coordinated metadata of the cluster.
