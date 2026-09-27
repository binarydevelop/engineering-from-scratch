# Phase 192: Partition Key Selection: Cardinality, Distribution, and Locality

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Evaluating low-cardinality vs high-cardinality keys for production stability.
* **Core First Principle:** The ideal partition key has high cardinality and uniform query distribution.
* **Key Artifact Produced:** `Key Selection Framework`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-192-partition-key-selection/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-192-partition-key-selection/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_192.py 2>/dev/null || true
```
