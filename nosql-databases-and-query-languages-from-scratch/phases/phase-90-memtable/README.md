# Phase 90: Memtable: In-Memory Sorted Mutation Buffer

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Implementing an in-memory sorted table using SkipList / Red-Black Tree.
* **Core First Principle:** Memtable buffers incoming writes in memory, keeping keys strictly sorted.
* **Key Artifact Produced:** `Memtable Implementation`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-90-memtable/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-90-memtable/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_90.py 2>/dev/null || true
```
