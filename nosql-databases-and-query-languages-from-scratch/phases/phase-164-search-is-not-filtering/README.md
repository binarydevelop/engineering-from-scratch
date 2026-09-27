# Phase 164: Search Is Not Ordinary Filtering: Full-Text and Relevance Scoring

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Why relational LIKE '%headphones%' fails on relevance and typo-tolerance.
* **Core First Principle:** Search ranks candidate records by statistical relevance rather than binary truth.
* **Key Artifact Produced:** `Search vs Filter Concept`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-164-search-is-not-filtering/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-164-search-is-not-filtering/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_164.py 2>/dev/null || true
```
