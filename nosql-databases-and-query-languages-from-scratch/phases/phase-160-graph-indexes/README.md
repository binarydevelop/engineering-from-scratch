# Phase 160: Graph Indexes: Point Seeks vs Traversal Pointers

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Creating schema indexes on node properties to anchor traversals.
* **Core First Principle:** Indexes locate the starting node; relationship traversal proceeds via pointers.
* **Key Artifact Produced:** `Index vs Traversal Analysis`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-160-graph-indexes/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-160-graph-indexes/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_160.py 2>/dev/null || true
```
