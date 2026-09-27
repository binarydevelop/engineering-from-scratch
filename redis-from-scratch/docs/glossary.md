# Redis & Systems Engineering Glossary

A rigorous reference of core systems concepts, networking mechanisms, storage trade-offs, and Redis internals.

---

### In-Memory Database & Storage Hierarchy
* **Volatile Memory (RAM/DRAM):** High-speed random-access memory directly addressable by the CPU (~50–100 ns latency). Data is lost when power is disconnected or the process crashes.
* **Non-Volatile Storage (NVMe / SSD / HDD):** Persistent block-based storage (~10–100 µs for NVMe flash; ~5–10 ms for spinning disk). Offers durability at the cost of 2 to 5 orders of magnitude higher latency.
* **In-Memory Database:** A database that stores its primary dataset directly in memory addresses rather than paging disk blocks through an OS buffer cache. Reads and writes execute at RAM speeds without random disk seeks.
* **Resident Set Size (RSS):** The portion of memory occupied by a process that is held in actual main physical RAM (excluding swapped pages).
* **Memory Fragmentation Ratio:** Calculated as $\frac{\text{used\_memory\_rss}}{\text{used\_memory}}$. A ratio $> 1.5$ indicates the operating system has allocated more physical pages to the allocator than the actual live dataset bytes, often caused by frequent allocations and deallocations.

---

### Networking & Event Loops
* **I/O Multiplexing:** An operating system capability (`epoll` on Linux, `kqueue` on macOS/BSD, `select` cross-platform) that allows a single thread to monitor thousands of file descriptors (sockets) simultaneously, waking up only when a descriptor becomes readable or writable.
* **Event Loop:** An architectural pattern where a single central loop continually waits for events (network I/O, timers, signals) and dispatches handlers sequentially. Redis’s `ae.c` implements this pattern.
* **Round Trip Time (RTT):** The time required for a network packet to travel from a client to the server and back. Typically 0.1 ms on localhost, 0.5–2 ms within a data center, and 20–100+ ms across regions.
* **RESP (Redis Serialization Protocol):** The binary-safe, text-framed, human-readable wire protocol used between Redis clients and servers. Standardized across RESP2 (5 basic types) and RESP3 (adds maps, sets, booleans, attributes, doubles).

---

### Internal Data Structures (Pinned Redis 7.4 Baseline)
* **SDS (Simple Dynamic String):** A binary-safe C string wrapper with explicit length tracking (`len`), allocated buffer capacity (`alloc`), and constant-time $O(1)$ length queries that avoids null-byte termination bugs.
* **Dict (Hash Table):** The central key-value index in Redis. Implemented with two hash tables (`ht[0]` and `ht[1]`) to perform **progressive rehashing** (moving buckets incrementally during reads and writes) so that table expansion never causes a catastrophic latency spike.
* **Listpack:** A compact memory-efficient sequence of serialized elements encoded into a single continuous byte buffer. Replaced legacy `ziplist` in Redis 7.0+ for memory-optimized small hashes and sorted sets.
* **Quicklist:** A two-level doubly linked list where each node contains a `listpack`. Used by Redis to represent the `LIST` data type, balancing constant-time push/pop at the boundaries with compact sequential storage.
* **Skiplist:** A probabilistic ordered data structure consisting of multiple forward-pointer levels over a sorted linked list. Used in Redis Sorted Sets (`ZSET`) to provide $O(\log N)$ search, insertion, and range queries.

---

### Expiration & Eviction
* **TTL (Time to Live):** The remaining duration (in seconds or milliseconds) before a key is marked expired.
* **Passive Expiration (Lazy):** An expired key is deleted only when a client explicitly attempts to read or write to it. If never read again, it remains in memory.
* **Active Expiration (Periodic Cycle):** A background timer task run by the Redis server 10 times per second (`serverCron`). It samples 20 random keys with TTLs from the active dictionary, deletes any that have expired, and repeats if more than 25% of the sampled keys were expired.
* **Eviction:** The process of reclaiming memory when `used_memory` reaches `maxmemory`. Unlike expiration (which is TTL-driven), eviction forcibly evicts keys based on configured policies (`noeviction`, `allkeys-lru`, `volatile-lru`, `allkeys-lfu`, `volatile-lfu`, `allkeys-random`, `volatile-random`, `volatile-ttl`).
* **Approximated LRU/LFU:** Redis does not maintain an exact doubly linked list of all dataset keys (which would cost 16–24 bytes of pointer overhead per key). Instead, it stores a 24-bit timestamp/counter in each `redisObject` header and samples a configurable number of random keys (default 5), evicting the best candidate among that sample.

---

### Persistence & Durability
* **RDB (Redis Database Snapshot):** A point-in-time binary snapshot of the entire Redis dataset serialized to disk (`dump.rdb`). Generated via `BGSAVE`, which calls Linux `fork()` to create a child process utilizing **Copy-on-Write (COW)** memory pages.
* **AOF (Append-Only File):** A write-ahead log that records every state-changing command received by the server in RESP format. Replaying the log on reboot reconstructs the dataset.
* **fsync Policies:**
  * `always`: Slower, syncs after every write command. High durability, low throughput.
  * `everysec` (Default): Background thread runs `fsync()` once per second. Maximum window of lost data is typically 1–2 seconds.
  * `no`: Delegates disk flushing entirely to the OS buffer cache (usually 30 seconds). Fastest, lowest durability.
* **AOF Rewrite (`BGREWRITEAOF`):** A background process that reads current memory state and writes the minimal stream of commands needed to recreate that state, discarding redundant historical log entries.

---

### Caching Patterns & Failure Modes
* **Cache-Aside (Lazy Loading):** The application first queries the cache. On a cache hit, data is returned. On a cache miss, the application queries the persistent database, writes the result to the cache with a TTL, and returns it.
* **Write-Through:** The application writes data to the cache, and the cache synchronously writes to the underlying database before acknowledging success.
* **Write-Behind (Write-Back):** The application writes data to the cache, which immediately acknowledges success and asynchronously flushes the write to the database in batches.
* **Cache Stampede (Thundering Herd):** When an intensely requested key expires, hundreds or thousands of concurrent incoming requests simultaneously experience a cache miss and all query the database simultaneously, causing saturation or downtime.
* **Hot Key:** A key that receives a disproportionate share of read or write traffic (e.g., millions of requests/sec to a celebrity profile), bottlenecking the specific single thread or single Redis node holding that key.

---

### Replication & High Availability
* **Primary-Replica Replication:** An asynchronous replication architecture where writes are accepted by a single Primary node and streamed to one or more read-only Replicas.
* **Replication Backlog:** A circular memory ring buffer maintained by the primary. If a replica disconnects briefly, it can reconnect and perform a **Partial Resynchronization (`PSYNC`)** by fetching missed byte offsets rather than transferring a full RDB snapshot.
* **Replication Lag:** The byte or temporal offset between the primary's `master_repl_offset` and the replica's acknowledged read offset.
* **Redis Sentinel:** A distributed consensus and monitoring system that supervises standalone Redis instances. Sentinel handles health monitoring, automatic failover (promoting a replica if the primary dies), and service discovery for clients.
* **Split-Brain:** A network failure mode where a partition isolates the old primary from its replicas, causing both the isolated primary and a newly promoted primary to accept divergent writes simultaneously.

---

### Partitioning & Clustering
* **Hash Slots:** Redis Cluster partitions keyspace into exactly **16,384** logical hash slots ($2^{14}$). Every key is mapped to a slot using `CRC16(key) mod 16384`. Nodes in the cluster are assigned contiguous or discrete ranges of slots.
* **Hash Tags:** Substrings wrapped in `{...}` inside a key name (e.g., `{user:123}:profile` and `{user:123}:orders`). Only the text between `{` and `}` is hashed, ensuring related keys land on the exact same hash slot and same cluster node, allowing multi-key atomic transactions.
* **MOVED Redirect:** A permanent redirection error returned by a Redis Cluster node when a client sends a command for a key belonging to a slot managed by a different node.
* **ASK Redirect:** A temporary redirection error returned during slot migration while data keys are actively moving between source and target nodes.

---

### Concurrency & Streaming
* **Pipelining:** A client technique that writes multiple commands onto the TCP socket buffer sequentially without waiting for individual replies, reading all replies back in a single batch. Drastically reduces the amortized cost of network Round Trip Time (RTT).
* **Optimistic Concurrency Control (`WATCH`):** Monitors specified keys for modifications. If another client writes to any watched key before `EXEC` runs, the transaction aborts and returns a null reply, prompting the client to retry.
* **Redis Streams:** An append-only log data structure indexed by millisecond timestamp and sequence ID (`<millisecondsTime>-<sequenceNumber>`). Supports multiple independent consumer groups, at-least-once message delivery, explicit acknowledgment (`XACK`), and pending entry tracking (`XPENDING`).
