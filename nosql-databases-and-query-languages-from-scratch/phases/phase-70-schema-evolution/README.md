# Phase 70: Schema Evolution: Zero-Downtime Migrations and Dual-Writing

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Migrating address strings to structured objects across 10,000,000 documents.
* **Core First Principle:** Evolve schemas lazily on read or via asynchronous background migration scripts.
* **Key Artifact Produced:** `Schema Evolution Migration`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-70-schema-evolution/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-70-schema-evolution/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_70.py 2>/dev/null || true
```
