# Phase 101: Consistency Levels: ONE, LOCAL_QUORUM, ALL, and Latency Tradeoffs

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Measuring read/write latency under ONE vs LOCAL_QUORUM vs ALL.
* **Core First Principle:** Consistency levels let the client tune the tradeoff between latency and staleness.
* **Key Artifact Produced:** `Consistency Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-101-consistency-levels/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-101-consistency-levels/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_101.py 2>/dev/null || true
```
