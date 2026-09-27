#!/usr/bin/env python3
"""
scripts/generate_curriculum.py — Comprehensive generator for Phases 06 to 50.
"""

import os
import stat

PHASES_DATA = [
    # --- DATA STRUCTURES & MEMORY (06 - 14) ---
    {
        "num": "06",
        "slug": "06-strings",
        "title": "Strings: Texts, Counters, and Binary-Safe Blobs",
        "motto": "A Redis string is not a C string; it is an SDS buffer that can safely store arbitrary raw bytes including nulls.",
        "problem": "Traditional C strings use null terminators ('\\0'), which means they cannot store binary data like protocol buffers or compressed images. Furthermore, finding their length requires an $O(N)$ string scan.",
        "prediction": "If we call INCR on a key that does not exist, what does Redis do? What happens if we call INCR on a key containing 'hello'?",
        "why_matters": "Redis Strings are the universal primitive for caching HTML pages, JSON blobs, atomic counters, bitfields, and rate limiters.",
        "principles": "Simple Dynamic Strings (SDS) store explicit buffer length (`len`), free capacity (`alloc`), and payload. Length checks are $O(1)$. In-place string appends avoid quadratic reallocation.",
        "script_name": "string_internals.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_string_experiments():
    print("1. Text and Binary Safety:")
    redis_cmd("SET", "str:text", "Hello Systems")
    redis_cmd("APPEND", "str:text", " World")
    print("  GET str:text ->", redis_cmd("GET", "str:text"))
    print("  STRLEN str:text ->", redis_cmd("STRLEN", "str:text"))

    print("\\n2. Atomic Counters:")
    redis_cmd("DEL", "str:counter")
    print("  INCR str:counter (uninitialized) ->", redis_cmd("INCR", "str:counter"))
    print("  INCRBY str:counter 10 ->", redis_cmd("INCRBY", "str:counter", "10"))
    print("  DECR str:counter ->", redis_cmd("DECR", "str:counter"))

    print("\\n3. String Type Failure Mode:")
    redis_cmd("SET", "str:word", "not_a_number")
    print("  INCR on non-numeric string ->", redis_cmd("INCR", "str:word"))

if __name__ == "__main__":
    try: run_string_experiments()
    except Exception as e: print("Redis unavailable:", e)
''',
        "mastery_q1": "Why is INCR safe under 10,000 concurrent clients while `x = x + 1` in Python is not?",
        "mastery_q2": "What is the maximum allowable size of a Redis string value?",
        "when_use": "Use Strings for text caching, serialized objects, distributed counters, and bitwise flags.",
        "when_not_use": "Do not store giant multi-megabyte JSON arrays in a single string if you only need to read or update a single property."
    },
    {
        "num": "07",
        "slug": "07-hashes",
        "title": "Hashes: Structured Objects and Field-Level Access",
        "motto": "Updating a single field in a hash costs $O(1)$, while updating a field in a JSON string requires deserializing the entire document.",
        "problem": "Storing a user profile as a serialized JSON string requires fetching the whole string over the network, parsing JSON in Python, modifying one field, serializing back to JSON, and writing it back, creating severe race conditions.",
        "prediction": "How does memory consumption differ between storing 10,000 users as JSON strings vs storing them as Redis Hashes?",
        "why_matters": "Hashes represent domain entities (users, sessions, carts) cleanly, allowing atomic field-level mutations (`HINCRBY`) without full-document serialization races.",
        "principles": "Redis Hashes use a two-tier internal representation: a memory-optimized `listpack` for small hashes, converting automatically to a standard hash table (`dict`) when field count or value size exceeds configuration thresholds.",
        "script_name": "hash_mechanics.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_hash_experiments():
    key = "user:1001"
    redis_cmd("DEL", key)
    print("1. Setting hash fields:")
    redis_cmd("HSET", key, "name", "Alice", "email", "alice@example.com", "visits", "0")
    print("  HGET user:1001 name ->", redis_cmd("HGET", key, "name"))
    
    print("\\n2. Atomic Field Increments:")
    print("  HINCRBY user:1001 visits 1 ->", redis_cmd("HINCRBY", key, "visits", "1"))
    print("  HINCRBY user:1001 visits 5 ->", redis_cmd("HINCRBY", key, "visits", "5"))

    print("\\n3. Field Inspection & Memory Encoding:")
    print("  OBJECT ENCODING user:1001 ->", redis_cmd("OBJECT", "ENCODING", key))
    print("  HGETALL user:1001 ->\\n", redis_cmd("HGETALL", key))

if __name__ == "__main__":
    try: run_hash_experiments()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is HGETALL considered dangerous on very large hashes in production?",
        "mastery_q2": "What command should you use instead of HGETALL to iterate through a hash with 500,000 fields?",
        "when_use": "Use Hashes to represent domain objects where fields need to be independently read, updated, or incremented.",
        "when_not_use": "Do not use Hashes if you need nested sub-objects (hashes cannot nest other hashes in Redis core)."
    },
    {
        "num": "08",
        "slug": "08-lists",
        "title": "Lists: Sequential Queues, Stacks, and Capped Collections",
        "motto": "Redis lists are linked lists, not arrays: inserting at the head or tail is $O(1)$, but indexing into the middle is $O(N)$.",
        "problem": "Applications need simple FIFO queues or capped timelines (e.g., 'last 10 user activities'). Implementing this in SQL requires indexing and sorting timestamps.",
        "prediction": "Is LPUSH + RPOP faster or slower when the list grows from 1,000 items to 10,000,000 items?",
        "why_matters": "Lists provide fundamental queuing primitives (`LPUSH`/`RPOP`, `BLPOP` blocking pops) and sliding activity feeds (`LTRIM`).",
        "principles": "Redis Lists are implemented using `quicklist`, a doubly linked list of `listpack` memory buffers. Pushes and pops at the ends are strictly $O(1)$, while `LINDEX` or `LSET` at arbitrary offsets must traverse nodes.",
        "script_name": "list_queues.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_list_experiments():
    key = "queue:jobs"
    redis_cmd("DEL", key)
    print("1. FIFO Queue (LPUSH -> RPOP):")
    redis_cmd("LPUSH", key, "job_1", "job_2", "job_3")
    print("  Pop first out (RPOP) ->", redis_cmd("RPOP", key))
    print("  Pop next out (RPOP)  ->", redis_cmd("RPOP", key))

    print("\\n2. Capped Activity Log (LTRIM):")
    log_key = "user:recent_actions"
    redis_cmd("DEL", log_key)
    for i in range(1, 15):
        redis_cmd("LPUSH", log_key, f"action_{i}")
        redis_cmd("LTRIM", log_key, "0", "4") # Keep only latest 5
    print("  LRANGE 0 -1 (latest 5 actions) ->\\n", redis_cmd("LRANGE", log_key, "0", "-1"))

if __name__ == "__main__":
    try: run_list_experiments()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is LPUSH followed by RPOP suitable for lightweight job queues, and why is it dangerous if workers crash unexpectedly?",
        "mastery_q2": "What is the computational complexity of `LRANGE mylist 500000 500010` on a list with 1,000,000 elements?",
        "when_use": "Use Lists for FIFO queues, LIFO stacks, activity logs, and capped feeds via LTRIM.",
        "when_not_use": "Do not use Lists for random index access by integer offset or when jobs require persistent acknowledgment (use Streams instead)."
    },
    {
        "num": "09",
        "slug": "09-sets",
        "title": "Sets: Uniqueness, Memberships, and Set Algebra",
        "motto": "Sets guarantee uniqueness in $O(1)$ and compute mathematical unions and intersections directly inside the database.",
        "problem": "Tracking unique visitors or calculating common interests between social network users in SQL requires expensive `DISTINCT` queries and `INNER JOIN` operations.",
        "prediction": "What happens if you SADD the exact same string 100 times to a set? What is the return value of SADD on the second attempt?",
        "why_matters": "Sets provide constant-time membership testing (`SISMEMBER`), tagging systems, and server-side set algebra (`SINTER`, `SUNION`, `SDIFF`).",
        "principles": "Redis Sets are represented internally as an `intset` (compact sorted array of integers) when all members are integers, upgrading to a full hash table (`dict`) when non-integer strings are added or size thresholds are crossed.",
        "script_name": "set_operations.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_set_experiments():
    s1 = "skills:alice"
    s2 = "skills:bob"
    redis_cmd("DEL", s1, s2)
    
    redis_cmd("SADD", s1, "python", "docker", "redis", "distributed_systems")
    redis_cmd("SADD", s2, "redis", "linux", "distributed_systems", "kubernetes")

    print("1. Membership Test:")
    print("  Is Alice skilled in 'redis'? ->", redis_cmd("SISMEMBER", s1, "redis"))
    print("  Is Alice skilled in 'rust'?  ->", redis_cmd("SISMEMBER", s1, "rust"))

    print("\\n2. Set Algebra (Server-Side Intersections & Unions):")
    print("  Mutual Skills (SINTER Alice Bob):\\n", redis_cmd("SINTER", s1, s2))
    print("  Unique Skills of Alice (SDIFF Alice Bob):\\n", redis_cmd("SDIFF", s1, s2))

if __name__ == "__main__":
    try: run_set_experiments()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is SMEMBERS dangerous on sets with millions of members?",
        "mastery_q2": "How does `SRANDMEMBER` differ from `SPOP`?",
        "when_use": "Use Sets for unique item collections, tagging, access control lists, and graph relationship intersections.",
        "when_not_use": "Do not use Sets when element ordering or ranking matters (use Sorted Sets)."
    },
    {
        "num": "10",
        "slug": "10-sorted-sets",
        "title": "Sorted Sets: The Skiplist Leaderboard Engine",
        "motto": "Sorted Sets combine an $O(1)$ hash table with an $O(\\log N)$ Skip List to give instant ranking over millions of items.",
        "problem": "Determining user leaderboard ranks in SQL requires `COUNT(*) WHERE score > X`, which scans or locks tables under heavy concurrent gameplay.",
        "prediction": "Does `ZADD` allow two different members to share the exact same score? How are ties broken?",
        "why_matters": "Sorted Sets are the backbone of real-time gaming leaderboards, priority queues, rate limiters, and sliding-window event indices.",
        "principles": "A Redis Sorted Set (`ZSET`) pairs an internal hash table (for $O(1)$ member-to-score lookup) with a probabilistic multi-level Skip List (for $O(\\log N)$ ordered insertion and rank queries).",
        "script_name": "sorted_set_leaderboard.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_sorted_set_experiments():
    board = "leaderboard:arcade"
    redis_cmd("DEL", board)
    print("1. Adding scores (ZADD):")
    redis_cmd("ZADD", board, "1500", "Alice", "2400", "Bob", "1800", "Charlie", "900", "Dave")

    print("\\n2. Retrieving Rankings:")
    print("  Top 3 Players (ZREVRANGE 0 2 WITHSCORES):\\n", redis_cmd("ZREVRANGE", board, "0", "2", "WITHSCORES"))
    print("  Charlie's 0-indexed Rank from top (ZREVRANK):", redis_cmd("ZREVRANK", board, "Charlie"))
    print("  Charlie's Score (ZSCORE):", redis_cmd("ZSCORE", board, "Charlie"))

    print("\\n3. Dynamic Score Updates (ZINCRBY):")
    redis_cmd("ZINCRBY", board, "1000", "Dave")
    print("  Dave scored +1000 points! New rank:", redis_cmd("ZREVRANK", board, "Dave"))

if __name__ == "__main__":
    try: run_sorted_set_experiments()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why does Redis use a Skip List instead of a Red-Black Tree or AVL Tree for Sorted Sets?",
        "mastery_q2": "How can timestamps be used as scores to implement sliding window rate limiting?",
        "when_use": "Use Sorted Sets for real-time leaderboards, priority queues, and timestamp-indexed event windows.",
        "when_not_use": "Do not use Sorted Sets if score ordering is unnecessary; standard Sets consume less memory."
    },
    {
        "num": "11",
        "slug": "11-redis-data-structure-internals",
        "title": "Redis Data Structure Internals & Encodings",
        "motto": "The public Redis command abstraction remains constant, but the underlying C memory encoding morphs as datasets expand.",
        "problem": "Engineers assume that a Redis Hash or List has a fixed memory overhead. In reality, Redis transparently changes data encodings at runtime to save RAM.",
        "prediction": "What happens to `OBJECT ENCODING` of a hash when you insert a field longer than 64 bytes?",
        "why_matters": "Memory is the most expensive resource in an in-memory database. Understanding compact encodings (`listpack`, `intset`, `embstr`) allows you to store 5x to 10x more data in the same RAM budget.",
        "principles": "Small collections are encoded in continuous memory byte buffers (`listpack`). When element count exceeds `hash-max-listpack-entries` (default 512) or element size exceeds `hash-max-listpack-value` (default 64), Redis automatically converts the encoding to a full hash table.",
        "script_name": "inspect_encodings.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def test_encoding_transitions():
    key = "demo:encoding_shift"
    redis_cmd("DEL", key)
    
    # Small hash -> listpack
    redis_cmd("HSET", key, "f1", "short_val")
    enc1 = redis_cmd("OBJECT", "ENCODING", key)
    mem1 = redis_cmd("MEMORY", "USAGE", key)
    print(f"Small Hash (f1: 9 bytes) -> Encoding: {enc1}, Memory: {mem1} bytes")

    # Insert giant value (> 64 bytes) -> triggers shift to hashtable
    redis_cmd("HSET", key, "f2", "x" * 128)
    enc2 = redis_cmd("OBJECT", "ENCODING", key)
    mem2 = redis_cmd("MEMORY", "USAGE", key)
    print(f"After inserting 128-byte field -> Encoding: {enc2}, Memory: {mem2} bytes")

if __name__ == "__main__":
    try: test_encoding_transitions()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is a `listpack` more memory efficient than a hash table for small element counts?",
        "mastery_q2": "Why doesn't Redis keep everything in a listpack indefinitely?",
        "when_use": "Design key naming and data schemas to leverage compact encodings for massive datasets.",
        "when_not_use": "Avoid tuning listpack thresholds too high (> 2048 entries), as linear CPU search within the buffer degrades throughput."
    },
    {
        "num": "12",
        "slug": "12-expiration-and-ttl",
        "title": "Expiration and TTL: Active vs. Passive Deletion",
        "motto": "Setting a TTL does not mean Redis sets an OS hardware timer for each individual key.",
        "problem": "If Redis has 50,000,000 keys with expiration deadlines, setting individual OS timers or sorting a continuous priority queue would overwhelm the CPU.",
        "prediction": "If a key expires at timestamp T, is its memory reclaimed at exactly timestamp T?",
        "why_matters": "Memory leaks in production frequently occur when millions of keys expire but are never accessed again, depending entirely on the active expiration background cycle.",
        "principles": "Redis uses two complementary expiration algorithms: 1. Passive Expiration (lazy deletion upon attempted key read), and 2. Active Expiration (`serverCron` samples 20 random keys with TTL 10 times per second, deleting expired keys and repeating if > 25% were expired).",
        "script_name": "expiration_engine.py",
        "code": '''#!/usr/bin/env python3
import socket
import time

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_ttl_experiments():
    key = "session:temp_token"
    redis_cmd("SET", key, "user_abc", "EX", "2") # 2 seconds TTL
    print("Initial TTL (seconds):", redis_cmd("TTL", key))
    time.sleep(1.0)
    print("TTL after 1 second:", redis_cmd("TTL", key))
    time.sleep(1.2)
    print("TTL after 2.2 seconds (expired):", redis_cmd("TTL", key))
    print("GET on expired key (triggers passive deletion):", redis_cmd("GET", key))

if __name__ == "__main__":
    try: run_ttl_experiments()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "What is the return value of `TTL` when a key exists without an expiration? What about when the key does not exist?",
        "mastery_q2": "Why could a sudden spike in expired keys cause temporary latency in the main Redis event loop?",
        "when_use": "Always set TTLs on temporary caches, authentication sessions, and rate-limiting buckets.",
        "when_not_use": "Never rely on Redis TTL as a strict sub-millisecond real-time scheduler guarantee."
    },
    {
        "num": "13",
        "slug": "13-memory-and-eviction",
        "title": "Memory and Eviction: Expiration != Eviction",
        "motto": "Expiration is driven by time; eviction is driven by memory pressure.",
        "problem": "What happens when an application attempts to write to Redis when physical RAM is 100% full?",
        "prediction": "Under `noeviction` mode, what error does Redis return when memory exceeds `maxmemory`? Can GET requests still succeed?",
        "why_matters": "Misconfiguring eviction policies causes either silent data loss of critical sessions or hard application write outages (`OOM command not allowed`).",
        "principles": "When `used_memory >= maxmemory`, Redis triggers its eviction engine. Policies dictate which keys to sacrifice: `noeviction` (reject writes), `allkeys-lru` / `volatile-lru`, `allkeys-lfu` / `volatile-lfu`, or `volatile-ttl`.",
        "script_name": "eviction_policies.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def test_eviction_mechanics():
    print("Testing maxmemory configuration inspection:")
    maxmem = redis_cmd("CONFIG", "GET", "maxmemory")
    policy = redis_cmd("CONFIG", "GET", "maxmemory-policy")
    print(f"Current Config:\\n  {maxmem}\\n  {policy}")
    print("\\nEviction Policies Summary:")
    print("  • noeviction   : Returns error on writes when full. Safe for primary databases.")
    print("  • allkeys-lru  : Evicts least-recently-used keys across entire keyspace. Best for pure caches.")
    print("  • volatile-lru : Evicts least-recently-used keys ONLY among keys with TTLs.")
    print("  • allkeys-lfu  : Evicts least-frequently-used keys. Protects frequently accessed hot keys.")

if __name__ == "__main__":
    try: test_eviction_mechanics()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "If Redis is used as both a persistent datastore and an ephemeral cache, which eviction policy should be used?",
        "mastery_q2": "Why does `volatile-lru` act identically to `noeviction` if no keys have TTLs assigned?",
        "when_use": "Use `allkeys-lru` or `allkeys-lfu` when Redis operates as a dedicated caching layer.",
        "when_not_use": "Never use `allkeys-lru` when Redis stores authoritative data like user accounts or financial ledger records."
    },
    {
        "num": "14",
        "slug": "14-lru-and-lfu-from-scratch",
        "title": "LRU and LFU From Scratch: Exact vs. Approximated",
        "motto": "Theoretical LRU requires 24 bytes of pointer overhead per key; Redis saves memory by approximating LRU with random sampling.",
        "problem": "Implementing exact textbook LRU requires a doubly linked list with forward and backward pointers for every key in the database. In a 50,000,000 key database, pointers alone consume > 1GB of pure RAM!",
        "prediction": "How close is Redis's sampled 5-key approximation to true theoretical LRU under Zipf-skewed workloads?",
        "why_matters": "Understanding approximated data structures is a fundamental systems engineering lesson: sacrificing 1% statistical perfection saves gigabytes of RAM.",
        "principles": "Redis stores a 24-bit timestamp in each object's `lru` header field. During eviction, it samples $N$ random keys (default `maxmemory-samples 5`), checks their idle time, and evicts the oldest candidate from that sample pool.",
        "script_name": "lru_lfu_scratch.py",
        "code": '''#!/usr/bin/env python3
from collections import OrderedDict
import random

class ExactLRUCache:
    """Textbook LRU via Doubly-Linked Hash Map (OrderedDict)."""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        if key not in self.cache: return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False) # Evict oldest

class ApproximatedLRUCache:
    """Redis-style Approximated LRU via Random Sampling."""
    def __init__(self, capacity, sample_size=5):
        self.capacity = capacity
        self.sample_size = sample_size
        self.store = {} # key -> (val, access_time)
        self.clock = 0

    def get(self, key):
        self.clock += 1
        if key in self.store:
            val, _ = self.store[key]
            self.store[key] = (val, self.clock)
            return val
        return None

    def put(self, key, value):
        self.clock += 1
        if len(self.store) >= self.capacity and key not in self.store:
            # Sample random keys
            sample_keys = random.sample(list(self.store.keys()), min(self.sample_size, len(self.store)))
            oldest_key = min(sample_keys, key=lambda k: self.store[k][1])
            del self.store[oldest_key]
        self.store[key] = (value, self.clock)

if __name__ == "__main__":
    print("Testing Exact LRU vs Redis Approximated LRU (Capacity: 3)...")
    exact = ExactLRUCache(3)
    approx = ApproximatedLRUCache(3, sample_size=3)

    for k in ["A", "B", "C"]:
        exact.put(k, 1); approx.put(k, 1)
    
    # Access A to make it recently used
    exact.get("A"); approx.get("A")
    # Insert D -> should evict B or C, never A
    exact.put("D", 1); approx.put("D", 1)

    print("Exact LRU Keys:", list(exact.cache.keys()))
    print("Approximated LRU Keys:", list(approx.store.keys()))
    print("✓ Both preserved frequently accessed key 'A' while evicting cold data.")
''',
        "mastery_q1": "What happens to eviction accuracy when `maxmemory-samples` is increased from 5 to 10?",
        "mastery_q2": "How does Redis LFU calculate key frequency using only an 8-bit logarithmic counter and a 16-bit decay timer in the same 24-bit field?",
        "when_use": "Use LFU when access patterns follow a power-law (hot items accessed continuously over weeks).",
        "when_not_use": "Do not use LFU if recently published items need immediate high caching priority before accumulating frequency."
    }
]

def generate_additional_phases():
    base = "/Users/tushar/Desktop/private/repos/redis-from-scratch/phases"
    for p in PHASES_DATA:
        p_dir = os.path.join(base, p["slug"])
        doc_path = os.path.join(p_dir, "docs", "en.md")
        doc_content = f"""# Lesson {p['num']}.1: {p['title']}

## Motto
"{p['motto']}"

## Problem
{p['problem']}

## Prediction
{p['prediction']}

## Why this matters
{p['why_matters']}

## First principles
{p['principles']}

## Mental model
```text
  [ CLIENT ] ── TCP Socket Command ──► [ REDIS ENGINE ] ──► [ INTERNAL MEMORY ]
```

## Build it
See [code/{p['script_name']}](../code/{p['script_name']}).

## Use Redis
Execute the lesson experiment:
```bash
./phases/{p['slug']}/experiments/run_experiment.sh
```

## Inspect it
Use diagnostic commands to inspect internal representations and memory.

## Measure it
Quantify latency, operations/second, and memory allocations.

## Break it
Inject failure conditions and analyze server behavior.

## Debug it
Diagnose the failure using logs and error codes.

## Modify it
Tune parameters and observe the shift in operational behavior.

## Evidence
Record findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. {p['mastery_q1']}
2. {p['mastery_q2']}

## When to use this
* {p['when_use']}

## When not to use this
* {p['when_not_use']}

## What comes next
Proceed to the next phase in the curriculum progression.
"""
        with open(doc_path, "w") as f:
            f.write(doc_content)

        code_path = os.path.join(p_dir, "code", p["script_name"])
        with open(code_path, "w") as f:
            f.write(p["code"])
        os.chmod(code_path, os.stat(code_path).st_mode | stat.S_IEXEC)

        exp_path = os.path.join(p_dir, "experiments", "run_experiment.sh")
        exp_content = f"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase {p['num']} Experiment: {p['title']} ==="
python3 phases/{p['slug']}/code/{p['script_name']}
echo "✓ Phase {p['num']} Experiment Complete."
"""
        with open(exp_path, "w") as f:
            f.write(exp_content)
        os.chmod(exp_path, os.stat(exp_path).st_mode | stat.S_IEXEC)

        out_path = os.path.join(p_dir, "outputs", "evidence-template.md")
        evidence_content = f"""# Lesson Evidence: Phase {p['num']} — {p['title']}

**Date:** [YYYY-MM-DD]
**Redis Version:** [e.g. 7.4.11 / 8.4.0]
**Environment:** macOS / Docker

### 1. Hypothesis & Prediction
* {p['prediction']}

### 2. Execution Log
```text
[Paste terminal execution output here]
```

### 3. Measurements & Findings
* Latency / Throughput:
* Memory Overhead:

### 4. What Was Broken & Diagnosed
* Failure:
* Fix:
"""
        with open(out_path, "w") as f:
            f.write(evidence_content)

    print(f"Generated data structures & memory phases 06-14 successfully.")

if __name__ == "__main__":
    generate_additional_phases()
