# The First-Principles Data Pipeline Design Framework

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

Before writing a single line of Python, SQL, or configuration, every production data pipeline must answer the **19 Core Invariants**. If an engineer cannot answer these questions, any architecture chosen is merely guesswork.

---

## The 19 Core Invariants of Data Pipeline Design

```text
       ┌────────────────────────────────────────────────────────┐
       │             1. SOURCE & INGESTION CONTRACT             │
       │   - Where is origin? (DB log, REST API, Kafka topic)   │
       │   - What is the volume, frequency, and network cost?   │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             2. LATENCY & TEMPORAL MODEL                │
       │   - Batch vs Streaming?                                │
       │   - Event time vs Processing time? Late data window?   │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             3. SEMANTICS & GRAIN                       │
       │   - What does ONE row represent?                       │
       │   - Natural Key vs Surrogate Key vs Event ID?          │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             4. FAILURE, IDEMPOTENCY & REPLAY           │
       │   - What if it runs twice? (Dedup / Upsert / Replace)  │
       │   - Can target be rebuilt from raw source from day 0?  │
       └──────────────────────────┬─────────────────────────────┘
                                  ▼
       ┌────────────────────────────────────────────────────────┐
       │             5. OBSERVABILITY & GOVERNANCE              │
       │   - How do downstream consumers know data is ready?    │
       │   - Who owns schema? How are contracts tested in CI?   │
       └────────────────────────────────────────────────────────┘
```

---

### 1. What is the source?
- Is it a transactional OLTP database (PostgreSQL, MySQL), an operational event stream (Kafka), an external 3rd-party SaaS API (Stripe, Salesforce), or flat files dumped into an object store?
- Does reading from the source impact production users (e.g., table locks or CPU spikes from unindexed `SELECT *`)?

### 2. How much data?
- What is the current historical volume (GB/TB)?
- What is the daily incremental growth rate (GB/day, rows/day)?
- Can the daily slice fit comfortably in memory on a single worker node (e.g., 500 MB), or does it require distributed processing (500 GB)?

### 3. How often does it change?
- Is the source append-only (immutable clicks, audit logs, sensor pings)?
- Or mutable (orders changing status: `PENDING` -> `SHIPPED` -> `DELIVERED`, user profile updates)?
- Are hard deletes executed in the source, or soft deletes (`deleted_at IS NOT NULL`)?

### 4. Batch or streaming?
- Does the consumer genuinely require fresh numbers within seconds to make automated operational decisions (e.g., fraud block, real-time bidding)?
- Or is the consumer human (analysts, executives, marketing managers) viewing reports once a day or once an hour?
- *Rule: Batch is default. Streaming is justified only when latency requirements dictate.*

### 5. What freshness is required?
- Define the Service Level Agreement (SLA) and Service Level Objective (SLO): e.g., *"Daily sales mart refreshed by 06:00 UTC with max lag of 6 hours"* or *"Real-time fraud table with max lag of 30 seconds"*.

### 6. What is the schema?
- Are types, column names, nullability, and invariants explicitly documented in a versioned contract?
- Or is it semi-structured JSON where nested fields appear or disappear dynamically?

### 7. Who owns the schema?
- Which engineering team authors the producer code?
- If the producer decides to rename a column or drop an attribute, what notification protocol and deprecation window exists?

### 8. What is the primary key or event ID?
- What set of columns uniquely identifies one logical record?
- If the source lacks a natural primary key, what surrogate key strategy is chosen, and what are its collision risks?

### 9. Can data arrive late?
- In event-driven pipelines, network disconnections, mobile offline queues, and upstream retries cause events generated at 10:00 to arrive at 10:45.
- What watermark and late-data policy governs when windows close?

### 10. Can data be duplicated?
- Distributed message brokers (Kafka, SQS) provide **at-least-once** delivery by default.
- If network acknowledgments drop, producers retry and send the exact same event twice.
- How does the pipeline deduplicate records (e.g., Bloom filters, hash sets, SQL `ROW_NUMBER()` window dedup, or upsert)?

### 11. Can data be updated or deleted?
- If orders are updated, how does the analytical warehouse reflect this?
- Type 1 SCD (overwrite in place)?
- Type 2 SCD (version history with `valid_from` and `valid_to` timestamps)?
- Lakehouse merge (`MERGE INTO target USING staging ON ...`)?

### 12. Can the pipeline be replayed?
- If a catastrophic calculation bug is found in month 6, can an engineer drop the downstream tables and recompute the last 180 days deterministically from immutable raw files?
- If not, the design is fragile.

### 13. What is the source of truth?
- Which system holds canonical authority?
- The OLTP database log is authoritative for financial balances. The downstream warehouse table is a derived projection. Never treat derived caches as authoritative truth.

### 14. What is derived data?
- Staging tables, normalized dimension tables, aggregated sales marts, and feature store vectors are derived representations. They can be purged, regenerated, or re-indexed at will.

### 15. What happens on failure?
- If worker 3 crashes halfway through writing a 10 GB partition, does the pipeline leave partial, corrupted files exposed to downstream readers?
- Or does it use atomic staging and publication (`_temporary` directory rename, transaction commit, or metadata pointer swap)?

### 16. How is correctness validated?
- Do automated data quality gates run before publication?
- Non-null checks, uniqueness checks, referential integrity tests, and row-count distribution anomalies.

### 17. How will downstream consumers know data is ready?
- Sensor partition signals?
- Metadata catalog status update?
- Airflow dataset triggers?
- Webhook notification?
- Never rely on "the clock says 6:00 AM so the data must be ready."

### 18. What retention is required?
- How long must raw logs be kept in hot storage vs cold object storage vs purged entirely for compliance (GDPR right-to-be-forgotten, CCPA)?

### 19. What does it cost?
- How much network transfer, compute CPU time, object storage GB/month, and warehouse scan billing will this pipeline incur?
- Have you optimized partition pruning and columnar projections to avoid scanning terabytes for a 10-row query?
