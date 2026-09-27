# Phase 82: Query-Driven Tables: Creating Multiple Tables for Multiple Access Patterns

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Creating orders_by_customer and orders_by_status.
* **Core First Principle:** In Cassandra, you duplicate data across tables to satisfy distinct query paths.
* **Key Artifact Produced:** `Query-Driven Table Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-82-query-driven-tables/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-82-query-driven-tables/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_82.py 2>/dev/null || true
```
