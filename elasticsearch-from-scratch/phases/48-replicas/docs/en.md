# Lesson 48.1: Replicas

## Motto
"A replica is an exact copy of a primary shard: it provides zero-downtime failover and scales read throughput."

## Problem
You have an index with 1 primary shard on Node A. Node A suffers a hardware failure and loses power. Your index is immediately 100% offline and all user searches fail with HTTP 503 errors.

## Prediction
If you configure `number_of_replicas: 1` on a 2-node cluster and Node A dies, can Node B continue serving search queries without data loss?

## Why this matters
Replicas provide High Availability (HA) and read scaling. Understanding the primary-replica lifecycle is crucial for distributed reliability.

## First principles
Two Fundamental Roles of Replicas:
1. **High Availability (Failover):** If the node holding the primary shard dies, Elasticsearch automatically promotes a replica shard to primary in milliseconds. Zero downtime, zero data loss.
2. **Read Scaling:** Replicas are fully functional, independent Lucene search indices. Search queries are load-balanced round-robin across primaries and replicas!

## Mental model
```text
Write Path:
  Client ──► Primary Shard (Node 1) ──► Replicates to Replica Shard (Node 2)

Read Path:
  Query 1 ──► Primary Shard (Node 1)
  Query 2 ──► Replica Shard (Node 2)  (Doubles Read Query Capacity!)
```

## Build it
See `code/replica_failover_sim.py` demonstrating primary promotion and read load balancing in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/48-replicas/experiments/run_experiment.sh
```

## Inspect it
Dynamically change replica count on a live index:
```bash
curl -X PUT http://localhost:9200/sharded_index/_settings -H "Content-Type: application/json" -d '{
  "index": { "number_of_replicas": 1 }
}'
```

## Measure it
Inspect shard allocation with `_cat/shards`: primary (`p`) vs replica (`r`).

## Break it
Set `number_of_replicas: 1` on a single-node cluster: observe cluster status turns **YELLOW** because Elasticsearch refuses to place a replica on the same physical node as the primary!

## Recover it
Either start a second node (via `make cluster-up`) or set `number_of_replicas: 0`.

## Modify it
Benchmark read query QPS with 0 replicas vs 2 replicas on a multi-node cluster.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch refuse to allocate a replica shard on the same physical node as its primary shard?
2. How do replicas double read throughput without doubling write throughput?

## Guarantees
* Replicas provide transparent failover if a primary shard node fails.

## Non-guarantees
* Replicas do NOT protect against user error (e.g. `DELETE /index` deletes primaries and replicas simultaneously!). Replicas != Backups!

## When to use this
* Every production index (minimum `number_of_replicas: 1`).

## When not to use this
* Temporary local development or initial bulk migrations where write speed is priority and replicas will be enabled later.

## What comes next
In Phase 49, we perform live Node Failure and observe automatic failover.
