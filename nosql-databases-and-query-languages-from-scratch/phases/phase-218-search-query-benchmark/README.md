# Phase 218: Search Query Benchmark: Cached Filters vs Deep Wildcard Regex

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Comparing exact term bitset filters with leading wildcard (*query) scans.
* **Core First Principle:** Leading wildcard queries scan the entire inverted index lexicon.
* **Key Artifact Produced:** `Search Benchmark Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-218-search-query-benchmark/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-218-search-query-benchmark/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_218.py 2>/dev/null || true
```
