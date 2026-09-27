# Phase 190: Range Partitioning Deep Dive: Splits, Merges, and Key Ordering

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Analyzing Google Bigtable and CockroachDB range splitting models.
* **Core First Principle:** Range partitioning enables range queries but requires dynamic split management.
* **Key Artifact Produced:** `Range Partitioning Guide`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-190-range-partitioning-deep/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-190-range-partitioning-deep/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_190.py 2>/dev/null || true
```
