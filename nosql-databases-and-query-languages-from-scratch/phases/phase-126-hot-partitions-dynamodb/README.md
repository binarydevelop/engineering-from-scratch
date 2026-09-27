# Phase 126: Hot Partitions: Throttling and Automatic Partition Splitting

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Exceeding 1,000 WCU / 3,000 RCU per partition and observing throttling.
* **Core First Principle:** Traffic skew overwhelms individual storage partitions, triggering HTTP 400s.
* **Key Artifact Produced:** `Throttling Simulation`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-126-hot-partitions-dynamodb/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-126-hot-partitions-dynamodb/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_126.py 2>/dev/null || true
```
