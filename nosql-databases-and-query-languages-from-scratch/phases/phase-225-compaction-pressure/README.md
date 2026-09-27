# Phase 225: Compaction Pressure: Generating Write Storms and SSTable Accumulation

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Flooding wide-column engine with writes until compaction lags behind.
* **Core First Principle:** Compaction lag causes read latency to spike as queries check more SSTables.
* **Key Artifact Produced:** `Compaction Stress Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-225-compaction-pressure/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-225-compaction-pressure/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_225.py 2>/dev/null || true
```
