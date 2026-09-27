# Lesson 50.1: Cluster Health

## Motto
"Green means all shards assigned; Yellow means data is safe but redundancy is compromised; Red means data is missing."

## Problem
On-call engineers often wake up to an alert: *"Cluster health is YELLOW"*. Panicking, they restart random nodes, accidentally turning a temporary yellow state into a catastrophic RED data outage.

## Prediction
Can user search queries still execute and return valid results when cluster health is YELLOW? What about when RED?

## Why this matters
Cluster health is the primary metric reported by Elasticsearch. Knowing exactly what each color guarantees prevents dangerous operational missteps.

## First principles
The Three Health States:
* **GREEN:** All primary shards AND all replica shards are allocated to active nodes. 100% capacity and full redundancy.
* **YELLOW:** All primary shards are active, but one or more replica shards are unassigned. **All data is 100% searchable and writable.** Redundancy is reduced: if the remaining node dies, data loss will occur.
* **RED:** At least one primary shard is unassigned and offline. **Data is missing.** Searches hitting that shard will fail or return partial hits!

## Mental model
```text
┌──────────┐
│  GREEN   │ ──► All Primaries Assigned + All Replicas Assigned. Full HA.
└──────────┘
┌──────────┐
│  YELLOW  │ ──► All Primaries Assigned. NO DATA LOST! (Missing some replicas).
└──────────┘
┌──────────┐
│   RED    │ ──► At least one Primary Shard OFFLINE! Data is currently missing!
└──────────┘
```

## Build it
See `code/cluster_health_state_machine.py` modeling health transitions in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/50-cluster-health/experiments/run_experiment.sh
```

## Inspect it
Check cluster health:
```bash
curl -s http://localhost:9200/_cluster/health?pretty
```

## Measure it
Inspect shard counts in `_cluster/health`:
* `active_primary_shards`
* `active_shards`
* `unassigned_shards`

## Break it
Intentionally turn the cluster YELLOW by setting `number_of_replicas: 1` in our single-node lab:
```bash
curl -X PUT http://localhost:9200/yellow_demo -H "Content-Type: application/json" -d '{"settings": {"number_of_replicas": 1}}'
curl -s http://localhost:9200/_cluster/health?pretty | grep "status"
```

## Recover it
Turn the cluster back to GREEN by setting replicas to 0:
```bash
curl -X PUT http://localhost:9200/yellow_demo/_settings -H "Content-Type: application/json" -d '{"index": {"number_of_replicas": 0}}'
curl -s http://localhost:9200/_cluster/health?pretty | grep "status"
```

## Modify it
Wait for a specific health status in automation scripts: `GET /_cluster/health?wait_for_status=green&timeout=30s`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an unassigned replica shard make cluster health YELLOW rather than RED?
2. If cluster health is RED, does Elasticsearch reject all search queries, or does it return partial hits?

## Guarantees
* YELLOW cluster health guarantees zero data loss and full query availability at the current moment.

## Non-guarantees
* YELLOW does not guarantee safety if another node fails.

## When to use this
* Every automated health check, deployment pipeline, and alerting monitor.

## When not to use this
* As the sole metric for performance (a green cluster can still suffer 5-second search latency).

## What comes next
In Phase 51, we investigate Shard Allocation and diagnostic deciders.
