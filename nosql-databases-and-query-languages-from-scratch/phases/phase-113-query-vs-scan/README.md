# Phase 113: Query vs Scan: The 100x Cost and Latency Disaster

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Measuring RCU consumption and execution time of Query vs Scan on 100,000 items.
* **Core First Principle:** Query reads only targeted keys; Scan reads every item in the entire table.
* **Key Artifact Produced:** `Query vs Scan Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-113-query-vs-scan/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-113-query-vs-scan/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_113.py 2>/dev/null || true
```
