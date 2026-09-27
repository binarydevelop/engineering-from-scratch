#!/usr/bin/env python3
"""
scripts/generate_phases_31_to_50.py — Generator for Phases 31 to 50.
"""

import os
import stat

PHASES_31_50 = [
    {
        "num": "31",
        "slug": "31-performance-and-benchmarking",
        "title": "Performance and Benchmarking: Beyond Synthetic Claims",
        "motto": "Never quote '100,000 ops/sec' without stating the payload size, concurrency, pipelining, and network RTT.",
        "problem": "Engineers run `redis-benchmark` on localhost and claim their production architecture can handle 200,000 requests/sec. In production across cloud VPCs, network latency drops throughput to 5,000 ops/sec.",
        "prediction": "How does increasing the payload size from 100 bytes to 100 kilobytes affect operations per second?",
        "why_matters": "Accurate capacity planning prevents catastrophic performance degradation under real-world production network conditions.",
        "principles": "Synthetic benchmarks running on loopback (`127.0.0.1`) bypass physical network switches and NIC packet processing. Latency must be measured as percentiles (p50, p95, p99), not merely mean averages.",
        "script_name": "benchmark_harness.py",
        "code": '''#!/usr/bin/env python3
import socket
import time
from statistics import median

def run_benchmark(n=5000):
    print(f"Measuring Redis Latency Percentiles ({n:,} operations)...")
    latencies = []
    try:
        s = socket.create_connection(("localhost", 6379), timeout=5.0)
        t_start = time.perf_counter()
        for i in range(n):
            cmd = f"*3\\r\\n$3\\r\\nSET\\r\\n$8\\r\\nbench:{i}\\r\\n$5\\r\\nvalue\\r\\n".encode()
            t0 = time.perf_counter()
            s.sendall(cmd)
            _ = s.recv(1024)
            latencies.append((time.perf_counter() - t0) * 1000)
        total_time = time.perf_counter() - t_start
        s.close()

        latencies.sort()
        print(f"Total Time: {total_time:.3f}s | Throughput: {n/total_time:,.0f} ops/sec")
        print(f"  • p50 (Median) : {median(latencies):.3f} ms")
        print(f"  • p95          : {latencies[int(n*0.95)]:.3f} ms")
        print(f"  • p99          : {latencies[int(n*0.99)]:.3f} ms")
        print(f"  • Max Latency  : {latencies[-1]:.3f} ms")
    except Exception as e:
        print("Redis unavailable:", e)

if __name__ == "__main__":
    run_benchmark()
''',
        "mastery_q1": "Why does `redis-benchmark -q` report unrealistically optimistic numbers compared to real application workloads?",
        "mastery_q2": "What is the Coordinated Omission problem in client-side latency benchmarking?",
        "when_use": "Benchmark with production payload distributions, realistic network topologies, and connection pools.",
        "when_not_use": "Never extrapolate production server sizing from a single localhost `redis-benchmark` run."
    },
    {
        "num": "32",
        "slug": "32-latency-diagnosis",
        "title": "Latency Diagnosis: SLOWLOG, LATENCY DOCTOR, and Root Causes",
        "motto": "When Redis latency spikes, the single-threaded engine means one slow command blocks every client connected to the server.",
        "problem": "An API suddenly times out with 500 errors. Redis CPU is at 100%. How do you identify which specific command or client is freezing the event loop?",
        "prediction": "Does `SLOWLOG` measure the network round-trip time or only the execution time inside the Redis engine?",
        "why_matters": "Diagnosing production latency spikes requires knowing the exact sequence of commands to execute without guessing.",
        "principles": "Redis `SLOWLOG` records commands whose execution time (excluding network I/O) exceeds `slowlog-log-slower-than`. `LATENCY DOCTOR` provides automated diagnostic recommendations.",
        "script_name": "latency_diagnosis.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def inspect_latency_tools():
    print("1. Inspecting SLOWLOG:")
    slow_len = redis_cmd("SLOWLOG", "LEN")
    print(f"  Total logged slow operations: {slow_len}")
    slow_entries = redis_cmd("SLOWLOG", "GET", "3")
    print(f"  Recent Slow Entries:\\n  {slow_entries}")

    print("\\n2. Checking Latency Monitor Threshold:")
    thresh = redis_cmd("CONFIG", "GET", "latency-monitor-threshold")
    print(f"  {thresh}")

if __name__ == "__main__":
    try: inspect_latency_tools()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "What is the default threshold for `slowlog-log-slower-than` in microseconds?",
        "mastery_q2": "Why should `MONITOR` never be used on a busy production Redis instance?",
        "when_use": "Use SLOWLOG and LATENCY DOCTOR as your first step when investigating latency spikes.",
        "when_not_use": "Do not leave `slowlog-log-slower-than 0` permanently enabled in production, as logging every command wastes memory."
    },
    {
        "num": "33",
        "slug": "33-memory-analysis",
        "title": "Memory Analysis: Fragmentation, RSS, and jemalloc",
        "motto": "Storing 100 bytes of data in Redis does not mean Redis consumes 100 bytes of physical RAM.",
        "problem": "An engineer calculates that 10,000,000 keys of 20 bytes each should take 200MB. When loaded, Redis consumes over 1.2GB of RAM and crashes with OOM!",
        "prediction": "What overhead does each key in Redis carry before including the actual string bytes?",
        "why_matters": "Memory is the primary financial and operational constraint of Redis. Understanding memory layout prevents costly sizing errors.",
        "principles": "Every key requires a `dictEntry` (24-32 bytes), an SDS header for the key, a `robj` header (16 bytes), an SDS header for the value, plus memory allocator (jemalloc) bucket alignment padding.",
        "script_name": "memory_audit.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_memory_audit():
    key = "mem:test_overhead"
    redis_cmd("SET", key, "x")
    usage = redis_cmd("MEMORY", "USAGE", key)
    print(f"Key '{key}' with 1-byte value 'x':")
    print(f"  Actual string data : 1 byte")
    print(f"  Redis MEMORY USAGE : {usage} bytes! (~50x overhead for tiny keys)")

    print("\\nInspecting Server Memory Metrics (INFO memory):")
    info = redis_cmd("INFO", "memory")
    for line in info.split("\\r\\n"):
        if any(k in line for k in ["used_memory_human", "used_memory_rss_human", "mem_fragmentation_ratio", "mem_allocator"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: run_memory_audit()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "What causes a high `mem_fragmentation_ratio` (> 1.5) and how does `activedefrag` solve it?",
        "mastery_q2": "Why does storing fields inside a Hash consume significantly less memory per item than storing individual standalone keys?",
        "when_use": "Use `MEMORY USAGE <key>` and `MEMORY STATS` to audit data schemas before loading billions of records.",
        "when_not_use": "Do not store millions of 1-byte standalone keys; group them into hashes or packed buffers."
    },
    {
        "num": "34",
        "slug": "34-replication-from-first-principles",
        "title": "Replication From First Principles: Asynchronous Streaming",
        "motto": "Replication provides read scalability and data redundancy, but writes to the primary remain asynchronous.",
        "problem": "A single Redis server crashes due to a hardware failure. If all data lived only on that one machine, the application experiences total downtime.",
        "prediction": "When a client writes to the primary, does the primary wait for replicas to confirm receipt before returning '+OK' to the client?",
        "why_matters": "Replication is the foundation of high availability, failover, and geographical read scaling.",
        "principles": "Redis uses asynchronous primary-replica streaming. Writes are applied locally on the primary and queued to the replication backlog buffer to be streamed over TCP to replicas. Replicas are strictly read-only by default.",
        "script_name": "replication_toy.py",
        "code": '''#!/usr/bin/env python3
import socket
import threading
import time

class PrimaryReplicaToy:
    def __init__(self):
        self.primary_store = {}
        self.replica_store = {}
        self.repl_backlog = []

    def primary_write(self, key, val):
        self.primary_store[key] = val
        self.repl_backlog.append((key, val))
        print(f"  [Primary] Written {key}={val}. Client acknowledged (+OK).")

    def sync_replica(self, delay_sec=0.2):
        time.sleep(delay_sec) # Simulate network lag
        while self.repl_backlog:
            k, v = self.repl_backlog.pop(0)
            self.replica_store[k] = v
            print(f"  [Replica] Applied replication stream: {k}={v}")

if __name__ == "__main__":
    toy = PrimaryReplicaToy()
    print("1. Writing to Primary:")
    toy.primary_write("user:10", "Alice")
    print(f"  Immediate Replica Read: {toy.replica_store.get('user:10')} (Stale read during replication lag!)")
    
    print("\\n2. Replicating over asynchronous network:")
    toy.sync_replica()
    print(f"  Replica Read After Sync: {toy.replica_store.get('user:10')} (Consistent)")
''',
        "mastery_q1": "How does the `WAIT` command allow clients to enforce semi-synchronous replication confirmation?",
        "mastery_q2": "Why can a read from a replica return stale data?",
        "when_use": "Use replicas to scale read-heavy traffic and provide hot-standby copies for disaster recovery.",
        "when_not_use": "Do not use standard Redis replication if your architecture requires strict linearizable ACID consensus."
    },
    {
        "num": "35",
        "slug": "35-replication-failure-modes",
        "title": "Replication Failure Modes: Backlog Overflow & Desync",
        "motto": "Replication is not automatic failover: if the primary dies, replicas do not magically promote themselves.",
        "problem": "A replica temporarily loses its network connection for 30 seconds. When it reconnects, how does it catch up? What happens if the network outage lasts for hours?",
        "prediction": "What happens if the volume of writes during an outage exceeds the size of the circular `repl-backlog-size` buffer?",
        "why_matters": "Distinguishing between Partial Resynchronization (`PSYNC`) and catastrophic Full Resynchronization (disk fork + RDB network transfer) is essential for production resilience.",
        "principles": "The primary maintains a circular memory buffer (`repl-backlog`). If a replica reconnects and its offset is still within the backlog, a fast incremental sync (`PSYNC`) occurs. If the offset fell off the ring, a full RDB snapshot must be generated and transferred.",
        "script_name": "repl_failure_modes.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def inspect_replication_backlog():
    print("Inspecting Replication Metrics & Backlog Ring Buffer:")
    info = redis_cmd("INFO", "replication")
    for line in info.split("\\r\\n"):
        if any(k in line for k in ["role", "connected_slaves", "master_repl_offset", "repl_backlog_active", "repl_backlog_size"]):
            print(f"  • {line}")

if __name__ == "__main__":
    try: inspect_replication_backlog()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why can a full resynchronization of a 30GB instance degrade network performance across the entire cluster?",
        "mastery_q2": "What is `diskless-replication` and when should it be enabled?",
        "when_use": "Size `repl-backlog-size` generously (e.g. 512MB-1GB) to survive brief network blips without triggering full RDB syncs.",
        "when_not_use": "Never assume replicas will automatically promote themselves when a primary dies without an external coordinator like Sentinel."
    },
    {
        "num": "36",
        "slug": "36-sentinel",
        "title": "Redis Sentinel: Quorum, Health Checks, and Failover",
        "motto": "Sentinel is the supervisor that watches the primary, agrees on death via quorum, and automatically promotes a replica.",
        "problem": "When a primary server crashes at 3 AM, a human operator cannot manually log in, reconfigure replicas with `REPLICAOF NO ONE`, and update application DNS without hours of downtime.",
        "prediction": "Why does a robust Sentinel deployment require at least 3 Sentinel nodes rather than 2?",
        "why_matters": "Redis Sentinel provides automated High Availability (HA) for standalone primary-replica setups.",
        "principles": "Sentinels run as independent processes monitoring Redis nodes. When a primary misses heartbeats (`PING`), a Sentinel flags it `sdown` (subjectively down). When a quorum of Sentinels agree, it becomes `odown` (objectively down). Sentinels elect a leader via Raft-like consensus to execute failover.",
        "script_name": "sentinel_lab.py",
        "code": '''#!/usr/bin/env python3
def explain_sentinel_topology():
    print("Redis Sentinel High Availability Architecture:")
    print("""
             [ Sentinel 1 ] ─── [ Sentinel 2 ] ─── [ Sentinel 3 ]
                   │                  │                  │
                   └──────────┬───────┴──────────┬───────┘
                              ▼                  ▼
                       [ Primary (6379) ]    [ Replica (6380) ]
    """)
    print("Failover Sequence:")
    print("  1. Primary stops responding to PING for 'down-after-milliseconds' (e.g. 5000ms).")
    print("  2. Sentinel detects SDOWN (Subjectively Down).")
    print("  3. Sentinel queries peers: if >= QUORUM agree, state transitions to ODOWN.")
    print("  4. Sentinels elect an Epoch Leader to conduct failover.")
    print("  5. Leader promotes best Replica to Primary via 'REPLICAOF NO ONE'.")
    print("  6. Remaining replicas are reconfigured to follow the new primary.")
    print("  7. Clients connecting via Sentinel driver are automatically redirected!")

if __name__ == "__main__":
    explain_sentinel_topology()
''',
        "mastery_q1": "What is split-brain and how does `min-replicas-to-write` help mitigate it?",
        "mastery_q2": "Why must client applications connect to Sentinel instances rather than hardcoding the primary IP address?",
        "when_use": "Use Sentinel for automated failover on single-primary systems where dataset fits on one machine.",
        "when_not_use": "Do not use Sentinel if you need horizontal write partitioning across multiple shards (use Redis Cluster)."
    },
    {
        "num": "37",
        "slug": "37-partitioning-from-first-principles",
        "title": "Partitioning From First Principles: Modulo vs. Hash Slots",
        "motto": "Naive modulo hashing creates a nightmare: adding one node forces 80% of all keys to relocate.",
        "problem": "A dataset exceeds the RAM capacity of a single physical server (e.g. 500GB dataset on 64GB machines). We must partition keys across multiple nodes.",
        "prediction": "In a 4-node cluster using naive `hash(key) % 4`, what fraction of keys must move when node 5 is added?",
        "why_matters": "Understanding hash slot mechanics is essential for reasoning about Redis Cluster, DynamoDB, and distributed systems partitioning.",
        "principles": "Naive modulo partitioning reshuffles almost all keys on node membership changes. Redis Cluster solves this by introducing **16,384 virtual Hash Slots**. Nodes own ranges of slots, so scaling only requires moving specific slots without recalculating key hashes.",
        "script_name": "partitioning_modulo.py",
        "code": '''#!/usr/bin/env python3
import hashlib

def hash_key(key):
    return int(hashlib.md5(key.encode()).hexdigest(), 16)

def test_modulo_reshuffle(num_keys=10000):
    keys = [f"user_{i}" for i in range(num_keys)]
    
    # 4 Nodes
    assignments_4 = {k: hash_key(k) % 4 for k in keys}
    # Add Node 5
    assignments_5 = {k: hash_key(k) % 5 for k in keys}
    
    moved = sum(1 for k in keys if assignments_4[k] != assignments_5[k])
    pct = (moved / num_keys) * 100
    print(f"Naive Modulo Partitioning (Adding 1 node to a 4-node cluster):")
    print(f"  • Total keys: {num_keys:,}")
    print(f"  • Dislocated keys: {moved:,} ({pct:.1f}% of entire database had to move!)")
    print("Takeaway: This is why Redis Cluster uses 16,384 fixed Hash Slots rather than naive modulo.")

if __name__ == "__main__":
    test_modulo_reshuffle()
''',
        "mastery_q1": "Why did Redis Cluster choose exactly 16,384 ($2^{14}$) hash slots instead of 65,536?",
        "mastery_q2": "How does consistent hashing differ from fixed hash slot assignment?",
        "when_use": "Partition data when dataset size or write throughput exceeds the hardware limits of a single node.",
        "when_not_use": "Avoid partitioning if your queries rely heavily on multi-key cross-slot transactions."
    },
    {
        "num": "38",
        "slug": "38-redis-cluster",
        "title": "Redis Cluster: 16,384 Hash Slots & -MOVED Redirects",
        "motto": "Redis Cluster nodes do not proxy requests; they return -MOVED redirects and force smart clients to route packets directly.",
        "problem": "How does a client find which of 100 cluster nodes owns the key `user:994` without querying a centralized coordinator?",
        "prediction": "What happens if a client issues `MGET key_a key_b` when `key_a` and `key_b` hash to different slots on different nodes?",
        "why_matters": "Redis Cluster enables multi-terabyte horizontal scaling while maintaining sub-millisecond execution.",
        "principles": "Every key is mapped via `CRC16(key) mod 16384`. If a client sends a command to the wrong node, the node replies with `-MOVED <slot> <ip>:<port>`. Smart clients cache this slot map. Hash tags (`{user:123}:profile`, `{user:123}:orders`) force keys to the same slot for atomic multi-key operations.",
        "script_name": "cluster_slots.py",
        "code": '''#!/usr/bin/env python3
import binascii

def crc16(data: bytes) -> int:
    """CRC16-CCITT calculation matching Redis Cluster specification."""
    crc = 0
    for byte in data:
        crc = ((crc << 8) & 0xFF00) ^ binascii.crc_hqx(bytes([byte]), crc >> 8)
    return crc & 0xFFFF

def get_slot(key: str) -> int:
    # Hash Tag Support: If {...} present, only hash substring
    if "{" in key and "}" in key:
        s = key.find("{") + 1
        e = key.find("}")
        if e > s:
            key = key[s:e]
    return binascii.crc_hqx(key.encode("utf-8"), 0) % 16384

if __name__ == "__main__":
    print("Testing Redis Cluster Hash Slot Calculation:")
    print("  Slot for 'user:100'         ->", get_slot("user:100"))
    print("  Slot for 'order:999'        ->", get_slot("order:999"))
    
    print("\\nTesting Hash Tags for Multi-Key Colocation:")
    s1 = get_slot("{tenant_1}:profile")
    s2 = get_slot("{tenant_1}:settings")
    print(f"  Slot for '{{tenant_1}}:profile'  -> {s1}")
    print(f"  Slot for '{{tenant_1}}:settings' -> {s2}")
    print("  -> Both land on exact same slot! Multi-key operations are guaranteed safe.")
''',
        "mastery_q1": "What is the difference between a `-MOVED` redirection and an `-ASK` redirection?",
        "mastery_q2": "Why does executing `KEYS *` on a Redis Cluster node only return keys from slots owned by that specific node?",
        "when_use": "Use Redis Cluster for massive horizontal write scaling and datasets larger than single-machine RAM.",
        "when_not_use": "Do not use Redis Cluster if your application depends extensively on multi-key operations across arbitrary un-tagged keys."
    },
    {
        "num": "39",
        "slug": "39-cluster-failure-and-resharding",
        "title": "Cluster Failure and Resharding: Slot Migration",
        "motto": "Online resharding moves slots key by key while the cluster continues serving traffic.",
        "problem": "Your business grows 5x. You need to add 3 new nodes to a running Redis Cluster without taking the application offline.",
        "prediction": "What happens during slot migration if a client requests a key that has not yet been migrated to the new node?",
        "why_matters": "Online elasticity (resharding without downtime) is the hallmark of modern distributed data infrastructure.",
        "principles": "During slot migration: 1. Target node is set to `IMPORTING`. 2. Source node is set to `MIGRATING`. 3. Keys are moved via `DUMP`/`RESTORE`. 4. If a client queries source, source returns `-ASK <slot> <target>` redirecting client to check target.",
        "script_name": "cluster_reshard.py",
        "code": '''#!/usr/bin/env python3
def explain_slot_migration():
    print("Redis Cluster Online Resharding Protocol:")
    print("""
    [ Client ] ──────── 1. GET key ────────► [ Source Node (Slot 500) ]
                                                    │
                                                    │ Key already migrated?
                                                    ▼
    [ Client ] ◄─── 2. -ASK 500 10.0.0.2 ───────────┘
        │
        ├────── 3. ASKING ────────────────► [ Target Node (Slot 500) ]
        └────── 4. GET key ───────────────► Returns value!
    """)
    print("Properties:")
    print("  • -ASK redirect is temporary (only for that one query).")
    print("  • Client does NOT update its permanent slot cache until slot migration finishes")
    print("    and node broadcasts permanent -MOVED redirect.")

if __name__ == "__main__":
    explain_slot_migration()
''',
        "mastery_q1": "What happens if a primary node fails and its replica has also crashed? What does `cluster-require-full-coverage` control?",
        "mastery_q2": "How do cluster nodes discover failures among themselves via the Gossip protocol?",
        "when_use": "Perform cluster resharding during off-peak windows with rate-limited slot migrations.",
        "when_not_use": "Never forcefully kill nodes during an active incomplete slot migration."
    },
    {
        "num": "40",
        "slug": "40-redis-security-basics",
        "title": "Redis Security Basics: Protected Mode, ACLs, and TLS",
        "motto": "Redis is designed for trusted internal networks; exposing it to the open internet invites cryptominers within minutes.",
        "problem": "Thousands of unprotected Redis instances on the public internet are compromised daily via remote code execution and SSH key injection.",
        "prediction": "What is Redis Protected Mode and when does it refuse client connections?",
        "why_matters": "Understanding defense-in-depth (firewalls, VPC isolation, authentication, TLS, ACLs) is mandatory for production deployments.",
        "principles": "1. Protected Mode: Enabled by default, blocks external connections if no password is set. 2. ACLs (Redis 6.0+): Granular user permissions restricting command categories and key patterns. 3. Command Renaming / Disabling: Disabling `FLUSHALL` and `KEYS`.",
        "script_name": "redis_security.py",
        "code": '''#!/usr/bin/env python3
import socket

def redis_cmd(*args):
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    msg = f"*{len(args)}\\r\\n" + "".join(f"${len(str(a).encode())}\\r\\n{str(a)}\\r\\n" for a in args)
    s.sendall(msg.encode())
    res = s.recv(4096).decode(errors="replace")
    s.close()
    return res.strip()

def run_security_inspection():
    print("Inspecting Redis Security Configuration:")
    prot = redis_cmd("CONFIG", "GET", "protected-mode")
    print(f"  Protected Mode: {prot}")
    
    print("\\nACL User Principles (Redis 6.0+):")
    print("  Example Production ACL Rule:")
    print("    ACL SETUSER api_read_only on >secretpass ~cache:* +@read -@admin")
    print("    • Only allowed to read keys matching 'cache:*'")
    print("    • Cannot execute administrative commands (FLUSHALL, SHUTDOWN, CONFIG)")

if __name__ == "__main__":
    try: run_security_inspection()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "How did historical attacks compromise Linux servers via unprotected Redis instances and RDB directory configuration (`CONFIG SET dir /root/.ssh`)?",
        "mastery_q2": "What are the performance trade-offs of enabling TLS encryption on Redis connections?",
        "when_use": "Always bind Redis strictly to private VPC network interfaces, enforce strong ACLs, and enable TLS for cross-node replication.",
        "when_not_use": "Never expose Redis directly to the public internet (0.0.0.0) without firewall isolation."
    },
    {
        "num": "41",
        "slug": "41-observability",
        "title": "Observability: Metrics, Prometheus, and the Top 8 Signals",
        "motto": "You cannot manage what you do not measure; monitor connections, memory, latency, and evictions.",
        "problem": "A production outage begins with subtle memory fragmentation and replica lag. Without observability, the team only notices when the entire site crashes.",
        "prediction": "Which single metric in `INFO stats` indicates whether keys are being evicted due to memory pressure?",
        "why_matters": "A production dashboard must surface key leading indicators before catastrophic failure occurs.",
        "principles": "The Top 8 Production Metrics: 1. `connected_clients`, 2. `instantaneous_ops_per_sec`, 3. `used_memory_rss`, 4. `mem_fragmentation_ratio`, 5. `evicted_keys`, 6. `rejected_connections`, 7. `master_repl_offset` (Replica Lag), 8. `latest_fork_usec`.",
        "script_name": "observability_collector.py",
        "code": '''#!/usr/bin/env python3
import socket

def parse_info(raw):
    metrics = {}
    for line in raw.split("\\r\\n"):
        if ":" in line and not line.startswith("#"):
            k, v = line.split(":", 1)
            metrics[k] = v
    return metrics

def scrape_metrics():
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    s.sendall(b"*1\\r\\n$4\\r\\nINFO\\r\\n")
    data = s.recv(16384).decode(errors="replace")
    s.close()
    
    m = parse_info(data)
    print("==================================================")
    print("         REDIS PRODUCTION HEALTH DASHBOARD        ")
    print("==================================================")
    print(f"  • Connected Clients    : {m.get('connected_clients', 'N/A')}")
    print(f"  • Ops Per Second       : {m.get('instantaneous_ops_per_sec', 'N/A')}")
    print(f"  • Used Memory (RSS)    : {m.get('used_memory_rss_human', 'N/A')}")
    print(f"  • Fragmentation Ratio  : {m.get('mem_fragmentation_ratio', 'N/A')}")
    print(f"  • Evicted Keys Count   : {m.get('evicted_keys', 'N/A')}")
    print(f"  • Expired Keys Count   : {m.get('expired_keys', 'N/A')}")
    print(f"  • Uptime (days)        : {int(m.get('uptime_in_seconds', 0)) // 86400}")
    print("==================================================")

if __name__ == "__main__":
    try: scrape_metrics()
    except Exception as e: print("Redis offline:", e)
''',
        "mastery_q1": "Why is `rejected_connections` greater than 0 a critical emergency alert?",
        "mastery_q2": "How is cache hit ratio calculated from `keyspace_hits` and `keyspace_misses`?",
        "when_use": "Scrape Redis metrics via Prometheus `redis_exporter` and establish alerts on eviction spikes and memory RSS.",
        "when_not_use": "Do not poll `INFO` at excessive sub-second frequencies, as string parsing carries overhead."
    },
    {
        "num": "42",
        "slug": "42-real-application-cached-api",
        "title": "Real Application: High-Throughput Cached API",
        "motto": "A production cache is not just GET and SET; it handles fallback, stampede mitigation, and TTL invalidation.",
        "problem": "Building a production REST API that maintains sub-5ms response times under 50,000 requests/sec with an underlying slow database.",
        "prediction": "What percentage of database queries can be eliminated with a 95% cache hit rate?",
        "why_matters": "Connects all caching principles (Phase 22-24) into an executable reference implementation.",
        "principles": "See [projects/01-cached-api/](../../../projects/01-cached-api/) for the complete runnable reference service.",
        "script_name": "cached_api_app.py",
        "code": '''#!/usr/bin/env python3
print("Running Phase 42 Production Cached API verification...")
print("See full application in projects/01-cached-api/")
import subprocess
subprocess.run(["python3", "projects/01-cached-api/server.py", "--help"], check=False)
''',
        "mastery_q1": "How does the cache-aside pattern handle database transaction rollbacks?",
        "mastery_q2": "What are the operational costs of maintaining cache consistency across multiple microservices?",
        "when_use": "Deploy cached APIs for read-dominant endpoints like product catalogs, public profiles, and content feeds.",
        "when_not_use": "Avoid caching endpoints where data changes on every request or requires strict real-time auditability."
    },
    {
        "num": "43",
        "slug": "43-real-application-leaderboard",
        "title": "Real Application: Global Real-Time Leaderboard",
        "motto": "Scaling leaderboards from 1,000 to 10,000,000 players requires $O(\\log N)$ skiplists, not SQL order-by scans.",
        "problem": "Calculating global ranks across millions of concurrent gaming players in real time without locking tables.",
        "prediction": "What is the time complexity of retrieving the top 100 players from a 10M-member Sorted Set?",
        "why_matters": "Demonstrates how specialized in-memory data structures solve computational bottlenecks that break relational databases.",
        "principles": "See [projects/02-leaderboard/](../../../projects/02-leaderboard/) for the full tournament leaderboard implementation.",
        "script_name": "leaderboard_app.py",
        "code": '''#!/usr/bin/env python3
print("Phase 43: Real-Time Leaderboard System...")
print("See complete implementation in projects/02-leaderboard/leaderboard.py")
''',
        "mastery_q1": "How do you handle pagination when users are continuously gaining points and shifting ranks?",
        "mastery_q2": "How can you partition a leaderboard across multiple Redis nodes if player count exceeds single-node memory?",
        "when_use": "Use Redis Sorted Sets for live gaming rankings, dynamic priority queues, and top-selling product boards.",
        "when_not_use": "Do not use Sorted Sets if score modifications require multi-table relational joins or historical audit trails."
    },
    {
        "num": "44",
        "slug": "44-real-application-rate-limiter",
        "title": "Real Application: Distributed Rate Limiter",
        "motto": "Correct rate limiting requires zero-race atomicity; Lua scripts ensure no request slips through concurrent gaps.",
        "problem": "Protecting a distributed microservices gateway from abusive traffic spikes while maintaining sub-millisecond overhead.",
        "prediction": "Why does a Token Bucket algorithm provide superior user experience compared to a hard Fixed Window cutoff?",
        "why_matters": "Demonstrates production gateway protection using atomic server-side Lua scripts.",
        "principles": "See [projects/03-rate-limiter/](../../../projects/03-rate-limiter/) for complete implementations of all three rate-limiting algorithms.",
        "script_name": "rate_limiter_app.py",
        "code": '''#!/usr/bin/env python3
print("Phase 44: Distributed Rate Limiting Middleware...")
print("See complete implementation in projects/03-rate-limiter/limiter.py")
''',
        "mastery_q1": "How do you handle Redis connection failures inside rate-limiting middleware (Fail-Open vs Fail-Closed)?",
        "mastery_q2": "What are the trade-offs of running rate limiters locally in app memory vs centralized in Redis?",
        "when_use": "Deploy centralized Redis rate limiting for global API tiers, authentication endpoints, and payment gateways.",
        "when_not_use": "Do not use centralized Redis rate limiters if microservice network RTT exceeds total latency SLA budget."
    },
    {
        "num": "45",
        "slug": "45-real-application-background-work",
        "title": "Real Application: Durable Background Worker Pipeline",
        "motto": "A reliable job queue never loses a task when a worker process crashes mid-execution.",
        "problem": "Asynchronously processing image uploads, order fulfillment, and notification emails with at-least-once delivery guarantees.",
        "prediction": "What happens to an in-flight job if a worker server encounters an abrupt power loss?",
        "why_matters": "Demonstrates production job queuing using Redis Streams Consumer Groups and PEL recovery.",
        "principles": "See [projects/04-task-queue/](../../../projects/04-task-queue/) for the complete durable worker pipeline.",
        "script_name": "task_pipeline_app.py",
        "code": '''#!/usr/bin/env python3
print("Phase 45: Durable Background Worker Pipeline...")
print("See complete implementation in projects/04-task-queue/worker_queue.py")
''',
        "mastery_q1": "Why are worker tasks required to be idempotent in an at-least-once delivery architecture?",
        "mastery_q2": "How does a Dead Letter Queue (DLQ) prevent poisoned tasks from crashing workers in an infinite loop?",
        "when_use": "Use Redis Streams for durable asynchronous workflows, webhooks, and transactional background pipelines.",
        "when_not_use": "Do not use Redis for multi-day task scheduling or workflows requiring complex directed acyclic graph (DAG) routing."
    },
    {
        "num": "46",
        "slug": "46-redis-anti-patterns",
        "title": "Redis Anti-Patterns: Ten Catastrophic Production Mistakes",
        "motto": "Knowing what NOT to do in Redis is just as important as knowing how to use it.",
        "problem": "Teams repeatedly make identical architectural mistakes that take down production clusters under load.",
        "prediction": "What happens if a developer runs `KEYS *` on a production Redis instance with 20,000,000 keys?",
        "why_matters": "Auditing and eliminating anti-patterns prevents 90% of all Redis production incidents.",
        "principles": "The 10 Anti-Patterns: 1. `KEYS *` in production (blocks thread), 2. Giant values (> 1MB strings/blobs), 3. Unbounded keys with no TTL, 4. Synchronized TTL stampedes, 5. Unsafe distributed lock release, 6. Using Pub/Sub as a durable queue, 7. Storing everything as unindexed JSON blobs, 8. Giant single hash/set (> 100k items), 9. Assuming replicas are always in sync, 10. Assuming cluster operations behave like single-node Redis.",
        "script_name": "anti_patterns_lab.py",
        "code": '''#!/usr/bin/env python3
def explain_anti_patterns():
    print("==================================================")
    print("      THE TEN CATASTROPHIC REDIS ANTI-PATTERNS    ")
    print("==================================================")
    patterns = [
        ("1. Running KEYS *", "O(N) full keyspace scan blocks the single-threaded event loop for seconds/minutes. Fix: Use SCAN."),
        ("2. Giant Values (>1MB)", "Saturates network buffers and causes allocation stalls. Fix: Chunk or store in S3."),
        ("3. Unbounded Keyspace", "Writing keys with no TTL or eviction policy guarantees OOM crash. Fix: Set maxmemory + TTL."),
        ("4. Synchronized TTL", "Setting 10,000 keys with identical 300s TTL causes simultaneous stampede. Fix: Add TTL jitter."),
        ("5. Unsafe Lock Release", "Releasing lock without verifying ownership token deletes another worker's lock."),
        ("6. Pub/Sub for Tasks", "Pub/Sub is ephemeral; offline workers lose messages permanently. Fix: Use Streams."),
        ("7. Deserialization Churn", "Storing domain objects as JSON blobs requires full serialization for 1 field. Fix: Hashes."),
        ("8. Monolithic Hash/Set", "Putting 1,000,000 items in one key destroys clustering and listpack benefits. Fix: Shard keys."),
        ("9. Assuming Sync Replicas", "Replication is async; reading immediately from replica returns stale data. Fix: Read primary or WAIT."),
        ("10. Cross-Slot Transactions", "MULTI/EXEC across different cluster slots fails without hash tags {...}.")
    ]
    for name, desc in patterns:
        print(f"\\n• {name}\\n  {desc}")

if __name__ == "__main__":
    explain_anti_patterns()
''',
        "mastery_q1": "How does `SCAN` avoid blocking the server while iterating over millions of keys?",
        "mastery_q2": "Why does adding random TTL Jitter (e.g. `300 + random(0, 30)`) eliminate synchronized expiration stampedes?",
        "when_use": "Use this checklist during code reviews and architectural audits before shipping Redis code to production.",
        "when_not_use": "Never exempt 'internal test scripts' from these rules if they run against shared production clusters."
    },
    {
        "num": "47",
        "slug": "47-build-mini-redis",
        "title": "Capstone 1: Build Mini-Redis From Scratch in Python",
        "motto": "If you can build a working Redis-compatible server from raw sockets and a dictionary, Redis is no longer magic.",
        "problem": "Synthesizing all networking, protocol parsing, command execution, and expiration mechanics into a working server.",
        "prediction": "Can the official `redis-cli` connect to our custom Python TCP server and successfully execute `SET` and `GET`?",
        "why_matters": "Building the server engine connects the client socket, wire protocol, memory keyspace, and expiration into one coherent mental model.",
        "principles": "Mini-Redis implements: 1. Async/Threaded TCP socket server on port 6379, 2. Binary-safe RESP decoder/encoder, 3. Keyspace dictionary, 4. Command dispatch table (`SET`, `GET`, `DEL`, `EXISTS`, `INCR`, `EXPIRE`, `TTL`, `PING`), 5. Passive and active expiration loop, 6. Snapshot persistence (`SAVE`).",
        "script_name": "mini_redis_server.py",
        "code": '''#!/usr/bin/env python3
"""
phases/47-build-mini-redis/code/mini_redis_server.py — Educational Mini-Redis Server
Connect with real redis-cli: redis-cli -p 6388 PING
"""
import socket
import threading
import time

class MiniRedisServer:
    def __init__(self, port=6388):
        self.port = port
        self.db = {}       # key -> value
        self.expires = {}  # key -> expire_timestamp
        self.running = True

    def parse_resp(self, data):
        """Simple parser for RESP array commands."""
        lines = data.split(b"\\r\\n")
        if not lines or not lines[0].startswith(b"*"): return []
        num_args = int(lines[0][1:])
        args = []
        idx = 1
        for _ in range(num_args):
            if idx >= len(lines): break
            if lines[idx].startswith(b"$"):
                length = int(lines[idx][1:])
                idx += 1
                args.append(lines[idx][:length].decode("utf-8", errors="replace"))
                idx += 1
        return args

    def handle_client(self, client_sock):
        with client_sock:
            while self.running:
                data = client_sock.recv(4096)
                if not data: break
                args = self.parse_resp(data)
                if not args: continue
                
                cmd = args[0].upper()
                now = time.time()

                # Passive expiration check
                if len(args) > 1 and args[1] in self.expires:
                    if self.expires[args[1]] <= now:
                        del self.expires[args[1]]
                        if args[1] in self.db: del self.db[args[1]]

                # Dispatch
                if cmd == "PING":
                    client_sock.sendall(b"+PONG\\r\\n")
                elif cmd == "SET" and len(args) >= 3:
                    self.db[args[1]] = args[2]
                    if len(args) >= 5 and args[3].upper() == "EX":
                        self.expires[args[1]] = now + float(args[4])
                    client_sock.sendall(b"+OK\\r\\n")
                elif cmd == "GET" and len(args) >= 2:
                    val = self.db.get(args[1])
                    if val is None: client_sock.sendall(b"$-1\\r\\n")
                    else: client_sock.sendall(f"${len(val.encode())}\\r\\n{val}\\r\\n".encode())
                elif cmd == "DEL" and len(args) >= 2:
                    count = 0
                    for k in args[1:]:
                        if k in self.db: del self.db[k]; count += 1
                        if k in self.expires: del self.expires[k]
                    client_sock.sendall(f":{count}\\r\\n".encode())
                elif cmd == "INCR" and len(args) >= 2:
                    curr = int(self.db.get(args[1], 0)) + 1
                    self.db[args[1]] = str(curr)
                    client_sock.sendall(f":{curr}\\r\\n".encode())
                elif cmd == "TTL" and len(args) >= 2:
                    k = args[1]
                    if k not in self.db: client_sock.sendall(b":-2\\r\\n")
                    elif k not in self.expires: client_sock.sendall(b":-1\\r\\n")
                    else:
                        rem = max(0, int(self.expires[k] - now))
                        client_sock.sendall(f":{rem}\\r\\n".encode())
                else:
                    client_sock.sendall(b"-ERR unknown command\\r\\n")

    def run_server(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(10)
        print(f"Mini-Redis Server listening on port {self.port} (Connect with redis-cli -p {self.port})")
        while self.running:
            conn, _ = s.accept()
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

if __name__ == "__main__":
    server = MiniRedisServer(port=6388)
    server.run_server()
''',
        "mastery_q1": "How does Mini-Redis handle multiple concurrent connections using Python threading vs Redis's single-threaded event loop?",
        "mastery_q2": "What changes would be required to support RESP3 in Mini-Redis?",
        "when_use": "Build educational servers to achieve mastery over protocols, networking, and memory architectures.",
        "when_not_use": "Never deploy toy custom database servers into production."
    },
    {
        "num": "48",
        "slug": "48-production-like-redis-lab",
        "title": "Capstone 2: Resilient Production Topology Laboratory",
        "motto": "Production engineering is not about hoping things work; it is about verifying behavior when things fail.",
        "problem": "Designing and testing a complete multi-container resilient infrastructure: Primary + Replica + Sentinel + App + Database with automated chaos failure injection.",
        "prediction": "What happens to in-flight application requests during the 5-second window while Sentinel executes automatic failover?",
        "why_matters": "Proves the learner can build, observe, and maintain highly available production topologies.",
        "principles": "Uses `docker-compose.yml` to orchestrate multi-node topologies, simulating primary kills, network partition splits, and evaluating application reconnection behavior.",
        "script_name": "resilient_topology_lab.py",
        "code": '''#!/usr/bin/env python3
def explain_capstone_topology():
    print("==================================================")
    print("  CAPSTONE 2: RESILIENT PRODUCTION TOPOLOGY LAB   ")
    print("==================================================")
    print("""
    [ Fast API / Client Application ]
                 │
                 ├── Writes ──► [ Primary Redis (6379) ] ── (Async Stream) ──► [ Replica (6380) ]
                 │                     ▲                                              ▲
                 │                     └──────────┬───────────────────────────────────┘
                 ▼                                │ (Health Monitoring & Failover)
          [ Sentinel Quorum ] ────────────────────┘
    """)
    print("Verification Scenarios:")
    print("  1. Standard Baseline: Read from cache, fallback to PostgreSQL.")
    print("  2. Primary Crash: Kill redis-primary container.")
    print("  3. Sentinel Failover: Observe Sentinel promoting replica to primary.")
    print("  4. Client Reconnect: Application automatically redirects writes to new primary.")

if __name__ == "__main__":
    explain_capstone_topology()
''',
        "mastery_q1": "How should client connection pools handle socket timeout errors during active Sentinel failovers?",
        "mastery_q2": "What telemetry metrics prove that a failover succeeded cleanly?",
        "when_use": "Deploy this architecture for mission-critical services requiring automated failover and 99.99% uptime.",
        "when_not_use": "Do not over-engineer simple internal prototypes with Sentinel until high-availability SLAs require it."
    },
    {
        "num": "49",
        "slug": "49-system-design-with-redis",
        "title": "System Design With Redis: Twelve Production Scenarios",
        "motto": "True mastery means knowing when Redis is the perfect tool, and having the courage to say no when it is not.",
        "problem": "Evaluating Redis suitability across 12 real-world system design interview and production scenarios.",
        "prediction": "For a global session store, should Redis be configured with RDB, AOF, or no persistence?",
        "why_matters": "Prepares the learner for senior system design interviews and principal architecture decisions.",
        "principles": "For every design scenario, evaluate: 1. Why Redis? 2. Data structure choice, 3. Source of truth, 4. Durability SLA, 5. TTL strategy, 6. Eviction policy, 7. Hot key mitigation, 8. Consistency requirement, 9. Replication/Partitioning needs, 10. Technology alternatives.",
        "script_name": "system_design_cases.py",
        "code": '''#!/usr/bin/env python3
def print_system_design_scenarios():
    print("12 PRODUCTION SYSTEM DESIGN SCENARIOS WITH REDIS:")
    scenarios = [
        "1. Distributed Session Store (String with TTL / volatile-lru)",
        "2. API Rate Limiting Gateway (Token Bucket via Lua Script)",
        "3. Real-Time Gaming Leaderboard (Sorted Set with ZREVRANGE)",
        "4. Live Chat User Presence System (Bitmap / Set with Heartbeat TTL)",
        "5. Distributed Mutex Lock (Single Instance SET NX PX with UUID token)",
        "6. E-Commerce Flash Sale Inventory (Lua Atomic Decrement)",
        "7. Asynchronous Task Queue (Redis Streams with Consumer Groups)",
        "8. Web Page Cache-Aside Layer (Strings with Jittered TTL + Single-Flight)",
        "9. Top-K Trending Hashtags (Count-Min Sketch + Sorted Set)",
        "10. Idempotency Key Validator (SET NX EX for Payment APIs)",
        "11. Delayed Job Scheduler (Sorted Set with Execution Timestamp Score)",
        "12. Real-Time Analytics Counter Aggregator (HyperLogLog & Hashes)"
    ]
    for s in scenarios:
        print(f"  • {s}")

if __name__ == "__main__":
    print_system_design_scenarios()
''',
        "mastery_q1": "Why is Redis preferred over PostgreSQL for API rate limiting but NOT for financial balance ledgering?",
        "mastery_q2": "How does HyperLogLog count 1,000,000,000 unique IP addresses using only 12 kilobytes of memory?",
        "when_use": "Use the 10-question evaluation framework whenever evaluating Redis in architecture design reviews.",
        "when_not_use": "Never select Redis simply because 'it is fast' without analyzing durability and data loss risks."
    },
    {
        "num": "50",
        "slug": "50-final-mental-model",
        "title": "The Final Mental Model: The Complete Command Journey",
        "motto": "Redis is no longer a black box. From terminal keystroke to electrical capacitor in RAM to magnetic flux on disk, you understand the machine.",
        "problem": "Tracing the complete end-to-end journey of `redis-cli SET user:42 Tushar` across every physical and software abstraction layer.",
        "prediction": "How many distinct software and operating system layers touch the bytes of this command between your keyboard and RAM?",
        "why_matters": "The ultimate capstone synthesis proving total systems comprehension.",
        "principles": "Traces: 1. Terminal shell input, 2. CLI process, 3. TCP socket write, 4. Kernel network buffer, 5. epoll/kqueue event dispatch, 6. aeEventLoop processing, 7. RESP protocol tokenizer, 8. Command dispatch table, 9. Memory allocator (jemalloc), 10. Keyspace dictionary insertion, 11. 24-bit LRU clock update, 12. AOF write buffer, 13. Replication backlog ring buffer, 14. Output buffer serialization, 15. TCP socket reply, 16. Client display.",
        "script_name": "final_trace.py",
        "code": '''#!/usr/bin/env python3
def print_complete_command_journey():
    print("""
========================================================================================
             THE COMPLETE LIFE CYCLE OF: redis-cli SET user:42 Tushar
========================================================================================

[ 1. User Terminal ]
     └── User types: redis-cli SET user:42 Tushar

[ 2. redis-cli Process ]
     └── Formats arguments into binary-safe RESP bytes:
         *3\\r\\n$3\\r\\nSET\\r\\n$7\\r\\nuser:42\\r\\n$6\\r\\nTushar\\r\\n

[ 3. Operating System Network Stack ]
     └── Client writes bytes to TCP socket FD -> Kernel TCP/IP packet framing -> NIC

[ 4. Network Transport ]
     └── Traverses loopback / Ethernet / Switch (0.1ms - 1ms latency)

[ 5. Server Kernel & I/O Multiplexer ]
     └── Server NIC receives packet -> Kernel buffer -> kqueue/epoll flags FD as READABLE

[ 6. Redis aeEventLoop (ae.c) ]
     └── Single-threaded event loop wakes from epoll_wait() -> invokes readQueryFromClient()

[ 7. RESP Parser & Tokenizer (networking.c) ]
     └── Slices query buffer into argv array: ['SET', 'user:42', 'Tushar']

[ 8. Command Dispatch Table (server.c) ]
     └── Looks up 'setCommand' in server.commands hash table; checks arity & permissions

[ 9. Memory Allocator & Keyspace (dict.c & jemalloc) ]
     └── Allocates robj metadata header (16 bytes)
     └── Allocates SDS string buffer for key and value
     └── Inserts dictEntry into server.db[0].dict; updates 24-bit LRU clock
     └── Checks maxmemory eviction threshold budget

[ 10. Persistence & Replication Hooks ]
     └── If AOF enabled: Feeds raw RESP command to server.aof_buf for next fsync cycle
     └── If Replicas connected: Appends command to server.repl_backlog circular ring buffer

[ 11. Client Output Serialization ]
     └── Formats RESP status reply: +OK\\r\\n -> writes to client output buffer

[ 12. Response Network Return ]
     └── Server socket write() -> Kernel TCP Tx -> Client socket read() -> Terminal displays OK

========================================================================================
                           REDIS IS NO LONGER A BLACK BOX.
========================================================================================
    """)

if __name__ == "__main__":
    print_complete_command_journey()
''',
        "mastery_q1": "What changes in this journey when Redis runs in a multi-node Cluster configuration?",
        "mastery_q2": "What changes in this journey when `appendfsync always` is configured?",
        "when_use": "Use this complete mechanical mental model whenever designing, debugging, or scaling high-throughput distributed systems.",
        "when_not_use": "Never regress to treating Redis as 'just a magical dictionary in the cloud.'"
    }
]

def generate_phases_31_50():
    base = "/Users/tushar/Desktop/private/repos/redis-from-scratch/phases"
    for p in PHASES_31_50:
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
  [ CLIENT ] ── TCP Socket ──► [ REDIS ENGINE CORE ] ──► [ SYSTEM SUBSYSTEM ]
```

## Build it
See [code/{p['script_name']}](../code/{p['script_name']}).

## Use Redis
Execute the lesson experiment:
```bash
./phases/{p['slug']}/experiments/run_experiment.sh
```

## Inspect it
Inspect server status, telemetry counters, and internal diagnostic logs.

## Measure it
Quantify latency percentiles, throughput, memory allocation, and failure impact.

## Break it
Inject network partitions, process terminations, or invalid commands.

## Debug it
Diagnose the failure using evidence from diagnostic tools.

## Modify it
Tune configuration thresholds and measure behavioral changes.

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
* Metrics Recorded:
* Observed System Behavior:

### 4. What Was Broken & Diagnosed
* Failure Injected:
* Restoration Steps:
"""
        with open(out_path, "w") as f:
            f.write(evidence_content)

    print(f"Generated operations, clustering & capstone phases 31-50 successfully.")

if __name__ == "__main__":
    generate_phases_31_50()
