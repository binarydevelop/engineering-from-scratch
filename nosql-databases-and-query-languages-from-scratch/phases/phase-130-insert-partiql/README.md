# Phase 130: INSERT With PartiQL: Inserting Items via SQL Syntax

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Inserting records using INSERT INTO Orders VALUE {'PK': '...', 'SK': '...'}.
* **Core First Principle:** Compiles directly to underlying PutItem call.
* **Key Artifact Produced:** `PartiQL INSERT Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-130-insert-partiql/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-130-insert-partiql/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_130.py 2>/dev/null || true
```
