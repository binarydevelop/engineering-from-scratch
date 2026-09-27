# Phase 159: Graph Constraints: Node Uniqueness and Mandatory Properties

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Enforcing CREATE CONSTRAINT FOR (u:User) REQUIRE u.email IS UNIQUE.
* **Core First Principle:** Uniqueness constraints prevent duplicate nodes and back lookups with B-trees.
* **Key Artifact Produced:** `Constraint Enforcement Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-159-graph-constraints/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-159-graph-constraints/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_159.py 2>/dev/null || true
```
