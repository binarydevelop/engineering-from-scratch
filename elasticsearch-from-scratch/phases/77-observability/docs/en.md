# Lesson 77.1: Observability

## Motto
"If you cannot measure it, you cannot operate it: track QPS, p95 latency, heap %, GC pauses, and write rejections."

## Problem
A cluster outage occurs. The engineering team argues over whether the failure was caused by slow disk I/O, JVM garbage collection, search query spikes, or unassigned shards. Without telemetry, post-mortems are speculation.

## Prediction
What are the top 5 metrics every Elasticsearch production dashboard must display?

## Why this matters
Elasticsearch exposes rich internal metrics via REST APIs and Prometheus exporters. Observability provides early warning before outages occur.

## First principles
The Golden Signals of Elasticsearch:
1. **Cluster Health & Unassigned Shards:** Green/Yellow/Red.
2. **JVM Heap Utilization & GC Pauses:** Heap % and duration of `old` generation garbage collection pauses.
3. **Search & Indexing Latency:** p50, p95, p99 times.
4. **Thread Pool Rejections:** `write.rejected` and `search.rejected` tasks.
5. **Disk Watermark Proximity:** Free disk percentage per node.

## Mental model
```text
           ELASTICSEARCH OBSERVABILITY SIGNALS
┌─────────────────────────────────────────────────────────────┐
│ 1. Health: GREEN (0 unassigned shards)                      │
│ 2. JVM Heap: 65% (GC old pauses < 100ms)                    │
│ 3. Indexing: 15,000 docs/sec | Latency p95: 4.2ms           │
│ 4. Search: 1,200 QPS         | Latency p95: 12.8ms          │
│ 5. Thread Pools: Write Queue: 12 / 10000 (0 rejected)       │
│ 6. Storage: Node 1 (62%), Node 2 (59%), Node 3 (61%)        │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/metrics_collector.py` polling and evaluating node statistics in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/77-observability/experiments/run_experiment.sh
```

## Inspect it
Retrieve comprehensive node statistics:
```bash
curl -s "http://localhost:9200/_nodes/stats?pretty" | grep -A 10 "jvm"
```
Inspect write and search thread pool stats:
```bash
curl -s "http://localhost:9200/_cat/thread_pool?v&h=node_name,name,active,queue,rejected,completed"
```

## Measure it
Plot query throughput and latency trends.

## Break it
Simulate high GC pause alerts by triggering artificial memory pressure.

## Recover it
Diagnose which node is lagging using `_cat/nodes?v&h=name,heap.percent,cpu,load_1m`.

## Modify it
Integrate with Prometheus via OpenTelemetry or Metricbeat.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is tracking thread pool `rejected` count more actionable than tracking average CPU usage?
2. What GC metric indicates that an Elasticsearch node is on the verge of an OutOfMemory crash?

## Guarantees
* Elasticsearch REST metrics provide real-time introspection into cluster internals.

## Non-guarantees
* Metrics APIs do not store historical trend graphs (use Prometheus/Grafana or Elasticsearch time-series indices).

## When to use this
* 24/7 production cluster monitoring and alerting.

## When not to use this
* Polling `_nodes/stats` every 10 milliseconds (polling itself consumes CPU; poll every 10s to 30s).

## What comes next
In Phase 78, we perform rigorous Capacity Planning.
