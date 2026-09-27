# Phase 239: Choosing Key-Value: When DynamoDB / Redis Fit Best

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Workload characteristics that demand constant O(1) latency at any scale.
* **Core First Principle:** Key-value stores excel at point lookups and strict access patterns.
* **Key Artifact Produced:** `Key-Value Evaluation Matrix`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-239-choosing-key-value/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-239-choosing-key-value/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_239.py 2>/dev/null || true
```
