# Cost Safety & Local-First Execution Guide

> **Core Rule:** 100% of the exercises, drills, simulations, and projects in this repository are designed to run **entirely locally at zero financial cost** using Docker containers, local emulators, and self-contained Python simulators.

---

## 1. Local-First Architecture

We enforce local-first execution to eliminate risk of unexpected cloud billing:

| System | Local Implementation | Emulation Fidelity | Cost |
| :--- | :--- | :--- | :--- |
| **MongoDB** | Official `mongo:7.0-jammy` container | 100% (Identical to production single-node/replica set) | **$0.00** |
| **Cassandra** | Official `cassandra:5.0.0` container | 100% (Identical JVM and storage engine) | **$0.00** |
| **DynamoDB** | `amazon/dynamodb-local:2.5.3` container | High (Validates schema, keys, types, PartiQL, condition expressions) | **$0.00** |
| **Redis** | Official `redis:7.4-alpine` container | 100% (Identical engine and commands) | **$0.00** |
| **Neo4j** | Official `neo4j:5.24.0-community` | 100% (Full Cypher 5 parsing and traversal engine) | **$0.00** |
| **Elasticsearch**| Official `elasticsearch:8.17.0` container | 100% (Complete JSON Query DSL and Lucene engine) | **$0.00** |

---

## 2. Critical Emulator Caveats (DynamoDB Local)

While `amazon/dynamodb-local` provides full API and syntax compatibility, you must understand where local emulators deviate from AWS Production DynamoDB:

1. **No Physical Storage Partitions:** DynamoDB Local stores all data in a local SQLite file. It does not physically split partitions at 10 GB boundaries or 1,000 WCU / 3,000 RCU limits.
2. **No Real Network Latency or Multi-AZ Replication:** Point lookups execute in sub-millisecond local process time rather than standard 4–10ms cross-AZ AWS round-trips.
3. **No Strict Throttling:** DynamoDB Local does not strictly enforce capacity unit throttling or HTTP 400 `ProvisionedThroughputExceededException` under burst load unless explicitly configured.
4. **PartiQL In-Memory Evaluation:** DynamoDB Local executes PartiQL syntax identically, but performance anomalies (such as full scans on secondary tables) must be measured by examining returned item counts rather than cloud billing metrics.

---

## 3. Optional AWS Cloud Experiments: Strict Safety Protocol

If you choose to run experiments against real AWS DynamoDB or AWS DocumentDB, you **MUST** follow these mandatory safety protocols:

### A. AWS Free Tier Awareness
* DynamoDB Free Tier includes **25 GB of storage**, **25 provisioned Write Capacity Units (WCU)**, and **25 provisioned Read Capacity Units (RCU)** per month indefinitely.
* **On-Demand Capacity:** DynamoDB charges per million read/write request units ($1.25 per million write units, $0.25 per million read units in us-east-1). Uncontrolled benchmark loops can incur real charges!

### B. Safety Checklist for Cloud Runs
1. **Set AWS Budgets:** Create an AWS Budget with a **$5.00 USD hard limit** and email alert before running any code.
2. **Use Table Tagging:** Tag all lab tables with `Environment=NoSQLScratchLab` and `AutoDelete=True`.
3. **Never Run Unbounded Scans in Cloud:** Scanning a 100 GB table in on-demand mode will consume 25,000 Read Request Units instantly.
4. **Always Execute Teardown:** Never leave cloud tables running overnight.

### C. Teardown & Verification Script
If you run against real AWS, run the automated cleanup script immediately after completion:
```bash
python3 scripts/cloud_cleanup.py --region us-east-1 --tag Environment=NoSQLScratchLab
```
Verify zero active tables:
```bash
aws dynamodb list-tables --region us-east-1
```
