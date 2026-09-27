# Phase 81: Distributed Search Simulator

A multi-shard distributed search cluster simulator implemented in Python standard library.

---

## 1. Features
* **Shard Routing:** Hashes document IDs across 3 independent shard worker instances.
* **Scatter-Gather Coordination:** Broadcasts lightweight sub-queries, executes local shard ranking, and merges candidates via Priority Queue into global top-$K$.
* **Failure Injection:** Simulates slow-shard tail latency and dead-node partial hit tolerance (`_shards.failed`).

---

## 2. Running Unit Tests

```bash
python3 projects/distributed_simulator/test_cluster.py
```
