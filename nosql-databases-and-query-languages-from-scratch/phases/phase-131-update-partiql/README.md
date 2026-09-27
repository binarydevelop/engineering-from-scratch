# Phase 131: UPDATE With PartiQL: Modifying Attributes and Nested Paths

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Executing UPDATE Orders SET total = 199.99 WHERE PK = '...' AND SK = '...'.
* **Core First Principle:** Compiles to native UpdateItem with UpdateExpression.
* **Key Artifact Produced:** `PartiQL UPDATE Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-131-update-partiql/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-131-update-partiql/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_131.py 2>/dev/null || true
```
