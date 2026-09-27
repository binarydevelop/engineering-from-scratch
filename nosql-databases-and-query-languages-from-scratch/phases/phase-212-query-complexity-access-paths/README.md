# Phase 212: Query Complexity by Access Path: The 6 Physical Latency Tiers

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Ranking point lookups, single-partition ranges, GSIs, multi-partitions, scans.
* **Core First Principle:** Access path geometry determines computational and network complexity.
* **Key Artifact Produced:** `Complexity Hierarchy Guide`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-212-query-complexity-access-paths/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-212-query-complexity-access-paths/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_212.py 2>/dev/null || true
```
