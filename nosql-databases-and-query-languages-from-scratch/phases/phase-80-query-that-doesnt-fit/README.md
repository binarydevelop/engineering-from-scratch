# Phase 80: Query That Doesn't Fit: When Cassandra Rejects Your Query

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Attempting to query by unindexed non-partition column.
* **Core First Principle:** Cassandra refuses queries that would require cluster-wide unindexed scans.
* **Key Artifact Produced:** `Rejected Query Analysis`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-80-query-that-doesnt-fit/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-80-query-that-doesnt-fit/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_80.py 2>/dev/null || true
```
