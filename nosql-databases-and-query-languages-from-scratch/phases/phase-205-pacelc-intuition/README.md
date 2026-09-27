# Phase 205: PACELC Intuition: Normal Operation Latency vs Consistency Tradeoffs

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Analyzing latency penalties of strong consistency during normal health.
* **Core First Principle:** PACELC explains why systems trade consistency for sub-5ms latency outside partitions.
* **Key Artifact Produced:** `PACELC Tradeoff Guide`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-205-pacelc-intuition/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-205-pacelc-intuition/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_205.py 2>/dev/null || true
```
