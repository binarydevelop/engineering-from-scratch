# Phase 114: Filter Expressions: Understanding Filter-After-Read Semantics

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Applying FilterExpression status = 'DELIVERED' to a Query operation.
* **Core First Principle:** Filter expressions discard items in memory after they have already been read from disk.
* **Key Artifact Produced:** `Filter-After-Read Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-114-filter-expressions/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-114-filter-expressions/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_114.py 2>/dev/null || true
```
