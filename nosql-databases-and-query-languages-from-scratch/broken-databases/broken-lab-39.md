# Broken NoSQL Lab 39: Last-Write-Wins clock drift silently overwriting modern data

## 1. System Failure Symptom
Production alerts are firing:
* **Alert:** High latency (p99 > 3,500ms) and coordinator thread pool starvation.
* **Component:** Data access layer under peak load (Lab #39).
* **Symptom:** Last-Write-Wins clock drift silently overwriting modern data.

## 2. Suspect Code / Schema
```text
-- Faulty query / configuration in Lab #39
SELECT * FROM table_data WHERE arbitrary_filter = 'active'; -- Missing partition key!
```

## 3. Forensic Diagnostic Steps
1. Run `./scripts/check-environment.sh`.
2. Inspect query execution plan using `explain('executionStats')` or `TRACING ON`.
3. Measure `totalDocsExamined` vs `nReturned`.
4. Calculate read amplification ratio.

## 4. Remediation Assignment
* Diagnose the exact root cause (Query, Index, Model, Partitioning, Consistency, Capacity).
* Remodel the schema or reindex the table.
* Verify p99 latency drops below 15ms.
