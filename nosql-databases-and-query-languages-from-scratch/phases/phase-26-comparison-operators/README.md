# Phase 26: Comparison Operators: $gt, $gte, $lt, $lte, $ne, $in, $nin

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Querying orders with total > 100 and status IN ['SHIPPED', 'DELIVERED'].
* **Core First Principle:** Comparison operators define range bounds on index b-tree nodes.
* **Key Artifact Produced:** `Comparison Query Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-26-comparison-operators/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-26-comparison-operators/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_26.py 2>/dev/null || true
```
