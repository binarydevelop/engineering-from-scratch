# Phase 117: Condition Expressions: Optimistic Locking and Concurrency Control

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Using attribute_exists and version = expected_version to prevent lost updates.
* **Core First Principle:** Condition expressions guarantee atomic compare-and-swap (CAS) safety.
* **Key Artifact Produced:** `Optimistic Locking Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-117-condition-expressions/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-117-condition-expressions/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_117.py 2>/dev/null || true
```
