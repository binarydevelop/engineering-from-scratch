# Phase 111: PutItem & GetItem: Sub-10ms Single-Item Point Lookups

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Executing point mutations and lookups via Boto3 / CLI.
* **Core First Principle:** GetItem hashes the partition key to locate the exact storage node in O(1) time.
* **Key Artifact Produced:** `Point Lookup Suite`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-111-put-get-item/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-111-put-get-item/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_111.py 2>/dev/null || true
```
