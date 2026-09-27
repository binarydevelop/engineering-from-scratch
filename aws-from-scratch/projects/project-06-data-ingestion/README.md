# Project 06: High-Throughput Data Ingestion Architecture

> **Motto:** Derive the ingestion pipeline from throughput, ordering, and replayability requirements—not by blindly picking Kafka or Kinesis.

---

## 1. Architectural Tradeoff: Choosing the Ingestion Primitive

Before drawing a single box, we must interrogate the incoming data requirements:

```text
                                  [ Incoming Stream of Events ]
                                                │
                                                ▼
                          Do you need REPLAYABILITY and STRICT ORDERING
                             across multiple concurrent consumers?
                                                │
                               ┌────────────────┴────────────────┐
                              YES                                NO
                               │                                 │
                               ▼                                 ▼
                     [ STREAMING PRIMITIVE ]            [ BUFFERING PRIMITIVE ]
                     Amazon Kinesis Data Streams         Amazon SQS / EventBridge
                     • Sharded partition log            • Independent point-to-point
                     • Configurable 24hr-365d replay     • Message deleted upon processing
                     • Strict partition ordering        • Loose/unordered standard delivery
```

---

## 2. Architectural Diagram (Streaming to S3 Data Lake)

```text
[ Thousands of IoT Devices / Mobile Apps ]
                    │
                    │ 1. Batch Ingestion: PutRecords (JSON / Parquet)
                    ▼
[ Amazon Kinesis Data Firehose / Kinesis Data Streams ]
                    │
                    │ 2. Buffer interval: 60 seconds OR 5 MB
                    │ 3. Automated Gzip compression & schema format conversion
                    ▼
[ AWS Lambda (Micro-batch transform & anonymization) ]
                    │
                    ▼
[ Amazon S3 Data Lake (Partitioned: year=2026/month=09/day=23/) ]
                    │
                    ▼
[ Amazon Athena (Serverless SQL Queries over S3 Objects via Presto/Trino) ]
```

---

## 3. Systems Realizations: The S3 Small File Problem

If your producers upload one 2KB JSON file directly to S3 every time a sensor reports:
1. **API Cost Explosion:** 1,000 sensors * 1 event/sec = 86,400,000 S3 PUT requests/day = ~$432/day in PUT API fees alone!
2. **Athena Query Degradation:** Scanning 1,000,000 tiny 2KB files in Athena requires 1,000,000 individual HTTP GETs and metadata lookups, causing queries to take minutes and run up huge scan costs.

**The Solution: Micro-batching via Firehose or Buffer Workers:**
- Buffer incoming events in memory or Kinesis for 60 seconds or until 5MB of data accumulates.
- Compress into a single columnar file (Parquet or Snappy Gzip).
- Flush a single large object to S3.
- Result: 99% reduction in S3 API costs and 50x faster Athena query performance.

---

## 4. Well-Architected Review

### Performance Efficiency
- S3 key prefix partitioning (`s3://data-lake/events/year=YYYY/month=MM/day=DD/`) enables partition pruning during queries.

### Cost Optimization
- Kinesis Data Firehose charges purely for data volume ingested (no hourly shard fees for standard Firehose ingestion).
- Athena serverless queries charge $5.00 per TB of data scanned. Using columnar Parquet with compression reduces scanned bytes by 80-90%.

---

## 5. Teardown & Cleanup

```bash
# Delete Kinesis Stream
aws kinesis delete-stream --stream-name aws-from-scratch-ingestion-stream

# Empty and delete Data Lake bucket
aws s3 rm "s3://$DATA_LAKE_BUCKET" --recursive
aws s3api delete-bucket --bucket "$DATA_LAKE_BUCKET"
```

### Verify Cleanup
```bash
./scripts/cleanup-check.sh
```
