# Project 02: Real-Time Global Leaderboard Engine

Demonstrates how Redis Sorted Sets (`ZSET`) combine an internal hash table with a probabilistic Skip List to achieve $O(\log N)$ updates, instant rank calculations, and paginated range retrieval.

---

## Architectural Mechanics

In a relational database (SQL), calculating a player's rank requires:
```sql
SELECT COUNT(*) FROM players WHERE score > (SELECT score FROM players WHERE id = 'user_42');
```
Across 10,000,000 players, this query requires scanning table indexes or sorting records, causing immense database CPU saturation under concurrent writes.

Redis Sorted Sets use two internal data structures for the same key:
1. **Hash Table (`dict`):** Maps `member -> score` for $O(1)$ score lookups (`ZSCORE`).
2. **Skip List (`zskiplist`):** Maintains elements sorted by score with multi-level span pointers.
   * `ZADD` / `ZINCRBY`: $O(\log N)$ insert / rebalance.
   * `ZRANK` / `ZREVRANK`: $O(\log N)$ rank calculation by summing span pointers.
   * `ZRANGE` / `ZREVRANGE`: $O(\log N + M)$ range retrieval.

---

## Running the Simulation

```bash
# Ensure Redis is running
make up

# Run leaderboard tournament simulation
python3 projects/02-leaderboard/leaderboard.py
```
