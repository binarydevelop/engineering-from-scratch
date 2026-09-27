# Data Quality Discipline and Verification Framework

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

A pipeline that runs without an error code is **not** evidence that the data is correct. A silent bug in SQL joins can duplicate revenue by 200%, while leaving the orchestration status as `SUCCESS`.

Data quality must be treated as a first-class engineering discipline with explicit automated gates.

---

## 1. The Six Dimensions of Data Quality

```text
       ┌────────────────────────────────────────────────────────┐
       │ 1. COMPLETENESS: Are expected values missing or NULL?  │
       ├────────────────────────────────────────────────────────┤
       │ 2. UNIQUENESS: Are records duplicated by primary key?  │
       ├────────────────────────────────────────────────────────┤
       │ 3. VALIDITY: Do values conform to types, formats, regex│
       ├────────────────────────────────────────────────────────┤
       │ 4. CONSISTENCY: Do cross-table relationships balance?  │
       ├────────────────────────────────────────────────────────┤
       │ 5. FRESHNESS: Has data arrived within agreed SLA time? │
       ├────────────────────────────────────────────────────────┤
       │ 6. ACCURACY: Does aggregate match upstream source sum? │
       └────────────────────────────────────────────────────────┘
```

---

## 2. The Hierarchy of Data Quality Checks

Data quality checks occur at distinct boundaries in the pipeline:

### 1. Ingestion Boundary (Pre-Flight Checks)
- **Format Validation**: Is the file valid JSON/CSV/Parquet syntax?
- **Schema Validation**: Are mandatory headers present? Are data types castable?
- **Action on Failure**: Quarantine poisoned files immediately to dead-letter storage before touching the staging database.

### 2. Transformation Boundary (In-Flight Assertions)
- **Grain Verification**: Before joining, verify row counts. After joining, check if row count exploded (Cartesian product symptom).
- **Referential Integrity**: Does every `user_id` in `orders` resolve to a valid customer in `dim_customer`?
- **Range Constraints**: Are order amounts non-negative (`total_amount >= 0`)? Are dates non-future (`created_at <= CURRENT_TIMESTAMP`)?

### 3. Publication Boundary (Post-Flight Reconciliation)
- **Reconciliation Check**:
  $$\sum \text{Orders}_{\text{raw}} = \sum \text{Orders}_{\text{mart}}$$
- **Volume Anomaly Detection**: Compare today's row count with the 14-day rolling average. If row count is $< 50\%$ or $> 300\%$, pause publication and alert oncall.

---

## 3. Handling Corrupted / Poison Records: Three Strategies

| Strategy | When to Use | Tradeoff |
| :--- | :--- | :--- |
| **Fail-Stop** | Financial ledgers, compliance audits, billing pipelines where 1 missing cent causes regulatory violations. | Halts downstream processing; high operational oncall friction. |
| **Quarantine (Dead-Letter Queue)** | High-throughput clickstreams, event ingestion, telemetry logs. Malformed rows written to `quarantine/` with error metadata. | Downstream continues smoothly; requires tooling to inspect, fix, and replay quarantined records. |
| **Drop & Count (Tolerated Error Rate)** | Non-critical IoT sensor noise where 0.01% packet loss is statistically negligible. | Simplest implementation; risk of silent error masking if threshold alerts are not configured. |

---

## 4. Statistical Distribution Checks

Schema validation verifies syntax; distribution checks verify reality:
- **Z-Score / Moving Standard Deviation**: Flag if average order value deviates by $> 3.5\sigma$.
- **Category Cardinality Drift**: Flag if a previously stable category column introduces 500 new unknown strings (indicating a bot attack or upstream scraper bug).
- **Null-Ratio Trend**: Flag if the null rate in optional column `promo_code` jumps from 10% to 90% (indicating frontend tracking breakdown).
