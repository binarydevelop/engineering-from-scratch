# Phase 144: Redis Search: Full-Text and Secondary Indexing in Memory

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Using FT.CREATE and FT.SEARCH to query structured hashes in RAM.
* **Core First Principle:** RedisSearch builds in-memory inverted indexes over Redis hashes and JSON.
* **Key Artifact Produced:** `RedisSearch Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-144-redis-search/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-144-redis-search/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_144.py 2>/dev/null || true
```
