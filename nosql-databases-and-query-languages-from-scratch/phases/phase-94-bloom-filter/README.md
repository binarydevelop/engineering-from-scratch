# Phase 94: Bloom Filter: Probabilistic SSTable Disk-Seek Pruning

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Building a Bloom filter and measuring false-positive rates.
* **Core First Principle:** Bloom filters allow the engine to skip SSTables that definitely do not have the key.
* **Key Artifact Produced:** `Bloom Filter Implementation`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-94-bloom-filter/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-94-bloom-filter/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_94.py 2>/dev/null || true
```
