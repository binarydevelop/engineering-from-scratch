# Phase 180: E-Commerce Access Patterns: Designing for 5 Heterogeneous Queries

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Orders by ID, customer orders, date ranges, status filters, and categories.
* **Core First Principle:** Multi-access pattern design across document and wide-column stores.
* **Key Artifact Produced:** `E-Commerce Modeling Blueprint`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-180-ecommerce-access-patterns/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-180-ecommerce-access-patterns/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_180.py 2>/dev/null || true
```
