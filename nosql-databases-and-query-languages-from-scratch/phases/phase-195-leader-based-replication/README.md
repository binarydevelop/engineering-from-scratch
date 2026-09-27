# Phase 195: Leader-Based Replication: Primary-Secondary Failover and Split-Brain

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

## Overview
* **Primary Question:** Raft/Paxos leader election, failover pauses, and split-brain risks.
* **Core First Principle:** Leader-based systems simplify consistency by routing all writes through one node.
* **Key Artifact Produced:** `Leader Failover Lab`

## Quick Navigation
* [Comprehensive Lesson Guide](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-195-leader-based-replication/docs/en.md)
* [Lab Evidence Workbook](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-195-leader-based-replication/outputs/evidence-template.md)
* [Query Thinking Framework](file:///Users/tushar/Desktop/private/repos/nosql-databases-and-query-languages-from-scratch/docs/query-thinking.md)

## Quickstart Commands
```bash
# Verify environment and inspect phase
./scripts/check-environment.sh
python3 -m pytest tests/test_phase_195.py 2>/dev/null || true
```
