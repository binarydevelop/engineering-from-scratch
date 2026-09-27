# Project 05: Build a Mini Relational Database Engine in Python

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Project Overview

In this project, you strip away the complexity of network layers and SQL parsers to implement the core mechanisms of a relational database in pure Python:
- **Table Storage:** Schema verification, in-memory tuple layout, primary key dictionary index.
- **Constraints:** Uniqueness enforcement and failure propagation.
- **Secondary Indexing:** Hash-based inverted index for fast attribute lookups.
- **Relational Algebra Operators:**
  - Selection ($\sigma$) -> Filtering
  - Projection ($\pi$) -> Column slicing
  - Joins ($\bowtie$) -> Nested Loop ($O(N \times M)$) vs Hash Join ($O(N + M)$).

---

## 2. Running Tests

```bash
pytest projects/05-mini-relational-db/test_engine.py
```
