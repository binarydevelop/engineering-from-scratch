# Systems Mental Models for Redis

> **Motto:** Understand it. Build it. Measure it. Break it. Fix it. Scale it. Ship it.

A software engineer who treats Redis as *"just a fast Python dictionary in the cloud"* will design systems that crash under high concurrency, lose data during restarts, corrupt state across race conditions, and saturate network cards.

This document collects the foundational architectural diagrams and system mental models taught across the curriculum.

---

## 1. The Naive Black Box vs. First-Principles Reality

### The Naive Intuition (Cargo Cult)
```text
┌────────────────────────────────────────────────────────┐
│  Client App                                            │
│    │                                                   │
│    ├── redis.set("user:1", "{...}") ──► [ MAGIC FAST   │
│    │                                    DICTIONARY ]   │
│    └── redis.get("user:1")          ◄── [ IN CLOUD   ]   │
└────────────────────────────────────────────────────────┘
Problems with this view:
- Why did SET block when another client ran KEYS *?
- Where did my data go when the server rebooted?
- Why did memory explode when storing 10M tiny strings?
- Why is SET failing with OOM even though the disk has 500GB free?
```

### The First-Principles Reality
```text
┌──────────────────────────────────────────────────────────────────────────────────┐
│ HOST OPERATING SYSTEM & KERNEL                                                   │
│                                                                                  │
│   Client TCP Socket (FD 12) ──── TCP Packets (RESP bytes) ───► Kernel Rx Buffer │
│                                                                        │         │
├────────────────────────────────────────────────────────────────────────┼─────────┤
│ REDIS SERVER PROCESS (Single-Threaded Engine Core)                     │         │
│                                                                        ▼         │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │ 1. I/O Multiplexer (epoll / kqueue / select)                             │   │
│   │    Wakes up event loop when FD 12 has readable bytes                     │   │
│   └────────────────────────────────────┬─────────────────────────────────────┘   │
│                                        ▼                                         │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │ 2. Client Query Buffer & RESP Parser                                     │   │
│   │    Parses: *3\r\n$3\r\nSET\r\n$6\r\nuser:1\r\n$4\r\nJohn\r\n             │   │
│   └────────────────────────────────────┬─────────────────────────────────────┘   │
│                                        ▼                                         │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │ 3. Command Table Lookup & Execution                                      │   │
│   │    Finds "setCommand" in command hash table; runs arity/type checks      │   │
│   └────────────────────────────────────┬─────────────────────────────────────┘   │
│                                        ▼                                         │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │ 4. Main Keyspace Dictionary (dict.c)                                     │   │
│   │    Allocates robj, inserts key SDS, inserts value SDS, updates 24-bit    │   │
│   │    LRU clock, checks maxmemory eviction budget                           │   │
│   └─────────────────┬──────────────────┬─────────────────┬───────────────────┘   │
│                     │                  │                 │                       │
│                     ▼                  ▼                 ▼                       │
│             ┌──────────────┐   ┌──────────────┐  ┌──────────────┐                │
│             │ TTL Dict     │   │ AOF Buffer   │  │ Repl Backlog │                │
│             │ (expires_at) │   │ (append-only)│  │ (ring buffer)│                │
│             └──────────────┘   └──────────────┘  └──────────────┘                │
│                                        │                                         │
│                                        ▼                                         │
│   ┌──────────────────────────────────────────────────────────────────────────┐   │
│   │ 5. Client Output Buffer & Response Serialization                         │   │
│   │    Encodes "+OK\r\n" -> writes to Tx buffer -> sends over socket         │   │
│   └──────────────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Complete Life Cycle of a Redis Command

When a client runs `SET key value`, the execution pipeline flows sequentially through the single thread:

```text
[ Client Application ]
        │
        │ 1. Encode command to RESP bytes: *3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n
        ▼
[ Client OS Network Stack ]
        │
        │ 2. TCP Handshake / Socket write() -> IP Packet
        ▼
[ Network Transport (RTT: 0.1ms - 50ms) ]
        │
        ▼
[ Redis Host Kernel Network Buffer ]
        │
        │ 3. Kernel marks socket File Descriptor (e.g. FD 14) as READABLE
        ▼
[ Redis aeEventLoop (ae.c) ]
        │
        │ 4. epoll_wait() / kqueue() returns FD 14
        ▼
[ readQueryFromClient() ]
        │
        │ 5. read() socket bytes into client->querybuf
        ▼
[ processInputBuffer() ]
        │
        │ 6. Parse RESP protocol into client->argv and client->argc
        ▼
[ processCommand() ]
        │
        │ 7. Lookup command in server.commands dictionary
        │    Check authentication, maxmemory budget, command arity
        ▼
[ call() -> setCommand() ]
        │
        │ 8. Search / insert into server.db[0].dict
        │    Allocate SDS memory via jemalloc
        │    Store expiration in server.db[0].expires (if EX/PX provided)
        │    Feed AOF buffer (if appendonly yes)
        │    Feed replication backlog buffer (if replicas connected)
        ▼
[ addReply() ]
        │
        │ 9. Write RESP status reply ("+OK\r\n") to client->buf
        ▼
[ writeToClient() / Socket write() ]
        │
        │ 10. Flush output buffer over TCP socket back to client
        ▼
[ Client Application receives "+OK" ]
```

---

## 3. The `redisObject` Memory Header

Every key and value in Redis is wrapped in a 16-byte C structure (`robj` in `server.h`):

```text
+-------------------+-------------------+--------------------+--------------------+
| type (4 bits)     | encoding (4 bits) | lru/lfu (24 bits)  | refcount (32 bits) |
| OBJ_STRING / HASH | RAW / LISTPACK /  | Last access time   | Reference count    |
| LIST / SET / ZSET | INTSET / HT       | or LFU frequency   | for memory sharing |
+-------------------+-------------------+--------------------+--------------------+
| ptr (64 bits / 8 bytes)                                                         |
| Pointer to actual payload (e.g. SDS string, Dict, Listpack buffer)              |
+---------------------------------------------------------------------------------+
```
**Consequence:** Even an empty string or 1-byte integer stored in Redis has at least **16 bytes of metadata header** before accounting for key SDS, dict entry pointers (`dictEntry` = 24 bytes), and memory allocator page fragmentation.

---

## 4. Expiration vs. Eviction

Learners frequently confuse these two independent memory reclamation systems:

```text
+---------------------------------------------------------------------------------+
|                               HOW MEMORY IS FREED                              |
+---------------------------------------------------------------------------------+
|                                                                                 |
|  1. EXPIRATION (TTL-driven)               2. EVICTION (Memory-budget-driven)    |
|                                                                                 |
|  Trigger: Time elapses past TTL.           Trigger: used_memory >= maxmemory.   |
|                                                                                 |
|  Passive: Deleted on read access.          Sampling: Redis picks N random keys  |
|  Active:  serverCron samples 20 keys                 (default 5), evaluates     |
|           10 times / sec. Reclaims memory            LRU clock / LFU counter,   |
|           independently of memory pressure.          and evicts the best key.   |
|                                                                                 |
|  Status: Normal operational lifecycle.     Status: Emergency defense against    |
|                                                    Out-Of-Memory (OOM) crashes. |
+---------------------------------------------------------------------------------+
```

---

## 5. Persistence: RDB vs. AOF

```text
                                  CLIENT WRITES
                                        │
                                        ▼
                                 [ REDIS MEMORY ]
                                  │            │
             Periodic Fork        │            │ Write-Ahead Log
             BGSAVE (COW)         │            │ (every write or every sec)
                    │             │            │
                    ▼             ▼            ▼
             [ Child Process ]            [ AOF Buffer ]
                    │                           │
                    │ Copy-on-Write Pages       │ fsync() policy
                    ▼                           ▼
             [ dump.rdb ]                [ appendonly.aof ]
        (Compact binary snapshot)     (Sequential RESP command log)
```

---

## 6. Caching Architecture & Cache Stampede

```text
                           STANDARD CACHE-ASIDE
                           
               1. GET key
  Client ──────────────────────► Redis Cache
    │                                │
    │ ◄─── Hit (Return Data) ────────┘
    │
    │ (On Miss)
    │
    ├─ 2. Query DB ────────────► Persistent Database (Postgres)
    │                                │
    │ ◄─── Row Returned ─────────────┘
    │
    └─ 3. SET key with TTL ────► Redis Cache
```

### The Thundering Herd (Stampede)
When a hot key expires at $T_0$, 5,000 incoming requests miss simultaneously:
```text
  5,000 Concurrent Requests ────► Redis (MISS! TTL expired)
             │
             │ All 5,000 execute DB query simultaneously
             ▼
     [ PostgreSQL DB ] ──► SATURATED / CPU 100% / CONNECTION POOL EXHAUSTED!
```

### Mitigation: Distributed Mutex (Single-Flight)
```text
  5,000 Requests ──► Redis (MISS)
             │
             ├── Request 1: SET lock:key token NX EX 5 (SUCCEEDS) ──► Queries DB & updates cache
             │
             └── Requests 2..5000: SET lock:key NX (FAILS) ─────────► Sleep 50ms & retry cache read
```

---

## 7. Primary-Replica Replication & Backlog Ring Buffer

```text
  [ CLIENT ] ── Writes ──► [ PRIMARY (Port 6379) ]
                                 │
                                 ├── 1. Apply to memory keyspace
                                 ├── 2. Append to Circular Backlog Buffer (1MB)
                                 │      [ ... bytes offset 104230 .. 204230 ... ]
                                 │
                                 └── 3. Async stream replication stream ──► [ REPLICA ]
                                                                             Reads & matches offset
```

---

## 8. Redis Cluster: 16,384 Hash Slots

```text
                     Client Request: GET user:9842
                                  │
                                  │ Slot = CRC16("user:9842") % 16384 = 7812
                                  ▼
                   ┌─────────────────────────────┐
                   │ Cluster Node A              │
                   │ Responsible for: 0 - 5460   │
                   └──────────────┬──────────────┘
                                  │
                                  │ -MOVED 7812 10.0.0.2:6379
                                  ▼
                            Client redirects
                                  │
                                  ▼
                   ┌─────────────────────────────┐
                   │ Cluster Node B              │
                   │ Responsible for: 5461 - 10922│
                   │ (Processes GET user:9842)   │
                   └─────────────────────────────┘
```

---

## 9. Pub/Sub (Ephemeral) vs. Streams (Durable Log)

```text
                         PUB/SUB (Fire & Forget)
  Publisher ── PUBLISH ──► Channel ──► [ Subscriber A (Online)  ] ── Receives
                                   ──► [ Subscriber B (Offline) ] ── LOST FOREVER!
  
                        REDIS STREAMS (Persistent Log)
  Producer ── XADD ──► [ Radix Tree Append-Only Stream ] (ID: 1711000000-0, 1711000000-1)
                                   │
                                   ├── Consumer Group "workers"
                                   │     ├── Worker 1: Reads msg 1 (In PEL until XACK)
                                   │     └── Worker 2: Reads msg 2 (In PEL until XACK)
                                   │
                                   └── Reconnected Worker: Reads from last acknowledged ID
```
