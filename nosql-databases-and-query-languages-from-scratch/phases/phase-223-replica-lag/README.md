# Phase 223: Replica Lag: Injecting Artificial Latency and Measuring Stale Read Rates

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Throttling network bandwidth to replica 2 and measuring staleness window.
* **Core First Principle:** Replica lag causes data divergence between nodes under eventual consistency.
* **Key Artifact Produced:** `Replica Lag Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-223-replica-lag/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-223-replica-lag/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_223.py 2>/dev/null || true
```
