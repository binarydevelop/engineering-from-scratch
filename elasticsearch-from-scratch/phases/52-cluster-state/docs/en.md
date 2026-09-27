# Lesson 52.1: Cluster State

## Motto
"Cluster state is the single source of truth: master consensus distributes mappings, indices, and shard routing tables."

## Problem
In a 20-node cluster, how does every node know which shard lives on which IP address, what data types exist in mappings, and which indices are open? If nodes have conflicting metadata, writes and searches go to the wrong servers.

## Prediction
What happens to cluster stability if cluster state metadata grows from 2 MB to 200 MB?

## Why this matters
Cluster State is coordinated by the elected **Master Node**. Understanding its size and broadcast frequency explains why mapping explosions and oversharding destabilize clusters.

## First principles
Cluster State Contents:
* Active cluster nodes list
* Indices metadata (settings, mappings)
* Shard routing tables (which shard is on which node)
* Index templates and ILM policies
Every time an index is created, mapping updated, or shard relocated, the Master updates the cluster state and broadcasts a diff to all nodes.

## Mental model
```text
ELECTED MASTER NODE
┌────────────────────────────────────────────────────────┐
│ Cluster State (Metadata, Routing Tables, Mappings)     │
└───────────────────────────┬────────────────────────────┘
                            │ Broadcast Diffs via Transport TCP (:9300)
             ┌──────────────┴──────────────┐
             ▼                             ▼
      DATA NODE 1                    DATA NODE 2
  (Keeps local copy)             (Keeps local copy)
```

## Build it
See `code/cluster_state_sim.py` simulating metadata broadcast in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/52-cluster-state/experiments/run_experiment.sh
```

## Inspect it
Inspect cluster state summary (exclude huge mappings to keep output readable):
```bash
curl -s "http://localhost:9200/_cluster/state/version,master_node,nodes?pretty"
```

## Measure it
Inspect the cluster state size and version number:
```bash
curl -s "http://localhost:9200/_cluster/stats?pretty" | grep -A 5 "cluster_state"
```

## Break it
Generate hundreds of indices with thousands of dynamic fields rapidly. Observe master node CPU spike as it attempts to serialize and broadcast huge metadata updates.

## Recover it
Limit dynamic mapping and consolidate indices.

## Modify it
Inspect master node tasks: `curl -s http://localhost:9200/_cluster/pending_tasks?pretty`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does every node in an Elasticsearch cluster maintain a copy of the cluster state?
2. What role does the active master node play in updating cluster state?

## Guarantees
* The master node guarantees linearizable cluster state updates across nodes.

## Non-guarantees
* Cluster state does not contain document bodies; only metadata.

## When to use this
* Auditing cluster health, metadata size, and master node performance.

## When not to use this
* Querying `GET _cluster/state` on large production clusters without filtering specific components (can return hundreds of megabytes of JSON).

## What comes next
In Phase 53, we investigate the deadly operational crisis: Mapping Explosion.
