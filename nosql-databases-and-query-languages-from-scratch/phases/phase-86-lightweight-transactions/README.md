# Phase 86: Lightweight Transactions (LWT): Paxos-Based Conditional Updates

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Using IF NOT EXISTS and IF status = 'PENDING' in CQL.
* **Core First Principle:** LWT uses a 4-phase Paxos consensus protocol, adding significant latency.
* **Key Artifact Produced:** `Paxos LWT Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-86-lightweight-transactions/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-86-lightweight-transactions/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_86.py 2>/dev/null || true
```
