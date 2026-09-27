# Phase 135: The PartiQL Trap: When Innocent SQL Syntax Triggers Full Table Scans

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Executing SELECT * FROM Orders WHERE status = 'PENDING' without a key.
* **Core First Principle:** PartiQL does not make DynamoDB relational; unindexed queries trigger full scans.
* **Key Artifact Produced:** `PartiQL Trap Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-135-partiql-trap/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-135-partiql-trap/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_135.py 2>/dev/null || true
```
