# Phase 66: Many-to-Many Modeling: Array of References vs Join Collections

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Modeling student courses and product tags.
* **Core First Principle:** Two-way embedding of IDs enables fast lookups from either direction.
* **Key Artifact Produced:** `N:M Modeling Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-66-many-to-many/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-66-many-to-many/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_66.py 2>/dev/null || true
```
