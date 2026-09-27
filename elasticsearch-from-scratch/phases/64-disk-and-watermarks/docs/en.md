# Lesson 64.1: Disk and Watermarks

## Motto
"Elasticsearch defends disk with three watermarks: 85% stops allocations, 90% relocates shards, 95% locks the cluster read-only."

## Problem
A node running out of disk space risks fatal Lucene segment corruption and crash loops. Without warning thresholds, a runaway write workload could completely fill the drive.

## Prediction
What happens to indexing requests when a data node exceeds 95% disk utilization?

## Why this matters
Elasticsearch enforces three automatic **Disk Allocation Watermarks** to safeguard the cluster.

## First principles
The Three Watermarks:
1. **Low Watermark (85%):** Master stops allocating new shards to this node. Existing shards remain writable.
2. **High Watermark (90%):** Master actively attempts to relocate existing shards away from this node to other nodes.
3. **Flood Stage (95%):** Master enforces a **read-only index block** (`index.blocks.read_only_allow_delete: true`). All write/indexing operations fail immediately!

## Mental model
```text
Disk Usage:
  0% ──────────────── 85% ──────────── 90% ──────────── 95% ────── 100%
  [ Normal Writing ] [ Low Mark ]      [ High Mark ]   [ Flood Stage! ]
                     No new shards     Relocate shards  READ-ONLY LOCK!
```

## Build it
See `code/watermark_simulator.py` demonstrating threshold triggers in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/64-disk-and-watermarks/experiments/run_experiment.sh
```

## Inspect it
Check disk utilization and watermarks across nodes:
```bash
curl -s "http://localhost:9200/_cat/allocation?v"
```

## Measure it
Inspect current watermark settings:
```bash
curl -s "http://localhost:9200/_cluster/settings?include_defaults=true" | grep -i "watermark" || true
```

## Break it
Simulate a flood stage lock by manually setting the read-only block on an index:
```bash
curl -X PUT http://localhost:9200/products_phase06/_settings -H "Content-Type: application/json" -d '{
  "index.blocks.read_only_allow_delete": true
}'
```
Attempt an indexing write: observe `ClusterBlockException`!

## Recover it
Free disk space, then clear the block:
```bash
curl -X PUT http://localhost:9200/products_phase06/_settings -H "Content-Type: application/json" -d '{
  "index.blocks.read_only_allow_delete": null
}'
```

## Modify it
Configure custom byte thresholds: `cluster.routing.allocation.disk.watermark.low: "50gb"`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the 95% flood stage lock the index into read-only mode instead of failing silently?
2. Why does freeing disk space NOT automatically remove the `read_only_allow_delete` block?

## Guarantees
* Flood stage prevents complete disk exhaustion and filesystem corruption.

## Non-guarantees
* Watermarks cannot save a cluster if all nodes reach 95% simultaneously.

## When to use this
* Disk monitoring, alerts, and emergency incident recovery.

## When not to use this
* Disabling disk thresholds in production (`cluster.routing.allocation.disk.threshold_enabled: false` is dangerous).

## What comes next
In Phase 65, we practice disaster recovery with Snapshots and Restore.
