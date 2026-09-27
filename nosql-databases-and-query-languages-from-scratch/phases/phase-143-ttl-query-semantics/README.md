# Phase 143: TTL Query Semantics: Expiring Keys, Sliding Windows, and Eviction Policies

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Setting EXPIRE on auth tokens and analyzing volatile-lru eviction.
* **Core First Principle:** Memory expiration is an active component of the operational data model.
* **Key Artifact Produced:** `TTL & Eviction Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-143-ttl-query-semantics/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-143-ttl-query-semantics/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_143.py 2>/dev/null || true
```
