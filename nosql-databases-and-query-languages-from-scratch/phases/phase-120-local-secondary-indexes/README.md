# Phase 120: Local Secondary Indexes (LSI): Synchronous Alternate Sort Keys

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Creating LSI sharing base partition key with alternate sort key.
* **Core First Principle:** LSIs provide strong consistency but enforce a 10GB partition size limit.
* **Key Artifact Produced:** `LSI Analysis Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-120-local-secondary-indexes/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-120-local-secondary-indexes/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_120.py 2>/dev/null || true
```
