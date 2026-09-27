# Phase 87: Secondary Indexing in Cassandra: SAI (Storage-Attached Indexes) vs 2i

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Comparing legacy 2i performance with modern Cassandra 5.0 SAI indexes.
* **Core First Principle:** SAI indexes column values alongside SSTables, avoiding global index traps.
* **Key Artifact Produced:** `SAI Index Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-87-secondary-indexes-cql/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-87-secondary-indexes-cql/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_87.py 2>/dev/null || true
```
