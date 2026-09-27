# Phase 118: Sort-Key Patterns: begins_with, between, and Hierarchical Encodings

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Querying orders using SK begins_with('2026-09') or between dates.
* **Core First Principle:** Sort keys support range queries on prefixes within the partition.
* **Key Artifact Produced:** `Sort-Key Prefix Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-118-sort-key-patterns/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-118-sort-key-patterns/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_118.py 2>/dev/null || true
```
