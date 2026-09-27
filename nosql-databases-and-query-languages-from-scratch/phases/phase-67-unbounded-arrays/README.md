# Phase 67: The Unbounded Array Anti-Pattern: Document Growth and 16MB Limit

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Simulating continuous comment appends until BSON document explodes.
* **Core First Principle:** Unbounded arrays cause WiredTiger page splits and hit the 16MB document limit.
* **Key Artifact Produced:** `Unbounded Array Failure Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-67-unbounded-arrays/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-67-unbounded-arrays/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_67.py 2>/dev/null || true
```
