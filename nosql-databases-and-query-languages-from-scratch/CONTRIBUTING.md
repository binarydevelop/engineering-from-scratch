# Contributing to NoSQL Databases & Query Languages From Scratch

Thank you for your interest in contributing! This repository is an educational curriculum dedicated to teaching NoSQL database engineering and query-language fluency from first principles.

---

## Pedagogical Standards

1. **First Principles Over Tutorials:** Do not submit superficial syntax cheat-sheets. Every lesson, exercise, or drill must explain the underlying physical storage reality (B-Tree, LSM Tree, SSTable, Inverted Index, Graph Adjacency List).
2. **Follow the Templates:**
   - All phases must follow [`LESSON_TEMPLATE.md`](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch/LESSON_TEMPLATE.md).
   - All query exercises must follow [`QUERY_TEMPLATE.md`](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch/QUERY_TEMPLATE.md).
3. **No Fluff or Vague Claims:**
   - Avoid buzzwords like "Cassandra scales infinitely" or "MongoDB is web-scale."
   - State specific computational complexities, disk I/O implications, memory bounds, and network hop costs.
4. **Local-First & Cost-Safe:**
   - All contributions must run locally via Docker Compose or pure Python standard library scripts.
   - Never introduce code requiring paid cloud subscriptions.
5. **Separate Solutions:**
   - Exercises and challenge descriptions reside in `exercises/`, `drills/`, or `phases/`.
   - Complete reference solutions must be placed strictly in `solutions/` to preserve learning progression.
6. **Verification Script:**
   - Run `./scripts/verify-repository.sh` before submitting any PR. It must pass with 0 errors.
