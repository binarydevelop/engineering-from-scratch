# Phase 123: Composite Keys: Encoding Multiple Dimensions into PK and SK Strings

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Encoding PK = ORG#123#USER#456, SK = ORDER#2026-09-25#ORD-99.
* **Core First Principle:** String concatenation creates multi-dimensional search capability within one key.
* **Key Artifact Produced:** `Composite Key Patterns`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-123-composite-keys/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-123-composite-keys/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_123.py 2>/dev/null || true
```
