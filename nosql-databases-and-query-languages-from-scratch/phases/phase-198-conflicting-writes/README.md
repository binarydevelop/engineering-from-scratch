# Phase 198: Conflicting Writes: Concurrent Mutations in Distributed Storage

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Simulating concurrent updates to the same key on two disconnected nodes.
* **Core First Principle:** Concurrent writes must be reconciled by timestamp, vector clock, or application.
* **Key Artifact Produced:** `Write Conflict Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-198-conflicting-writes/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-198-conflicting-writes/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_198.py 2>/dev/null || true
```
