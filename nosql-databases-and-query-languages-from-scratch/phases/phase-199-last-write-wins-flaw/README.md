# Phase 199: Last-Write-Wins (LWW): The Hidden Clock Drift Trap

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Simulating NTP clock drift and demonstrating silent data overwrites.
* **Core First Principle:** Physical clock drift destroys causality in distributed systems.
* **Key Artifact Produced:** `Clock Drift Failure Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-199-last-write-wins-flaw/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-199-last-write-wins-flaw/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_199.py 2>/dev/null || true
```
