# Phase 211: Why Data Modeling Reduces Transaction Need: The Aggregate Solution

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Embedding related items in a single document to achieve atomic invariants without 2PC.
* **Core First Principle:** Modeling the aggregate correctly makes multi-record transactions unnecessary.
* **Key Artifact Produced:** `Aggregate Modeling Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-211-data-modeling-reduces-transactions/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-211-data-modeling-reduces-transactions/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_211.py 2>/dev/null || true
```
