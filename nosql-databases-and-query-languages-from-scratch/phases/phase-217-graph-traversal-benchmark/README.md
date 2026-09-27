# Phase 217: Graph Traversal Benchmark: Bounded Hops vs Combinatorial Explosion

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Measuring execution time of 1-hop, 2-hop, 3-hop, and unconstrained traversals.
* **Core First Principle:** Unconstrained graph traversals suffer exponential combinatorial path explosion.
* **Key Artifact Produced:** `Graph Traversal Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-217-graph-traversal-benchmark/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-217-graph-traversal-benchmark/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_217.py 2>/dev/null || true
```
