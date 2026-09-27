# Phase 208: Multi-Document Transactions: Distributed 2-Phase Commit in MongoDB

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Using session.startTransaction() across multiple collections and shards.
* **Core First Principle:** Multi-document transactions provide full ACID at the cost of throughput and latency.
* **Key Artifact Produced:** `MongoDB Transaction Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-208-multi-document-transactions/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-208-multi-document-transactions/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_208.py 2>/dev/null || true
```
