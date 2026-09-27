# Lesson 65.1: Snapshots and Restore

## Motto
"Replicas are for high availability; snapshots are for disaster recovery. Never treat replicas as backups."

## Problem
A rogue script or human error issues `DELETE /products`. In 50 milliseconds, Elasticsearch dutifully deletes all primary shards AND all replica shards across the entire cluster. Replicas did not save you!

## Prediction
Can you restore a deleted index from an incremental snapshot repository taken an hour earlier?

## Why this matters
**Replicas $
eq$ Backups.** Snapshots are point-in-time point-to-point incremental backups written to external storage (S3, GCS, Shared Filesystem).

## First principles
Snapshot Architecture:
* **Snapshot Repository:** An external storage destination (`fs`, `s3`, `gcs`).
* **Incremental Snapshots:** Snapshots save Lucene segments. Because segments are immutable, subsequent snapshots only copy newly created segments, making them fast and storage-efficient.
* **Restore:** Reconstructs the index by downloading segments into a fresh shard.

## Mental model
```text
Index Segments:
  T0: Segment _0 (1GB) ──► Snapshot 1: Copies Segment _0 (1GB)
  T1: Segment _1 (200MB) ──► Snapshot 2: Copies ONLY Segment _1 (200MB! Incremental!)
```

## Build it
See `code/snapshot_incremental_sim.py` demonstrating incremental segment hashing in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/65-snapshots-and-restore/experiments/run_experiment.sh
```

## Inspect it
Register a local filesystem snapshot repository and take a snapshot:
```bash
curl -X PUT http://localhost:9200/_snapshot/backup_repo -H "Content-Type: application/json" -d '{
  "type": "fs",
  "settings": { "location": "/usr/share/elasticsearch/snapshots" }
}'
curl -X PUT "http://localhost:9200/_snapshot/backup_repo/snapshot_1?wait_for_completion=true"
```

## Measure it
Inspect snapshot metadata:
```bash
curl -s http://localhost:9200/_snapshot/backup_repo/snapshot_1?pretty
```

## Break it
Delete the index: `curl -X DELETE http://localhost:9200/products_phase06`. Confirm it is gone!

## Recover it
Restore the index from snapshot:
```bash
curl -X POST "http://localhost:9200/_snapshot/backup_repo/snapshot_1/_restore?wait_for_completion=true"
curl -s http://localhost:9200/products_phase06/_search?pretty
```
Data is 100% restored!

## Modify it
Restore with index renaming: `{"rename_pattern": "(.+)", "rename_replacement": "restored_$1"}`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does having 3 replicas provide zero protection against `DELETE /my_index`?
2. Why are subsequent snapshots of the same index vastly faster than the initial snapshot?

## Guarantees
* Restoring a snapshot recreates the exact index state at the time the snapshot completed.

## Non-guarantees
* Snapshots do not capture writes that occurred after the snapshot finished.

## When to use this
* Disaster recovery, production backups, and staging environment hydration.

## When not to use this
* Real-time failover between live cluster nodes (that is what replicas do).

## What comes next
In Phase 66, we explore Index Lifecycle Management (ILM) and data tiering.
