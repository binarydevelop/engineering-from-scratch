# Phase 200: Final Design Challenge — Global E-Commerce Data Platform

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. The Challenge Statement

You are the Principal Data Architect for **GlobalCart**, a multinational e-commerce retailer operating across 24 countries, processing 150 million transactions and 2.5 billion clickstream events every day.

Your mission is to design the entire enterprise data platform from first principles.
**Do not jump to a list of vendor tools.** You must independently justify every byte movement, storage format, latency SLA, failure recovery model, and governance boundary.

---

## 2. Business & Engineering Requirements

### 1. Sources & Ingestion
- **Transactional Core**: 50 sharded PostgreSQL database clusters handling user accounts, carts, checkout, inventory, and payments.
- **Clickstream Telemetry**: Web, iOS, and Android clients emitting page impressions, searches, add-to-carts, and checkout steps (peak: 120,000 events/second).
- **Third-Party SaaS APIs**: Stripe (payment settlements), Zendesk (support tickets), and Salesforce (B2B leads), ingested on hourly and daily schedules.

### 2. Analytical Consumers & Freshness Targets
- **Executive & Financial Reporting**: Daily net revenue, tax accruals, and partner settlement reports ready by **06:00 UTC**, accurate to the cent, fully auditable.
- **Operational Fraud & Inventory Dashboards**: Near-real-time dashboards alerting on suspicious payment velocities and stockouts within **30 seconds**.
- **Customer Lifetime Value & Churn Modeling**: Machine Learning feature store requiring daily and hourly batch point-in-time joins without data leakage.

### 3. Non-Functional Constraints & Operational Realities
- **PII & Regulatory Compliance**: GDPR "Right to be Forgotten" mandates deleting or irreversibly tokenizing specific customer IDs across all raw, staging, and lakehouse storage within 30 days.
- **Schema Evolution**: 60 distributed product teams deploy backend code multiple times per day. The platform must prevent breaking schema changes from taking down downstream analytics.
- **Historical Backfills**: The business frequently changes refund allocation accounting rules. The platform must support backfilling 3 years of daily financial partitions deterministically.
- **Cost Engineering**: Object storage is cheap; unindexed compute scans across petabytes are financially ruinous. Storage formats and partition keys must enforce aggressive pruning.

---

## 3. The 12 Architecture Dimensions You Must Reason Through

```text
       ┌────────────────────────────────────────────────────────┐
       │ 1. DATA CONTRACTS & OWNERSHIP BOUNDARIES               │
       ├────────────────────────────────────────────────────────┤
       │ 2. INGESTION TOPOLOGY: Batch vs CDC vs Streams         │
       ├────────────────────────────────────────────────────────┤
       │ 3. LAKEHOUSE STORAGE & OPEN FORMAT SPECIFICATION       │
       ├────────────────────────────────────────────────────────┤
       │ 4. GRAIN & DIMENSIONAL WAREHOUSE MODELING              │
       ├────────────────────────────────────────────────────────┤
       │ 5. ORCHESTRATION & DEPENDENCY TOPOLOGY                 │
       ├────────────────────────────────────────────────────────┤
       │ 6. DATA QUALITY & PRE-FLIGHT VALIDATION GATES          │
       ├────────────────────────────────────────────────────────┤
       │ 7. METADATA, CATALOG & COLUMN-LEVEL LINEAGE            │
       ├────────────────────────────────────────────────────────┤
       │ 8. DATA OBSERVABILITY, TELEMETRY & ALERTING            │
       ├────────────────────────────────────────────────────────┤
       │ 9. ATOMIC COMMIT, STAGING & PARTITION SWAP             │
       ├────────────────────────────────────────────────────────┤
       │ 10. REPLAYABILITY & HISTORICAL BACKFILL ENGINE         │
       ├────────────────────────────────────────────────────────┤
       │ 11. PRIVACY, TOKENIZATION & GDPR ERASURE               │
       ├────────────────────────────────────────────────────────┤
       │ 12. INFRASTRUCTURE SIZING, PRUNING & COST ENGINEERING   │
       └────────────────────────────────────────────────────────┘
```

---

## 4. Evaluation Rubric: What Separates Senior from Novice

| Novice Proposal | Senior Data Platform Design |
| :--- | :--- |
| "We will use Kafka + Spark + Snowflake + Airflow." | Deconstructs storage physics, network transfer, partition keys, failure blast radiuses, and cost models before naming tools. |
| Puts all data into streaming. | Identifies that financial ledgering requires deterministic batch reconciliation, whereas fraud needs streaming. Uses batch where simple and cheap. |
| Ingests raw OLTP tables with `SELECT * FROM orders`. | Uses Change Data Capture (CDC) via transaction log parsing to avoid table locks and replication lag on primary OLTP databases. |
| Treats `SUCCESS` exit code as proof data is valid. | Implements automated pre-flight, in-flight, and post-flight quality gates verifying uniqueness, nullability, and volume distributions. |
| No plan for schema drift or late events. | Defines versioned producer-consumer data contracts, watermarks, late-data side-outputs, and dead-letter quarantine queues. |
