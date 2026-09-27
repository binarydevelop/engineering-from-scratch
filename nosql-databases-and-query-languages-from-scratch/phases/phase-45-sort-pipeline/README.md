# Phase 45: $sort: Ordering Pipeline Output in Memory and on Disk

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Sorting top customers by total lifetime spend DESC.
* **Core First Principle:** Sorting after $group requires an in-memory sort buffer or allowDiskUse.
* **Key Artifact Produced:** `Pipeline Sort Optimization`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-45-sort-pipeline/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-45-sort-pipeline/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_45.py 2>/dev/null || true
```
