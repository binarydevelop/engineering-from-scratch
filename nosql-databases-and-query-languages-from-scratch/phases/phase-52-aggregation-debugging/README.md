# Phase 52: Aggregation Debugging: Inspecting Intermediate Stage Outputs

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Using $limit and intermediate inspection to debug broken pipelines.
* **Core First Principle:** Step-by-step pipeline debugging catches shape and type errors early.
* **Key Artifact Produced:** `Pipeline Debugging Playbook`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-52-aggregation-debugging/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-52-aggregation-debugging/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_52.py 2>/dev/null || true
```
