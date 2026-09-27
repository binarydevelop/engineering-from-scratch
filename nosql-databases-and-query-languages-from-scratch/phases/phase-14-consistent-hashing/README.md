# Phase 14: Consistent Hashing: Virtual Nodes and Minimal Key Relocation

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Building a consistent hashing ring simulator with vnodes.
* **Core First Principle:** Consistent hashing limits key migration to exactly K/N keys.
* **Key Artifact Produced:** `Consistent Hashing Simulator`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-14-consistent-hashing/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-14-consistent-hashing/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_14.py 2>/dev/null || true
```
