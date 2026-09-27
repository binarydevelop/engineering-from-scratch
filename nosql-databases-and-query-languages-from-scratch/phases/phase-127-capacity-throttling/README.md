# Phase 127: Capacity & Throttling: On-Demand vs Provisioned Capacity Modes

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Calculating RCU/WCU costs for 4KB read blocks and 1KB write blocks.
* **Core First Principle:** Understanding DynamoDB billing and capacity allocation mechanics.
* **Key Artifact Produced:** `Capacity Planning Workbook`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-127-capacity-throttling/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-127-capacity-throttling/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_127.py 2>/dev/null || true
```
