# Phase 30: Array $elemMatch: Enforcing Multiple Conditions on the Same Element

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Filtering orders having an item with price > 50 AND qty >= 2.
* **Core First Principle:** Naive array query matches across different elements; $elemMatch binds to one.
* **Key Artifact Produced:** `elemMatch Filter Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-30-elemmatch/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-30-elemmatch/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_30.py 2>/dev/null || true
```
