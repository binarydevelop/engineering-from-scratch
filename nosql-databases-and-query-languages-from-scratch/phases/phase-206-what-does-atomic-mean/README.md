# Phase 206: What Does Atomic Mean Here? Atomicity Boundaries in NoSQL

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Comparing single-document atomicity with multi-statement ACID transactions.
* **Core First Principle:** In NoSQL, atomicity is guaranteed at the partition or document boundary.
* **Key Artifact Produced:** `Atomicity Boundary Matrix`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-206-what-does-atomic-mean/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-206-what-does-atomic-mean/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_206.py 2>/dev/null || true
```
