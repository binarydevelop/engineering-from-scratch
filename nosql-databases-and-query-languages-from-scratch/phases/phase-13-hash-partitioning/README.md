# Phase 13: Hash Partitioning: hash(key) % N Across Sharded Nodes

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Splitting keys across N nodes and observing movement when N changes.
* **Core First Principle:** Modulo hashing reshuffles (N-1)/N keys when scaling nodes.
* **Key Artifact Produced:** `Hash Partitioning Simulator`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-13-hash-partitioning/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-13-hash-partitioning/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_13.py 2>/dev/null || true
```
