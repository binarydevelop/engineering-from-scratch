# Phase 105: Failure Lab: Killing a Node Under Different Consistency Levels

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Killing 1 node in a 3-node cluster and testing QUORUM vs ALL writes.
* **Core First Principle:** QUORUM writes succeed with 1 node down; ALL writes fail immediately.
* **Key Artifact Produced:** `Replica Down Failure Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-105-failure-lab-replica-down/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-105-failure-lab-replica-down/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_105.py 2>/dev/null || true
```
