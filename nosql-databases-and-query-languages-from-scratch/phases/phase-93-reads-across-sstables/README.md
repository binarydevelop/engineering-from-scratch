# Phase 93: Reads Across SSTables: Multi-Table Merges and Version Reconciliation

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Reading a key that exists across multiple SSTables.
* **Core First Principle:** The engine checks SSTables newest-to-oldest, merging surviving columns.
* **Key Artifact Produced:** `Multi-SSTable Reader`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-93-reads-across-sstables/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-93-reads-across-sstables/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_93.py 2>/dev/null || true
```
