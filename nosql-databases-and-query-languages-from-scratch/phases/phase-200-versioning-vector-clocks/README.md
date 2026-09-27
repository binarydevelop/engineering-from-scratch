# Phase 200: Versioning & Vector Clocks: Causality Tracking Without Clocks

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Implementing vector clocks to detect concurrent divergent mutations.
* **Core First Principle:** Vector clocks capture happened-before causal relationships deterministically.
* **Key Artifact Produced:** `Vector Clock Implementation`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-200-versioning-vector-clocks/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-200-versioning-vector-clocks/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_200.py 2>/dev/null || true
```
