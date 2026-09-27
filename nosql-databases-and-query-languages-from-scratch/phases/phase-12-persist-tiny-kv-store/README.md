# Phase 12: Persist Tiny KV Store: Append-Only Write-Ahead Log (WAL) & Recovery

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Appending mutations to disk log, crashing, and recovering on restart.
* **Core First Principle:** Sequential disk writes achieve high throughput and crash durability.
* **Key Artifact Produced:** `Persistent KV Store with WAL`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-12-persist-tiny-kv-store/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-12-persist-tiny-kv-store/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_12.py 2>/dev/null || true
```
