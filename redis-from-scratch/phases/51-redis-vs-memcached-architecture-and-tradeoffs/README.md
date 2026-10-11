# Phase 51: Redis vs Memcached: Deep Engine Architecture and Selection Framework

## 1. Why This Matters for MAANG & Senior/Staff Roles
A standard System Design interview trap is using Redis and Memcached interchangeably. While both are in-memory data stores, their internal thread models, memory allocation engines, and operational profiles are radically different. Senior engineers must explain precisely why one outperforms the other under specific concurrency and data access patterns.

---

## 2. Core Concepts & Architecture Deep-Dive
### Internal Architecture Comparison
1. **Thread Model & Concurrency**:
   - **Memcached**: Multi-threaded architecture utilizing thread-safe mutexes. Scales vertically to consume 32-64 CPU cores on a single host. Excels at high-core multi-threaded CPU saturation for simple GET/SET workloads.
   - **Redis**: Single-threaded event loop (epoll-based) for command execution, with auxiliary threads for I/O and disk flushing. Eliminates mutex contention, context switching, and race conditions, but cannot utilize multi-core machines on a single instance without running multiple processes or Redis Cluster.
2. **Memory Management**:
   - **Memcached (Slab Allocator)**: Pre-allocates memory into Slabs and Chunks to eliminate memory fragmentation. Disadvantage: slab calcification if item sizes vary widely over time.
   - **Redis (jemalloc / glibc malloc)**: Allocates raw memory dynamically per object. More memory efficient for complex structures, but susceptible to memory fragmentation over long operational periods.
3. **Data Richness**:
   - **Memcached**: Pure key-value (Strings/Blobs only). To update a list element, application must fetch entire object, deserialize, update, serialize, and write back (high network overhead and race condition hazard).
   - **Redis**: Rich native data structures (Strings, Hashes, Lists, Sets, Sorted Sets, HyperLogLog, Bitmaps, Streams). In-place atomic mutations (`HSET`, `ZINCRBY`, `LPUSH`) without network transfer.

---

## 3. High-Value Interview Angle & Failure Modes
### Trade-Offs & Selection Matrix
- **Choose Memcached when**:
  - Simple key-value caching of static objects (HTML fragments, session tokens).
  - Multi-threaded read throughput on large multi-core hardware where scaling horizontal instances is undesirable.
  - No need for data persistence, replication, or advanced data types.
- **Choose Redis when**:
  - Rich data manipulation required (leaderboards via Sorted Sets, rate limiters via sliding window, set intersection).
  - Persistence is required (RDB snapshots, AOF append log).
  - Pub/Sub, Redis Streams, or Lua atomic script transactions needed.
  - High availability via Sentinel or clustering via Redis Cluster is required.

---

## 4. Hands-On Practice & Implementation Drills
### Benchmark & Memory Verification Commands
```bash
# Verify Redis memory fragmentation ratio
redis-cli info memory
# Look for: mem_fragmentation_ratio (ideal: 1.0 - 1.5; > 1.5 indicates severe fragmentation)

# Trigger active memory defragmentation
redis-cli config set activedefrag yes
```

---

## 5. Key Takeaways & Cheat Sheet
- Memcached is multi-threaded with a slab allocator; excels at high-throughput simple string caching.
- Redis is single-threaded event loop; excels at rich data types and in-place atomic operations.
- Redis provides persistence (RDB/AOF), replication, and clustering; Memcached is an ephemeral cache.
- Articulate the threading model and data structure manipulation capabilities in interviews.
