# Phase 58: Equality / Sort / Range (ESR) Rule: Designing Optimal Compound Indexes

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Applying Equality first, Sort second, Range third.
* **Core First Principle:** ESR rule prevents expensive in-memory sorts and minimizes scanned keys.
* **Key Artifact Produced:** `ESR Benchmark Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-58-esr-rule/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-58-esr-rule/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_58.py 2>/dev/null || true
```
