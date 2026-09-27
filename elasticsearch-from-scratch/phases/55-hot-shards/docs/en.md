# Lesson 55.1: Hot Shards

## Motto
"A distributed cluster is only as fast as its most overloaded shard: key skew and bad routing create hot shards."

## Problem
A 10-node cluster has 9 idle nodes at 5% CPU, while 1 single node is pinned at 100% CPU with search threads constantly timing out. Even though 90% of the cluster is idle, total application latency degrades.

## Prediction
What causes one specific shard or node to receive 10x more search or indexing traffic than peer shards?

## Why this matters
Distributed systems assume balanced load. A **Hot Shard** bottlenecks the entire cluster, negating the benefits of horizontal scaling.

## First principles
Causes of Hot Shards:
1. **Custom Routing Skew:** A single customer/tenant generates 80% of all writes and searches, overloading their designated shard.
2. **Monotonic Key Routing:** All recent time-series data hits the newest active shard.
3. **Uneven Shard Sizing:** One shard contains 100GB of data while others have 5GB.
4. **Heavy Wildcard or Aggregation Queries:** Repeatedly hitting the same specific shard.

## Mental model
```text
Balanced Cluster (Ideal):
  Node 1: [Shard 0] (10% CPU)  |  Node 2: [Shard 1] (10% CPU)  |  Node 3: [Shard 2] (10% CPU)

Hot Shard Bottleneck (Skew):
  Node 1: [Shard 0] (99% CPU - HOT!) ──► CLUSTER SEARCH THROTTLED!
  Node 2: [Shard 1] ( 2% CPU)
  Node 3: [Shard 2] ( 3% CPU)
```

## Build it
See `code/hot_shard_simulator.py` simulating skewed traffic distributions in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/55-hot-shards/experiments/run_experiment.sh
```

## Inspect it
Identify hot threads on cluster nodes:
```bash
curl -s http://localhost:9200/_nodes/hot_threads
```
Inspect CPU and indexing rate across shards:
```bash
curl -s "http://localhost:9200/_cat/shards?v&s=docs:desc"
```

## Measure it
Compare CPU utilization and queue depths across data nodes.

## Break it
Simulate hot shard traffic by sending thousands of writes with the same routing key to one node.

## Recover it
1. Use `index.routing_partition_size` to spread large tenants across multiple shards.
2. Re-route shards away from stressed nodes using `_cluster/reroute`.

## Modify it
Inspect thread pool write rejections on the hot node.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an idle node not automatically help a peer node suffering from a hot shard?
2. How does the `_nodes/hot_threads` API reveal CPU bottlenecks?

## Guarantees
* Elasticsearch provides diagnostic APIs (`hot_threads`, `_cat/shards`) to pinpoint unbalanced load.

## Non-guarantees
* Elasticsearch cannot magically balance traffic if the application data model is intrinsically skewed.

## When to use this
* Capacity troubleshooting, load balancing diagnosis, and multi-tenant performance tuning.

## When not to use this
* Perfectly uniform workloads where all nodes share equal load.

## What comes next
In Phase 56, we examine Search Caching mechanisms.
