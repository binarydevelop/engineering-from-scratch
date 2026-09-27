# Phase 213: Benchmark Methodology: p50, p95, p99, Concurrency, and Warmup

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Building a reproducible benchmarking harness for database testing.
* **Core First Principle:** Averages lie; tail latency (p99) dictates user experience in distributed systems.
* **Key Artifact Produced:** `Benchmark Rig Guide`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-213-benchmark-methodology/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-213-benchmark-methodology/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_213.py 2>/dev/null || true
```
