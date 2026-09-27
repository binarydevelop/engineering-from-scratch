# Phase 97: Tombstone Overload: Tombstone Overwhelming Scans and JVM Crashes

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Creating 100,000 tombstones and executing a range query.
* **Core First Principle:** Scanning tombstones consumes heap memory and triggers ReadTimeoutException.
* **Key Artifact Produced:** `Tombstone Overload Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-97-tombstone-problems/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-97-tombstone-problems/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_97.py 2>/dev/null || true
```
