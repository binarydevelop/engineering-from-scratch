# Phase 146: Why Graph Databases? Deep Traversal vs Relational Joins

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Workload: Finding friends of friends, fraud rings, and dependency chains.
* **Core First Principle:** Relational joins scale exponentially O(N^k); graph traversal scales linearly O(k).
* **Key Artifact Produced:** `Graph Motivation Doc`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-146-why-graph/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-146-why-graph/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_146.py 2>/dev/null || true
```
