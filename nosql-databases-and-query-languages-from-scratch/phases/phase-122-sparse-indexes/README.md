# Phase 122: Sparse Index Patterns: Filtering Un-Populated Attributes Automatically

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Creating an index on is_fraudulent attribute that only indexes flagged orders.
* **Core First Principle:** DynamoDB only indexes items that contain the GSI primary key attributes.
* **Key Artifact Produced:** `Sparse Index Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-122-sparse-indexes/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-122-sparse-indexes/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_122.py 2>/dev/null || true
```
