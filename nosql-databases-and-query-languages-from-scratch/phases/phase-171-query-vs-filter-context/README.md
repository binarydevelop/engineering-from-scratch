# Phase 171: Query vs Filter Context: Relevance Scoring (BM25) vs Bitset Caching

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Measuring performance difference between scoring clauses and cached filters.
* **Core First Principle:** Filter context skips score calculation and caches result bitsets in RAM.
* **Key Artifact Produced:** `Scoring vs Caching Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-171-query-vs-filter-context/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-171-query-vs-filter-context/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_171.py 2>/dev/null || true
```
