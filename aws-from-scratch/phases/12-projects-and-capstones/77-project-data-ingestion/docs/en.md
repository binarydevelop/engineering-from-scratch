# Phase 77: Project: Data Ingestion Architecture

## Motto
> Derive the pipeline from throughput, ordering, and replayability requirements—not by blindly picking Kafka.

**Type:** Architecture Project & Big Data Pipeline  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 17: S3 From First Principles  
**AWS Services Involved:** Amazon Kinesis Data Streams / Firehose, S3 Data Lake, Athena  
**Cost Vector:** Kinesis Firehose charges $0.029 per GB ingested with zero idle shard fees.  

---

## Problem
Thousands of IoT devices send 10,000 events per second. Writing each event as a separate file to S3 creates the 'Small File Problem' (crushing S3 API costs and making SQL queries impossibly slow).

---

## Prediction
Micro-batching events in Kinesis Data Firehose buffers data into 5MB chunks, compresses with Snappy/Gzip, and flushes columnar Parquet files to S3, reducing costs by 99%.

---

## Why this matters
This is Project 06: the big data ingestion standard for streaming analytics and serverless data lakes.

---

## First principles
Ingestion trade-off: Point-to-point queues (SQS) do not support replayability or multiple concurrent consumer groups. Streaming logs (Kinesis / Kafka) maintain an immutable, ordered partition log re-playable from 24 hours to 365 days. Micro-batching solves the S3 small-file problem.

---

## Mental model
```text
Project 06 Architecture:
[ 10,000 IoT Devices ] ──► [ Kinesis Data Streams / Firehose ]
                                        │
                                        │ Buffer: 60s OR 5MB (Micro-batching)
                                        │ Automated Compression (Parquet / Gzip)
                                        ▼
                         [ Amazon S3 Partitioned Data Lake ]
                         (s3://data-lake/year=2026/month=09/day=23/)
                                        │
                                        ▼ Serverless SQL Queries
                         [ Amazon Athena (Presto / Trino) ]
```

---

## Architecture before AWS
Self-hosted Apache Kafka clusters + Apache Flume + Hadoop HDFS clusters.

---

## Build the primitive
```python
with open('projects/project-06-data-ingestion/README.md') as f:
    print("Project 06 loaded:", "High-Throughput Data Ingestion" in f.read())
```

---

## Use AWS
```bash
# Implementation commands in projects/project-06-data-ingestion/README.md
```

---

## Inspect it
```bash
aws kinesis list-streams --output table
```

---

## Measure it
Measure cost savings: 1,000 individual PUTs ($0.005) vs 1 micro-batched 5MB PUT ($0.000005) = 99.9% cheaper!

---

## Break it
Write 100,000 tiny 1KB files directly to S3 and run an Athena query.

---

## Diagnose it
Athena query takes 45 seconds and scans massive metadata overhead.

---

## Recover it
Buffer events with Firehose into 5MB Parquet files; query time drops to 1.2 seconds.

---

## Security
Enforce S3 bucket encryption using KMS and partition key access control.

---

## Cost
### Cost Warning
Kinesis Firehose charges $0.029 per GB ingested with zero idle shard fees.

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
Follow teardown commands in `projects/project-06-data-ingestion/README.md`.
```

---

## Verify cleanup
```bash
./scripts/cleanup-check.sh
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-77-evidence.md`.

---

## Questions for mastery
1. What is the 'S3 Small File Problem' and how does micro-batching solve it?
2. What are the architectural differences between Amazon SQS and Amazon Kinesis Data Streams?
3. How does columnar storage (Parquet) reduce Amazon Athena query scan costs by 80-90%?

---

## When to use this
Use for high-throughput clickstream data, IoT telemetry, log aggregation, and real-time analytics.

---

## When not to use this
Do not use Kinesis for simple asynchronous microservice task decoupling (use SQS).

---

## What comes next
Phase 78: Architecture Evolution — Scaling an application from 100 to 10M users.
