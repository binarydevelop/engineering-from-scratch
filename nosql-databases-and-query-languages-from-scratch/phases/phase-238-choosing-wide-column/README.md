# Phase 238: Choosing Wide-Column: When Apache Cassandra / ScyllaDB Fit Best

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Workload characteristics that demand LSM Tree sequential write scale.
* **Core First Principle:** Wide-column stores excel at massive write velocity and known access paths.
* **Key Artifact Produced:** `Wide-Column Evaluation Matrix`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-238-choosing-wide-column/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-238-choosing-wide-column/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_238.py 2>/dev/null || true
```
