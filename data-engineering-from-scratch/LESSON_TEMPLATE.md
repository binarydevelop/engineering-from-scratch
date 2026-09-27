# Lesson [XX]: [Lesson Title]

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. Problem
State the concrete data engineering problem without mentioning specific vendor tools.
- What failure, bottleneck, ambiguity, or operational breakdown occurs here?
- What are the real symptoms (e.g., memory exhaustion, duplicate rows, silent schema drift, corrupted downstream reports)?

---

## 2. Prediction
Before running any code or pipeline:
- Predict the exact output row count.
- Predict the byte size and file layout.
- Predict what will happen if this pipeline is executed twice in succession.
- Predict which component will fail first under heavy load or poisoned data.

---

## 3. Why This Matters
Connect this lesson to production data engineering reality:
- How does this problem cause financial loss, SLA breaches, or customer-facing dashboard errors?
- Why is naive code dangerous in production?

---

## 4. First Principles
Deconstruct the underlying physics of data and systems:
- Disk I/O vs memory vs network bandwidth.
- Row-wise storage layout vs columnar binary serialization.
- Relational integrity vs distributed eventual consistency.
- Wall-clock time vs event-generation time vs processing time.

---

## 5. Mental Model
Provide the core conceptual diagram or flowchart:
```text
[Source System] ──(Ingest)──> [Staging Storage] ──(Validate)──> [Transformed Model] ──(Publish)──> [Consumer]
```
Explain the core invariant: What must remain true throughout this stage?

---

## 6. Source Data
Specify the input dataset:
- File format (CSV, JSON, Parquet, WAL log, database table).
- Location and volume.
- Sample records showing typical, edge-case, and boundary data.

---

## 7. Schema
Document the formal contract:
| Field Name | Physical Type | Logical Type | Nullable | Primary Key | Description |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | `VARCHAR(64)` | UUID | No | Yes | Canonical unique event identifier |

---

## 8. Build the Simple Version
Implement the primitive implementation in pure Python or standard SQL:
- No heavyweight frameworks.
- Demonstrate the raw mechanics so every byte and state transition is transparent.

---

## 9. Run It
Execute the script or pipeline:
```bash
python code/main.py
```
Observe standard output, exit codes, and generated artifacts.

---

## 10. Inspect Intermediate Data
Inspect the intermediate artifacts before final publication:
- Temporary files, staging tables, checkpoint markers, quarantine directories.
- Did the data match our expected physical format?

---

## 11. Validate Output
Run programmatic assertions on the target:
- Row count check (`count(*) == expected_count`).
- Uniqueness assertion (`count(distinct id) == count(id)`).
- Nullability constraint check (`count(*) filter (where field is null) == 0`).
- Range and domain validation.

---

## 12. Measure It
Quantify performance metrics:
- Throughput: Rows processed per second, MB/s.
- I/O: Bytes scanned vs bytes written.
- Memory: Peak memory utilization (RSS).
- Latency: p50, p95, and p99 processing duration.

---

## 13. Break It
Intentionally inject failure to observe degradation:
- Corrupt a record (inject string into integer column, inject null into primary key).
- Kill the process halfway through execution (`SIGKILL`).
- Simulate duplicate source delivery.
- Simulate out-of-order/late-arriving records.

---

## 14. Recover It
Demonstrate the operational recovery procedure:
- How does the pipeline detect partial work?
- How is the quarantine/dead-letter queue used?
- How does the pipeline self-heal or allow safe operator intervention?

---

## 15. Replay It
Verify idempotency and historical replayability:
- Re-run the exact same input on top of existing target.
- Does the target duplicate rows, corrupt counts, or remain mathematically identical?
- How do backfills operate across a historical date window?

---

## 16. Schema Evolution
Test what happens when the contract evolves:
- Producer adds a new optional column.
- Producer renames an existing column or changes data type.
- Verify whether the reader fails safely or adapts without data loss.

---

## 17. Production Implications
Discuss the real-world operational context:
- When does this primitive scale to its limits?
- What tool or engine is typically adopted once manual maintenance becomes too costly?
- Cost drivers: Storage costs vs scan compute vs network egress.

---

## 18. Evidence
Record the empirical results in `outputs/evidence-template.md`.

---

## 19. Questions for Mastery
Answer deep, non-trivial engineering questions:
1. *Why does this problem require an architectural pattern rather than simply throwing more memory at the machine?*
2. *If this step crashes midway, what exact state remains on disk, and how does the next run determine where to resume?*
3. *What are the tradeoffs between validating data at the edge during ingestion vs validating lazily in the analytical warehouse?*

---

## 20. What Comes Next
Link forward to the next logical phase in the curriculum.
