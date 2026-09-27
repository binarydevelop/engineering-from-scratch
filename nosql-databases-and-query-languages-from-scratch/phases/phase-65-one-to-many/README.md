# Phase 65: One-to-Many Modeling: Bounded Child Lists vs Referencing

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Comparing embedded order line items vs referenced forum comments.
* **Core First Principle:** Bounded 1:N belongs in-document; unbounded 1:N must be referenced.
* **Key Artifact Produced:** `1:N Cardinality Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-65-one-to-many/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-65-one-to-many/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_65.py 2>/dev/null || true
```
