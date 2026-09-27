# Phase 77: Insert: Append-Only Writes and Upsert Semantics

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Inserting rows into wide-column tables and observing upsert behavior.
* **Core First Principle:** In Cassandra, INSERT and UPDATE are identical operations to the LSM tree.
* **Key Artifact Produced:** `CQL Insert Operations`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-77-insert-cql/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-77-insert-cql/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_77.py 2>/dev/null || true
```
