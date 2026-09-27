# Phase 216: DynamoDB Benchmark: Query Operation vs Table Scan Under Load

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Measuring execution time and capacity consumption of Query vs Scan.
* **Core First Principle:** Query maintains constant latency; Scan latency scales linearly with dataset size.
* **Key Artifact Produced:** `DynamoDB Benchmark Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-216-dynamo-query-scan-benchmark/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-216-dynamo-query-scan-benchmark/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_216.py 2>/dev/null || true
```
