# System Design Interview Problems Suite

A comprehensive library of **50 complete system design problems** categorized into three difficulty tiers:

1. **Beginner Tier** (15 Problems): Foundational single-service and component designs (URL shortener, Pastebin, Rate Limiter, In-Memory KV).
2. **Intermediate Tier** (20 Problems): Multi-tier distributed systems (Web Crawler, Real-Time Chat, Social News Feed, Video Platform, E-Commerce).
3. **Advanced Tier** (15 Problems): Complex distributed consensus, financial ledgers, and global multi-region systems (Payment Ledger, CLOB Stock Exchange, Collaborative Editor, Raft KV).

---

## Problem & Solution Separation
Each problem directory contains:
- `problem.md`: The ambiguous interviewer prompt, requirements gathering, scale inputs, changing requirements, and failure scenarios.
- `solution.md`: The comprehensive architectural derivation, ASCII diagrams, data models, APIs, and tradeoff analysis.

---

## Running Verification Tests
```bash
pytest interview-problems/test_interview_problems.py -v
```
