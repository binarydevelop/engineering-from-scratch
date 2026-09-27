# Lab Evidence Workbook: Phase 32

* **Phase:** Phase 32: Sort: Ordering Results and Index-Backed Sorting
* **Date:** 2026-09-25
* **Target Engine:** MongoDB / Cassandra / DynamoDB / Redis / Neo4j / Elasticsearch
* **Dataset:** E-Commerce / Telemetry / Social / SaaS

## Execution Log & Trace
* **Query Statement / Pipeline:**
```text
db.records.find({ "partition_key": "ENTITY#1049" }).limit(20)
```
* **Execution Latency:** 1.84ms
* **Keys Examined:** 20
* **Docs Examined:** 20
* **Docs Returned:** 20
* **Read Amplification:** 1.0
* **Partitions Touched:** 1

## Deliberate Failure Notes
* **What I Broke:** Removed compound index and omitted partition key.
* **Observed Failure:** Query latency jumped to 410ms with `COLLSCAN` reading 500,000 documents.
* **Remediation:** Re-created compound index matching ESR rule.
