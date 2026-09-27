# Operational Troubleshooting & Diagnostic Playbook

This playbook provides actionable diagnostic procedures for debugging connection failures, cluster degradation, query slowness, and memory pressure across all supported NoSQL database engines.

---

## 1. Quick Diagnostic Cheat Sheet

| Symptom | Probable Cause | Immediate Diagnostic Command |
| :--- | :--- | :--- |
| **MongoDB Slow Query** | Missing index / `COLLSCAN` | `db.collection.find(...).explain("executionStats")` |
| **Cassandra Read Timeout** | Scanned too many tombstones / missing partition key | `TRACING ON;` then run query in `cqlsh` |
| **Cassandra Node Down** | Heap OOM or Gossip failure | `nodetool status` and `nodetool info` |
| **DynamoDB Throttling** | Consumed capacity exceeded / Hot partition | Inspect `ConsumedReadCapacityUnits` in CloudWatch or local logs |
| **Redis Memory Spike** | Missing key TTLs / unconstrained buffer | `redis-cli info memory` and `redis-cli --bigkeys` |
| **Redis Slowness** | O(N) command blocking single thread | `redis-cli slowlog get 10` |
| **Neo4j Out of Memory** | Unconstrained variable-length traversal | `PROFILE MATCH ...` check DB hits and heap |
| **Elasticsearch Cluster Yellow/Red** | Unassigned shards / disk watermark | `curl -s localhost:9200/_cluster/allocation/explain` |
| **Elasticsearch Circuit Breaker** | Fielddata heap limit reached | `curl -s localhost:9200/_nodes/stats/breaker` |

---

## 2. MongoDB Diagnostics

### A. Execution Plan Inspection
Always verify `totalDocsExamined` vs `nReturned`:
```javascript
var exp = db.orders.find({ customer_id: "CUST-1049", status: "PENDING" }).explain("executionStats");
print("Docs Examined: " + exp.executionStats.totalDocsExamined);
print("Docs Returned: " + exp.executionStats.nReturned);
print("Stage: " + exp.executionStats.executionStages.stage);
```
* **Red Flag:** If `stage == "COLLSCAN"`, the database is scanning every document on disk.
* **Resolution:** Add a compound index covering the equality predicates and sort fields:
  ```javascript
  db.orders.createIndex({ customer_id: 1, status: 1 });
  ```

### B. Profiling Slow Queries in Production
Enable the native profiler for operations taking longer than 50ms:
```javascript
db.setProfilingLevel(1, { slowms: 50 });
// View the top 5 slowest queries:
db.system.profile.find().sort({ millis: -1 }).limit(5).pretty();
```

---

## 3. Apache Cassandra & LSM Tree Diagnostics

### A. Diagnosing Tombstone Overload
When rows are deleted in an LSM tree, tombstones accumulate until compaction:
```sql
TRACING ON;
SELECT * FROM device_events WHERE device_id = 'DEV-01' LIMIT 10;
```
* **Look for in Trace Output:** `Read 1 live rows and 104,291 tombstone cells`.
* **Impact:** Coordinator issues a `ReadFailureException` when tombstone scan threshold is exceeded (`tombstone_failure_threshold = 100000`).
* **Resolution:** Trigger manual compaction or adjust compaction strategy:
  ```bash
  nodetool compact nosql_scratch device_events
  ```

### B. Checking Node Gossip & Token Distribution
```bash
docker exec -it nosql-cassandra nodetool status
docker exec -it nosql-cassandra nodetool ring
```

---

## 4. Amazon DynamoDB Diagnostics

### A. Differentiating Query vs Scan
* If code calls `boto3.client('dynamodb').scan()`, replace immediately with `boto3.client('dynamodb').query()`.
* Ensure `KeyConditionExpression` contains the exact partition key.
* If filtering by an attribute other than the primary key, evaluate whether creating a Global Secondary Index (GSI) is economically justified by the read volume.

### B. Hot Partition Detection
* If 1% of keys consume 90% of capacity, apply write sharding:
  Append a random integer suffix (`PK = ITEM#1029#` + `rand(0, 9)`) to distribute writes evenly across partition nodes.

---

## 5. Redis Diagnostics

### A. Inspecting the Slowlog
Redis executes commands on an event loop. A single slow command (like `KEYS *` or `HGETALL` on a 1,000,000-field hash) halts all other operations:
```bash
redis-cli slowlog get 20
```

### B. Finding Memory Hogs
```bash
redis-cli --bigkeys
redis-cli --memkeys
```

---

## 6. Elasticsearch Diagnostics

### A. Diagnosing Unassigned Shards
When cluster health is RED or YELLOW:
```bash
curl -X GET "http://localhost:9200/_cluster/allocation/explain?pretty"
```
* Common cause: Disk watermark exceeded (> 85% disk used forces Elasticsearch to stop allocating shards).
* Resolution: Free disk space or lower threshold:
  ```bash
  curl -X PUT "http://localhost:9200/_cluster/settings" -H 'Content-Type: application/json' -d'
  {
    "transient": {
      "cluster.routing.allocation.disk.watermark.low": "90%",
      "cluster.routing.allocation.disk.watermark.high": "95%"
    }
  }'
  ```

### B. Analyzing Tokenizer & Query DSL Parsing
Verify how Elasticsearch tokenizes text before searching:
```bash
curl -X POST "http://localhost:9200/_analyze?pretty" -H 'Content-Type: application/json' -d'
{
  "analyzer": "standard",
  "text": "Wireless Noise-Cancelling Headphones"
}'
```
