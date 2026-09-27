# Phase 153: Variable-Length Paths: Traversing Multi-Hop Chains (*1..5)

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Finding connections up to 3 hops away: (a)-[:FRIEND*1..3]->(b).
* **Core First Principle:** Variable-length paths expand recursively; unconstrained paths risk memory exhaustion.
* **Key Artifact Produced:** `Multi-Hop Traversal Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-153-variable-length-paths/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-153-variable-length-paths/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_153.py 2>/dev/null || true
```
