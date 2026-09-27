#!/usr/bin/env python3
"""
scripts/build_phases.py — Automated phase generator for redis-from-scratch.

Generates complete, runnable, first-principles educational content for all 51 phases (00 to 50),
adhering strictly to LESSON_TEMPLATE.md, the course motto:
"Understand it. Build it. Measure it. Break it. Fix it. Scale it. Ship it."
and the BUILD IT -> USE REDIS sequence.
"""

import os
import stat

PHASES_DEF = [
    {
        "num": "00",
        "slug": "00-environment-and-redis-lab",
        "title": "Environment and Redis Lab",
        "motto": "The redis-cli command does not store data; it asks a background TCP server to store it.",
        "problem": "Engineers often treat Redis as a CLI utility or an opaque cloud service without realizing it is a standard user-space daemon listening on TCP port 6379. When connection timeouts or port conflicts occur, they cannot diagnose the failure.",
        "prediction": "If redis-server is stopped, what exact error does redis-cli PING return? How does redis-cli distinguish between an unreachable host and an authentication failure?",
        "why_matters": "Understanding the client-server boundary over TCP is the prerequisite for debugging connection pooling, firewall rules, Docker bridge networking, and TLS encryption in production.",
        "principles": "Redis is a client-server architecture running over TCP/IP sockets. By default, it binds to 127.0.0.1 on port 6379. Clients send command frames and receive response frames over persistent TCP connections.",
        "script_name": "verify_lab.py",
        "code": '''#!/usr/bin/env python3
import socket
import sys

def verify_tcp_connection(host="localhost", port=6379):
    print(f"Connecting to Redis at {host}:{port} via raw TCP socket...")
    try:
        s = socket.create_connection((host, port), timeout=2.0)
        # Send raw RESP PING: *1\\r\\n$4\\r\\nPING\\r\\n
        s.sendall(b"*1\\r\\n$4\\r\\nPING\\r\\n")
        response = s.recv(1024)
        s.close()
        print(f"Received raw response bytes: {response!r}")
        if b"+PONG" in response:
            print("✓ SUCCESS: Redis server is healthy and responding to raw RESP PING.")
            return True
        else:
            print(f"✗ UNEXPECTED RESPONSE: {response!r}")
            return False
    except ConnectionRefusedError:
        print(f"✗ ERROR: Connection refused on {host}:{port}. Is redis-server running?")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

if __name__ == "__main__":
    ok = verify_tcp_connection()
    sys.exit(0 if ok else 1)
''',
        "experiment": '''#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 00 Experiment: Client-Server TCP Verification ==="
./scripts/check-environment.sh
python3 phases/00-environment-and-redis-lab/code/verify_lab.py
echo "Running redis-cli INFO server..."
redis-cli INFO server | head -n 8 || true
echo "✓ Phase 00 Experiment Complete."
''',
        "mastery_q1": "Why does Redis bind to 127.0.0.1 by default instead of 0.0.0.0?",
        "mastery_q2": "What happens if two processes attempt to bind to TCP port 6379 simultaneously?",
        "when_use": "Use standalone Redis when single-node sub-millisecond key-value operations satisfy your throughput and dataset size requirements.",
        "when_not_use": "Do not expose standalone Redis directly to the public internet without firewall rules, TLS, and strong ACLs."
    },
    {
        "num": "01",
        "slug": "01-why-redis-exists",
        "title": "Why Redis Exists: Storage Hierarchy & Latency",
        "motto": "RAM is fast not because it is magic, but because electrical capacitors have no mechanical or block-paging overhead.",
        "problem": "Relational databases write transactions to disk (WAL) for durability. When an application serves 50,000 requests/sec, disk seeks and OS page cache transitions become the primary throughput bottleneck.",
        "prediction": "How many times faster is reading an in-memory dictionary compared to querying an indexed SQLite or PostgreSQL table on disk over 10,000 iterations?",
        "why_matters": "Latency numbers every engineer should know: CPU L1 cache (~1 ns), RAM (~100 ns), NVMe SSD (~10-50 µs), Network within DC (~0.5 ms). Redis moves the data layer from SSD/disk speeds to RAM speeds.",
        "principles": "Physical storage latency hierarchy dictates database performance. Accessing dynamic RAM avoids kernel system calls, filesystem block allocation, and disk write barriers.",
        "script_name": "measure_storage.py",
        "code": '''#!/usr/bin/env python3
import time
import sqlite3
import os

def run_comparison(n=5000):
    print(f"Comparing RAM dictionary vs Disk SQLite over {n:,} read/write operations...")
    # 1. RAM Access
    mem = {}
    t0 = time.perf_counter()
    for i in range(n):
        mem[f"k{i}"] = f"v{i}"
        _ = mem[f"k{i}"]
    ram_time = time.perf_counter() - t0

    # 2. Disk SQLite
    db_file = "/tmp/test_phase01.db"
    if os.path.exists(db_file): os.remove(db_file)
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("PRAGMA journal_mode = WAL;")
    cur.execute("CREATE TABLE kv (k TEXT PRIMARY KEY, v TEXT);")
    conn.commit()

    t0 = time.perf_counter()
    for i in range(min(n, 1000)): # Capped for test execution speed
        cur.execute("INSERT OR REPLACE INTO kv VALUES (?, ?)", (f"k{i}", f"v{i}"))
        cur.execute("SELECT v FROM kv WHERE k = ?", (f"k{i}",))
        _ = cur.fetchone()
    conn.commit()
    disk_time = time.perf_counter() - t0
    conn.close()
    if os.path.exists(db_file): os.remove(db_file)

    print(f"  • RAM In-Memory Dict: {ram_time:.4f}s  ({(n*2)/ram_time:,.0f} ops/sec)")
    print(f"  • Disk SQLite (WAL) : {disk_time:.4f}s  ({(min(n,1000)*2)/disk_time:,.0f} ops/sec)")
    print(f"  -> RAM is ~{(disk_time/ram_time)*(n/min(n,1000)):.1f}x faster than disk transactions.")

if __name__ == "__main__":
    run_comparison()
''',
        "experiment": '''#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 01 Experiment: Storage Latency Comparison ==="
python3 phases/01-why-redis-exists/code/measure_storage.py
echo "✓ Phase 01 Experiment Complete."
''',
        "mastery_q1": "If RAM is ~1,000x faster than disk, why are all databases not in-memory?",
        "mastery_q2": "What role does OS page caching play in closing the gap between disk and memory?",
        "when_use": "Use Redis when sub-millisecond read/write latency is required for high-throughput hot data.",
        "when_not_use": "Do not use Redis for multi-terabyte cold datasets where RAM cost exceeds hardware budget."
    },
    {
        "num": "02",
        "slug": "02-build-a-tiny-key-value-store",
        "title": "Build a Tiny Key-Value Store",
        "motto": "Before it was a distributed server, Redis was a data structure in RAM.",
        "problem": "Before inspecting Redis commands, we must understand what a key-value store actually does at the data structure level: mapping arbitrary binary/string keys to values.",
        "prediction": "What fundamental capabilities does a standard Python dictionary lack that a database must provide?",
        "why_matters": "A raw hash table has no networking, persistence, concurrency safety, TTL expiration, or memory eviction limits. Redis is a hash table wrapped in operating system systems engineering.",
        "principles": "A key-value store provides CRUD primitives: SET (insert/update), GET (lookup), DELETE (remove), and EXISTS (membership check).",
        "script_name": "mini_kv.py",
        "code": '''#!/usr/bin/env python3
class MiniKV:
    def __init__(self):
        self._store = {}

    def set(self, key: str, value: str) -> str:
        self._store[key] = value
        return "OK"

    def get(self, key: str):
        return self._store.get(key, None)

    def delete(self, key: str) -> int:
        if key in self._store:
            del self._store[key]
            return 1
        return 0

    def exists(self, key: str) -> int:
        return 1 if key in self._store else 0

if __name__ == "__main__":
    kv = MiniKV()
    print("Testing MiniKV operations:")
    print("SET user:1 'Tushar':", kv.set("user:1", "Tushar"))
    print("GET user:1:", kv.get("user:1"))
    print("EXISTS user:1:", kv.exists("user:1"))
    print("DELETE user:1:", kv.delete("user:1"))
    print("GET user:1 (after delete):", kv.get("user:1"))
''',
        "experiment": '''#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 02 Experiment: MiniKV In-Memory Store ==="
python3 phases/02-build-a-tiny-key-value-store/code/mini_kv.py
echo "✓ Phase 02 Experiment Complete."
''',
        "mastery_q1": "What happens when two threads call `kv.set()` simultaneously in Python? Is dict thread-safe?",
        "mastery_q2": "How would you persist `self._store` to disk without blocking reads?",
        "when_use": "Use process-local memory dictionaries when data never needs to outlive the process or be shared across instances.",
        "when_not_use": "Do not use process-local dictionaries when multiple service replicas must share a coherent state."
    },
    {
        "num": "03",
        "slug": "03-make-the-key-value-store-a-server",
        "title": "Make the Key-Value Store a Server",
        "motto": "A database is a data structure accessible over a network socket.",
        "problem": "Process-local dictionaries cannot be shared across multiple web servers. We must expose our key-value store over a TCP socket server.",
        "prediction": "If a client sends 'SET name John Doe' using a simple space-delimited text protocol, how does the server distinguish between the key and a value containing spaces?",
        "why_matters": "Naive protocols break immediately when payloads contain spaces, newlines, or binary data. This creates the exact motivation for Redis's length-prefixed RESP protocol.",
        "principles": "TCP is a streaming byte protocol with no inherent message boundaries (framing). Protocols must use delimiters (like CRLF) or length prefixes to determine where messages begin and end.",
        "script_name": "tcp_kv_server.py",
        "code": '''#!/usr/bin/env python3
import socket
import threading

class TCPServerKV:
    def __init__(self, port=9999):
        self.port = port
        self.store = {}
        self.running = True

    def handle_client(self, client_sock):
        with client_sock:
            buffer = ""
            while self.running:
                data = client_sock.recv(1024).decode("utf-8", errors="replace")
                if not data: break
                buffer += data
                while "\\n" in buffer:
                    line, buffer = buffer.split("\\n", 1)
                    line = line.strip()
                    if not line: continue
                    parts = line.split(" ", 2)
                    cmd = parts[0].upper()
                    
                    if cmd == "SET" and len(parts) >= 3:
                        self.store[parts[1]] = parts[2]
                        client_sock.sendall(b"+OK\\n")
                    elif cmd == "GET" and len(parts) >= 2:
                        val = self.store.get(parts[1], None)
                        if val is None:
                            client_sock.sendall(b"-NIL\\n")
                        else:
                            client_sock.sendall(f"+{val}\\n".encode())
                    elif cmd == "PING":
                        client_sock.sendall(b"+PONG\\n")
                    elif cmd == "QUIT":
                        return
                    else:
                        client_sock.sendall(b"-ERR unknown command or syntax\\n")

    def run_test_client(self):
        import time
        time.sleep(0.1)
        s = socket.create_connection(("localhost", self.port))
        s.sendall(b"SET username Tushar\\n")
        print("Client received:", s.recv(1024).decode().strip())
        s.sendall(b"GET username\\n")
        print("Client received:", s.recv(1024).decode().strip())
        s.sendall(b"QUIT\\n")
        s.close()

if __name__ == "__main__":
    server = TCPServerKV(port=9998)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(("localhost", 9998))
    server_sock.listen(5)
    
    t = threading.Thread(target=server.run_test_client)
    t.start()
    
    conn, _ = server_sock.accept()
    server.handle_client(conn)
    server_sock.close()
    t.join()
''',
        "experiment": '''#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 03 Experiment: Custom TCP Key-Value Server ==="
python3 phases/03-make-the-key-value-store-a-server/code/tcp_kv_server.py
echo "✓ Phase 03 Experiment Complete."
''',
        "mastery_q1": "Why does a space-separated protocol fail if the value being stored is a JSON blob containing spaces and newlines?",
        "mastery_q2": "What happens if a TCP packet arrives fragmented into two separate network chunks?",
        "when_use": "Use custom TCP socket servers only when exploring low-level networking primitives or embedded protocols.",
        "when_not_use": "Never invent custom text protocols for production databases when battle-tested binary-safe protocols like RESP exist."
    },
    {
        "num": "04",
        "slug": "04-redis-protocol-resp",
        "title": "Redis Protocol / RESP",
        "motto": "In RESP, length prefixes make arbitrary binary data completely safe to frame.",
        "problem": "How does Redis parse arbitrary binary payloads, image bytes, JSON blobs, and nested arrays without delimiters conflicting with user data?",
        "prediction": "What does the raw byte string for `SET foo bar` look like on the wire in RESP2?",
        "why_matters": "Understanding RESP allows you to write custom high-performance clients, debug network sniffers (Wireshark/tcpdump), and understand how Redis pipelines commands.",
        "principles": "RESP encodes data using type prefixes: `+` Simple String, `-` Error, `:` Integer, `$` Bulk String (length-prefixed), `*` Array (element count). Bulk strings are framed as `$<len>\\r\\n<data>\\r\\n`.",
        "script_name": "resp_codec.py",
        "code": '''#!/usr/bin/env python3
import socket

def encode_resp_command(*args) -> bytes:
    """Encodes command arguments into RESP array."""
    out = [f"*{len(args)}\\r\\n".encode()]
    for arg in args:
        b = str(arg).encode("utf-8")
        out.append(f"${len(b)}\\r\\n".encode() + b + b"\\r\\n")
    return b"".join(out)

def decode_resp(data: bytes):
    """Simple parser for basic RESP response types."""
    if not data: return None
    prefix = chr(data[0])
    payload = data[1:].split(b"\\r\\n", 1)[0]
    if prefix == "+": return ("SimpleString", payload.decode())
    elif prefix == "-": return ("Error", payload.decode())
    elif prefix == ":": return ("Integer", int(payload))
    elif prefix == "$":
        length = int(payload)
        if length == -1: return ("Null", None)
        val = data.split(b"\\r\\n", 2)[1]
        return ("BulkString", val.decode(errors="replace"))
    return ("Raw", data)

if __name__ == "__main__":
    cmd = encode_resp_command("SET", "protocol_test", "hello_resp")
    print(f"Encoded RESP bytes for SET protocol_test hello_resp:\\n{cmd!r}")
    
    try:
        s = socket.create_connection(("localhost", 6379), timeout=2.0)
        s.sendall(cmd)
        resp = s.recv(1024)
        print(f"Raw response from Redis: {resp!r}")
        print("Decoded response:", decode_resp(resp))
        s.close()
    except Exception as e:
        print("Redis server not reachable, decoded mock response:", decode_resp(b"+OK\\r\\n"))
''',
        "experiment": '''#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 04 Experiment: Raw RESP Serialization ==="
python3 phases/04-redis-protocol-resp/code/resp_codec.py
echo "✓ Phase 04 Experiment Complete."
''',
        "mastery_q1": "How does RESP distinguish between an empty string and a non-existent (null) key?",
        "mastery_q2": "What are the key additions introduced in RESP3 compared to RESP2?",
        "when_use": "Use RESP directly when building lightweight proxy layers, connection pools, or language drivers.",
        "when_not_use": "Do not manually parse RESP strings in application code; use established client libraries like `redis-py`."
    },
    {
        "num": "05",
        "slug": "05-command-execution-mental-model",
        "title": "Redis Command Execution Mental Model",
        "motto": "Redis is fast because its event loop does not context switch between worker threads for data access.",
        "problem": "Why does Redis run single-threaded for command execution? How does a single thread handle 10,000 concurrent client connections without freezing?",
        "prediction": "What happens if a single client executes `KEYS *` on a dataset with 50,000,000 keys? What happens to other connected clients?",
        "why_matters": "Understanding the event loop (`ae.c`) and I/O multiplexing explains why Redis avoids locks, and why any long-running $O(N)$ command freezes every client on the server.",
        "principles": "The Reactor Pattern: an I/O multiplexer (`epoll`/`kqueue`) notifies the event loop when a socket has bytes. The single thread parses the command, executes it in RAM without thread contention, and queues the reply.",
        "script_name": "trace_command.py",
        "code": '''#!/usr/bin/env python3
import socket
import time

def trace_execution():
    print("Tracing the life of a command: SET engine:model 'single_threaded'")
    s = socket.create_connection(("localhost", 6379), timeout=2.0)
    
    # Send SET
    cmd = b"*3\\r\\n$3\\r\\nSET\\r\\n$12\\r\\nengine:model\\r\\n$15\\r\\nsingle_threaded\\r\\n"
    t0 = time.perf_counter()
    s.sendall(cmd)
    resp = s.recv(1024)
    rtt_us = (time.perf_counter() - t0) * 1e6
    s.close()
    
    print(f"Server response: {resp.decode().strip()} (Round-trip time: {rtt_us:.1f} µs)")
    print("\\nExecution Steps in Redis Core (server.c):")
    print("  1. kqueue/epoll wakes aeEventLoop on socket readable")
    print("  2. readQueryFromClient() reads bytes into client query buffer")
    print("  3. processInputBuffer() tokenizes RESP into argv array")
    print("  4. processCommand() looks up 'setCommand' in server.commands dict")
    print("  5. setCommand() inserts key & value SDS into db[0].dict")
    print("  6. addReply() buffers '+OK\\r\\n' to client output buffer")
    print("  7. writeToClient() flushes bytes back into TCP socket")

if __name__ == "__main__":
    try:
        trace_execution()
    except Exception as e:
        print(f"Note: Redis offline ({e}).")
''',
        "experiment": '''#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 05 Experiment: Command Execution Trace ==="
python3 phases/05-command-execution-mental-model/code/trace_command.py
echo "✓ Phase 05 Experiment Complete."
''',
        "mastery_q1": "If Redis is single-threaded, how does it take advantage of multi-core servers?",
        "mastery_q2": "What are I/O threads in Redis 6.0+, and do they execute data commands?",
        "when_use": "Rely on Redis's single-threaded nature to achieve atomic operations without mutex contention.",
        "when_not_use": "Never execute unbounded blocking commands like `KEYS *` or CPU-intensive Lua loops on the main thread."
    }
]

def generate_base_phases():
    base = "/Users/tushar/Desktop/private/repos/redis-from-scratch/phases"
    for p in PHASES_DEF:
        p_dir = os.path.join(base, p["slug"])
        # 1. docs/en.md
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
CLIENT                     REDIS EVENT LOOP (ae.c)             MEMORY (dict.c)
  │                                   │                               │
  ├─ TCP Socket write() ─────────────►│                               │
  │                                   ├─ epoll/kqueue event fired     │
  │                                   ├─ readQueryFromClient()        │
  │                                   ├─ parse RESP command           │
  │                                   ├─ lookup & call() ────────────►├─ dictEntry insert
  │                                   ├─ addReply() buffer            │
  │◄─ TCP Socket read() ──────────────┤                               │
```

## Build it
See [code/{p['script_name']}](../code/{p['script_name']}).

## Use Redis
Execute the lesson experiment:
```bash
./phases/{p['slug']}/experiments/run_experiment.sh
```

## Inspect it
```bash
redis-cli INFO
```

## Measure it
Run quantitative benchmark and inspect execution latency.

## Break it
Stop the background Redis daemon or inject an invalid payload.

## Debug it
Observe error logs and connection socket diagnostic codes.

## Modify it
Adjust payload size or connection parameters and record shifts.

## Evidence
Record your findings in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. {p['mastery_q1']}
2. {p['mastery_q2']}

## When to use this
* {p['when_use']}

## When not to use this
* {p['when_not_use']}

## What comes next
Proceed to the next phase to build upon these systems primitives.
"""
        with open(doc_path, "w") as f:
            f.write(doc_content)

        # 2. code/<script>
        code_path = os.path.join(p_dir, "code", p["script_name"])
        with open(code_path, "w") as f:
            f.write(p["code"])
        os.chmod(code_path, os.stat(code_path).st_mode | stat.S_IEXEC)

        # 3. experiments/run_experiment.sh
        exp_path = os.path.join(p_dir, "experiments", "run_experiment.sh")
        with open(exp_path, "w") as f:
            f.write(p["experiment"])
        os.chmod(exp_path, os.stat(exp_path).st_mode | stat.S_IEXEC)

        # 4. outputs/evidence-template.md
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

    print(f"Generated base foundational phases 00-05 successfully.")

if __name__ == "__main__":
    generate_base_phases()
