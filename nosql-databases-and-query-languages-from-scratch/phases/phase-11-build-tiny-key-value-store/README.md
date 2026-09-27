# Phase 11: Build a Tiny Key-Value Store: In-Memory PUT, GET, and DELETE

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Building an in-memory dictionary store from first principles.
* **Core First Principle:** Memory provides sub-microsecond access but zero persistence.
* **Key Artifact Produced:** `In-Memory KV Implementation`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-11-build-tiny-key-value-store/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-11-build-tiny-key-value-store/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_11.py 2>/dev/null || true
```
