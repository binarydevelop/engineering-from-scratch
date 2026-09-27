# Phase 95: Compaction: Merging SSTables, Write Amplification, and Space Reclaim

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Merging 5 SSTables into 1 consolidated table, discarding dead versions.
* **Core First Principle:** Compaction reclaims disk space and bounds read latency at the cost of write I/O.
* **Key Artifact Produced:** `Compaction Simulator`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-95-compaction/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-95-compaction/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_95.py 2>/dev/null || true
```
