# Phase 98: Compaction Strategies: Size-Tiered, Leveled, and Time-Window

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Analyzing STCS (write-heavy), LCS (read-heavy), and TWCS (time-series).
* **Core First Principle:** Selecting the right compaction strategy controls read, write, and space amplification.
* **Key Artifact Produced:** `Compaction Strategy Guide`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-98-compaction-strategies/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-98-compaction-strategies/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_98.py 2>/dev/null || true
```
