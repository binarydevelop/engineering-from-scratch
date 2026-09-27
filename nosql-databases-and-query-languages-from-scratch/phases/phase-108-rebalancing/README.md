# Phase 108: Rebalancing: Adding Nodes and Measuring Token Migration Cost

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Adding node 4 to a 3-node ring and tracking streaming data transfer.
* **Core First Principle:** Rebalancing streams SSTables across nodes, consuming network and disk bandwidth.
* **Key Artifact Produced:** `Cluster Rebalance Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-108-rebalancing/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-108-rebalancing/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_108.py 2>/dev/null || true
```
