# Phase 83: CQL Update & Delete: Writing Mutations and Tombstones

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Updating columns and deleting rows in wide-column storage.
* **Core First Principle:** Deletes write tombstones; updates write new cell timestamps to the Memtable.
* **Key Artifact Produced:** `Mutation & Tombstone Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-83-cql-update-delete/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-83-cql-update-delete/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_83.py 2>/dev/null || true
```
