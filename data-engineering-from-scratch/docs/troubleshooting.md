# Data Engineering Field Troubleshooting Guide

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

When production pipelines break, panic is the enemy. Use this systematic troubleshooting guide to isolate the failure layer.

---

## 1. The Five Triage Questions

Before inspecting logs or modifying code, answer:
1. **Did the job fail technically, or did it produce bad data?** (Job error vs data quality failure).
2. **What was the input volume compared to normal?** (Did volume spike 10x or drop to 0?).
3. **What is the logical execution date/interval?** (Is it today's run or a historical backfill?).
4. **Has the upstream schema or contract changed?** (Check producer deployments and commit logs).
5. **Is the pipeline idempotent?** (Can we re-run safely, or will re-running duplicate rows?).

---

## 2. Common Production Incidents & Resolution Playbooks

### Incident 1: Metric Inflation / Doubled Revenue
- **Symptom**: Dashboard reports 2x or 3x expected revenue; row counts in fact table suddenly increased.
- **Root Cause**: A SQL `JOIN` on non-unique keys, or an un-idempotent batch pipeline executed twice without deduplication.
- **Diagnosis**:
  ```sql
  -- Check for duplicate natural keys
  SELECT order_id, COUNT(*)
  FROM fact_orders
  GROUP BY order_id
  HAVING COUNT(*) > 1;
  ```
- **Remediation**: Apply deduplication (`ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC) = 1`) or convert `INSERT` to atomic partition overwrite / `MERGE`.

---

### Incident 2: Out of Memory (OOM) / Worker Crash
- **Symptom**: Python exits with `Exit Code 137` (SIGKILL by OS OOM killer) or Spark reports `java.lang.OutOfMemoryError: Java heap space`.
- **Root Cause**: Reading an entire multi-gigabyte dataset into memory (`f.read()`, `json.load()`, or unconstrained `collect()`) instead of streaming/chunking.
- **Diagnosis**: Check OS RSS memory logs or Spark executor memory metrics.
- **Remediation**:
  1. Stream records line-by-line (`csv.reader` generator).
  2. Use DuckDB streaming scans or PyArrow batch readers (`iter_batches()`).
  3. Increase partition count to reduce per-task memory size.

---

### Incident 3: The Straggler Problem / Data Skew
- **Symptom**: Distributed batch job runs 99 tasks in 2 minutes, but the 100th task runs for 45 minutes.
- **Root Cause**: Extreme key skew (e.g., `user_id IS NULL` or a massive enterprise customer accounting for 80% of all events grouped into a single partition).
- **Diagnosis**:
  ```sql
  SELECT user_id, COUNT(*) AS event_count
  FROM raw_events
  GROUP BY user_id
  ORDER BY event_count DESC
  LIMIT 10;
  ```
- **Remediation**: Salt the skewed join key (`CONCAT(user_id, '_', CAST(FLOOR(RANDOM() * 10) AS INT))`) or isolate null values before joining.

---

### Incident 4: CDC Stream Gap / Missing Records
- **Symptom**: Analytical warehouse table is missing records that definitely exist in the operational database.
- **Root Cause**: Consumer was offline longer than WAL log retention; WAL segments were pruned; or checkpoint was committed before target write succeeded.
- **Diagnosis**: Compare maximum source primary key / timestamp with target table maximum:
  ```sql
  -- Source
  SELECT COUNT(*), MAX(updated_at) FROM source_orders;
  -- Warehouse
  SELECT COUNT(*), MAX(updated_at) FROM stg_orders;
  ```
- **Remediation**: Trigger an isolated snapshot/reconciliation backfill for the missing time window.
