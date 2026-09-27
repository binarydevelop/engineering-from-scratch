# Phase 121: Index Projection: KEYS_ONLY vs INCLUDE vs ALL

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Evaluating storage overhead vs fetch cost for GSI attribute projections.
* **Core First Principle:** Projecting ALL attributes duplicates table data; KEYS_ONLY requires table back-fetches.
* **Key Artifact Produced:** `Index Projection Matrix`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-121-index-projection/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-121-index-projection/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_121.py 2>/dev/null || true
```
