# Redis Command Reference & Time Complexity Matrix

A reference of the commands explored across the 51 phases, classified by time complexity, data type, and operational risk level.

---

## 1. Strings (Phase 06)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **SET** | `SET key value [EX s\|PX ms] [NX\|XX]` | $O(1)$ | Low | Sets string value with optional expiration and existence guards. |
| **GET** | `GET key` | $O(1)$ | Low | Retrieves string value. Returns nil if missing. |
| **INCR** / **DECR** | `INCR key` / `DECR key` | $O(1)$ | Low | Atomic integer increment/decrement. Creates key at 0 if missing. |
| **MSET** | `MSET k1 v1 k2 v2 ...` | $O(N)$ | Medium | Sets multiple keys atomically. $N$ is count of keys. |
| **MGET** | `MGET k1 k2 ...` | $O(N)$ | Medium | Returns multiple values in one round-trip. |
| **APPEND** | `APPEND key value` | $O(1)$ amortized | Low | Appends value to existing string. |
| **STRLEN** | `STRLEN key` | $O(1)$ | Low | Returns length in bytes from SDS header. |

---

## 2. Hashes (Phase 07)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **HSET** | `HSET key field val [field val...]` | $O(1)$ per field | Low | Sets one or more fields in a hash. |
| **HGET** | `HGET key field` | $O(1)$ | Low | Retrieves a single field. |
| **HMGET** | `HMGET key f1 f2 ...` | $O(N)$ | Low | Retrieves multiple fields. |
| **HGETALL** | `HGETALL key` | $O(N)$ | **HIGH** | Returns all fields/values. DANGEROUS on giant hashes with 100k+ fields. |
| **HSCAN** | `HSCAN key cursor [COUNT c]` | $O(1)$ per step | Low | Safe cursor-based iteration through hash fields. |
| **HINCRBY** | `HINCRBY key field delta` | $O(1)$ | Low | Atomically increments numeric hash field. |

---

## 3. Lists (Phase 08)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **LPUSH** / **RPUSH**| `LPUSH key val...` | $O(1)$ per item | Low | Inserts at head/tail of quicklist. |
| **LPOP** / **RPOP** | `LPOP key [count]` | $O(1)$ | Low | Removes and returns items from head/tail. |
| **LRANGE** | `LRANGE key start stop` | $O(S + N)$ | Medium | Returns range. $S$ is offset distance from nearest head/tail. |
| **LLEN** | `LLEN key` | $O(1)$ | Low | Returns count of items in list. |

---

## 4. Sets (Phase 09)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **SADD** | `SADD key member...` | $O(1)$ per member | Low | Adds unique members to set. |
| **SREM** | `SREM key member...` | $O(1)$ per member | Low | Removes members from set. |
| **SISMEMBER** | `SISMEMBER key member` | $O(1)$ | Low | Constant-time membership test. |
| **SMEMBERS** | `SMEMBERS key` | $O(N)$ | **HIGH** | Returns all members. Blocks thread if set has millions of members. |
| **SSCAN** | `SSCAN key cursor` | $O(1)$ per step | Low | Incremental cursor iterator. |
| **SINTER** / **SUNION**| `SINTER k1 k2...` | $O(N \times M)$ | **HIGH** | Set intersection/union. CPU-intensive on large cardinality. |

---

## 5. Sorted Sets (Phase 10)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **ZADD** | `ZADD key score member...` | $O(\log N)$ | Low | Adds member with score into skiplist + dict. |
| **ZRANGE** | `ZRANGE key min max [BYSCORE]` | $O(\log N + M)$ | Medium | Returns elements ordered by rank or score. $M$ is returned count. |
| **ZRANK** | `ZRANK key member` | $O(\log N)$ | Low | Computes 0-based rank of member via skiplist span traversal. |
| **ZSCORE** | `ZSCORE key member` | $O(1)$ | Low | Retrieves score directly from hash table lookup. |
| **ZINCRBY** | `ZINCRBY key delta member` | $O(\log N)$ | Low | Atomically increments member score and rebalances skiplist. |

---

## 6. Expiration & Keyspace Management (Phases 11-13)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **EXPIRE** / **PEXPIRE**| `EXPIRE key seconds` | $O(1)$ | Low | Sets TTL on existing key. |
| **TTL** / **PTTL** | `TTL key` | $O(1)$ | Low | Returns remaining TTL (-1 if persistent, -2 if missing). |
| **PERSIST** | `PERSIST key` | $O(1)$ | Low | Removes expiration deadline from key. |
| **DEL** | `DEL key...` | $O(N)$ | Medium | Deletes keys. If value is large collection, memory deallocation blocks. |
| **UNLINK** | `UNLINK key...` | $O(1)$ sync | Low | Non-blocking delete. Reclaims memory in background thread (`bio.c`). |
| **KEYS** | `KEYS pattern` | $O(N)$ | **CRITICAL** | NEVER run in production. Scans whole database; blocks event loop. |
| **SCAN** | `SCAN cursor [MATCH p] [COUNT c]` | $O(1)$ per step | Low | Safe, non-blocking keyspace cursor iteration. |

---

## 7. Streams & Messaging (Phases 26-28)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **PUBLISH** | `PUBLISH channel message` | $O(N + M)$ | Low | Publishes to connected subscribers. Fire-and-forget. |
| **SUBSCRIBE** | `SUBSCRIBE channel` | $O(1)$ | Low | Enters subscriber loop. |
| **XADD** | `XADD key * field val...` | $O(1)$ | Low | Appends message entry to persistent stream radix tree. |
| **XREAD** | `XREAD [BLOCK ms] STREAMS k id` | $O(N)$ | Low | Reads entries newer than ID. Optional blocking poll. |
| **XGROUP CREATE** | `XGROUP CREATE k grp id [MKSTREAM]` | $O(1)$ | Low | Creates consumer group tracking stream offset. |
| **XREADGROUP** | `XREADGROUP GROUP grp csm STREAMS k >` | $O(N)$ | Low | Reads unassigned messages for a consumer in group. |
| **XACK** | `XACK key grp id...` | $O(1)$ | Low | Acknowledges message and removes from Pending Entries List (PEL). |

---

## 8. Transactions & Scripting (Phases 16-17)

| Command | Syntax | Complexity | Operational Risk | Description |
| :--- | :--- | :--- | :--- | :--- |
| **MULTI** | `MULTI` | $O(1)$ | Low | Enters transactional buffering mode. |
| **EXEC** | `EXEC` | $O(N)$ commands | Medium | Executes queued commands sequentially and atomically. |
| **DISCARD** | `DISCARD` | $O(1)$ | Low | Clears transaction queue without executing. |
| **WATCH** | `WATCH key...` | $O(1)$ per key | Low | Sets optimistic concurrency watch flag on keys. |
| **EVAL** / **FCALL** | `EVAL script numkeys [keys...]` | Script-dependent | **HIGH** | Runs Lua script atomically on engine core. Infinite loops hang Redis! |
