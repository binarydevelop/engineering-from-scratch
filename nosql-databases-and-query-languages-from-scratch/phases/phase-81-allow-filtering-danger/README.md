# Phase 81: Why ALLOW FILTERING Is Dangerous: The Full Cluster Scan Trap

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Measuring latency and CPU when forcing ALLOW FILTERING on 1M rows.
* **Core First Principle:** ALLOW FILTERING forces the coordinator to scan every partition across all nodes.
* **Key Artifact Produced:** `ALLOW FILTERING Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-81-allow-filtering-danger/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-81-allow-filtering-danger/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_81.py 2>/dev/null || true
```
