# Phase 73: CQL Looks Like SQL — But Isn't SQL: Query Constraints

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Why SELECT * FROM orders WHERE status = 'SHIPPED' fails in CQL.
* **Core First Principle:** CQL syntax resembles SQL, but execution is strictly bound to key structure.
* **Key Artifact Produced:** `CQL vs SQL Contrast Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-73-cql-is-not-sql/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-73-cql-is-not-sql/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_73.py 2>/dev/null || true
```
