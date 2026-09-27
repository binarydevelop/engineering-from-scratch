# Phase 158: MERGE: Idempotent Match-or-Create Graph Semantics

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Using MERGE with ON CREATE SET and ON MATCH SET.
* **Core First Principle:** MERGE matches an existing pattern or atomically creates it if absent.
* **Key Artifact Produced:** `MERGE Idempotency Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-158-merge-mutations/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-158-merge-mutations/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_158.py 2>/dev/null || true
```
