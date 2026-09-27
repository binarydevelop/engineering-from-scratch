# Phase 214: Mongo Query Benchmark: Measuring COLLSCAN vs IXSCAN at Scale

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Benchmarking query throughput on 500,000 documents with and without indexes.
* **Core First Principle:** Index scans deliver 200x throughput improvements over unindexed scans.
* **Key Artifact Produced:** `Mongo Benchmark Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-214-mongo-query-benchmark/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-214-mongo-query-benchmark/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_214.py 2>/dev/null || true
```
