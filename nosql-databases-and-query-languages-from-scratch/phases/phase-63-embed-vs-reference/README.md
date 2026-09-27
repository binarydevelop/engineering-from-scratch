# Phase 63: Embed vs Reference: The Central Document Modeling Dilemma

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Formulating rules for when to embed data vs when to link by ID.
* **Core First Principle:** Embed if data is read together and bounded; reference if unbounded or shared.
* **Key Artifact Produced:** `Embedding Decision Matrix`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-63-embed-vs-reference/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-63-embed-vs-reference/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_63.py 2>/dev/null || true
```
