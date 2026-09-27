#!/usr/bin/env python3
"""
Generator for Phases 00 to 15 of kafka-from-scratch.
Adheres strictly to LESSON_TEMPLATE.md and repository principles.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PHASES_DIR = BASE_DIR / "phases"

def write_phase(phase_dir_name, doc_content, code_files, exp_script, evidence_content):
    phase_dir = PHASES_DIR / phase_dir_name
    (phase_dir / "docs").mkdir(parents=True, exist_ok=True)
    (phase_dir / "code").mkdir(parents=True, exist_ok=True)
    (phase_dir / "experiments").mkdir(parents=True, exist_ok=True)
    (phase_dir / "outputs").mkdir(parents=True, exist_ok=True)

    with open(phase_dir / "docs" / "en.md", "w") as f:
        f.write(doc_content)

    for fname, code in code_files.items():
        with open(phase_dir / "code" / fname, "w") as f:
            f.write(code)

    exp_path = phase_dir / "experiments" / "run_experiment.sh"
    with open(exp_path, "w") as f:
        f.write(exp_script)
    os.chmod(exp_path, 0o755)

    with open(phase_dir / "outputs" / "evidence-template.md", "w") as f:
        f.write(evidence_content)

    print(f"Generated phase: {phase_dir_name}")

# ==============================================================================
# PHASE 00: Environment and Kafka Lab
# ==============================================================================
p00_doc = """# Lesson 00: Environment and Kafka Lab

## Motto
"Before you can reason about distributed logs, you must prove your client can talk to the server process across a raw network socket."

## Problem
Many engineers treat Kafka as a monolithic cloud utility or a mysterious CLI suite. When a client throws `ConnectionRefusedError` or `NoBrokersAvailable`, they guess randomly. We must establish a minimal, completely transparent, reproducible local Kafka lab and verify our ability to inspect its socket and state directly.

## Prediction
1. What process is actually running when we start Kafka in modern KRaft mode?
2. How does a client running on the host OS communicate with a broker running inside a container on port 9092?

## Why this matters
Kafka is a standard user-space server process written in Java/Scala that listens on TCP ports and appends bytes to disk files. If you understand its host-port binding, listener mapping, and process lifecycle, distributed system configuration stops being mysterious.

## First principles
Kafka operates strictly as a network service:
* **Server Process:** A single JVM instance running `kafka.Kafka`.
* **KRaft Quorum:** Eliminates external ZooKeeper; broker and controller state run inside the same or dedicated processes.
* **TCP Listeners:** Brokers bind to network sockets (e.g. `0.0.0.0:9092`) and advertise reachable hostnames to clients.

## Mental model
```text
Host Machine (macOS / Linux)
┌────────────────────────────────────────────────────────┐
│ Python Client / CLI                                    │
│ (kafka-python-ng / confluent-kafka)                    │
└────────────────────────────────────────────────────────┘
                           │ TCP Connection
                           ▼ (localhost:9092)
┌────────────────────────────────────────────────────────┐
│ Docker Engine (Container: kafka-lab-single)            │
│   └── Java JVM Process: kafka.Kafka                    │
│         ├── Port 9092 (PLAINTEXT client traffic)       │
│         ├── Port 9093 (CONTROLLER internal Raft quorum)│
│         └── Storage: /tmp/kraft-combined-logs          │
└────────────────────────────────────────────────────────┘
```

## Build it
See [verify_lab.py](../code/verify_lab.py) for a direct socket probe and metadata query script.

```python
import socket

def test_socket(host='localhost', port=9092):
    s = socket.create_connection((host, port), timeout=3)
    s.close()
    return True
```

## Use Kafka
Launch the container and query cluster metadata:

```bash
make up
docker exec kafka-lab-single /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092
```

## Inspect it
Check the running JVM process inside the container:
```bash
docker exec kafka-lab-single ps aux
```

## Measure it
Measure ping latency and TCP connection establishment time to port 9092.

## Break it
Stop the container and observe the exact error raised by Python clients.

## Recover it
Run `make up` and re-verify connectivity.

## Modify it
Change the advertised listener in `docker-compose.yml` to an invalid IP and observe the connection failure.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka require distinct `listeners` and `advertised.listeners` configurations?
2. What role does the controller port (9093) play in a KRaft cluster?

## Guarantees
* A running, unfenced KRaft broker responds to metadata requests over PLAINTEXT.

## Non-guarantees
* Having port 9092 open does not guarantee the cluster is ready to accept writes if the KRaft quorum is partitioned.

## When to use this
* During local development, integration testing, and protocol debugging.

## When not to use this
* Single-broker setups should never run in production environments requiring high availability.

## What comes next
In Phase 01, we examine the fundamental architectural failure of point-to-point synchronous architectures that led to the creation of Kafka.
"""

p00_code = {
    "verify_lab.py": """#!/usr/bin/env python3
import socket
import sys

def check_tcp(host, port):
    print(f"Testing TCP socket connection to {host}:{port}...")
    try:
        s = socket.create_connection((host, port), timeout=3)
        s.close()
        print(f" [OK] Successfully established TCP handshake with {host}:{port}")
        return True
    except Exception as e:
        print(f" [FAIL] Could not connect to {host}:{port}: {e}")
        return False

def check_kafka_metadata():
    print("Testing Kafka Cluster Metadata query via Python client...")
    try:
        from kafka import KafkaAdminClient
        admin = KafkaAdminClient(bootstrap_servers="localhost:9092", request_timeout_ms=3000)
        cluster_metadata = admin.describe_cluster()
        print(f" [OK] Cluster connection successful!")
        print(f"      Cluster ID: {cluster_metadata.get('cluster_id')}")
        print(f"      Controller ID: {cluster_metadata.get('controller_id')}")
        print(f"      Active Brokers: {len(cluster_metadata.get('brokers', []))}")
        admin.close()
        return True
    except Exception as e:
        print(f" [FAIL] Kafka metadata check failed: {e}")
        return False

if __name__ == "__main__":
    tcp_ok = check_tcp("localhost", 9092)
    if not tcp_ok:
        print("\\nHint: Did you run 'make up' to start the Kafka container?")
        sys.exit(1)
    meta_ok = check_kafka_metadata()
    if meta_ok:
        print("\\nEnvironment is fully operational!")
        sys.exit(0)
    else:
        sys.exit(1)
"""
}

p00_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 00 Experiment: Verifying Kafka Lab Environment ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/verify_lab.py
"""

p00_evidence = """# Phase 00 Evidence Log

* **Date:**
* **Kafka Version:** Apache Kafka 3.8.0 (KRaft)
* **Prediction:**
* **Commands executed:**
* **TCP Connection Status:**
* **Cluster ID:**
* **What surprised me:**
* **What failed:**
* **Recovery action:**
"""

write_phase("00-environment-and-kafka-lab", p00_doc, p00_code, p00_exp, p00_evidence)

# ==============================================================================
# PHASE 01: Why Kafka Exists
# ==============================================================================
p01_doc = """# Lesson 01: Why Kafka Exists

## Motto
"Synchronous point-to-point connections turn downstream latency spikes into upstream system outages."

## Problem
In early web architectures, Service A (e.g. Checkout Service) synchronously called Service B (Inventory), Service C (Payment), Service D (Analytics), and Service E (Email Notifications).
As systems scale, this direct architecture collapses under:
1. **Tight Coupling:** Adding a new downstream consumer requires modifying and redeploying upstream producers.
2. **Cascading Failures:** If Service E stalls or crashes, Service A's HTTP worker threads block waiting for timeouts, exhausting thread pools and causing checkout outages.
3. **Inability to Replay:** If Analytics has a bug and needs last week's data recalculated, Service A cannot re-send millions of historical requests.

## Prediction
What happens to checkout response time when one of four downstream services encounters a 500ms database lock?

## Why this matters
Decoupling producers from consumers via an immutable log changes distributed system architecture from fragile request-reply webs into resilient, asynchronous event streams.

## Mental model
```text
The Fragile Web (Synchronous Direct Calls)
Checkout API ──(HTTP)──► Inventory (15ms)
             ├──(HTTP)──► Payment (50ms)
             ├──(HTTP)──► Analytics (400ms - SLOW!)  <-- Blocks Checkout!
             └──(HTTP)──► Email (Down! Timeout 3s)    <-- Fails Checkout!

The Decoupled Log (Kafka Architecture)
Checkout API ──(Append)──► [ Durable Log: orders ]
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
    Inventory Worker     Payment Worker        Analytics Worker
    (Reads at 15ms)      (Reads at 50ms)       (Reads at its own pace)
```

## Build it
See [direct_coupled_services.py](../code/direct_coupled_services.py) which simulates a synchronous checkout pipeline and measures total latency when downstream services degrade.

## Use Kafka
In Kafka, the producer performs a single fast append to the `orders` topic. Downstream workers independently pull events without impacting checkout latency.

## Inspect it
Observe how total latency in direct coupling equals the sum of all downstream latencies plus any timeouts.

## Measure it
Compare total transaction latency of synchronous calls vs. appending to an asynchronous event buffer.

## Break it
Inject a 3-second sleep into the Email notification service and watch the entire checkout process freeze.

## Recover it
Decouple the notification service using an intermediate queue or log.

## Modify it
Add a 5th downstream service (Fraud Scoring) to the synchronous pipeline and observe code changes required in the checkout service.

## Evidence
Record results in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does temporal decoupling allow services to undergo maintenance without dropping events?
2. Why is an append-only log superior to a simple in-memory queue for analytics fan-out?

## Guarantees
* Asynchronous log ingestion isolates producer latency from consumer processing time.

## Non-guarantees
* Asynchronous decoupling does not guarantee immediate consistency; downstream consumers will have eventual consistency.

## When to use this
* High-throughput event ingestion, multi-team decoupled microservices, audit logging, analytics fan-out.

## When not to use this
* Strict synchronous request-response workflows where the caller immediately requires an interactive query result (e.g. user authentication).

## What comes next
In Phase 02, we discard all third-party software and build an append-only log from scratch in pure Python.
"""

p01_code = {
    "direct_coupled_services.py": """#!/usr/bin/env python3
import time
import random

def service_inventory(order_id):
    time.sleep(0.010) # 10ms
    return "inventory_reserved"

def service_payment(order_id):
    time.sleep(0.030) # 30ms
    return "payment_processed"

def service_analytics(order_id, slow=False):
    if slow:
        time.sleep(0.400) # 400ms latency spike
    else:
        time.sleep(0.005)
    return "analytics_recorded"

def service_email(order_id, failing=False):
    if failing:
        time.sleep(1.0) # 1s timeout
        raise TimeoutError("Email gateway timeout!")
    time.sleep(0.015)
    return "email_sent"

def synchronous_checkout(order_id, slow_analytics=False, fail_email=False):
    start = time.time()
    results = {}
    try:
        results['inventory'] = service_inventory(order_id)
        results['payment'] = service_payment(order_id)
        results['analytics'] = service_analytics(order_id, slow=slow_analytics)
        results['email'] = service_email(order_id, failing=fail_email)
        duration_ms = (time.time() - start) * 1000
        print(f"Checkout {order_id} SUCCEEDED in {duration_ms:.1f}ms")
        return True, duration_ms
    except Exception as e:
        duration_ms = (time.time() - start) * 1000
        print(f"Checkout {order_id} FAILED after {duration_ms:.1f}ms with error: {e}")
        return False, duration_ms

if __name__ == "__main__":
    print("--- 1. Normal Conditions ---")
    synchronous_checkout("ORD-101")

    print("\\n--- 2. Slow Downstream Analytics ---")
    synchronous_checkout("ORD-102", slow_analytics=True)

    print("\\n--- 3. Downstream Email Failure (Cascading Outage) ---")
    synchronous_checkout("ORD-103", fail_email=True)
"""
}

p01_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 01 Experiment: Measuring Fragility of Direct Synchronous Coupling ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/direct_coupled_services.py
"""

p01_evidence = """# Phase 01 Evidence Log

* **Date:**
* **Baseline Latency (ms):**
* **Degraded Latency with Slow Consumer (ms):**
* **Checkout Outage Triggered By:**
* **Key Realization:**
"""

write_phase("01-why-kafka-exists", p01_doc, p01_code, p01_exp, p01_evidence)

# ==============================================================================
# PHASE 02: Build an Append-Only Log
# ==============================================================================
p02_doc = """# Lesson 02: Build an Append-Only Log

## Motto
"A database modifies data in place; a log records the immutable passage of time."

## Problem
How do you store a continuous stream of events so that writes are fast, data is never accidentally overwritten, and consumers can read sequentially from any point in time?

## Prediction
If you only append bytes to the end of a file, what is the computational complexity $O(?)$ of writing a new record, and why does disk hardware favor this pattern?

## Why this matters
The append-only log is the conceptual seed of Apache Kafka. Every topic partition in Kafka is fundamentally an append-only log on disk. Understanding this primitive eliminates 90% of the confusion around offsets and immutability.

## First principles
* **Sequential Write:** Writing to the tail of a file avoids moving disk heads (on HDDs) and avoids block erase/re-write cycles (on SSDs).
* **Length Prefixing:** Prefixing each record with its byte length enables safe framing and sequential parsing without parsing delimiters.
* **Monotonic Offset:** Each record is identified by an ever-increasing integer index ($0, 1, 2, ...$).

## Mental model
```text
Disk File: mini_log.dat
Offset 0: [length: 12 bytes][data: user-created]
Offset 1: [length: 10 bytes][data: email-sent]
Offset 2: [length: 15 bytes][data: payment-started]
Offset 3: [length: 17 bytes][data: payment-completed] <--- Append point (Tail)
```

## Build it
See [mini_log.py](../code/mini_log.py).
We build a pure Python class `MiniLog` that supports:
1. `append(data: bytes) -> int` (returns monotonic offset)
2. `read(from_offset: int) -> list[tuple[int, bytes]]`

## Use Kafka
In Kafka, every partition is stored inside a directory named `<topic>-<partition>` containing `.log` files written using this exact append-only paradigm.

## Inspect it
Read the raw binary file created by `mini_log.py` using `hexdump` or Python `open(..., 'rb')`.

## Measure it
Measure write throughput of 10,000 appends.

## Break it
Simulate a partial write (corrupt the length header) and observe how sequential reading detects truncation or corruption.

## Recover it
Truncate the corrupted tail bytes back to the last valid record boundary.

## Modify it
Add a CRC32 checksum to each record header to detect payload corruption.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an append-only log make concurrent reading and writing thread-safe without heavy locking?
2. Why can you not "delete" record #2 without rewriting the entire file?

## Guarantees
* Appends are strictly ordered and immutable.
* Historical records cannot be silently modified.

## Non-guarantees
* A single file cannot grow infinitely; it will eventually exhaust disk space (solved later by segment rolling and retention).

## When to use this
* Event streaming, financial audit ledgers, database write-ahead logs (WAL).

## When not to use this
* Workloads requiring frequent in-place updates of key-value pairs (use B-Trees or LSM-Trees instead).

## What comes next
In Phase 03, we explore the crucial distinction between the log's append offset and a consumer's reading position.
"""

p02_code = {
    "mini_log.py": """#!/usr/bin/env python3
import struct
import os
from pathlib import Path

class MiniLog:
    \"\"\"
    A first-principles append-only log on disk.
    Record Format on Disk:
      [8 bytes: monotonic offset (uint64)]
      [4 bytes: payload length (uint32)]
      [N bytes: raw payload]
    \"\"\"
    HEADER_FORMAT = ">QI" # 8-byte unsigned long long, 4-byte unsigned int
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.file = open(filepath, "a+b")
        self.next_offset = self._recover_next_offset()

    def _recover_next_offset(self) -> int:
        self.file.seek(0, os.SEEK_END)
        size = self.file.tell()
        if size == 0:
            return 0
        # Scan headers to find last offset
        self.file.seek(0, os.SEEK_SET)
        last_offset = -1
        while True:
            header_bytes = self.file.read(self.HEADER_SIZE)
            if len(header_bytes) < self.HEADER_SIZE:
                break
            offset, length = struct.unpack(self.HEADER_FORMAT, header_bytes)
            last_offset = offset
            self.file.seek(length, os.SEEK_CUR) # Skip payload
        return last_offset + 1

    def append(self, payload: bytes) -> int:
        offset = self.next_offset
        header = struct.pack(self.HEADER_FORMAT, offset, len(payload))
        self.file.seek(0, os.SEEK_END)
        self.file.write(header + payload)
        self.file.flush() # Ensure flush to OS buffer
        self.next_offset += 1
        return offset

    def read_from(self, start_offset: int = 0):
        \"\"\"Sequentially reads records starting from start_offset.\"\"\"
        self.file.seek(0, os.SEEK_SET)
        records = []
        while True:
            header_bytes = self.file.read(self.HEADER_SIZE)
            if len(header_bytes) < self.HEADER_SIZE:
                break
            offset, length = struct.unpack(self.HEADER_FORMAT, header_bytes)
            payload = self.file.read(length)
            if offset >= start_offset:
                records.append((offset, payload))
        return records

    def close(self):
        self.file.close()

if __name__ == "__main__":
    log_path = "/tmp/test_mini_log.dat"
    if os.path.exists(log_path):
        os.remove(log_path)

    log = MiniLog(log_path)
    print("Appending events...")
    off0 = log.append(b"user-created:alice")
    off1 = log.append(b"email-sent:alice@example.com")
    off2 = log.append(b"payment-started:amount=50")
    off3 = log.append(b"payment-completed:amount=50")

    print(f"Appended 4 records. Next offset will be: {log.next_offset}")
    log.close()

    # Re-open and read from offset 2
    log_reader = MiniLog(log_path)
    print("\\nReading from offset 2:")
    for offset, data in log_reader.read_from(2):
        print(f"  Offset {offset}: {data.decode()}")
    log_reader.close()
"""
}

p02_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 02 Experiment: Running MiniLog Append-Only Implementation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/mini_log.py
"""

p02_evidence = """# Phase 02 Evidence Log

* **Date:**
* **Log File Location:**
* **Records Appended:**
* **Observed Binary Header Size:**
* **Reading from Offset 2 Output:**
* **What surprised me:**
"""

write_phase("02-build-an-append-only-log", p02_doc, p02_code, p02_exp, p02_evidence)

# ==============================================================================
# PHASE 03: Offsets
# ==============================================================================
p03_doc = """# Lesson 03: Offsets

## Motto
"The log offset belongs to the storage engine; the consumer position belongs to the application."

## Problem
A consumer starts reading a log from offset 0. It processes 10 records, and then its process crashes.
When the consumer restarts:
* Where does it resume?
* If it restarts from 0, it re-processes all 10 records (duplicates).
* If it forgets where it was, it might skip records (data loss).
How do we decouple the log's physical append position from each reader's processing position?

## Prediction
What happens if a consumer commits its offset to disk *before* executing the business logic, and crashes during processing?

## Why this matters
The core distinction between:
$$\\text{Log Offset} \\neq \\text{Consumer Position}$$
is the foundation of Kafka's multi-consumer architecture, replay capabilities, and delivery semantics (at-most-once vs. at-least-once).

## Mental model
```text
Log on Disk:
Offsets:     0     1     2     3     4     5     6     7 (Log End Offset = 8)
          [ R0 | R1 | R2 | R3 | R4 | R5 | R6 | R7 ]
                                 ▲                 ▲
                                 │                 │
                Consumer Position│                 │Append Point (LEO)
                (Last Committed = 3)
                Next Fetch = 4
```

## Build it
See [offsets_experiment.py](../code/offsets_experiment.py).
We implement explicit consumer offset tracking on top of `MiniLog`:
1. Processing with commit-after-work (At-Least-Once).
2. Processing with commit-before-work (At-Most-Once).
3. Simulating crashes to observe duplicate processing vs lost events.

## Use Kafka
In Kafka, consumer offsets are stored as messages in an internal, compacted topic named `__consumer_offsets`.

## Inspect it
Check the saved consumer position file on disk and compare it with the log's next append offset.

## Measure it
Measure the performance cost of persisting consumer offsets after every record vs. batching offset commits.

## Break it
Kill the consumer process halfway through a batch of 100 records and observe what happens upon restart.

## Recover it
Restart the consumer and observe how it reads its saved offset to resume cleanly.

## Modify it
Change the crash point to occur *before* the offset save, and observe duplicate processing.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka allow multiple consumer groups to maintain completely independent offsets on the same partition?
2. What is the danger of committing offsets asynchronously in the background?

## Guarantees
* A consumer position is a deterministic pointer into an immutable sequence of records.

## Non-guarantees
* Saving an offset does not mean the downstream database write succeeded unless they are coordinated atomically.

## When to use this
* In every streaming architecture where progress must be saved across worker restarts.

## When not to use this
* Ephemeral fire-and-forget messaging where dropped messages are completely irrelevant (e.g. lossy audio streaming).

## What comes next
In Phase 04, we turn our local Python log into a network service accessible over TCP sockets.
"""

p03_code = {
    "offsets_experiment.py": """#!/usr/bin/env python3
import os
import json
import time
from pathlib import Path
import sys

# Import MiniLog from Phase 02
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

OFFSET_STORE = "/tmp/consumer_offset.json"

def load_consumer_offset():
    if os.path.exists(OFFSET_STORE):
        with open(OFFSET_STORE, "r") as f:
            return json.load(f).get("offset", 0)
    return 0

def save_consumer_offset(offset):
    with open(OFFSET_STORE, "w") as f:
        json.dump({"offset": offset}, f)

def simulate_consumer(log, mode="commit_after", crash_at=None):
    current_pos = load_consumer_offset()
    print(f"\\n[Consumer] Resuming from offset: {current_pos} (mode: {mode})")
    records = log.read_from(current_pos)
    
    processed = []
    for off, data in records:
        if mode == "commit_before":
            save_consumer_offset(off + 1)
        
        if crash_at is not None and off == crash_at:
            print(f" [CRASH!] Consumer crashed while processing offset {off}!")
            return processed, False
        
        # Simulate business logic
        payload = data.decode()
        processed.append((off, payload))
        print(f" [Process] Offset {off}: {payload}")
        
        if mode == "commit_after":
            save_consumer_offset(off + 1)
            
    return processed, True

if __name__ == "__main__":
    log_path = "/tmp/offsets_demo.dat"
    if os.path.exists(log_path): os.remove(log_path)
    if os.path.exists(OFFSET_STORE): os.remove(OFFSET_STORE)

    log = MiniLog(log_path)
    for i in range(5):
        log.append(f"event-{i}".encode())

    print("--- 1. Crash with 'commit_before' (Risk: Data Loss) ---")
    simulate_consumer(log, mode="commit_before", crash_at=2)
    print("Restarting consumer after crash...")
    simulate_consumer(log, mode="commit_before")

    print("\\n--- Resetting State ---")
    if os.path.exists(OFFSET_STORE): os.remove(OFFSET_STORE)

    print("--- 2. Crash with 'commit_after' (Risk: Duplicate Processing) ---")
    simulate_consumer(log, mode="commit_after", crash_at=2)
    print("Restarting consumer after crash...")
    simulate_consumer(log, mode="commit_after")
"""
}

p03_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 03 Experiment: Demonstrating Offset Commit Mechanics & Failure Modes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/offsets_experiment.py
"""

p03_evidence = """# Phase 03 Evidence Log

* **Date:**
* **Behavior with Commit-Before-Processing:**
* **Behavior with Commit-After-Processing:**
* **Which records were duplicated:**
* **Which records were skipped/lost:**
* **Mastery Insight:**
"""

write_phase("03-offsets", p03_doc, p03_code, p03_exp, p03_evidence)

# ==============================================================================
# PHASE 04: Make the Log a Network Service
# ==============================================================================
p04_doc = """# Lesson 04: Make the Log a Network Service

## Motto
"A local log is an embedded library; a network log is a distributed infrastructure service."

## Problem
In Phase 02 and 03, our `MiniLog` was accessed via direct in-process Python calls (`log.append()`).
In real distributed architectures, producers and consumers run on different machines across the network.
How do we expose the append-only log over TCP sockets without breaking sequentiality?

## Prediction
What happens to incoming concurrent append requests when multiple producer clients connect to a single TCP socket server?

## Why this matters
Understanding the client-server boundary separates protocol serialization from on-disk persistence. Kafka is fundamentally a TCP server accepting binary wire protocols.

## First principles
* **Framed TCP Protocol:** Streaming TCP is a byte stream, not a packet stream. Messages must be length-delimited.
* **Request Dispatching:** The server decodes client commands (`APPEND`, `FETCH`), interacts with the disk log, and returns structured responses.

## Mental model
```text
Producer Process                      Server Process (TCP Port 9999)
┌─────────────────┐  APPEND "hello"  ┌──────────────────────────────┐
│ MiniLog Client  │ ────────────────►│ TCP Socket Acceptor          │
└─────────────────┘                  │    │                         │
                                     │    ▼                         │
Consumer Process                     │ MiniLog Storage (mini_log.dat)
┌─────────────────┐   FETCH from 0   │    │                         │
│ MiniLog Client  │ ────────────────►│    ▼                         │
└─────────────────┘ ◄────────────────┤ Returns: [(0, "hello")]      │
```

## Build it
See [tcp_log_server.py](../code/tcp_log_server.py) and [tcp_log_client.py](../code/tcp_log_client.py).
We implement a lightweight TCP server supporting:
* `APPEND <payload>` -> replies `OFFSET <n>`
* `FETCH <start_offset>` -> replies `RECORDS <json_list>`

## Use Kafka
Kafka implements its own high-performance binary protocol (`ProduceRequest`, `FetchRequest`) over TCP port 9092.

## Inspect it
Use `nc` (netcat) or raw Python sockets to send text commands directly to the server.

## Measure it
Measure latency of network append over TCP vs. local in-process append.

## Break it
Kill the TCP server process while a client is in the middle of sending an append.

## Recover it
Restart the server; verify previous records were persisted to disk and new appends receive the next monotonic offset.

## Modify it
Add a `PING` command to the TCP server to implement a basic healthcheck.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does TCP framing require length prefixes rather than simple newline delimiters when payloads contain arbitrary binary data?
2. What happens if the server crashes after writing to disk but before sending the TCP response to the client?

## Guarantees
* Remote clients can append and fetch records concurrently over standard TCP sockets.

## Non-guarantees
* Our simple TCP server does not implement TLS security, authentication, or multi-broker replication.

## When to use this
* Whenever decoupling producers and consumers across process boundaries.

## When not to use this
* Single-process applications where IPC or in-memory queues have lower latency overhead.

## What comes next
In Phase 05, we expand our single log into multiple named logical streams: Topics.
"""

p04_code = {
    "tcp_log_server.py": """#!/usr/bin/env python3
import socket
import threading
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

class TCPLogServer:
    def __init__(self, host="127.0.0.1", port=9999, log_path="/tmp/tcp_log.dat"):
        self.host = host
        self.port = port
        self.log = MiniLog(log_path)
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def handle_client(self, conn):
        with conn:
            buffer = ""
            while True:
                data = conn.recv(1024)
                if not data: break
                buffer += data.decode("utf-8", errors="ignore")
                while "\\n" in buffer:
                    line, buffer = buffer.split("\\n", 1)
                    line = line.strip()
                    if not line: continue
                    parts = line.split(" ", 2)
                    cmd = parts[0].upper()
                    
                    if cmd == "APPEND" and len(parts) >= 2:
                        payload = parts[1].encode("utf-8")
                        with self.lock:
                            offset = self.log.append(payload)
                        conn.sendall(f"OK OFFSET {offset}\\n".encode())
                    elif cmd == "FETCH" and len(parts) >= 2:
                        start_offset = int(parts[1])
                        with self.lock:
                            records = self.log.read_from(start_offset)
                        serializable = [{"offset": o, "data": d.decode("utf-8", errors="ignore")} for o, d in records]
                        conn.sendall(f"OK RECORDS {json.dumps(serializable)}\\n".encode())
                    elif cmd == "PING":
                        conn.sendall(b"PONG\\n")
                    else:
                        conn.sendall(b"ERR UNKNOWN_COMMAND\\n")

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[TCPLogServer] Listening on {self.host}:{self.port}...")
        try:
            while True:
                conn, _ = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()
        except KeyboardInterrupt:
            print("\\nShutting down server.")
        finally:
            self.server_socket.close()
            self.log.close()

if __name__ == "__main__":
    server = TCPLogServer()
    server.run()
""",
    "tcp_log_client.py": """#!/usr/bin/env python3
import socket
import json
import time

def send_command(cmd, host="127.0.0.1", port=9999):
    s = socket.create_connection((host, port), timeout=3)
    s.sendall(f"{cmd}\\n".encode())
    resp = s.recv(4096).decode()
    s.close()
    return resp.strip()

if __name__ == "__main__":
    print("Testing PING:")
    print(f" -> {send_command('PING')}")

    print("\\nAppending 3 events over TCP:")
    for event in ["login:alice", "view_item:shoes", "add_cart:shoes"]:
        resp = send_command(f"APPEND {event}")
        print(f" Appended '{event}' -> Server Reply: {resp}")

    print("\\nFetching events from offset 0:")
    resp = send_command("FETCH 0")
    print(f" Raw reply: {resp}")
"""
}

p04_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 04 Experiment: Testing TCP Log Server and Client ==="
cd "$(dirname "$0")/.."

# Start server in background
../../.venv/bin/python3 code/tcp_log_server.py &
SERVER_PID=$!
sleep 1

# Run client requests
../../.venv/bin/python3 code/tcp_log_client.py

# Terminate background server
kill $SERVER_PID
echo "Server terminated."
"""

p04_evidence = """# Phase 04 Evidence Log

* **Date:**
* **Server Port:** 9999
* **Append Responses:**
* **Fetch JSON payload:**
* **What surprised me about socket programming:**
"""

write_phase("04-make-the-log-a-network-service", p04_doc, p04_code, p04_exp, p04_evidence)

# ==============================================================================
# PHASE 05: Topics
# ==============================================================================
p05_doc = """# Lesson 05: Topics

## Motto
"A topic is a named logical stream; multiplexing unrelated events into a single log creates chaos."

## Problem
In any real company, different business events occur simultaneously:
* User clicks (`pageviews`)
* Financial transactions (`payments`)
* Security logins (`auth_events`)
If all of these events are dumped into a single log file, every consumer must read and discard 95% of records they don't care about, wasting CPU, network, and disk I/O.
How do we organize events into discrete, isolated logical streams?

## Prediction
If topic `payments` has 10 records and topic `pageviews` has 10,000 records, should their offset sequences interfere with each other?

## Why this matters
In Kafka, a **Topic** is the primary organizational unit. It represents a named stream of records. Crucially, **each topic maintains its own independent offset space**.

## Mental model
```text
Broker Storage Root (/tmp/kafka-logs)
├── Topic: "orders"
│   └── mini_log_orders.dat   --> Offsets: 0, 1, 2, 3
├── Topic: "payments"
│   └── mini_log_payments.dat --> Offsets: 0, 1, 2
└── Topic: "notifications"
    └── mini_log_notifications.dat --> Offsets: 0, 1, 2, 3, 4, 5
```

## Build it
See [topic_log_manager.py](../code/topic_log_manager.py).
We implement a `TopicManager` that dynamically provisions independent `MiniLog` instances keyed by topic name.

## Use Kafka
Create and list topics on the real Kafka broker:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic orders --partitions 1 --replication-factor 1
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

## Inspect it
Observe how appending to `orders` does not advance the offset of `payments`.

## Measure it
Compare consumer processing time when filtering events from a shared log vs reading from dedicated topics.

## Break it
Attempt to write to a non-existent topic when auto-topic creation is disabled.

## Recover it
Explicitly create the topic using administrative commands.

## Modify it
Implement topic deletion in `TopicManager` and observe disk cleanup.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does having separate topics eliminate consumer-side filtering overhead?
2. Why should production Kafka clusters disable `auto.create.topics.enable`?

## Guarantees
* Topics have completely independent offset spaces and physical files.

## Non-guarantees
* A topic alone does not provide horizontal scale across multiple servers; that requires partitions (Phase 07).

## When to use this
* Organizing discrete event types across business domains.

## When not to use this
* Creating a dynamic topic per user (e.g. `user-topic-1234`)—this creates thousands of tiny files and crashes broker OS file handles.

## What comes next
In Phase 06, we transition from our Python prototype to writing real Kafka producers and consumers with official client libraries.
"""

p05_code = {
    "topic_log_manager.py": """#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

class TopicLogManager:
    def __init__(self, base_dir="/tmp/topics_lab"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.topics = {}

    def _get_log(self, topic: str) -> MiniLog:
        if topic not in self.topics:
            topic_file = self.base_dir / f"{topic}.dat"
            self.topics[topic] = MiniLog(str(topic_file))
        return self.topics[topic]

    def produce(self, topic: str, record: bytes) -> int:
        log = self._get_log(topic)
        return log.append(record)

    def consume(self, topic: str, start_offset: int = 0):
        log = self._get_log(topic)
        return log.read_from(start_offset)

    def list_topics(self):
        return [f.stem for f in self.base_dir.glob("*.dat")]

if __name__ == "__main__":
    import shutil
    if os.path.exists("/tmp/topics_lab"):
        shutil.rmtree("/tmp/topics_lab")

    mgr = TopicLogManager()
    print("Producing to independent topics...")
    mgr.produce("orders", b"order-created:1001")
    mgr.produce("orders", b"order-created:1002")
    mgr.produce("payments", b"payment-auth:1001")
    mgr.produce("notifications", b"sms:welcome")

    print(f"\\nDiscovered Topics: {mgr.list_topics()}")

    print("\\nConsuming 'orders' topic:")
    for off, data in mgr.consume("orders", 0):
        print(f"  [orders] Offset {off}: {data.decode()}")

    print("\\nConsuming 'payments' topic:")
    for off, data in mgr.consume("payments", 0):
        print(f"  [payments] Offset {off}: {data.decode()}")
"""
}

p05_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 05 Experiment: Testing Multi-Topic Log Isolation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/topic_log_manager.py
"""

p05_evidence = """# Phase 05 Evidence Log

* **Date:**
* **Topics Created:**
* **Independent Offsets Observed:**
* **Key architectural difference between a topic and a file:**
"""

write_phase("05-topics", p05_doc, p05_code, p05_exp, p05_evidence)

# ==============================================================================
# PHASE 06: Kafka Producers and Consumers
# ==============================================================================
p06_doc = """# Lesson 06: Kafka Producers and Consumers

## Motto
"The client library is not a dumb proxy; it is a sophisticated background routing and batching engine."

## Problem
Now that we understand the mechanics of logs, offsets, TCP sockets, and topics, how do we interact with a real production-grade Apache Kafka 3.8.0 cluster using official Python client libraries?

## Prediction
What happens when `producer.send()` is called? Does it make an immediate network call, or does it buffer the record in memory?

## Why this matters
Writing reliable producers and consumers requires understanding the client lifecycle: serialization, partition assignment, network accumulator buffers, and the polling loop.

## First principles
* **Bootstrap Servers:** The client connects to an initial broker IP only to fetch the full cluster metadata (all brokers and partition leaders).
* **Record Format:** Key, Value, Headers, Partition, Timestamp.
* **Poll Loop:** Consumers must call `poll()` periodically to fetch batches and keep their group heartbeat alive.

## Mental model
```text
Producer Application
┌────────────────────────────────────────────────────────┐
│ producer.send(topic="orders", key=b"k1", value=b"v1")  │
│   └── Serializes to bytes                              │
│   └── Computes target partition                        │
│   └── Places into in-memory RecordAccumulator buffer   │
└────────────────────────────────────────────────────────┘
                           │ (Background Sender Thread)
                           ▼
Kafka Broker (port 9092)
                           │
                           ▼ (Consumer poll() request)
Consumer Application
┌────────────────────────────────────────────────────────┐
│ consumer.poll(timeout_ms=1000)                         │
│   └── Deserializes payload                             │
│   └── Yields ConsumerRecord(offset, key, value, ...)   │
└────────────────────────────────────────────────────────┘
```

## Build it
See [producer.py](../code/producer.py) and [consumer.py](../code/consumer.py).

## Use Kafka
Run the Python producer and consumer against the local container:
```bash
python3 code/producer.py
python3 code/consumer.py
```

## Inspect it
Inspect the published records using the Kafka CLI consumer:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic lab-orders \
  --from-beginning \
  --property print.key=true \
  --property print.offset=true
```

## Measure it
Measure time taken to publish 1,000 individual records synchronously (`flush()` after each) vs asynchronously.

## Break it
Point `bootstrap_servers` to an invalid port and observe how the client library behaves.

## Recover it
Fix the bootstrap string and observe automatic client reconnection.

## Modify it
Add custom record headers (e.g. `[("correlation-id", b"xyz-123")]`) in the producer and print them in the consumer.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `producer.send()` return a future rather than blocking immediately?
2. What is the role of `flush()`?

## Guarantees
* Records confirmed by the broker are durable according to the topic's configuration.

## Non-guarantees
* Calling `producer.send()` without checking errors or flushing does not guarantee the record reached the broker.

## When to use this
* In any service producing or consuming event data with Kafka.

## When not to use this
* Do not create a new Producer instance per HTTP request; Producer instances are thread-safe long-lived singletons designed to be shared.

## What comes next
In Phase 07, we investigate why a single log per topic cannot scale, and discover why Partitions exist.
"""

p06_code = {
    "producer.py": """#!/usr/bin/env python3
import time
import json
from kafka import KafkaProducer

def run_producer():
    print("Connecting KafkaProducer to localhost:9092...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        acks="all"
    )

    topic = "lab-orders"
    print(f"Producing 5 sample records to '{topic}'...")
    for i in range(1, 6):
        order = {
            "order_id": 1000 + i,
            "customer": f"user_{i}",
            "amount": round(19.99 * i, 2),
            "timestamp": time.time()
        }
        key = f"customer-{i}"
        future = producer.send(topic, key=key, value=order)
        # Block for acknowledgement to inspect metadata
        record_metadata = future.get(timeout=5)
        print(f" [Ack] Sent order {order['order_id']} -> Topic: {record_metadata.topic}, "
              f"Partition: {record_metadata.partition}, Offset: {record_metadata.offset}")

    producer.flush()
    producer.close()
    print("Producer finished successfully.")

if __name__ == "__main__":
    run_producer()
""",
    "consumer.py": """#!/usr/bin/env python3
import json
from kafka import KafkaConsumer

def run_consumer():
    print("Connecting KafkaConsumer to localhost:9092...")
    consumer = KafkaConsumer(
        "lab-orders",
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=5000, # Stop if no records for 5s
        key_deserializer=lambda k: k.decode("utf-8") if k else None,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    print("Consuming records from 'lab-orders':")
    count = 0
    for record in consumer:
        count += 1
        print(f" [Record] Partition: {record.partition}, Offset: {record.offset}, "
              f"Key: {record.key}, Value: {record.value}")

    consumer.close()
    print(f"Consumed {count} records.")

if __name__ == "__main__":
    run_consumer()
"""
}

p06_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 06 Experiment: Running Real Kafka Producer and Consumer ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/producer.py
../../.venv/bin/python3 code/consumer.py
"""

p06_evidence = """# Phase 06 Evidence Log

* **Date:**
* **Kafka Version:** 3.8.0
* **Topic Created:** lab-orders
* **Produced Offsets:**
* **Consumed Offsets:**
* **Observed Partitions:**
"""

write_phase("06-kafka-producers-and-consumers", p06_doc, p06_code, p06_exp, p06_evidence)

# ==============================================================================
# PHASE 07: Why Partitions Exist
# ==============================================================================
p07_doc = """# Lesson 07: Why Partitions Exist

## Motto
"A single log is bound to a single disk and a single thread; partitions are Kafka's unit of scalability."

## Problem
Imagine a high-traffic topic receiving 500,000 events/second (e.g. ad impressions or clickstreams).
If a topic consists of only a single append-only log file:
1. **Disk I/O Bottleneck:** A single log file can only reside on a single disk on a single broker machine.
2. **Network Bottleneck:** All traffic must enter through one network interface card (NIC).
3. **Consumer Bottleneck:** A single log cannot be safely consumed in parallel without complex locking.
How can a single logical topic scale horizontally across 10, 50, or 100 machines?

## Prediction
Can Kafka provide total ordering across all messages in a topic that has 10 partitions?

## Why this matters
**Partitions are the fundamental unit of parallelism, storage, and ordering in Kafka.**
Understanding that:
$$\\text{Total Ordering} = \\text{Partition-Scoped Only}$$
is the single most important mental leap in Kafka architecture.

## Mental model
```text
Topic: "user-clicks" (Divided into 3 Partitions)

Partition 0: [ 0 | 1 | 2 | 3 | 4 ]  ──► Stored on Broker 1 (Disk A)
Partition 1: [ 0 | 1 | 2 | 3 ]      ──► Stored on Broker 2 (Disk B)
Partition 2: [ 0 | 1 | 2 | 3 | 4 | 5]──► Stored on Broker 3 (Disk C)
```

## Build it
See [partitioned_log_sim.py](../code/partitioned_log_sim.py).
We implement a multi-partition log simulation that round-robins writes across multiple independent logs and demonstrates partition-local offset counting.

## Use Kafka
Create a topic with 3 partitions and produce records:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic multi-partition-topic --partitions 3 --replication-factor 1
```

## Inspect it
Inspect the partition distribution with `kafka-topics.sh --describe`.

## Measure it
Measure write throughput of 1 partition vs. 3 partitions.

## Break it
Assume that offset 4 in Partition 0 occurred "before" offset 3 in Partition 1; observe why timestamps, not offsets, must be used to compare across partitions.

## Recover it
Align partition keys so causally related events always land in the same partition.

## Modify it
Scale the topic partition count from 3 to 6 using `kafka-topics.sh --alter --partitions 6`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does each partition have its own independent offset sequence starting from 0?
2. Why does Kafka NOT guarantee total global ordering across an entire topic?

## Guarantees
* Strict, deterministic ordering is guaranteed within any single partition.

## Non-guarantees
* No ordering guarantees exist between different partitions of the same topic.

## When to use this
* Always! Virtually every production Kafka topic uses multiple partitions.

## When not to use this
* Topics that strictly require global FIFO ordering across all events must use exactly 1 partition (and accept the throughput bottleneck).

## What comes next
In Phase 08, we learn how to control which record goes to which partition using Keys.
"""

p07_code = {
    "partitioned_log_sim.py": """#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

class PartitionedLog:
    def __init__(self, topic_dir="/tmp/partitioned_topic", num_partitions=3):
        self.topic_dir = Path(topic_dir)
        self.topic_dir.mkdir(parents=True, exist_ok=True)
        self.num_partitions = num_partitions
        self.partitions = [
            MiniLog(str(self.topic_dir / f"partition-{p}.dat"))
            for p in range(num_partitions)
        ]
        self.round_robin_counter = 0

    def append(self, payload: bytes) -> tuple[int, int]:
        target_partition = self.round_robin_counter % self.num_partitions
        self.round_robin_counter += 1
        offset = self.partitions[target_partition].append(payload)
        return target_partition, offset

    def close(self):
        for p in self.partitions:
            p.close()

if __name__ == "__main__":
    if os.path.exists("/tmp/partitioned_topic"):
        shutil.rmtree("/tmp/partitioned_topic")

    plog = PartitionedLog(num_partitions=3)
    print("Appending 9 records across 3 partitions (Round-Robin):\\n")
    for i in range(9):
        msg = f"event-{i}".encode()
        partition, offset = plog.append(msg)
        print(f" Message '{msg.decode()}' -> Landed in Partition {partition} at Offset {offset}")

    plog.close()
    print("\\nNotice: Each partition maintains its own local offsets (0, 1, 2)!")
"""
}

p07_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 07 Experiment: Partitioning Mechanics & Local Offsets ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/partitioned_log_sim.py
"""

p07_evidence = """# Phase 07 Evidence Log

* **Date:**
* **Number of Partitions:** 3
* **Records Appended:** 9
* **Observed Offsets per Partition:**
* **Why global topic ordering is impossible with multiple partitions:**
"""

write_phase("07-why-partitions-exist", p07_doc, p07_code, p07_exp, p07_evidence)

# ==============================================================================
# PHASE 08: Partitioning by Key
# ==============================================================================
p08_doc = """# Lesson 08: Partitioning by Key

## Motto
"The key determines the partition; same key equals same partition equals preserved ordering."

## Problem
In Phase 07, we saw that multiple partitions increase throughput, but total topic-wide ordering is lost.
What if your application requires strict ordering for specific entities?
For example, in banking, all transactions for `account-42` must be processed in exact chronological order (`deposit` before `withdrawal`).
How can we preserve per-entity ordering while still enjoying multi-partition throughput?

## Prediction
If you produce 100 messages with key `user-42` to a 5-partition topic, how many different partitions will receive those messages?

## Why this matters
Keys enable **deterministic routing**. All records sharing the same key are routed to the exact same partition, guaranteeing chronological processing order for that entity.

## Mental model
```text
Record Key: "user-42"
       │
       ▼
Murmur2 Hash / CRC32 Hash:  hash("user-42") = 0x8F14B2C1 (Integer: 2400490177)
       │
       ▼
Modulo Partition Count:      2400490177 % 3 Partitions = Partition 1
       │
       ▼
Guaranteed Destination:      Partition 1 (ALWAYS, as long as partition count is constant!)
```

## Build it
See [key_partitioning.py](../code/key_partitioning.py).
We test hashing algorithms and observe key-to-partition mapping.

## Use Kafka
Produce records with keys and inspect which partition they land on.

## Inspect it
Use `kafka-console-consumer.sh` with `--property print.partition=true` to verify partition mapping.

## Measure it
Measure distribution uniformity when using UUID keys vs sequential keys.

## Break it
Increase the partition count of the topic from 3 to 5 halfway through producing, and observe how `hash(key) % N` changes destination partitions, breaking ordering!

## Recover it
Never resize partitions dynamically if strict key-to-partition consistency across historical data is required without a re-keying migration plan.

## Modify it
Implement a custom partitioner that sends all VIP customers (`vip-*`) to a dedicated partition.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does altering the partition count of an existing topic break the key-to-partition mapping?
2. What partition routing strategy does Kafka use when the record key is `null`?

## Guarantees
* Records with the same non-null key always map to the same partition, provided partition count remains unchanged.

## Non-guarantees
* Key-based routing does NOT guarantee even distribution if the keys themselves are skewed.

## When to use this
* Whenever per-entity ordering matters (e.g. per user, per order, per IoT device).

## When not to use this
* When events have no natural entity identifier, or when keys would cause massive partition skew (Phase 09).

## What comes next
In Phase 09, we examine what happens when key distribution is skewed: Hot Partitions.
"""

p08_code = {
    "key_partitioning.py": """#!/usr/bin/env python3
import mmh3 # MurmurHash3 or built-in hash
import zlib
from collections import defaultdict

def kafka_default_partitioner(key_bytes: bytes, num_partitions: int) -> int:
    \"\"\"
    Kafka's DefaultPartitioner uses Murmur2 (or positive hash % num_partitions).
    Here we simulate using standard 32-bit hash % num_partitions.
    \"\"\"
    # Use CRC32 / positive int representation
    hash_val = zlib.crc32(key_bytes) & 0x7fffffff
    return hash_val % num_partitions

if __name__ == "__main__":
    num_partitions = 3
    print(f"Topic has {num_partitions} partitions.\\n")

    # 1. Same key repeatedly
    key_a = b"user-42"
    print(f"--- 1. Producing 5 events with SAME key: {key_a.decode()} ---")
    for i in range(5):
        part = kafka_default_partitioner(key_a, num_partitions)
        print(f" Event {i} (Key: {key_a.decode()}) -> Partition: {part}")

    # 2. Different keys
    print("\\n--- 2. Producing events with DIFFERENT keys ---")
    keys = [b"user-1", b"user-2", b"user-3", b"user-4", b"user-5", b"user-6"]
    dist = defaultdict(list)
    for k in keys:
        part = kafka_default_partitioner(k, num_partitions)
        dist[part].append(k.decode())
        print(f" Key: {k.decode()} -> Partition: {part}")

    print("\\nSummary Partition Allocation:")
    for p in range(num_partitions):
        print(f"  Partition {p}: {dist[p]}")
"""
}

p08_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 08 Experiment: Verifying Key-to-Partition Routing Consistency ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/key_partitioning.py
"""

p08_evidence = """# Phase 08 Evidence Log

* **Date:**
* **Key Tested:** user-42
* **Target Partition:**
* **Did 100% of events with user-42 land on the same partition?**
* **Effect of altering partition count on key mapping:**
"""

write_phase("08-partitioning-by-key", p08_doc, p08_code, p08_exp, p08_evidence)

# ==============================================================================
# PHASE 09: Hot Partitions
# ==============================================================================
p09_doc = """# Lesson 09: Hot Partitions

## Motto
"Having 100 partitions does not save you if 90% of your events carry the exact same key."

## Problem
An e-commerce platform keys all events by `merchant_id`.
99% of merchants are small mom-and-pop sellers with 5 orders/day.
One merchant is a global megastore (e.g. Amazon or Nike) generating 200,000 orders/minute.
What happens to the Kafka cluster?
The single partition mapped to that one giant merchant receives 95% of all traffic, saturating its broker's CPU and disk, while the remaining 31 partitions sit virtually idle.
This is a **Hot Partition**.

## Prediction
If one partition receives 10x more writes than others, can scaling consumer instances in a consumer group alleviate the bottleneck?

## Why this matters
Partitioning only scales horizontally if the key distribution is balanced. Key design is a critical system design responsibility.

## Mental model
```text
Topic: 4 Partitions (Skewed Workload)
Partition 0: [ Megastore orders... (90% of all data) ]  <-- HOT PARTITION (CPU 99%, Disk Bottleneck)
Partition 1: [ Small store A ]                          <-- IDLE
Partition 2: [ Small store B ]                          <-- IDLE
Partition 3: [ Small store C ]                          <-- IDLE
```

## Build it
See [hot_partition_analyzer.py](../code/hot_partition_analyzer.py).
We generate skewed workloads and calculate coefficient of variation ($CV$) across partitions.

## Use Kafka
Produce a skewed dataset to Kafka and analyze partition offsets.

## Inspect it
Check partition offset deltas using `kafka-consumer-groups.sh` or topic partition describe tools.

## Measure it
Measure latency and disk byte distribution across partitions under skewed keys.

## Break it
Send 99% of messages with key `"system"` and watch Partition 0 queue depth explode while Partition 1 and 2 remain empty.

## Recover it
Implement **Salted Keys** (e.g. `"merchant_id:salt_0"`, `"merchant_id:salt_1"`) to scatter the hot entity across multiple partitions when strict global per-entity order is not required.

## Modify it
Add salting to the hot key and measure the restoration of workload balance.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does consumer scaling fail to solve a hot partition bottleneck?
2. What are the trade-offs of key salting regarding per-entity event ordering?

## Guarantees
* The partitioner strictly follows its hashing algorithm.

## Non-guarantees
* Kafka does not automatically detect or rebalance hot partitions at runtime.

## When to use this
* During capacity planning, key schema design, and partition skew debugging.

## When not to use this
* Premature key salting when per-entity ordering is mandatory and throughput fits comfortably within a single partition's capacity.

## What comes next
In Phase 10, we build Consumer Groups from first principles to distribute partition workloads across multiple workers.
"""

p09_code = {
    "hot_partition_analyzer.py": """#!/usr/bin/env python3
import random
import zlib
from collections import Counter

def get_partition(key: str, num_partitions: int = 4) -> int:
    return (zlib.crc32(key.encode("utf-8")) & 0x7fffffff) % num_partitions

def run_skew_simulation(total_records=10000, skew_ratio=0.90):
    print(f"Simulating {total_records} records with {int(skew_ratio*100)}% traffic skew...")
    counts = Counter()

    for _ in range(total_records):
        if random.random() < skew_ratio:
            key = "HOT_CUSTOMER_NIKE"
        else:
            key = f"small_customer_{random.randint(1, 100)}"
        part = get_partition(key, num_partitions=4)
        counts[part] += 1

    print("\\nPartition Traffic Distribution:")
    for p in range(4):
        pct = (counts[p] / total_records) * 100
        bar = "█" * int(pct // 2)
        print(f" Partition {p}: {counts[p]:5d} msgs ({pct:5.1f}%) | {bar}")

if __name__ == "__main__":
    run_skew_simulation()
"""
}

p09_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 09 Experiment: Analyzing Key Skew and Hot Partitions ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/hot_partition_analyzer.py
"""

p09_evidence = """# Phase 09 Evidence Log

* **Date:**
* **Total Records Tested:** 10,000
* **Skew Percentage:** 90%
* **Distribution Across 4 Partitions:**
* **Max vs Min Partition Delta:**
* **System Design Strategy to Mitigate:**
"""

write_phase("09-hot-partitions", p09_doc, p09_code, p09_exp, p09_evidence)

# ==============================================================================
# PHASE 10: Consumer Groups From First Principles
# ==============================================================================
p10_doc = """# Lesson 10: Consumer Groups From First Principles

## Motto
"Without consumer groups, multiple workers duplicate each other's work; with consumer groups, workers divide the partitions."

## Problem
You have a topic with 4 partitions receiving 10,000 orders/sec.
A single consumer process can only process 2,500 orders/sec.
You spin up a second consumer process.
If both consumers simply connect to the topic independently, **both consumers read all 4 partitions**, processing every single order twice!
How do multiple consumer processes coordinate to divide partition workloads without manual configuration?

## Prediction
If a topic has 4 partitions and 2 consumers join the same consumer group, how many partitions will each consumer receive?

## Why this matters
**The Consumer Group is Kafka's fundamental abstraction for elastic horizontal read scaling.**
It enforces the cardinal rule of Kafka consumption:
$$\\text{One Partition} \\longrightarrow \\text{At most ONE active consumer in a group}$$

## Mental model
```text
Topic "orders" (4 Partitions)
[ Partition 0 ] ──┐
[ Partition 1 ] ──┼──► Consumer Process 1
                  │
[ Partition 2 ] ──┼──► Consumer Process 2
[ Partition 3 ] ──┘

Both consumers belong to Group: "order-processors"
Result: Zero duplicate processing. Total throughput doubled!
```

## Build it
See [consumer_group_sim.py](../code/consumer_group_sim.py).
We simulate range partition assignment across a group of workers.

## Use Kafka
Run two consumers specifying the exact same `--group` parameter.

## Inspect it
Inspect consumer group membership and partition assignment:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group order-processors
```

## Measure it
Measure total processing throughput with 1 consumer vs 2 consumers in the same group.

## Break it
Start 2 consumers without specifying a group (or with different group IDs) and observe duplicate processing.

## Recover it
Assign both consumers to the same group ID.

## Modify it
Change the partition assignment strategy from `RangeAssignor` to `RoundRobinAssignor`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka prohibit two consumers in the same group from consuming the same partition concurrently?
2. What allows two *different* consumer groups to read the same partition concurrently?

## Guarantees
* Within a group, each partition is assigned to exactly one consumer member at any instant.

## Non-guarantees
* Kafka does not load-balance individual records across consumers; it assigns entire partitions.

## When to use this
* Whenever scaling consumer processing across a pool of worker instances.

## When not to use this
* When you want true broadcast/pub-sub where every consumer receives every message (use independent group IDs instead).

## What comes next
In Phase 11, we examine the hard mathematical limit of consumer group parallelism.
"""

p10_code = {
    "consumer_group_sim.py": """#!/usr/bin/env python3
def assign_partitions_range(partitions: list[int], consumers: list[str]) -> dict[str, list[int]]:
    \"\"\"Simulates Kafka's RangeAssignor algorithm.\"\"\"
    if not consumers: return {}
    num_parts = len(partitions)
    num_cons = len(consumers)
    parts_per_cons = num_parts // num_cons
    extra = num_parts % num_cons

    assignment = {}
    idx = 0
    for i, cons in enumerate(consumers):
        take = parts_per_cons + (1 if i < extra else 0)
        assignment[cons] = partitions[idx : idx + take]
        idx += take
    return assignment

if __name__ == "__main__":
    partitions = [0, 1, 2, 3] # 4 Partitions
    print(f"Topic Partitions: {partitions}\\n")

    print("--- Scenario A: 1 Consumer in Group ---")
    print(assign_partitions_range(partitions, ["Consumer-A"]))

    print("\\n--- Scenario B: 2 Consumers in Group ---")
    print(assign_partitions_range(partitions, ["Consumer-A", "Consumer-B"]))

    print("\\n--- Scenario C: 4 Consumers in Group ---")
    print(assign_partitions_range(partitions, ["Consumer-A", "Consumer-B", "Consumer-C", "Consumer-D"]))
"""
}

p10_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 10 Experiment: Consumer Group Range Partition Assignment Simulation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/consumer_group_sim.py
"""

p10_evidence = """# Phase 10 Evidence Log

* **Date:**
* **Partitions Tested:** [0, 1, 2, 3]
* **Assignment with 2 Consumers:**
* **Assignment with 4 Consumers:**
* **Core Rule of Consumer Groups:**
"""

write_phase("10-consumer-groups-from-first-principles", p01_doc, p10_code, p10_exp, p10_evidence)

# ==============================================================================
# PHASE 11: Consumer Parallelism Limits
# ==============================================================================
p11_doc = """# Lesson 11: Consumer Parallelism Limits

## Motto
"You cannot have more active workers in a group than you have partitions in the topic."

## Problem
A junior engineer notices that consumer lag is accumulating on an `orders` topic.
The topic has **3 partitions**.
In an attempt to speed up consumption, they deploy **10 consumer pods** on Kubernetes.
To their bewilderment, consumer throughput does not increase by a single record.
Why?

## Prediction
If a topic has 3 partitions and 5 consumers join the group, what will the 4th and 5th consumers do?

## Why this matters
This is one of the most common capacity-planning mistakes in production.
$$\\text{Max Active Parallelism in a Group} = \\text{Number of Partitions}$$
Any consumers beyond the partition count sit 100% idle.

## Mental model
```text
Topic: 3 Partitions [ P0, P1, P2 ]
Consumer Group: 5 Consumer Pods

P0 ──► Consumer 1 (ACTIVE)
P1 ──► Consumer 2 (ACTIVE)
P2 ──► Consumer 3 (ACTIVE)
       Consumer 4 (IDLE - 0 Partitions Assigned)
       Consumer 5 (IDLE - 0 Partitions Assigned)
```

## Build it
See [parallelism_limits.py](../code/parallelism_limits.py).
We test partition assignment when $Consumers > Partitions$.

## Use Kafka
Start 5 consumer processes in the same group against a 3-partition topic and inspect them with `kafka-consumer-groups.sh`.

## Inspect it
Observe that 2 consumers report `PARTITION: -` and `CURRENT-OFFSET: -`.

## Measure it
Measure CPU utilization of the idle consumer processes.

## Break it
Kill one of the active consumers (e.g. Consumer 1) and watch an idle consumer instantly get assigned the orphaned partition!

## Recover it
Idle consumers serve as automatic hot-standbys for failover.

## Modify it
Increase partition count to 5 using `kafka-topics.sh --alter --partitions 5` and watch the 2 idle consumers immediately activate.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka make idle consumers hot-standbys rather than allowing multiple consumers to share a single partition?
2. If you need 50 parallel consumer threads, how many partitions must the topic have?

## Guarantees
* Active consumers within a group never exceed the partition count.

## Non-guarantees
* Adding consumers beyond the partition count will not reduce lag.

## When to use this
* Capacity planning and autoscaling configuration (HPA on Kubernetes).

## When not to use this
* Over-provisioning consumer replicas beyond partition count wastes memory and CPU.

## What comes next
In Phase 12, we study the mechanics of Consumer Rebalancing when members join or die.
"""

p11_code = {
    "parallelism_limits.py": """#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../10-consumer-groups-from-first-principles/code")))
from consumer_group_sim import assign_partitions_range

def test_limits():
    partitions = [0, 1, 2] # 3 Partitions
    consumers = [f"Worker-{i}" for i in range(1, 6)] # 5 Consumers

    assignment = assign_partitions_range(partitions, consumers)
    print(f"Topic Partitions: {len(partitions)}")
    print(f"Active Consumers in Group: {len(consumers)}\\n")

    for cons, parts in assignment.items():
        status = f"ACTIVE (Partitions: {parts})" if parts else "IDLE (Hot-standby)"
        print(f"  {cons}: {status}")

if __name__ == "__main__":
    test_limits()
"""
}

p11_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 11 Experiment: Demonstrating Consumer Parallelism Ceiling ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/parallelism_limits.py
"""

p11_evidence = """# Phase 11 Evidence Log

* **Date:**
* **Partitions:** 3
* **Consumers Deployed:** 5
* **Number of Idle Consumers:** 2
* **Architectural Lesson:**
"""

write_phase("11-consumer-parallelism-limits", p11_doc, p11_code, p11_exp, p11_evidence)

# ==============================================================================
# PHASE 12: Consumer Rebalancing
# ==============================================================================
p12_doc = """# Lesson 12: Consumer Rebalancing

## Motto
"When membership changes, partitions must be redistributed; how gracefully that happens defines availability."

## Problem
In a dynamic cluster, consumers crash, deploy new code, or scale up with traffic.
When a consumer dies or joins, who decides which partitions move to which workers?
How does the cluster prevent two consumers from simultaneously reading and committing the same partition during a transition?
This coordination protocol is called a **Consumer Rebalance**.

## Prediction
What happens to active message consumption during an "eager" stop-the-world rebalance?

## Why this matters
Rebalance storms can stall consumption for seconds or minutes. Understanding heartbeat threads, `session.timeout.ms`, and rebalance assignors is essential for production stability.

## First principles
* **Group Coordinator:** One Kafka broker is elected to coordinate the group (determined by hashing group ID into `__consumer_offsets`).
* **Heartbeats:** Consumers send background heartbeats to the coordinator. If heartbeats cease for `session.timeout.ms`, the consumer is evicted.
* **JoinGroup & SyncGroup:** Consumers rejoin, a group leader computes the assignment, and the coordinator broadcasts it.

## Mental model
```text
Timeline of a Consumer Rebalance (Eager / Stop-the-World)
T0: Consumer 1 and Consumer 2 reading normally
T1: Consumer 3 sends JoinGroup request (Scaling up)
T2: Coordinator signals REBALANCE_IN_PROGRESS on next heartbeat
T3: ALL consumers pause consumption and revoke current partitions (STOP-THE-WORLD)
T4: Group leader computes new assignment
T5: Coordinator distributes SyncGroup response
T6: Consumers resume consumption on newly assigned partitions
```

## Build it
See [rebalance_observer.py](../code/rebalance_observer.py).
We implement a consumer with a `ConsumerRebalanceListener` that tracks partition assignment and revocation callbacks.

## Use Kafka
Run multiple consumers, then terminate one with SIGTERM and watch the remaining consumer rebalance.

## Inspect it
Observe the rebalance events printed in consumer console logs.

## Measure it
Measure the duration from SIGTERM until partition reassignment completes.

## Break it
Simulate a slow consumer that blocks the poll thread longer than `max.poll.interval.ms` and observe the coordinator evicting it.

## Recover it
Ensure long processing is offloaded to worker threads so `poll()` is invoked regularly.

## Modify it
Configure Cooperative Sticky Assignor (`CooperativeStickyAssignor`) to avoid stop-the-world pauses.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What is the difference between `session.timeout.ms` and `max.poll.interval.ms`?
2. How does Cooperative Sticky Rebalancing improve upon classic Eager Rebalancing?

## Guarantees
* After rebalance completes, each partition is assigned to exactly one active group member.

## Non-guarantees
* During an eager rebalance, active consumption is paused across the group.

## When to use this
* Monitoring consumer group stability and sizing poll interval parameters.

## When not to use this
* Avoid triggering rebalances unnecessarily through poor timeout configuration.

## What comes next
In Phase 13, we examine Offset Commits and explore how commit timing dictates delivery guarantees.
"""

p12_code = {
    "rebalance_observer.py": """#!/usr/bin/env python3
import time
import sys
from kafka import KafkaConsumer, ConsumerRebalanceListener

class LoggingRebalanceListener(ConsumerRebalanceListener):
    def on_partitions_revoked(self, revoked):
        parts = [p.partition for p in revoked]
        print(f" [REBALANCE EVENT] Partitions REVOKED: {parts} (Commit offsets now!)")

    def on_partitions_assigned(self, assigned):
        parts = [p.partition for p in assigned]
        print(f" [REBALANCE EVENT] Partitions ASSIGNED: {parts} (Start fetching!)")

def run_observer(member_name="Consumer-1"):
    print(f"Starting {member_name} with RebalanceListener...")
    consumer = KafkaConsumer(
        "lab-orders",
        bootstrap_servers=["localhost:9092"],
        group_id="rebalance-lab-group",
        enable_auto_commit=True,
        consumer_timeout_ms=10000
    )
    consumer.subscribe(["lab-orders"], listener=LoggingRebalanceListener())

    print(f"{member_name} subscribed. Polling loop active. (Press Ctrl+C to stop)...")
    try:
        while True:
            msg_batch = consumer.poll(timeout_ms=1000)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\\n{member_name} leaving group gracefully...")
    finally:
        consumer.close()
        print(f"{member_name} closed.")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Consumer-1"
    run_observer(name)
"""
}

p12_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 12 Experiment: Observing Rebalance Callbacks ==="
cd "$(dirname "$0")/.."
# Run observer briefly
../../.venv/bin/python3 code/rebalance_observer.py Worker-A &
PID1=$!
sleep 2

../../.venv/bin/python3 code/rebalance_observer.py Worker-B &
PID2=$!
sleep 3

kill -SIGINT $PID2
sleep 2
kill -SIGINT $PID1
"""

p12_evidence = """# Phase 12 Evidence Log

* **Date:**
* **Group Tested:** rebalance-lab-group
* **Revocation Callbacks Observed:**
* **Assignment Callbacks Observed:**
* **Rebalance Duration:**
"""

write_phase("12-consumer-rebalancing", p12_doc, p12_code, p12_exp, p12_evidence)

# ==============================================================================
# PHASE 13: Offset Commits
# ==============================================================================
p13_doc = """# Lesson 13: Offset Commits

## Motto
"An uncommitted offset is a promise of duplicate processing upon restart."

## Problem
A consumer fetches 500 records from Kafka.
How and when does Kafka know the consumer has finished processing them?
If the consumer process crashes, how does Kafka decide which offset to hand the replacement consumer?
This is governed by **Offset Commits**.

## Prediction
If `enable.auto.commit=true` (the default) commits offsets every 5 seconds, what happens if your application crashes 4 seconds after processing 1,000 records?

## Why this matters
Blindly relying on default auto-commits causes silent duplicate processing or data loss during crashes. Production systems require deliberate commit strategies (`commitSync` or `commitAsync`).

## First principles
* **The `__consumer_offsets` Topic:** Committed offsets are simply messages written to an internal, compacted topic: `(group, topic, partition) -> offset`.
* **Synchronous vs Asynchronous Commits:**
  * `commitSync()`: Blocks until the coordinator broker acknowledges the commit. High reliability, adds latency.
  * `commitAsync()`: Fire-and-forget commit. Fast, but cannot safely retry without sequence guards.

## Mental model
```text
Consumer Loop
┌────────────────────────────────────────────────────────┐
│ 1. records = consumer.poll()                           │
│ 2. for record in records:                              │
│       process_business_logic(record)                   │
│ 3. consumer.commitSync()  ─────────────────────────┐   │
└────────────────────────────────────────────────────┼───┘
                                                     ▼ (TCP Commit Request)
Kafka Coordinator Broker
┌────────────────────────────────────────────────────────┐
│ Writes to internal compacted topic:                    │
│   Key:   [Group: "order-svc", Topic: "orders", Part: 0]│
│   Value: [Committed Offset: 42, Timestamp: ...]        │
└────────────────────────────────────────────────────────┘
```

## Build it
See [commit_semantics_demo.py](../code/commit_semantics_demo.py).
We demonstrate manual offset commits using synchronous and batched approaches.

## Use Kafka
Inspect committed offsets using the CLI:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group commit-lab-group
```

## Inspect it
Observe the difference between `CURRENT-OFFSET` and `LOG-END-OFFSET`.

## Measure it
Compare loop throughput of committing after *every single record* vs committing once *per batch*.

## Break it
Process records but never call `commitSync()`; restart the consumer and observe it re-reading from the old offset forever.

## Recover it
Implement proper batch commit at the end of each poll loop.

## Modify it
Configure manual commit with explicit offset maps (`{TopicPartition: OffsetAndMetadata}`).

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does committing after every single message destroy consumer throughput?
2. What is the danger of `commitAsync()` if a later commit succeeds before an earlier retried commit?

## Guarantees
* A committed offset represents the position from which a restarting consumer will fetch.

## Non-guarantees
* Committing an offset does not guarantee the downstream database transaction committed unless two-phase commit or transactional outbox is used.

## When to use this
* In all production consumers where data loss or uncontrolled duplicates must be managed.

## When not to use this
* Trivial analytics or telemetry where duplicate or dropped counts are acceptable.

## What comes next
In Phase 14, we formalize At-Most-Once vs. At-Least-Once delivery semantics through controlled failure injection.
"""

p13_code = {
    "commit_semantics_demo.py": """#!/usr/bin/env python3
import json
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

def run_manual_commit_demo():
    print("Connecting consumer with manual commit (enable_auto_commit=False)...")
    consumer = KafkaConsumer(
        "lab-orders",
        bootstrap_servers=["localhost:9092"],
        group_id="manual-commit-group",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        consumer_timeout_ms=5000
    )

    records = consumer.poll(timeout_ms=2000)
    print(f"Polled {sum(len(v) for v in records.values())} records across {len(records)} partitions.")

    for tp, batch in records.items():
        print(f"\\nProcessing partition {tp.partition}:")
        for record in batch:
            print(f"  Processed record offset: {record.offset}")
        
        # Commit exact next offset (offset + 1)
        last_offset = batch[-1].offset
        consumer.commit({
            tp: OffsetAndMetadata(last_offset + 1, "processed-by-worker-1")
        })
        print(f" [COMMITTED] Successfully committed offset {last_offset + 1} for partition {tp.partition}")

    consumer.close()

if __name__ == "__main__":
    run_manual_commit_demo()
"""
}

p13_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 13 Experiment: Verifying Manual Offset Commits ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/commit_semantics_demo.py
"""

p13_evidence = """# Phase 13 Evidence Log

* **Date:**
* **Group:** manual-commit-group
* **Auto Commit Enabled:** False
* **Committed Offset:**
* **Output of kafka-consumer-groups.sh describe:**
"""

write_phase("13-offset-commits", p13_doc, p13_code, p13_exp, p13_evidence)

# ==============================================================================
# PHASE 14: At-Most-Once and At-Least-Once
# ==============================================================================
p14_doc = """# Lesson 14: At-Most-Once and At-Least-Once

## Motto
"You cannot avoid failures in a distributed system; you can only choose whether failures cause data loss or duplicate processing."

## Problem
Every software engineer wishes for magic "exactly-once" delivery without thinking.
In the physical world of networks and separate processes, failures happen between operations.
Consider the two operations:
1. `write_to_database(record)`
2. `commit_offset_to_kafka(record.offset)`

Which one do you execute first?
* If you commit offset **before** writing to the database, and the database crashes $\\implies$ **Data is permanently lost (At-Most-Once)**.
* If you write to database **before** committing offset, and the consumer crashes $\\implies$ **Record is processed a second time upon restart (At-Least-Once)**.

## Prediction
Why is At-Least-Once the standard default across 99% of enterprise software?

## Why this matters
Understanding why At-Least-Once delivery produces duplicate events forces software engineers to design **Idempotent Consumers** (Phase 15).

## Mental model
```text
At-Most-Once (Commit BEFORE Processing)
[ Commit Offset: 5 ] ──► Crash! ──► (DB write never happens!)
Result: Event 5 was skipped forever. Lost data.

At-Least-Once (Process BEFORE Commit)
[ DB Write: Event 5 ] ──► Crash! ──► (Offset 5 was never committed!)
Restart: Fetches Event 5 again!
Result: Event 5 written to DB twice. Duplicate data.
```

## Build it
See [delivery_semantics_lab.py](../code/delivery_semantics_lab.py).
We inject simulated crashes before and after database writes to prove data loss vs duplicate insertion.

## Use Kafka
Observe consumer behavior under auto-commit (`at-most-once` if processing takes longer than commit interval) vs manual commit.

## Inspect it
Query the target SQLite database to count missing vs duplicate records.

## Measure it
Quantify the duplicate rate during simulated worker restarts.

## Break it
Simulate SIGKILL immediately after a database insert.

## Recover it
Implement database deduplication (idempotency).

## Modify it
Tune `auto.commit.interval.ms` to observe how it alters the failure window.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is data loss usually considered catastrophic, while duplicate delivery is manageable?
2. Under what rare conditions is At-Most-Once acceptable?

## Guarantees
* At-Least-Once guarantees no event will be dropped, at the expense of potential duplicates.
* At-Most-Once guarantees no duplicate processing, at the expense of potential lost events.

## Non-guarantees
* Neither pattern alone guarantees exactly-once business side effects.

## When to use this
* Use At-Least-Once as the baseline for all business-critical event processing.

## When not to use this
* Never use At-Most-Once for financial, billing, or compliance systems.

## What comes next
In Phase 15, we build Idempotent Consumers to convert At-Least-Once duplicates into safe, exactly-once business results.
"""

p14_code = {
    "delivery_semantics_lab.py": """#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = "/tmp/delivery_lab.db"

def setup_db():
    if os.path.exists(DB_PATH): os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE orders (id TEXT, amount REAL)")
    conn.commit()
    conn.close()

def at_most_once_flow(events, crash_at=2):
    print("--- Testing AT-MOST-ONCE (Commit BEFORE Processing) ---")
    setup_db()
    committed_offset = 0
    
    for offset, event in enumerate(events):
        # 1. Commit offset FIRST
        committed_offset = offset + 1
        
        # 2. Crash simulation
        if offset == crash_at:
            print(f" [CRASH] Worker killed at offset {offset} BEFORE DB write!")
            break
            
        # 3. DB write
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO orders VALUES (?, ?)", (event["id"], event["amount"]))
        conn.commit()
        conn.close()

    print(f"State on disk: Committed offset = {committed_offset}")
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT count(*) FROM orders").fetchone()[0]
    print(f"Orders in database: {rows} (Expected {len(events)}) -> DATA LOSS OCCURRED!")
    conn.close()

def at_least_once_flow(events, crash_at=2):
    print("\\n--- Testing AT-LEAST-ONCE (Process BEFORE Commit) ---")
    setup_db()
    committed_offset = 0
    
    for offset, event in enumerate(events):
        # 1. DB write FIRST
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO orders VALUES (?, ?)", (event["id"], event["amount"]))
        conn.commit()
        conn.close()
        
        # 2. Crash simulation
        if offset == crash_at:
            print(f" [CRASH] Worker killed at offset {offset} AFTER DB write, BEFORE commit!")
            break
            
        # 3. Commit offset SECOND
        committed_offset = offset + 1

    print(f"State on disk: Committed offset = {committed_offset}")
    print("Worker restarts from committed offset and re-processes...")
    # Re-run from committed_offset
    for offset in range(committed_offset, crash_at + 1):
        event = events[offset]
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO orders VALUES (?, ?)", (event["id"], event["amount"]))
        conn.commit()
        conn.close()

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("SELECT count(*) FROM orders").fetchone()[0]
    print(f"Orders in database: {rows} (Events were 3) -> DUPLICATE PROCESSING OCCURRED!")
    conn.close()

if __name__ == "__main__":
    sample_events = [
        {"id": "ORD-1", "amount": 10.0},
        {"id": "ORD-2", "amount": 20.0},
        {"id": "ORD-3", "amount": 30.0},
    ]
    at_most_once_flow(sample_events, crash_at=1)
    at_least_once_flow(sample_events, crash_at=1)
"""
}

p14_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 14 Experiment: Demonstrating At-Most-Once vs At-Least-Once Failure Modes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/delivery_semantics_lab.py
"""

p14_evidence = """# Phase 14 Evidence Log

* **Date:**
* **Events Tested:** 3
* **Records in DB under At-Most-Once Crash:**
* **Records in DB under At-Least-Once Crash:**
* **Which failure mode is safer and why:**
"""

write_phase("14-at-most-once-and-at-least-once", p14_doc, p14_code, p14_exp, p14_evidence)

# ==============================================================================
# PHASE 15: Idempotent Consumers
# ==============================================================================
p15_doc = """# Lesson 15: Idempotent Consumers

## Motto
"Duplicate delivery is a network inevitability; duplicate side-effects are an application bug."

## Problem
In Phase 14, we proved that under At-Least-Once delivery, consumers will inevitably receive duplicate messages whenever a network partition, rebalance, or process crash occurs between processing and offset committing.
If the event is `charge_credit_card(user_id, $50)` and the consumer runs twice, the customer is billed $100!
How do we make our consumer robust against duplicate deliveries?

## Prediction
What happens if an order processing consumer checks an `idempotency_keys` table inside the same database transaction as the business write?

## Why this matters
**Building idempotent consumers is the single most critical engineering pattern in event-driven architecture.**
It bridges the gap between Kafka's At-Least-Once transport guarantee and the business requirement of exactly-once side effects.

## Mental model
```text
Event: { "event_id": "evt_9981", "action": "charge", "amount": 50 }

Consumer Process
   │
   ▼
[ Check Idempotency Store: Has "evt_9981" been processed? ]
   ├── YES ──► SKIP execution! Commit offset immediately. (No duplicate billing!)
   └── NO  ──► 1. Execute charge ($50)
               2. Record "evt_9981" in processed_events table
               3. Commit offset to Kafka
```

## Build it
See [idempotent_consumer.py](../code/idempotent_consumer.py).
We implement an order fulfillment consumer using an atomic SQLite transaction that combines business logic with an `idempotent_keys` check.

## Use Kafka
Deliver the exact same message 3 times to the consumer.

## Inspect it
Inspect the database tables to verify that despite 3 deliveries, the customer was only charged once.

## Measure it
Measure latency overhead of checking the idempotency store per transaction.

## Break it
Remove the uniqueness constraint on `event_id` and observe duplicate billing return.

## Recover it
Restore the unique constraint or transactional idempotency guard.

## Modify it
Implement idempotency using a Redis `SET key EX 86400 NX` cache with a TTL.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is an auto-generated database primary key (e.g. `AUTO_INCREMENT`) useless as an idempotency key?
2. What makes an `event_id` generated by the original producer effective for deduplication?

## Guarantees
* Processing the same event $N$ times produces the identical business state as processing it once.

## Non-guarantees
* Idempotency keys stored in memory or non-durable caches can be lost during crashes.

## When to use this
* In every consumer performing non-idempotent operations: charging money, sending emails, updating bank balances.

## When not to use this
* Naturally idempotent operations (e.g. `SET user_status = 'ACTIVE'`, `temperature = 72.0`).

## What comes next
In Phase 16, we turn to producer performance: Producer Batching and the latency/throughput trade-off.
"""

p15_code = {
    "idempotent_consumer.py": """#!/usr/bin/env python3
import sqlite3
import os

DB_PATH = "/tmp/idempotent_lab.db"

class IdempotentOrderConsumer:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        if os.path.exists(self.db_path): os.remove(self.db_path)
        conn = sqlite3.connect(self.db_path)
        # Business table
        conn.execute("CREATE TABLE orders (order_id TEXT PRIMARY KEY, amount REAL)")
        # Idempotency table
        conn.execute("CREATE TABLE processed_events (event_id TEXT PRIMARY KEY, processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        conn.commit()
        conn.close()

    def process_record(self, event_id: str, order_id: str, amount: float):
        conn = sqlite3.connect(self.db_path)
        try:
            # ATOMIC TRANSACTION: Check idempotency + execute business write together
            with conn:
                cursor = conn.cursor()
                # Check if event was already handled
                cursor.execute("SELECT 1 FROM processed_events WHERE event_id = ?", (event_id,))
                if cursor.fetchone() is not None:
                    print(f" [DUPLICATE DETECTED] Event {event_id} already processed. SKIPPING side effect!")
                    return False

                # Execute business write
                cursor.execute("INSERT INTO orders (order_id, amount) VALUES (?, ?)", (order_id, amount))
                # Record idempotency key
                cursor.execute("INSERT INTO processed_events (event_id) VALUES (?)", (event_id,))
                print(f" [PROCESSED] Successfully executed order {order_id} for ${amount:.2f}")
                return True
        finally:
            conn.close()

if __name__ == "__main__":
    consumer = IdempotentOrderConsumer()
    
    # Simulate receiving the exact same event 3 times (due to retries / crashes)
    event = {"event_id": "evt_uuid_12345", "order_id": "ORD-501", "amount": 99.95}

    print("Delivery 1:")
    consumer.process_record(event["event_id"], event["order_id"], event["amount"])

    print("\\nDelivery 2 (Duplicate replay):")
    consumer.process_record(event["event_id"], event["order_id"], event["amount"])

    print("\\nDelivery 3 (Duplicate replay):")
    consumer.process_record(event["event_id"], event["order_id"], event["amount"])

    conn = sqlite3.connect(DB_PATH)
    orders = conn.execute("SELECT * FROM orders").fetchall()
    print(f"\\nFinal Database Orders: {orders}")
    print("Result: Exactly 1 order in database despite 3 deliveries!")
    conn.close()
"""
}

p15_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 15 Experiment: Running Idempotent Consumer Simulation ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/idempotent_consumer.py
"""

p15_evidence = """# Phase 15 Evidence Log

* **Date:**
* **Event ID:** evt_uuid_12345
* **Deliveries Attempted:** 3
* **Actual Business Executions:** 1
* **Deduplication Strategy Used:**
"""

write_phase("15-idempotent-consumers", p15_doc, p15_code, p15_exp, p15_evidence)

print("Phases 00 to 15 successfully generated!")
