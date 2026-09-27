# Lesson 49.1: Node Failure

## Motto
"Controlled failure testing: kill the node holding a primary shard and observe real-time failover and shard recovery."

## Problem
Engineers assume high-availability works because it is written in documentation. In production, when a node drops off the network, unexpected timeouts occur because teams have never observed live failover.

## Prediction
If a 3-node cluster loses Node 1 holding Primary Shard 0:
1. What does cluster health become?
2. How many seconds does failover take?
3. Do search queries fail during promotion?

## Why this matters
Master node heartbeats, replica promotion, and peer recovery are the core distributed resilience mechanisms of Elasticsearch.

## First principles
Failover Sequence:
1. Master node detects missing heartbeats from Node 1 (default 10s ping timeout).
2. Master updates cluster state: marks Node 1 dead.
3. Master checks for active replica shards of missing primaries.
4. Promotes Replica Shard 0 on Node 2 to **Primary**.
5. Cluster health transitions from **GREEN $	o$ YELLOW** (all primaries active, but missing a replica).
6. Master allocates a new unassigned replica on Node 3 and begins **Peer Recovery** (copying Lucene segments over network).
7. Once sync finishes, cluster transitions back to **GREEN**!

## Mental model
```text
T0: Healthy (Green)
  Node 1: Primary 0  |  Node 2: Replica 0  |  Node 3: Master

T1: Kill Node 1!
  Node 1: [DEAD]     |  Node 2: Replica 0  |  Node 3: Master (Detects dead node)

T2: Failover (Yellow)
  Node 1: [DEAD]     |  Node 2: PRIMARY 0  |  Node 3: Starts peer recovery to Node 3

T3: Recovered (Green)
  Node 1: [DEAD]     |  Node 2: PRIMARY 0  |  Node 3: REPLICA 0 (Data replicated!)
```

## Build it
See `code/node_failure_monitor.py` polling cluster state changes during failure.

## Use Elasticsearch
Run the experiment against the 3-node cluster lab (`docker-compose.cluster.yml`):
```bash
./phases/49-node-failure/experiments/run_experiment.sh
```

## Inspect it
Observe active cluster nodes before and after:
```bash
curl -s "http://localhost:9200/_cat/nodes?v"
curl -s "http://localhost:9200/_cat/shards?v"
```

## Measure it
Measure time elapsed from container termination (`docker stop es-cluster-02`) to replica promotion.

## Break it
Kill the active master node (`es01`) and observe how the remaining two nodes elect a new master via Raft-based consensus without data loss.

## Recover it
Restart the stopped container (`docker start es-cluster-02`) and watch Elasticsearch re-balance and re-assign shards.

## Modify it
Inspect cluster health recovery speed with `_cat/recovery`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does cluster health turn YELLOW and not RED when a node hosting a primary shard dies (assuming replicas exist)?
2. How does peer recovery avoid re-copying existing matching Lucene segments? (Engine uses sequence numbers and translog replay).

## Guarantees
* As long as at least one primary or replica shard exists, data remains available for search.

## Non-guarantees
* If a node dies while hosting an un-replicated primary (`number_of_replicas: 0`), that shard's data is lost and the cluster turns RED.

## When to use this
* Disaster recovery validation and chaos engineering drills.

## When not to use this
* Do not terminate nodes in production during active unthrottled reindexing.

## What comes next
In Phase 50, we define and live-trigger Cluster Health states: Green, Yellow, and Red.
