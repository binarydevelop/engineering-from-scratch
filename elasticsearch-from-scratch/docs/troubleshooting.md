# Elasticsearch Production Troubleshooting Guide

A field guide for diagnosing, mitigating, and recovering from distributed search engine failures.

---

## 1. Cluster Health Degradation (Yellow or Red)

### Diagnostic Command
```bash
curl -s http://localhost:9200/_cluster/health?pretty
curl -s "http://localhost:9200/_cat/indices?v&health=red,yellow"
curl -s "http://localhost:9200/_cat/shards?v&h=index,shard,prirep,state,unassigned.reason" | grep UNASSIGNED
```

### Interpretation
* **Yellow:** All primary shards are active, but one or more replica shards cannot be placed.
  * *Root Cause in Single-Node Lab:* You configured `number_of_replicas: 1` on an index, but only 1 node exists. Elasticsearch refuses to place a replica on the same physical node as the primary.
  * *Fix:* Set replicas to 0 for single-node development:
    ```bash
    curl -X PUT http://localhost:9200/*/_settings -H "Content-Type: application/json" -d '{"index": {"number_of_replicas": 0}}'
    ```
* **Red:** One or more primary shards are unassigned. At least some data is completely offline and searches will return partial hits.
  * *Diagnosis:* Run `GET _cluster/allocation/explain` to see the exact reason why Lucene cannot allocate the shard.

---

## 2. Investigating Unassigned Shards

### Command
```bash
curl -X POST http://localhost:9200/_cluster/allocation/explain?pretty -H "Content-Type: application/json" -d '{
  "index": "products",
  "shard": 0,
  "primary": true
}'
```
### Common Deciders
* `same_shard`: Cannot allocate primary and replica on the same node.
* `disk_threshold`: Node has exceeded the high watermark (90% disk usage).
* `node_not_found`: Node holding shard store was terminated or lost network connectivity.

---

## 3. Disk Watermark Violations & Read-Only Flood Stage

Elasticsearch enforces three progressive disk protection thresholds:
* **Low Watermark (85%):** Stops allocating new shards to this node.
* **High Watermark (90%):** Attempts to relocate existing shards away from this node.
* **Flood Stage (95%):** Forces index into **read-only** mode (`index.blocks.read_only_allow_delete: true`). Any write or indexing request will fail immediately with `ClusterBlockException`.

### Recovery Command
```bash
# 1. Clean up disk space or expand volume
# 2. Reset the read-only block
curl -X PUT http://localhost:9200/*/_settings -H "Content-Type: application/json" -d '{
  "index.blocks.read_only_allow_delete": null
}'
```

---

## 4. Circuit Breaker Exceptions (`circuit_breaking_exception`)

### Symptom
```json
{
  "type": "circuit_breaking_exception",
  "reason": "[parent] Data too large, data for [<transport_request>] would be [512345678/488.6mb], which is larger than the limit of [490000000/467.2mb]"
}
```

### Root Cause
An expensive aggregation, script, or `fielddata` un-inversion attempted to allocate more JVM heap than allowed by the parent circuit breaker (`indices.breaker.total.limit`).

### Immediate Mitigation
1. Cancel long-running tasks:
   ```bash
   curl -s http://localhost:9200/_tasks?detailed=true&actions=*search*
   curl -X POST http://localhost:9200/_tasks/<task_id>/_cancel
   ```
2. Avoid loading analyzed `text` into fielddata—switch queries to use `keyword` fields backed by columnar doc values.

---

## 5. Indexing Backpressure (`EsRejectedExecutionException`)

### Symptom
HTTP 429 Too Many Requests response during bulk ingestion:
```text
EsRejectedExecutionException[rejected execution of org.elasticsearch.transport.TransportService$7 on QueueResizingEsThreadPoolExecutor[write, queue capacity = 200]]
```

### Root Cause
Clients are submitting bulk batches faster than Lucene can write, segment-encode, and fsync data to disk. The fixed-size `write` thread pool queue (default 200 or 1000 tasks) is saturated.

### Best Practice Fix
Implement exponential backoff in the client application with jitter. Reduce concurrent indexing threads and measure sweet-spot bulk batch sizes (typically 5 MB to 15 MB per request).
