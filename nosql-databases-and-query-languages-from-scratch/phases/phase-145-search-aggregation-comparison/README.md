# Phase 145: Redis Search vs SQL: Comparing Query Expressiveness and Speed

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Comparing SQL query execution to RedisSearch in-memory aggregation.
* **Core First Principle:** In-memory indexed queries execute with ultra-low latency but high RAM cost.
* **Key Artifact Produced:** `Redis vs SQL Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-145-search-aggregation-comparison/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-145-search-aggregation-comparison/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_145.py 2>/dev/null || true
```
