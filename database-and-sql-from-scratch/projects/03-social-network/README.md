# Project 03: Social Network Graph & Feed Engine

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Project Overview

This project models social interactions, follower graph relationships, mutual connections, post engagement rates, and feed generation.

---

## 2. Key Queries Implemented

- Follower and following counts
- Mutual follow pairs (graph cycle detection)
- Popular posts by likes and comments
- User activity feeds sorted chronologically
- Engagement rate scores
- Active users vs lurkers
- Composite index optimization for feed queries
- Keyset cursor pagination (eliminating slow `OFFSET`)

---

## 3. Running the Social Lab

```bash
make seed-social
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab < projects/03-social-network/social_queries.sql
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab < projects/03-social-network/indexing_and_pagination.sql
```
