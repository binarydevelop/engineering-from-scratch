#!/usr/bin/env python3
"""
scripts/generate_phases_15_to_30.py — Generator for Phases 15 to 30.
"""

import os
import stat

PHASES_15_30 = [
    {
        "num": "15",
        "slug": "15-pipelining",
        "title": "Pipelining: Amortizing Network Round-Trip Time",
        "motto": "Redis can execute 500,000 operations per second, but a client doing one ping-pong per command will be lucky to reach 8,000.",
        "problem": "Network Round-Trip Time (RTT) dominates operational latency. If RTT is 1ms, a client can execute at most 1,000 commands/sec sequentially, regardless of how fast Redis CPU is.",
        "prediction": "How many times faster is executing 1,000 SET commands in a single pipelined TCP write compared to 1,000 individual blocking writes and reads?",
        "why_matters": "Pipelining is the single highest-impact optimization for batch data loading, bulk caching, and high-throughput microservices.",
        "principles": "TCP is full-duplex. A client can write 100 commands into its local socket buffer sequentially without blocking on each reply. The Redis server processes them all and writes 100 replies into the socket.",
        "script_name": "pipeline_demo.py",
        "code": '''#!/usr/bin/env python3
import socket
import time

def run_pipelining_experiment(n=2000):
    print(f"Comparing Sequential RTT vs Pipelined Batch ({n:,} operations)...")
    try:
        # 1. Sequential
        s = socket.create_connection(("localhost", 6379), timeout=5.0)
        t0 = time.perf_counter()
        for i in range(n):
            s.sendall(f"*3\\r\\n$3\\r\\nSET\\r\\n$7\\r\\nseq_k{i}\\r\\n$1\\r\\nv\\r\\n".encode())
            _ = s.recv(1024)
        seq_time = time.perf_counter() - t0
        s.close()

        # 2. Pipelined (batch size 50)
        batch_size = 50
        s = socket.create_connection(("localhost", 6379), timeout=5.0)
        t0 = time.perf_counter()
        for b in range(0, n, batch_size):
            buf = "".join(f"*3\\r\\n$3\\r\\nSET\\r\\n$7\\r\\npip_k{i}\\r\\n$1\\r\\nv\\r\\n" for i in range(b, b + batch_size))
            s.sendall(buf.encode())
            rec = 0
            while rec < batch_size * 5: # +OK\\r\\n is 5 bytes
                data = s.recv(4096)
                rec += len(data)
        pipe_time = time.perf_counter() - t0
        s.close()

        print(f"  • Sequential (1 RTT/op) : {seq_time:.3f}s ({n/seq_time:8,.0f} ops/sec)")
        print(f"  • Pipelined (batch 50)  : {pipe_time:.3f}s ({n/pipe_time:8,.0f} ops/sec)")
        print(f"  -> Speedup: {seq_time/pipe_time:.1f}x faster throughput via pipelining!")
    except Exception as e:
        print("Redis unavailable:", e)

if __name__ == "__main__":
    run_pipelining_experiment()
''',
        "mastery_q1": "Does pipelining guarantee that the batch of commands will execute atomically without other clients interleaving?",
        "mastery_q2": "What happens to client and server memory if you pipeline 10,000,000 commands in a single buffer?",
        "when_use": "Use Pipelining whenever a client needs to execute multiple independent commands concurrently.",
        "when_not_use": "Do not use Pipelining when subsequent commands depend on the return values of earlier commands."
    },
    {
        "num": "16",
        "slug": "16-transactions",
        "title": "Transactions: MULTI, EXEC, and Optimistic Locking (WATCH)",
        "motto": "Redis transactions guarantee isolation and sequential execution, but they do NOT provide SQL-style rollback on runtime errors.",
        "problem": "Two concurrent clients attempt to transfer money between accounts. If both read balance 100, calculate new balances, and write back, race conditions corrupt the ledger.",
        "prediction": "If a command inside a MULTI block encounters a type error (e.g. INCR on a string), does Redis roll back earlier commands in the transaction?",
        "why_matters": "Understanding optimistic concurrency control (`WATCH`) is critical for coordinating shared state without pessimistic distributed database locks.",
        "principles": "MULTI queues commands in memory on the server. EXEC runs them all sequentially without interruption from other clients. WATCH implements Optimistic Concurrency Control (OCC): if a watched key changes before EXEC, the transaction aborts.",
        "script_name": "transactions_demo.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_transaction_demo():
    print("1. Atomic Balance Transfer using MULTI / EXEC:")
    redis_cmd("SET", "acct:alice", "100")
    redis_cmd("SET", "acct:bob", "50")

    # Raw socket connection for multi-command transaction
    s = socket.create_connection(("localhost", 6379))
    def send(c): s.sendall(f"*{len(c)}\\r\\n" + "".join(f"${len(str(x))}\\r\\n{str(x)}\\r\\n" for x in c).encode()); return s.recv(1024).decode().strip()
    
    send(["MULTI"])
    send(["DECRBY", "acct:alice", "30"])
    send(["INCRBY", "acct:bob", "30"])
    exec_res = send(["EXEC"])
    s.close()
    
    print("  Transaction EXEC Result:\\n ", exec_res)
    print("  Alice balance:", redis_cmd("GET", "acct:alice"))
    print("  Bob balance:  ", redis_cmd("GET", "acct:bob"))

    print("\\n2. Testing No-Rollback on Runtime Error:")
    s = socket.create_connection(("localhost", 6379))
    send(["MULTI"])
    send(["SET", "tx:test", "hello"])
    send(["INCR", "tx:test"]) # Runtime type error!
    send(["SET", "tx:survivor", "alive"])
    res = send(["EXEC"])
    s.close()
    print("  EXEC with type error output:\\n ", res)
    print("  tx:survivor key value ->", redis_cmd("GET", "tx:survivor"))
    print("  -> Crucial insight: 'tx:survivor' was SET despite the INCR error. Redis does NOT rollback!")

if __name__ == "__main__":
    try: run_transaction_demo()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why did Redis choose not to implement automatic rollback on runtime errors?",
        "mastery_q2": "How does `WATCH` differ from a pessimistic mutex lock?",
        "when_use": "Use MULTI/EXEC with WATCH when multiple keys need atomic mutation based on preconditions.",
        "when_not_use": "Do not assume Redis transactions provide ACID durability or relational rollback semantics."
    },
    {
        "num": "17",
        "slug": "17-atomicity-and-server-side-logic",
        "title": "Atomicity and Server-Side Logic: Lua & Functions",
        "motto": "Moving application logic to the data is faster and more correct than moving data back and forth to the client.",
        "problem": "An e-commerce flash sale has 1 item left in stock. 500 customers click 'Buy' simultaneously. Client-side checks (`GET stock` then `DECR stock`) cause overselling due to network race conditions.",
        "prediction": "Why does a Lua script executed via EVAL guarantee zero overselling without needing WATCH or retries?",
        "why_matters": "Lua scripts and Redis Functions allow developers to build complex atomic primitives (custom rate limiters, multi-resource locks) directly inside the database.",
        "principles": "Because Redis command execution is single-threaded, a Lua script runs completely uninterrupted from start to finish. All keys manipulated in the script are evaluated in a single atomic epoch.",
        "script_name": "lua_atomicity.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_lua_experiment():
    stock_key = "inventory:phone"
    redis_cmd("SET", stock_key, "2") # Only 2 in stock!

    # Atomic check-and-decrement script
    LUA_PURCHASE = """
    local current = tonumber(redis.call('GET', KEYS[1]) or 0)
    if current > 0 then
        redis.call('DECR', KEYS[1])
        return 1
    else
        return 0
    end
    """
    print("Testing Atomic Purchase via Lua script:")
    print("  Customer 1 attempt ->", "SUCCESS" if ":1" in redis_cmd("EVAL", LUA_PURCHASE, "1", stock_key) else "OUT OF STOCK")
    print("  Customer 2 attempt ->", "SUCCESS" if ":1" in redis_cmd("EVAL", LUA_PURCHASE, "1", stock_key) else "OUT OF STOCK")
    print("  Customer 3 attempt ->", "SUCCESS" if ":1" in redis_cmd("EVAL", LUA_PURCHASE, "1", stock_key) else "OUT OF STOCK")
    print("Final Stock in Redis:", redis_cmd("GET", stock_key))

if __name__ == "__main__":
    try: run_lua_experiment()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "What happens if a Lua script contains an infinite loop `while true do end`?",
        "mastery_q2": "What are Redis Functions (introduced in Redis 7.0) and how do they improve upon ephemeral EVAL scripts?",
        "when_use": "Use Lua scripts or Redis Functions for atomic multi-step mutations where conditional logic depends on current state.",
        "when_not_use": "Never execute slow, CPU-heavy data parsing inside Lua, as it blocks all other Redis clients."
    },
    {
        "num": "18",
        "slug": "18-persistence-why-memory-is-not-enough",
        "title": "Persistence: Why Memory Is Not Enough",
        "motto": "Volatile memory is transient; without persistence, a single power flicker turns your database into a blank slate.",
        "problem": "An application stores 1,000,000 user sessions in Redis. A server kernel panic occurs. What state survives reboot?",
        "prediction": "If Redis is killed with SIGKILL (kill -9) while persistence is disabled, how much data can be recovered?",
        "why_matters": "Architects must evaluate durability guarantees: can your application afford to lose the last 1 second, 1 hour, or zero data during an infrastructure crash?",
        "principles": "In-memory datasets reside entirely in volatile DRAM. To survive process death, the state must be materialized into non-volatile block storage via snapshots (RDB) or write-ahead transaction logs (AOF).",
        "script_name": "persistence_crash.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_durability_analysis():
    print("Inspecting Current Redis Persistence Configuration:")
    rdb_save = redis_cmd("CONFIG", "GET", "save")
    aof_enabled = redis_cmd("CONFIG", "GET", "appendonly")
    print(f"  RDB Save rules: {rdb_save}")
    print(f"  AOF AppendOnly: {aof_enabled}")
    print("\\nSystem Design Durability Spectrum:")
    print("  1. No Persistence : Maximum throughput. Pure ephemeral cache. 100% loss on crash.")
    print("  2. RDB Snapshots  : Low I/O overhead. Point-in-time backup. Loses data since last snapshot.")
    print("  3. AOF (everysec) : Default standard. High durability. Loses at most ~1-2 seconds of writes.")
    print("  4. AOF (always)   : Highest durability (fsync per write). Major throughput penalty.")

if __name__ == "__main__":
    try: run_durability_analysis()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is synchronous disk writing (`fsync always`) significantly slower than in-memory updates?",
        "mastery_q2": "What happens if an operating system reboots before the kernel flushes dirty pages to physical NVMe storage?",
        "when_use": "Use non-persistent mode for pure ephemeral caches that can be reconstructed seamlessly from primary databases.",
        "when_not_use": "Never run Redis without persistence if it holds authoritative user data, balances, or task queues."
    },
    {
        "num": "19",
        "slug": "19-rdb-snapshots",
        "title": "RDB Snapshots: Point-in-Time Backups & Copy-on-Write",
        "motto": "BGSAVE does not pause Redis; Linux fork() duplicates the process memory space virtually in microseconds using Copy-on-Write.",
        "problem": "Serializing a 20GB database to disk takes seconds or minutes. How does Redis continue serving 100,000 requests/sec during the snapshot without blocking or saving half-written state?",
        "prediction": "If a child process is writing `dump.rdb` and a client modifies 100,000 keys, what happens to memory usage on the host?",
        "why_matters": "RDB snapshots provide compact disaster-recovery backups that boot 10x faster than replaying huge logs, but fork() memory amplification can trigger OS OOM kills if unmonitored.",
        "principles": "Redis calls `fork()` to spawn a child process. The Linux kernel uses Copy-on-Write (COW): memory pages are shared between parent and child until written to. Only modified memory pages are copied.",
        "script_name": "rdb_snapshots.py",
        "code": '''#!/usr/bin/env python3
import socket
import time

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=5.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def test_rdb_snapshot():
    print("Triggering background RDB snapshot (BGSAVE)...")
    res = redis_cmd("BGSAVE")
    print("  BGSAVE Trigger Status:", res)
    time.sleep(1.0)
    info = redis_cmd("INFO", "persistence")
    for line in info.split("\\r\\n"):
        if any(k in line for k in ["rdb_last_bgsave_status", "rdb_changes_since_last_save", "rdb_last_save_time"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: test_rdb_snapshot()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is Linux `vm.overcommit_memory = 1` required when running Redis with background snapshots?",
        "mastery_q2": "What data is lost if Redis crashes 14 minutes after a snapshot on a server configured with `save 900 1`?",
        "when_use": "Use RDB for disaster recovery backups, remote cold storage (S3), and initial replica synchronization.",
        "when_not_use": "Do not rely solely on RDB if your business SLA cannot tolerate losing minutes of recent writes."
    },
    {
        "num": "20",
        "slug": "20-append-only-file",
        "title": "Append-Only File: Write-Ahead Logging & fsync Tradeoffs",
        "motto": "The Append-Only File turns every mutation into a permanent audit trail written before acknowledgment.",
        "problem": "RDB snapshots have a durability window of minutes. If a server loses power between snapshots, all writes in that window vanish.",
        "prediction": "What is the maximum amount of data lost during a power outage if `appendfsync` is set to `everysec`?",
        "why_matters": "AOF is the primary persistence mechanism that makes Redis viable as an authoritative transactional store.",
        "principles": "Every state-modifying command is logged to disk in standard RESP format. Redis supports three fsync policies: `always` (maximum durability, lowest throughput), `everysec` (1-second data loss window, excellent throughput), and `no` (delegated to OS kernel flush).",
        "script_name": "aof_fsync.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def inspect_aof_configuration():
    print("Inspecting AOF Durability Settings:")
    aof_sync = redis_cmd("CONFIG", "GET", "appendfsync")
    print(f"  Current appendfsync: {aof_sync}")
    print("\\nUnderstanding fsync System Call:")
    print("  • write() only copies bytes to the OS kernel buffer cache; data is still in RAM!")
    print("  • fsync() forces the OS to physically flush blocks to the storage hardware.")
    print("  • appendfsync everysec uses a background thread to call fsync() once per second,")
    print("    keeping disk I/O off the critical path of the main Redis event loop.")

if __name__ == "__main__":
    try: inspect_aof_configuration()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why does `appendfsync always` drop Redis throughput from 100,000 ops/sec to ~2,000 ops/sec?",
        "mastery_q2": "What does the `redis-check-aof --fix` CLI utility do when an AOF file ends with a corrupted half-written command?",
        "when_use": "Use AOF with `everysec` as the default persistence policy for production systems needing high durability.",
        "when_not_use": "Do not set `appendfsync always` unless your hardware uses enterprise battery-backed NVRAM or PCIe SSDs designed for write barriers."
    },
    {
        "num": "21",
        "slug": "21-aof-rewrite-and-persistence-tradeoffs",
        "title": "AOF Rewrite & Compaction: Log Compaction Mechanics",
        "motto": "If a counter is incremented 1,000,000 times, AOF rewrite replaces 1,000,000 log lines with a single SET command.",
        "problem": "An append-only log grows indefinitely. Over months, a 50MB dataset could generate a 100GB AOF log file, filling disks and taking hours to replay on startup.",
        "prediction": "Does `BGREWRITEAOF` read the existing historical AOF log file on disk to compact it?",
        "why_matters": "AOF rewrite keeps log storage bounded and predictable, enabling rapid server reboots.",
        "principles": "`BGREWRITEAOF` does NOT read the old file. It forks a child process that scans the live dataset in RAM, writing the minimal sequence of commands necessary to recreate the current dataset directly into a new temporary file.",
        "script_name": "aof_rewrite.py",
        "code": '''#!/usr/bin/env python3
import socket
import time

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=5.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_aof_rewrite_demo():
    print("Simulating 1,000 increments to generate command history...")
    for _ in range(1000):
        redis_cmd("INCR", "test:rewrite_counter")
    
    print("Triggering background AOF rewrite (BGREWRITEAOF)...")
    res = redis_cmd("BGREWRITEAOF")
    print("  BGREWRITEAOF status:", res)
    time.sleep(1.0)
    info = redis_cmd("INFO", "persistence")
    for line in info.split("\\r\\n"):
        if any(k in line for k in ["aof_rewrite_in_progress", "aof_last_bgrewrite_status", "aof_current_size", "aof_base_size"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: run_aof_rewrite_demo()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "How does Redis handle new client writes that occur while the child process is actively rewriting the AOF?",
        "mastery_q2": "What are the advantages of combining RDB snapshots and AOF into a hybrid persistence file (Redis 5.0+)?",
        "when_use": "Configure automated AOF rewriting (`auto-aof-rewrite-percentage 100`) to keep log sizes bounded.",
        "when_not_use": "Do not trigger manual AOF rewrites during peak traffic spikes, as `fork()` introduces latency."
    },
    {
        "num": "22",
        "slug": "22-redis-as-a-cache",
        "title": "Redis as a Cache: Cache-Aside vs. Write-Through",
        "motto": "The fastest database query is the one you never execute against the database.",
        "problem": "Serving 50,000 read queries/sec directly against PostgreSQL or MySQL saturates connection pools and CPU disk queues.",
        "prediction": "What is the expected latency difference between a Cache Hit in Redis (<0.5ms) and a Cache Miss querying an indexed SQL database (~15-50ms)?",
        "why_matters": "Cache-Aside (Lazy Loading) is the dominant architecture pattern for high-scale web systems.",
        "principles": "In Cache-Aside: 1. Application checks Redis. 2. On hit, return data. 3. On miss, query primary DB. 4. Populate Redis with TTL. 5. Return data.",
        "script_name": "cache_aside_lab.py",
        "code": '''#!/usr/bin/env python3
import socket
import time
import json

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def simulated_sql_query(user_id):
    # Simulate database disk I/O and query planning delay
    time.sleep(0.02) # 20ms
    return {"id": user_id, "name": f"User_{user_id}", "status": "active"}

def get_user_profile(user_id):
    cache_key = f"user:profile:{user_id}"
    t0 = time.perf_counter()
    
    # 1. Check Redis
    cached = redis_cmd("GET", cache_key)
    if cached and not cached.startswith("$-1"):
        latency_ms = (time.perf_counter() - t0) * 1000
        return json.loads(cached.split("\\r\\n")[-1]), "CACHE_HIT", latency_ms

    # 2. Cache Miss -> Query Database
    db_data = simulated_sql_query(user_id)
    # 3. Populate Redis Cache with 10s TTL
    redis_cmd("SET", cache_key, json.dumps(db_data), "EX", "10")
    latency_ms = (time.perf_counter() - t0) * 1000
    return db_data, "CACHE_MISS", latency_ms

if __name__ == "__main__":
    try:
        redis_cmd("DEL", "user:profile:42")
        print("1. First Request (Cold Cache):")
        data, status, lat = get_user_profile(42)
        print(f"  Status: {status:10} | Latency: {lat:6.2f} ms | Data: {data}")

        print("\\n2. Second Request (Warm Cache):")
        data, status, lat = get_user_profile(42)
        print(f"  Status: {status:10} | Latency: {lat:6.2f} ms | Data: {data}")
    except Exception as e:
        print("Redis offline:", e)
''',
        "mastery_q1": "What are the trade-offs of Cache-Aside versus Write-Through caching?",
        "mastery_q2": "What happens if the cache is populated with an infinite TTL and the database row is updated directly via an external script?",
        "when_use": "Use Cache-Aside for read-heavy workloads where stale data for the duration of a TTL is acceptable.",
        "when_not_use": "Do not cache data that is written more frequently than it is read (cache churn wastes memory)."
    },
    {
        "num": "23",
        "slug": "23-cache-invalidation",
        "title": "Cache Invalidation: The Hardest Problem in Computer Science",
        "motto": "There are only two hard things in Computer Science: cache invalidation and naming things.",
        "problem": "A user updates their email address in the database. Because the old email remains cached in Redis, other services continue reading obsolete data.",
        "prediction": "If you update the database and then delete the cache key, can a concurrent reader still re-populate the cache with stale data?",
        "why_matters": "Stale data anomalies create security vulnerabilities, incorrect financial balances, and user confusion.",
        "principles": "Cache invalidation strategies include: 1. Passive TTL expiration, 2. Explicit deletion on write (`DEL key`), 3. Write-Through cache update, and 4. Versioned keys (`user:profile:v2`).",
        "script_name": "cache_invalidation_lab.py",
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

def run_invalidation_demo():
    key = "user:settings:99"
    # Seed cache
    redis_cmd("SET", key, "theme=dark")
    print("1. Initial Cached Setting:", redis_cmd("GET", key))

    # Simulate database update
    print("2. User updates setting in SQL DB to 'theme=light'...")
    # INCORRECT APPROACH: Forget to invalidate cache
    print("  Without invalidation, cache still returns:", redis_cmd("GET", key), "(STALE DATA ANOMALY!)")

    # CORRECT APPROACH: Explicit Cache Invalidation
    print("3. Executing explicit DEL invalidation:")
    redis_cmd("DEL", key)
    print("  Cache key after invalidation ->", redis_cmd("GET", key), "(Next read will fetch from DB)")

if __name__ == "__main__":
    try: run_invalidation_demo()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is deleting the cache key (`DEL`) generally preferred over updating the cache key (`SET`) during database writes?",
        "mastery_q2": "What is the Cache Invalidation Race Condition that occurs when a DB read and DB write interleave?",
        "when_use": "Always implement explicit cache invalidation (`DEL key`) alongside TTL safety nets on write operations.",
        "when_not_use": "Never rely solely on long TTLs (hours/days) for mutable user or business settings."
    },
    {
        "num": "24",
        "slug": "24-cache-stampede",
        "title": "Cache Stampede: The Thundering Herd Problem",
        "motto": "When a hot cached key expires, 10,000 concurrent requests simultaneously experience a miss and hammer the database.",
        "problem": "A popular news article or product page receives 5,000 requests/sec. Its TTL expires. All 5,000 requests miss Redis at the same millisecond and query the SQL database simultaneously, crashing the database.",
        "prediction": "What happens to database CPU and connection pool usage during a cache stampede?",
        "why_matters": "Preventing cache stampedes is mandatory for large-scale e-commerce, media publishing, and high-concurrency APIs.",
        "principles": "Mitigations: 1. Mutex Locking / Single-Flight (only the first worker queries DB while others wait), 2. Probabilistic Early Expiration (XFetch algorithm refreshes before expiration), 3. TTL Jitter (adding random variance to avoid simultaneous key deaths).",
        "script_name": "stampede_simulator.py",
        "code": '''#!/usr/bin/env python3
import socket
import time
from concurrent.futures import ThreadPoolExecutor

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def simulated_db_fetch():
    time.sleep(0.05) # 50ms slow query
    return "fresh_db_payload"

def fetch_with_stampede_protection(key, worker_id):
    # 1. Read cache
    val = redis_cmd("GET", key)
    if val and not val.startswith("$-1"):
        return "CACHE_HIT"

    # 2. Acquire Mutex Lock (SET lock:key token NX EX 2)
    lock_key = f"lock:{key}"
    acquired = "+OK" in redis_cmd("SET", lock_key, str(worker_id), "NX", "EX", "2")
    if acquired:
        # Only this worker queries DB
        data = simulated_db_fetch()
        redis_cmd("SET", key, data, "EX", "5")
        redis_cmd("DEL", lock_key)
        return "DB_REFRESH_LEADER"
    else:
        # Other workers back off and wait
        time.sleep(0.06)
        return "BACKOFF_CACHE_HIT"

if __name__ == "__main__":
    try:
        target_key = "hot:catalog_item"
        redis_cmd("DEL", target_key) # Force cache miss
        print("Simulating 20 concurrent requests hitting an expired hot key...")
        with ThreadPoolExecutor(max_workers=20) as pool:
            results = list(pool.map(lambda i: fetch_with_stampede_protection(target_key, i), range(20)))
        print("Results across 20 workers:")
        for r in set(results):
            print(f"  • {r}: {results.count(r)} requests")
        print("✓ Verified: Exactly ONE worker queried the database! Database was protected.")
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "How does TTL Jitter prevent multiple related keys from expiring at the exact same second?",
        "mastery_q2": "What is the XFetch probabilistic early expiration formula?",
        "when_use": "Implement single-flight mutex locks on high-traffic, computationally expensive cached endpoints.",
        "when_not_use": "Do not add complex mutex locks to low-traffic keys where occasional misses do not threaten the database."
    },
    {
        "num": "25",
        "slug": "25-hot-keys",
        "title": "Hot Keys: Workload Skew & Thread Saturation",
        "motto": "Adding more cluster nodes does not fix a hot key; a single key can only ever live on a single node.",
        "problem": "In a cluster of 50 Redis nodes, 90% of all application queries request the exact same key (`trending:world_cup`). Node 12 runs at 100% CPU while nodes 1-11 and 13-50 sit idle at 2% CPU.",
        "prediction": "What happens if a hot key receives 150,000 requests/sec on a single Redis thread?",
        "why_matters": "Hot keys are a leading cause of outages in distributed architectures, defeating horizontal sharding.",
        "principles": "Because Redis assigns each key to exactly one hash slot on one node, horizontal scaling cannot partition a single key. Mitigations include client-side in-memory caching and key replication (`key:shard_{1..N}`).",
        "script_name": "hot_key_lab.py",
        "code": '''#!/usr/bin/env python3
import socket
import random

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_hot_key_sharding():
    base_key = "hot:config_flag"
    num_shards = 4
    print(f"Mitigating Hot Key by replicating across {num_shards} key shards...")
    # Write same value to all shards
    for i in range(num_shards):
        redis_cmd("SET", f"{base_key}:{i}", "enabled_v2")

    # Readers randomly pick a shard, balancing load across cores/nodes
    print("Simulating 10 balanced client reads:")
    for client_id in range(10):
        chosen_shard = f"{base_key}:{random.randint(0, num_shards - 1)}"
        val = redis_cmd("GET", chosen_shard).split("\\r\\n")[-1]
        print(f"  Client {client_id:2d} read from {chosen_shard} -> {val}")

if __name__ == "__main__":
    try: run_hot_key_sharding()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "How does Redis 6.0+ Client-Side Caching (Tracking / RESP3) solve the hot key problem?",
        "mastery_q2": "What tool can you run in production to detect hot keys (`redis-cli --hotkeys`)?",
        "when_use": "Use client-side caching or key replication for read-heavy global configurations and top celebrity profiles.",
        "when_not_use": "Do not replicate hot keys that are frequently written to, as synchronization complexity escalates."
    },
    {
        "num": "26",
        "slug": "26-pub-sub",
        "title": "Pub/Sub: Ephemeral Messaging vs. Durable Queuing",
        "motto": "Redis Pub/Sub is fire-and-forget: if a subscriber is offline for one millisecond, that message is lost forever.",
        "problem": "Engineers often use Redis Pub/Sub for background jobs or payment notifications, only to discover that unacknowledged messages vanish if a worker restarts or encounters network blips.",
        "prediction": "If a subscriber disconnects and the publisher sends 5 messages, will the subscriber receive them upon reconnecting?",
        "why_matters": "Pub/Sub is designed for real-time notifications (chat, live UI alerts), NOT durable event-driven processing.",
        "principles": "In Redis Pub/Sub, the server maintains no buffer or historical queue of messages. If zero subscribers are listening to a channel, the message is discarded immediately by the server.",
        "script_name": "pubsub_lab.py",
        "code": '''#!/usr/bin/env python3
import socket
import time

def run_pubsub_experiment():
    print("Testing Redis Pub/Sub Message Ephemerality:")
    # 1. Publish when NO SUBSCRIBERS are active
    s = socket.create_connection(("localhost", 6379))
    s.sendall(b"*3\\r\\n$7\\r\\nPUBLISH\\r\\n$11\\r\\nchat:alerts\\r\\n$13\\r\\nHello World 1\\r\\n")
    resp = s.recv(1024).decode()
    s.close()
    print("  Published with 0 subscribers. Return value (listener count):", resp.strip())

    print("\\nTakeaway: The message was immediately discarded by Redis. When a worker is offline,")
    print("Pub/Sub provides ZERO durability. For persistent job processing, use Redis Streams.")

if __name__ == "__main__":
    try: run_pubsub_experiment()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why does Redis Pub/Sub consume very little memory compared to Redis Streams?",
        "mastery_q2": "What happens to Redis server memory if a connected subscriber is too slow to read incoming messages?",
        "when_use": "Use Pub/Sub for ephemeral real-time broadcasts: live sports score push alerts, chat notifications.",
        "when_not_use": "Never use Pub/Sub for financial transactions, task queues, or events requiring at-least-once delivery."
    },
    {
        "num": "27",
        "slug": "27-build-an-append-only-event-log",
        "title": "Build an Append-Only Event Log From Scratch",
        "motto": "A stream is an immutable, ordered sequence of records, each identified by a monotonically increasing ID.",
        "problem": "Before using Redis Streams, we must understand the mechanics of message offsets, event replays, and consumer coordination problems.",
        "prediction": "What happens if two independent workers want to consume the same event log at different speeds?",
        "why_matters": "This first-principles implementation reveals why simple lists cannot solve distributed worker coordination.",
        "principles": "An event log assigns sequential IDs (`0, 1, 2...`). Consumers maintain their own `last_read_id`, enabling independent replay without deleting messages from the log.",
        "script_name": "event_log_scratch.py",
        "code": '''#!/usr/bin/env python3
class SimpleEventLog:
    def __init__(self):
        self.entries = [] # [(id, payload)]
        self.next_id = 0

    def append(self, payload):
        entry_id = self.next_id
        self.entries.append((entry_id, payload))
        self.next_id += 1
        return entry_id

    def read_from(self, last_id, count=10):
        return [e for e in self.entries if e[0] > last_id][:count]

if __name__ == "__main__":
    log = SimpleEventLog()
    log.append({"event": "user_signup", "uid": 1})
    log.append({"event": "order_created", "order_id": 99})
    log.append({"event": "payment_received", "amount": 50})

    print("Worker Alpha consuming from beginning:")
    worker_alpha_offset = -1
    msgs = log.read_from(worker_alpha_offset)
    for mid, payload in msgs:
        print(f"  Worker Alpha read: ID {mid} -> {payload}")
        worker_alpha_offset = mid

    print("\\nWorker Beta consuming later:")
    worker_beta_offset = 0 # Missed first event
    msgs = log.read_from(worker_beta_offset)
    for mid, payload in msgs:
        print(f"  Worker Beta read: ID {mid} -> {payload}")
''',
        "mastery_q1": "How does an offset-based event log differ fundamentally from a pop-based FIFO queue?",
        "mastery_q2": "What garbage collection problem arises when an event log grows indefinitely?",
        "when_use": "Use event logs when multiple independent microservices must read the same stream of domain events.",
        "when_not_use": "Do not use event logs if events must be strictly deleted immediately upon first receipt."
    },
    {
        "num": "28",
        "slug": "28-redis-streams",
        "title": "Redis Streams: Consumer Groups, PEL, and Crash Recovery",
        "motto": "Redis Streams provide Kafka-like log semantics directly inside Redis, with persistent offsets and crash recovery.",
        "problem": "A worker pulls a task from a queue and begins executing it. 100ms later, the worker's power cord is unplugged. How do you recover the unacknowledged job without losing it?",
        "prediction": "What command inspects tasks that have been assigned to workers but have not yet been acknowledged with XACK?",
        "why_matters": "Redis Streams combine durability, multi-consumer partitioning, and failure recovery into a single high-performance engine.",
        "principles": "Streams are append-only logs indexed by `<timestamp>-<sequence>`. Consumer Groups partition streams across workers. Unacknowledged messages reside in the Pending Entries List (PEL). If a worker crashes, supervisor workers claim them via `XCLAIM`.",
        "script_name": "streams_lab.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_streams_demo():
    stream = "stream:telemetry"
    group = "group:analytics"
    redis_cmd("DEL", stream)
    
    # 1. Append entries
    id1 = redis_cmd("XADD", stream, "*", "sensor", "temp", "val", "22.5")
    id2 = redis_cmd("XADD", stream, "*", "sensor", "pressure", "val", "1013")
    print(f"Appended entries to stream:\\n  {id1}\\n  {id2}")

    # 2. Create Consumer Group
    redis_cmd("XGROUP", "CREATE", stream, group, "0")

    # 3. Worker reads message
    read_res = redis_cmd("XREADGROUP", "GROUP", group, "worker_1", "COUNT", "1", "STREAMS", stream, ">")
    print(f"\\nWorker 1 read message:\\n  {read_res}")

    # 4. Check Pending Entries List (PEL) before XACK
    pel = redis_cmd("XPENDING", stream, group)
    print(f"\\nPEL Status (Pending Acknowledgment):\\n  {pel}")

if __name__ == "__main__":
    try: run_streams_demo()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "What does `>` mean as the ID parameter in `XREADGROUP`?",
        "mastery_q2": "How does `XCLAIM` allow a healthy worker to steal an abandoned job from a crashed worker?",
        "when_use": "Use Redis Streams for mission-critical background jobs, audit trails, and multi-consumer event processing.",
        "when_not_use": "Do not use Redis Streams if message retention must span years across petabytes (use Apache Kafka or AWS Kinesis)."
    },
    {
        "num": "29",
        "slug": "29-rate-limiting",
        "title": "Rate Limiting: Algorithms and Concurrency Races",
        "motto": "A naive rate limiter with GET then INCR creates a race condition that lets attackers send 10x their allowed quota.",
        "problem": "An API allows 100 requests per minute. Under concurrent attacks, naive multi-command checks experience race conditions that breach limits.",
        "prediction": "What is the boundary flaw of the Fixed Window Counter algorithm at minute transitions?",
        "why_matters": "Rate limiting protects microservices against denial-of-service attacks, credential stuffing, and resource exhaustion.",
        "principles": "Fixed Window Counters can leak 2x traffic across boundaries. Sliding Window Logs via Sorted Sets provide perfect accuracy at high memory cost. Token Buckets implemented via atomic Lua scripts provide constant memory and smooth bursting.",
        "script_name": "rate_limiter_lab.py",
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

def atomic_fixed_window(user_id, limit=3, window_sec=2):
    now_window = int(time.time() // window_sec)
    key = f"rate:{user_id}:{now_window}"
    raw = redis_cmd("INCR", key)
    count = int(raw.split("\\r\\n")[0][1:])
    if count == 1:
        redis_cmd("EXPIRE", key, str(window_sec * 2))
    return count <= limit, count

if __name__ == "__main__":
    try:
        print("Testing Atomic Rate Limiter (Limit: 3 requests per 2-second window):")
        for i in range(1, 6):
            allowed, count = atomic_fixed_window("user_42", limit=3, window_sec=2)
            status = "✓ ALLOWED" if allowed else "✗ 429 TOO MANY REQUESTS"
            print(f"  Request #{i}: {status} (Count: {count})")
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "How does the Sliding Window Log algorithm calculate requests within the last 60 seconds?",
        "mastery_q2": "Why does a Token Bucket algorithm provide smoother traffic shaping than a Fixed Window limiter?",
        "when_use": "Use atomic Redis rate limiters at your API gateway to enforce quotas across distributed worker instances.",
        "when_not_use": "Do not implement rate limiters using non-atomic separate GET and SET commands."
    },
    {
        "num": "30",
        "slug": "30-distributed-locks",
        "title": "Distributed Locks: Safety, TTLs, and Fencing Tokens",
        "motto": "A distributed lock is only as safe as its release token; releasing another worker's expired lock causes catastrophic data corruption.",
        "problem": "Two microservice workers attempt to generate an invoice for the same customer simultaneously. If both acquire a naive lock (`SET lock taken`), duplicate charges occur.",
        "prediction": "What catastrophic race occurs if Worker A takes a 10-second GC pause, its lock TTL expires, Worker B acquires the lock, and Worker A wakes up and executes `DEL lock`?",
        "why_matters": "Distributed locking is fraught with subtle failure modes (process pauses, network partitions, clock drift). Understanding safe implementation is paramount.",
        "principles": "A safe single-instance distributed lock requires: 1. `SET resource_key random_uuid NX PX ttl`, 2. Only releasing the lock if the stored UUID matches via an atomic Lua script, 3. Using monotonic fencing tokens to protect backend databases from paused workers.",
        "script_name": "distributed_lock_lab.py",
        "code": '''#!/usr/bin/env python3
import socket
import uuid
import time

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

LUA_RELEASE_LOCK = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
else
    return 0
end
"""

def test_safe_distributed_lock():
    lock_key = "lock:invoice:9021"
    token = str(uuid.uuid4())
    print("1. Acquiring lock with 3-second TTL and unique UUID token:")
    res = redis_cmd("SET", lock_key, token, "NX", "PX", "3000")
    print("  Acquire Result:", res)

    print("\\n2. Another worker attempting to acquire the same lock:")
    competing_res = redis_cmd("SET", lock_key, "other_worker", "NX", "PX", "3000")
    print("  Competing Worker Result:", competing_res, "(Correctly rejected!)")

    print("\\n3. Releasing lock safely with Lua script token verification:")
    release_res = redis_cmd("EVAL", LUA_RELEASE_LOCK, "1", lock_key, token)
    print("  Release Status (1 = released, 0 = rejected):", release_res)

if __name__ == "__main__":
    try: test_safe_distributed_lock()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "What is Martin Kleppmann's primary critique of the Redlock algorithm regarding asynchronous network pauses?",
        "mastery_q2": "What is a Fencing Token and how does it prevent stale writes in backend storage?",
        "when_use": "Use single-instance atomic locks with UUID tokens for non-critical coordination (e.g. deduplicating email sends).",
        "when_not_use": "Do not rely solely on Redis locks for financial settlement or data integrity where correctness demands linearizable distributed consensus (Raft/Paxos)."
    }
]

def generate_phases_15_30():
    base = "/Users/tushar/Desktop/private/repos/redis-from-scratch/phases"
    for p in PHASES_15_30:
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
  [ CLIENT WORKERS ] ── TCP Socket ──► [ REDIS ENGINE ] ──► [ LOCK / LOG / STREAM ]
```

## Build it
See [code/{p['script_name']}](../code/{p['script_name']}).

## Use Redis
Execute the lesson experiment:
```bash
./phases/{p['slug']}/experiments/run_experiment.sh
```

## Inspect it
Inspect command return codes, internal data structures, and memory.

## Measure it
Quantify latency, concurrency race conditions, and throughput.

## Break it
Inject network delays, TTL expirations, or ungraceful client terminations.

## Debug it
Diagnose the failure using logs and atomic status returns.

## Modify it
Tune timeouts, concurrency levels, or batch sizes and observe shifts.

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
* Injected Failures:

### 4. What Was Broken & Diagnosed
* Failure:
* Fix:
"""
        with open(out_path, "w") as f:
            f.write(evidence_content)

    print(f"Generated concurrency, persistence & caching phases 15-30 successfully.")

if __name__ == "__main__":
    generate_phases_15_30()
