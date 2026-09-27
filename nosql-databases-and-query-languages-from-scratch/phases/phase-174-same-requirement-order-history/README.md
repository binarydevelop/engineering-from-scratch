# Phase 174: Same Requirement Across Databases: Customer Order History

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Implementing 'Latest 20 orders for customer 42' in Mongo, Cassandra, and DynamoDB.
* **Core First Principle:** Different physical storage engines require different schema encodings.
* **Key Artifact Produced:** `Cross-Paradigm Order History`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-174-same-requirement-order-history/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-174-same-requirement-order-history/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_174.py 2>/dev/null || true
```
