# Phase 215: Cassandra Partition Benchmark: Single Partition vs Filtering

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Benchmarking partition key queries against ALLOW FILTERING queries.
* **Core First Principle:** Partition queries scale with cluster size; unpartitioned queries collapse.
* **Key Artifact Produced:** `Cassandra Benchmark Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-215-cassandra-partition-benchmark/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-215-cassandra-partition-benchmark/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_215.py 2>/dev/null || true
```
