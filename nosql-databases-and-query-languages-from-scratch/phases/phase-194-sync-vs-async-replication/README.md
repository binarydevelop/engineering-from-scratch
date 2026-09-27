# Phase 194: Synchronous vs Asynchronous Replication: Latency vs Data Loss Window

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Measuring write latency and replica lag in synchronous vs async pipelines.
* **Core First Principle:** Synchronous replication guarantees zero data loss; async minimizes write latency.
* **Key Artifact Produced:** `Sync vs Async Benchmark`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-194-sync-vs-async-replication/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-194-sync-vs-async-replication/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_194.py 2>/dev/null || true
```
