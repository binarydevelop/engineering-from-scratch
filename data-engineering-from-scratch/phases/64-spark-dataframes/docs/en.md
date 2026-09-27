# Phase 64: Spark Structured DataFrames

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. Problem
Transform distributed data using Spark DataFrames and inspect Catalyst query execution plans.
Without rigorous engineering discipline, this failure mode leads to silent data corruption, out-of-memory crashes, duplicate metrics, or unhandled schema drift that damages organizational trust.

## 2. Prediction
Before executing the pipeline or experiment in this phase:
- Predict the exact output row count and storage footprint.
- Predict the failure behavior if this step executes twice in succession.
- Predict what happens when poisoned or out-of-order records are encountered.

## 3. Why This Matters
In production data engineering, a pipeline that reports `SUCCESS` with an exit code of `0` is **not** evidence of data correctness. Understanding this phase ensures you can design resilient systems where data integrity is mechanically guaranteed rather than assumed.

## 4. First Principles
Deconstruct the underlying physical and relational invariants:
- **I/O and Storage**: Hardware limits (disk sequential throughput vs random seek, memory bandwidth).
- **Relational Integrity**: Set theory, grain definitions, and deterministic transformations.
- **Temporal Guarantees**: Wall-clock vs event generation time vs processing watermarks.

## 5. Mental Model
```text
[Upstream Source] ──(Ingest & Stage)──> [Validation Gate] ──(Transform)──> [Atomic Commit] ──> [Consumer]
```
The central invariant: *State transitions must be atomic, idempotent, and verifiable.*

## 6. Source Data
Input records for this phase demonstrate typical payloads, boundary conditions, and intentional edge cases:
- Format: Structured records, CSV/JSON, or Parquet partitions.
- Grain: Documented atomic entity represented by a single row.

## 7. Schema
| Field Name | Type | Nullable | Primary Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `record_id` | `VARCHAR(64)` | No | Yes | Canonical unique record identifier |
| `payload_value` | `NUMERIC(12,2)` | No | No | Numeric measurement or metric |
| `event_timestamp` | `TIMESTAMP_TZ` | No | No | ISO 8601 UTC timestamp of occurrence |

## 8. Build the Simple Version
Implement the fundamental mechanics in pure Python or standard ANSI SQL without relying on heavy external frameworks. Review `code/main.py` for the reference implementation.

## 9. Run It
Execute the phase pipeline:
```bash
python phases/64-spark-dataframes/code/main.py
```

## 10. Inspect Intermediate Data
Inspect temporary staging files, checkpoint files, and quarantine outputs before final publication. Verify that no partial state is exposed to consumers.

## 11. Validate Output
Run programmatic assertions:
- Row count matches mathematical expectation.
- Primary keys are strictly unique (`count(distinct id) == count(id)`).
- Nullability and value range bounds are obeyed.

## 12. Measure It
Quantify performance metrics:
- Throughput: Rows/sec and MB/sec.
- Memory consumption: Peak RSS memory.
- Storage efficiency: Uncompressed vs compressed byte layout.

## 13. Break It
Intentionally inject failure:
- Corrupt a record (inject string into numeric column, null primary key).
- Kill the process mid-execution.
- Re-run the exact same input to test for duplicate generation.

## 14. Recover It
Execute the remediation and recovery procedure:
- Quarantine corrupted records to dead-letter storage.
- Clean up intermediate staging tables.
- Resume from persistent checkpoint offsets.

## 15. Replay It
Demonstrate idempotency: Re-running the pipeline on identical source data must produce the exact same final state without row duplication or altered totals.

## 16. Schema Evolution
Evaluate contract changes:
- Adding optional columns (backward compatible).
- Renaming or altering types (breaking change requiring migration).

## 17. Production Implications
Connect this lesson to production tooling:
- When does custom code hit its scaling limits?
- How do industry engines (DuckDB, Spark, Airflow, dbt) formalize this primitive?
- Cost drivers: Storage retention, network egress, and compute hours.

## 18. Evidence
Record your empirical findings in `outputs/evidence-template.md`.

## 19. Questions for Mastery
1. *Why does this problem require architectural guarantees rather than simply increasing server memory?*
2. *If this pipeline terminates abruptly at 50% completion, what exact state remains on disk, and how does the recovery mechanism ensure consistency?*
3. *What are the tradeoffs between validating data at the ingestion boundary versus lazily during warehouse transformations?*

## 20. What Comes Next
Proceed to the next phase in the curriculum to build upon these verified primitives.
