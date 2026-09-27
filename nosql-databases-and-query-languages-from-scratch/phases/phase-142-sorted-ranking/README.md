# Phase 142: Sorted Ranking: Sorted Sets (ZSET) and Real-Time Leaderboards

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Using ZADD, ZREVRANGE, and ZRANK for gaming leaderboards and rate limits.
* **Core First Principle:** Skip lists maintain elements in sorted order by score in O(log N) time.
* **Key Artifact Produced:** `Sorted Set Leaderboard Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-142-sorted-ranking/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-142-sorted-ranking/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_142.py 2>/dev/null || true
```
