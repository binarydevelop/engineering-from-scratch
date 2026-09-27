# Phase 210: DynamoDB Transactions: TransactWriteItems & TransactGetItems

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Executing all-or-nothing mutations across up to 100 items in DynamoDB.
* **Core First Principle:** DynamoDB transactions consume 2x capacity units to execute 2-phase coordination.
* **Key Artifact Produced:** `DynamoDB Transaction Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-210-dynamodb-transactions/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-210-dynamodb-transactions/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_210.py 2>/dev/null || true
```
