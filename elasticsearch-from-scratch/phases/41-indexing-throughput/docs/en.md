# Lesson 41.1: Indexing Throughput

## Motto
"Indexing throughput is governed by the bottleneck: bulk size, refresh interval, replica count, and client concurrency."

## Problem
You are tasked with ingesting 500 million documents into an Elasticsearch cluster. At the initial rate of 2,000 docs/sec, the ingestion will take 70 hours! How do you systematically tune the cluster to ingest at 50,000 docs/sec?

## Prediction
Which of these levers yields the greatest indexing speedup: increasing bulk batch size, disabling replicas during ingestion, or disabling refresh?

## Why this matters
High-throughput ingestion is a core capacity planning requirement for logs, clickstreams, and data migrations.

## First principles
The Four Levers of Indexing Throughput:
1. **Bulk Size:** Sweet spot is 5MB to 15MB per batch (avoids HTTP overhead and JVM heap spikes).
2. **Refresh Interval:** Set `index.refresh_interval: -1` or `"30s"` during bulk loads.
3. **Replicas:** Set `number_of_replicas: 0` during initial ingestion. Re-enable replicas once ingestion finishes (building replicas via segment copy is vastly faster than indexing twice!).
4. **Client Concurrency:** Run multiple client workers matching available CPU cores on ingest nodes.

## Mental model
```text
Slow Configuration (2,000 docs/sec):
  1 doc/req + refresh=1s + replicas=1 + 1 client thread

Tuned Configuration (50,000 docs/sec):
  1,000 docs/bulk (10MB) + refresh=-1 + replicas=0 + 8 concurrent workers
```

## Build it
See `code/throughput_benchmark.py` running a parameterized ingestion benchmark.

## Use Elasticsearch
Run the experiment:
```bash
./phases/41-indexing-throughput/experiments/run_experiment.sh
```

## Inspect it
Monitor indexing rate and thread pool queue status:
```bash
curl -s "http://localhost:9200/_cat/thread_pool/write?v&h=node_name,name,active,queue,rejected,completed"
```

## Measure it
Compare ingestion rates (docs/sec) across all four configuration combinations.

## Break it
Overwhelm the write thread pool by launching 100 concurrent bulk threads on a single node and observe `rejected` task counts rising.

## Recover it
Implement client-side exponential backoff and match worker concurrency to available cluster indexing threads.

## Modify it
Benchmark with `index.translog.durability: async` vs `request`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is building replica shards via segment copy after ingestion faster than indexing to replicas concurrently during ingestion?
2. What metric in `_cat/thread_pool` indicates that the cluster cannot keep up with write ingestion?

## Guarantees
* Applying these levers maximizes hardware saturation for ingestion.

## Non-guarantees
* Setting `number_of_replicas: 0` leaves the data vulnerable to hardware failure during the ingestion window.

## When to use this
* Large-scale data imports, nightly batch loads, and cluster bootstrapping.

## When not to use this
* Standard steady-state operational indexing where real-time replica safety and search freshness are required.

## What comes next
In Phase 42, we cross the boundary into Distributed Systems: Sharding From First Principles.
