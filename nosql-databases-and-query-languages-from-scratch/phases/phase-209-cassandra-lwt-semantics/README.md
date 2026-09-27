# Phase 209: Cassandra Lightweight Transactions (LWT): Compare-And-Set (CAS)

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Implementing bank account transfers with IF balance >= amount.
* **Core First Principle:** LWT uses 4-phase Paxos consensus, multiplying round-trip latency.
* **Key Artifact Produced:** `Cassandra LWT Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-209-cassandra-lwt-semantics/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-209-cassandra-lwt-semantics/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_209.py 2>/dev/null || true
```
