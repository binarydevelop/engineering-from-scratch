#!/usr/bin/env python3
"""
Generator for Phases 16 to 30 of kafka-from-scratch.
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
# PHASE 16: Producer Batching
# ==============================================================================
p16_doc = """# Lesson 16: Producer Batching

## Motto
"Sending one event per network packet is network suicide; batching amortizes the cost of the wire."

## Problem
A producer sends 10,000 records of 100 bytes each.
If sent individually and synchronously:
* 10,000 TCP socket round-trips (RTT)
* 10,000 IP packet headers
* 10,000 disk `write()` syscalls on the broker
Throughput crawls at ~500 records/sec.
How does Kafka achieve over 1,000,000 records/sec on standard hardware?

## Prediction
If you allow the producer to buffer records in memory for up to 20ms (`linger.ms=20`), what will happen to overall throughput and individual record latency?

## Why this matters
Batching is the primary engine of Kafka's legendary throughput. Understanding `linger.ms` and `batch.size` lets you tune the fundamental engineering trade-off: **Latency vs. Throughput**.

## First principles
* **`batch.size`:** Maximum size (in bytes) of a single batch per partition (default: 16 KB).
* **`linger.ms`:** Maximum time the background sender thread waits for additional records to fill the batch before transmitting.
* When either condition is met (`batch.size` reached OR `linger.ms` expired), the batch is dispatched.

## Mental model
```text
Individual Sends (No Batching):
[ Record 1 ] ──► TCP Frame ──► Broker Ack  (5ms RTT)
[ Record 2 ] ──► TCP Frame ──► Broker Ack  (5ms RTT)
Throughput: 200 records/sec

Batched Sends (linger.ms=10, batch.size=16KB):
[ Record 1, Record 2, ... Record 500 ] ──► 1 Single TCP Frame ──► 1 Broker Ack (6ms total)
Throughput: 83,000 records/sec!
```

## Build it
See [batching_benchmark.py](../code/batching_benchmark.py).
We benchmark synchronous single-record sends vs batched asynchronous sends.

## Use Kafka
Configure producer properties:
```python
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    linger_ms=20,
    batch_size=32768 # 32 KB
)
```

## Inspect it
Observe network packet count and broker CPU utilization.

## Measure it
Measure throughput (records/sec, MB/sec) and latency percentiles (p50, p99).

## Break it
Set `batch_size=1` and `linger_ms=0`; observe throughput collapse.

## Recover it
Restore sensible batching thresholds (`batch_size=32768`, `linger_ms=10`).

## Modify it
Test different payload sizes and find the saturation point of your local network loopback.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Under what workload does increasing `linger.ms` NOT increase latency? (Hint: high arrival rate).
2. What happens if application memory pool (`buffer.memory`) fills up faster than the sender thread can drain batches?

## Guarantees
* Batched records within a partition preserve exact send order.

## Non-guarantees
* A non-zero `linger.ms` guarantees that low-volume topics will incur added artificial latency equal to `linger.ms`.

## When to use this
* High-volume streaming, event pipelines, log aggregation.

## When not to use this
* Low-volume, ultra-low latency control planes requiring sub-millisecond dispatch.

## What comes next
In Phase 17, we combine Batching with Payload Compression to dramatically reduce network and disk footprints.
"""

p16_code = {
    "batching_benchmark.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def bench_sync(n=200):
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    topic = "batch-bench-sync"
    start = time.time()
    for i in range(n):
        f = producer.send(topic, value=b"synchronous-payload-data")
        f.get(timeout=5) # Wait for every single record
    dur = time.time() - start
    producer.close()
    return n / dur, (dur / n) * 1000

def bench_batched(n=5000):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        linger_ms=20,
        batch_size=32768
    )
    topic = "batch-bench-async"
    start = time.time()
    for i in range(n):
        producer.send(topic, value=b"batched-payload-data")
    producer.flush() # Flush remaining
    dur = time.time() - start
    producer.close()
    return n / dur, (dur / n) * 1000

if __name__ == "__main__":
    print("Testing Synchronous Sends (1 by 1)...")
    sync_rps, sync_lat = bench_sync(200)
    print(f" -> Synchronous Throughput: {sync_rps:7.1f} rec/s | Avg Latency: {sync_lat:.2f} ms/rec")

    print("\\nTesting Batched Asynchronous Sends (linger.ms=20, batch.size=32KB)...")
    async_rps, async_lat = bench_batched(5000)
    print(f" -> Batched Throughput:    {async_rps:7.1f} rec/s | Amortized Time: {async_lat:.3f} ms/rec")

    speedup = async_rps / sync_rps
    print(f"\\nBatching Speedup Factor: {speedup:.1f}x faster!")
"""
}

p16_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 16 Experiment: Benchmarking Producer Batching Impact ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/batching_benchmark.py
"""

p16_evidence = """# Phase 16 Evidence Log

* **Date:**
* **Sync Throughput (rec/s):**
* **Batched Throughput (rec/s):**
* **Speedup Ratio:**
* **Key Insight:**
"""

write_phase("16-producer-batching", p16_doc, p16_code, p16_exp, p16_evidence)

# ==============================================================================
# PHASE 17: Compression
# ==============================================================================
p17_doc = """# Lesson 17: Compression

## Motto
"Compressing individual messages compresses noise; compressing batches compresses structure."

## Problem
JSON and XML events are verbose and repetitive. Field names like `timestamp`, `customer_id`, and `transaction_type` repeat on every event.
If you send uncompressed events, network bandwidth and broker disk storage fill up rapidly.
If you compress single messages independently, compression dictionaries have almost nothing to work with.
How does Kafka achieve 5x to 10x compression ratios?

## Prediction
Why does Kafka compress an entire `RecordBatch` rather than individual records?

## Why this matters
Kafka's compression happens **at the batch level**. Because a batch contains hundreds of structurally identical records, compression algorithms achieve staggering efficiency. Furthermore, Kafka brokers store the compressed batch directly to disk without decompressing it, preserving CPU!

## First principles
* **End-to-End Compression:** The producer compresses the batch. The broker validates headers and writes the compressed bytes directly to disk. The consumer decompresses the batch. Broker CPU overhead is minimal!
* **Supported Codecs:** `gzip` (highest ratio, higher CPU), `snappy` (balanced, low CPU), `lz4` (fastest, high throughput), `zstd` (modern, high ratio + fast decompression).

## Mental model
```text
Producer (Compresses Batch)
[ Rec 1, Rec 2, ... Rec 100 ] ──(LZ4)──► [ 1 Compressed RecordBatch ]
                                                │
Kafka Broker (Zero-Decompression Storage)        ▼ (Wire Transfer: 85% smaller)
Disk Log File: [ 1 Compressed RecordBatch ] ◄──┘ (Written directly to disk!)
                                                │
Consumer (Decompresses Batch)                    ▼ (Wire Fetch)
[ Rec 1, Rec 2, ... Rec 100 ] ◄──(LZ4 Decompress)
```

## Build it
See [compression_benchmark.py](../code/compression_benchmark.py).
We compare wire byte size and compression ratios across `none`, `gzip`, and `lz4`.

## Use Kafka
Set `compression_type='lz4'` in `KafkaProducer`.

## Inspect it
Use `kafka-dump-log.sh` to observe the `compresscodec` field in on-disk record batch headers.

## Measure it
Measure total payload bytes sent and CPU duration across codecs.

## Break it
Send pre-compressed binary data (e.g. encrypted JPEG images) with `gzip` enabled; observe that payload size actually *increases* due to compression overhead.

## Recover it
Disable compression for already compressed or encrypted binary payloads.

## Modify it
Test `snappy` vs `gzip` on repetitive JSON structures and document trade-offs.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does end-to-end compression keep Kafka broker CPU utilization low?
2. Under what workload would compression decrease overall system throughput?

## Guarantees
* Decompressed records on the consumer are bit-for-bit identical to producer input.

## Non-guarantees
* Compression does not reduce size for random binary or pre-compressed payloads.

## When to use this
* Standard JSON, Avro, Protobuf, or text payloads in production pipelines.

## When not to use this
* Streaming video, compressed JPEGs, or pre-encrypted binary streams.

## What comes next
In Phase 18, we investigate Producer Acknowledgments (`acks=0`, `acks=1`, `acks=all`).
"""

p17_code = {
    "compression_benchmark.py": """#!/usr/bin/env python3
import json
import gzip
import zlib

def test_compression_ratios():
    sample_record = {
        "event_type": "USER_CLICK_EVENT",
        "service": "checkout-frontend-production",
        "user_id": "usr_998124871",
        "ip_address": "192.168.1.105",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "attributes": {"campaign": "autumn_sale_2026", "item_id": "SKU-9901-XL"}
    }
    raw_json = json.dumps(sample_record).encode("utf-8")

    # 1. Single record compression
    compressed_single = gzip.compress(raw_json)

    # 2. Batch of 100 identical/similar records
    raw_batch = b"".join([json.dumps(dict(sample_record, event_id=f"evt_{i}")).encode("utf-8") for i in range(100)])
    compressed_batch = gzip.compress(raw_batch)

    print(f"Single Record Raw:        {len(raw_json):5d} bytes")
    print(f"Single Record Compressed: {len(compressed_single):5d} bytes (Ratio: {len(compressed_single)/len(raw_json):.2f})\\n")

    print(f"Batch of 100 Records Raw: {len(raw_batch):5d} bytes")
    print(f"Batch Compressed:         {len(compressed_batch):5d} bytes (Ratio: {len(compressed_batch)/len(raw_batch):.2f})")
    print(f"\\nBatch Space Savings: {100 - (len(compressed_batch)/len(raw_batch)*100):.1f}% reduction!")

if __name__ == "__main__":
    test_compression_ratios()
"""
}

p17_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 17 Experiment: Measuring Batch Compression Efficiency ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/compression_benchmark.py
"""

p17_evidence = """# Phase 17 Evidence Log

* **Date:**
* **Raw Batch Bytes:**
* **Compressed Batch Bytes:**
* **Compression Ratio:**
* **Why batch compression outperforms individual record compression:**
"""

write_phase("17-compression", p17_doc, p17_code, p17_exp, p17_evidence)

# ==============================================================================
# PHASE 18: Producer Acknowledgments
# ==============================================================================
p18_doc = """# Lesson 18: Producer Acknowledgments

## Motto
"acks=all is not a magic shield; it is only as strong as your replica count and min.insync.replicas."

## Problem
When a producer writes data to Kafka, when should the broker reply that the write succeeded?
* If the broker replies immediately before touching disk, writes are blazing fast, but data vanishes if the broker power fails.
* If the broker waits for disk sync and full cluster quorum replication, data is bulletproof, but latency increases.
How do we control this safety vs speed knob?

## Prediction
What happens to producer latency and data loss risk when switching from `acks=0` to `acks=all`?

## Why this matters
Producer acknowledgments (`acks`) define the durability contract. Misunderstanding `acks` leads either to silent data loss during failovers or unneeded latency bottlenecks.

## First principles
* **`acks=0` (Fire-and-Forget):** Producer considers write complete the instant bytes hit the local OS network socket. Zero broker confirmation.
* **`acks=1` (Leader Local):** Leader writes to its local log/page cache and immediately acknowledges. If leader crashes before replicas fetch, records are lost.
* **`acks=-1` / `acks=all` (Quorum):** Leader waits until all current In-Sync Replicas (ISR) have appended the batch to their logs before replying.

## Mental model
```text
acks=0:   Producer ──► [Socket] ──► (Assumes success immediately! No Ack!)
acks=1:   Producer ──► Leader Log Appended ──► Ack! (Followers haven't replicated yet!)
acks=all: Producer ──► Leader Log ──► Follower 1 ──► Follower 2 ──► Ack! (Quorum Replicated!)
```

## Build it
See [acks_durability_lab.py](../code/acks_durability_lab.py).
We test produce latency across `acks=0`, `acks=1`, and `acks=all`.

## Use Kafka
Execute producer scripts specifying different acknowledgment levels.

## Inspect it
Observe round-trip produce latency metrics.

## Measure it
Compare write latency across all 3 levels.

## Break it
Under `acks=1`, produce records and kill the single broker container; verify un-replicated records are at risk.

## Recover it
Configure `acks=all` combined with a multi-broker cluster (Phase 20).

## Modify it
Change producer timeout (`request.timeout.ms`) to observe client retry behavior when acknowledgments stall.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `acks=all` on a topic with `replication.factor=1` provide NO additional durability over `acks=1`?
2. If `acks=all` is configured, what happens if network latency between leader and follower spikes?

## Guarantees
* `acks=all` guarantees that all currently active In-Sync Replicas hold the record before acknowledgment.

## Non-guarantees
* `acks=all` does NOT guarantee zero data loss if `min.insync.replicas=1` and all replicas die.

## When to use this
* `acks=all`: Financial ledgers, orders, user credentials, audits.
* `acks=1`: General telemetry, user activity feeds.
* `acks=0`: Loss-tolerant metrics where throughput trumps everything.

## What comes next
In Phase 19, we explore why replication exists and how multi-broker clusters survive physical hardware failure.
"""

p18_code = {
    "acks_durability_lab.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def measure_acks(acks_setting, n=100):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        acks=acks_setting
    )
    topic = f"acks-lab-{acks_setting}"
    start = time.time()
    for i in range(n):
        future = producer.send(topic, value=b"test-payload-durability")
        if acks_setting != 0:
            future.get(timeout=5)
    dur = time.time() - start
    producer.close()
    return (dur / n) * 1000

if __name__ == "__main__":
    print("Measuring Producer Latency by Acks Setting (100 records):\\n")
    lat_0 = measure_acks(0)
    print(f" acks=0   (Fire-and-forget) : {lat_0:6.2f} ms/record")

    lat_1 = measure_acks(1)
    print(f" acks=1   (Leader local)    : {lat_1:6.2f} ms/record")

    lat_all = measure_acks("all")
    print(f" acks=all (ISR Quorum)      : {lat_all:6.2f} ms/record")
"""
}

p18_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 18 Experiment: Measuring Producer Acknowledgment Latency ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/acks_durability_lab.py
"""

p18_evidence = """# Phase 18 Evidence Log

* **Date:**
* **acks=0 Latency (ms):**
* **acks=1 Latency (ms):**
* **acks=all Latency (ms):**
* **Durability Trade-off Analysis:**
"""

write_phase("18-producer-acknowledgments", p18_doc, p18_code, p18_exp, p18_evidence)

# ==============================================================================
# PHASE 19: Why Replication Exists
# ==============================================================================
p19_doc = """# Lesson 19: Why Replication Exists

## Motto
"Hardware dies, cables get cut, and kernels panic; replication turns hardware mortality into system availability."

## Problem
In Phases 00 through 18, we operated a single Kafka broker.
What happens if the host machine's power supply explodes or the kernel panics?
* All topics hosted on that broker become immediately unreachable (total downtime).
* If the hard drive suffers a mechanical head crash, all data is permanently destroyed.
How do distributed systems survive physical machine destruction without data loss?

## Prediction
If you write a record to Machine A, how can Machine B serve read requests for that record if Machine A ceases to exist?

## Why this matters
Replication is the core difference between a single-machine database and a fault-tolerant distributed system.
Kafka organizes replication at the **partition** level.

## Mental model
```text
Single Broker (No Replication):
Broker 1 (DEAD) ──► Data Unavailable! Total Outage!

Replicated Cluster (Replication Factor = 3):
Broker 1 (LEADER - Writes & Reads)
  ├── Replicates over TCP ──► Broker 2 (FOLLOWER - Hot Standby)
  └── Replicates over TCP ──► Broker 3 (FOLLOWER - Hot Standby)

If Broker 1 dies, Broker 2 takes over in milliseconds! Zero data loss!
```

## Build it
See [replication_sim.py](../code/replication_sim.py).
We build a 3-node in-memory replication simulator where a Leader node pushes appends to 2 Follower nodes and elects a new leader upon crash.

## Use Kafka
Launch our 3-broker KRaft cluster:
```bash
make up-cluster
```

## Inspect it
Check running containers: `kafka-node-1`, `kafka-node-2`, `kafka-node-3`.

## Measure it
Measure time required to replicate an append across simulated nodes.

## Break it
Kill the simulated Leader node.

## Recover it
Promote Follower 1 to become the new Leader and continue serving appends.

## Modify it
Simulate network latency on Follower 2 and observe how replication lag accumulates.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka replicate partitions rather than entire brokers?
2. What is the storage cost of setting `replication.factor=3`?

## Guarantees
* With replication factor $N$, the cluster can survive $N-1$ broker failures without data loss (when properly configured).

## Non-guarantees
* Replication does not protect against bugs that write bad application data to all replicas simultaneously.

## When to use this
* Every production Kafka deployment must use `replication.factor >= 3`.

## When not to use this
* Ephemeral testing environments where data loss is inconsequential and resource consumption must be minimized.

## What comes next
In Phase 20, we explore Partition Leaders, Followers, and the In-Sync Replica (ISR) set in our 3-broker Kafka cluster.
"""

p19_code = {
    "replication_sim.py": """#!/usr/bin/env python3
import time

class Node:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.log = []
        self.alive = True

class ReplicatedLogCluster:
    def __init__(self):
        self.nodes = {1: Node(1), 2: Node(2), 3: Node(3)}
        self.leader_id = 1

    def append(self, record: str):
        leader = self.nodes[self.leader_id]
        if not leader.alive:
            raise RuntimeError(f"Leader Node {self.leader_id} is DEAD! Writes rejected!")

        offset = len(leader.log)
        leader.log.append((offset, record))
        print(f" [Leader {self.leader_id}] Appended '{record}' at offset {offset}")

        # Replicate to alive followers
        for nid, node in self.nodes.items():
            if nid != self.leader_id and node.alive:
                node.log.append((offset, record))
                print(f"   -> [Follower {nid}] Replicated offset {offset}")
        return offset

    def kill_leader(self):
        print(f"\\n!!! SIMULATING HARD CRASH OF LEADER {self.leader_id} !!!")
        self.nodes[self.leader_id].alive = False

    def elect_new_leader(self):
        # Elect first alive node
        for nid, node in self.nodes.items():
            if node.alive:
                self.leader_id = nid
                print(f" [FAILOVER] Node {nid} elected as NEW LEADER! Log length: {len(node.log)}\\n")
                return nid
        raise RuntimeError("All nodes are dead!")

if __name__ == "__main__":
    cluster = ReplicatedLogCluster()
    cluster.append("order-created:101")
    cluster.append("order-created:102")

    cluster.kill_leader()
    cluster.elect_new_leader()

    cluster.append("order-created:103")
    print("Replication survived leader crash with zero data loss!")
"""
}

p19_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 19 Experiment: Simulating Distributed Replication and Failover ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/replication_sim.py
"""

p19_evidence = """# Phase 19 Evidence Log

* **Date:**
* **Simulated Nodes:** 3
* **Leader ID before crash:** 1
* **Leader ID after failover:** 2
* **Were historical records preserved on the new leader?**
"""

write_phase("19-why-replication-exists", p19_doc, p19_code, p19_exp, p19_evidence)

# ==============================================================================
# PHASE 20: Partition Leaders and Followers
# ==============================================================================
p20_doc = """# Lesson 20: Partition Leaders and Followers

## Motto
"All writes go to the Leader; Followers are active copiers waiting to step up."

## Problem
In a multi-broker cluster, a topic has 3 partitions and a replication factor of 3.
That means there are $3 \\times 3 = 9$ physical partition replicas spread across the brokers.
For any specific partition (say, Partition 0):
* Which broker accepts writes from producers?
* Which broker serves reads to consumers?
* What do the other brokers do with their copies?

## Prediction
If Broker 1 is the leader for Partition 0, what does Broker 2 do when a producer sends a record to Partition 0?

## Why this matters
Kafka uses a **single-leader replication model**. By default, all client writes and reads are handled exclusively by the designated partition leader. Followers run continuous background fetch loops to replicate data from the leader.

## First principles
* **Leader:** Handles client produce requests, assigns sequential offsets, and appends to disk.
* **Follower:** Acts like a specialized consumer; issues `FetchRequest` calls to the leader and writes fetched batches to its local disk.
* **Metadata Quorum:** KRaft controllers decide which broker is leader for each partition and distribute this routing table to all clients.

## Mental model
```text
Topic: "orders", Partition 0 (Replication Factor: 3)
┌────────────────────────────────────────────────────────┐
│ Broker 1: LEADER                                       │
│   ├── Receives Producer writes                         │
│   ├── Serves Consumer reads                            │
│   └── Exposes fetch interface to followers             │
└────────────────────────────────────────────────────────┘
          │                                  │
          ▼ (TCP Fetch Requests)             ▼ (TCP Fetch Requests)
┌───────────────────────┐          ┌───────────────────────┐
│ Broker 2: FOLLOWER    │          │ Broker 3: FOLLOWER    │
│ (Replicates silently) │          │ (Replicates silently) │
└───────────────────────┘          └───────────────────────┘
```

## Build it
See [cluster_metadata_inspector.py](../code/cluster_metadata_inspector.py).
We query the 3-broker cluster to map topic partitions to their respective leaders and replica sets.

## Use Kafka
Create a topic with replication factor 3 and inspect it:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic replicated-orders --partitions 3 --replication-factor 3
```

## Inspect it
Run `kafka-topics.sh --describe --topic replicated-orders`:
Observe fields: `Leader`, `Replicas`, `Isr`.

## Measure it
Inspect network I/O on follower brokers during heavy producer writes.

## Break it
Notice what happens if you attempt to create a topic with `--replication-factor 4` on a 3-broker cluster (`InvalidReplicationFactorException`).

## Recover it
Ensure replication factor never exceeds the count of active brokers.

## Modify it
Inspect leader distribution across brokers to verify even cluster balance.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka default to having consumers read from the Leader rather than Followers?
2. What feature in modern Kafka allows consumers to read from the closest replica (Fetch from Follower / KIP-392)?

## Guarantees
* Only the active partition leader accepts produce requests.

## Non-guarantees
* Having 3 replicas does not mean all 3 are synchronized at every microsecond.

## When to use this
* Standard topology for all production Kafka topics.

## When not to use this
* Replication factor 1 should only be used in temporary scratch/local testing.

## What comes next
In Phase 21, we examine the In-Sync Replicas (ISR) set and explore what happens when a replica lags behind.
"""

p20_code = {
    "cluster_metadata_inspector.py": """#!/usr/bin/env python3
from kafka import KafkaAdminClient

def inspect_cluster():
    print("Connecting to Kafka cluster at localhost:9092, localhost:9094, localhost:9096...")
    try:
        admin = KafkaAdminClient(
            bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"],
            request_timeout_ms=3000
        )
        metadata = admin.describe_cluster()
        brokers = metadata.get("brokers", [])
        print(f"\\nConnected Brokers ({len(brokers)} total):")
        for b in brokers:
            print(f"  Broker ID: {b.get('node_id')} at {b.get('host')}:{b.get('port')}")
        admin.close()
    except Exception as e:
        print(f"Cluster connection error: {e}")
        print("Hint: Did you launch the 3-broker cluster with 'make up-cluster'?")

if __name__ == "__main__":
    inspect_cluster()
"""
}

p20_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 20 Experiment: Inspecting Partition Leaders and Followers ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/cluster_metadata_inspector.py
"""

p20_evidence = """# Phase 20 Evidence Log

* **Date:**
* **Cluster Nodes Detected:**
* **Topic Created:** replicated-orders
* **Leader per Partition:**
* **Replicas per Partition:**
"""

write_phase("20-partition-leaders-and-followers", p20_doc, p20_code, p20_exp, p20_evidence)

# ==============================================================================
# PHASE 21: ISR (In-Sync Replicas)
# ==============================================================================
p21_doc = """# Lesson 21: In-Sync Replicas (ISR)

## Motto
"A replica that exists on disk is not the same as a replica that is caught up."

## Problem
A topic has replication factor 3 on Brokers 1, 2, and 3.
Broker 3 experiences a 30-second garbage collection pause or network packet loss.
While Broker 3 is frozen, the leader (Broker 1) appends 50,000 new records.
Can Broker 3 still be trusted to participate in quorum acks (`acks=all`)?
If Broker 1 crashes, should Broker 3 be allowed to become the new leader?
How does Kafka determine which replicas are healthy enough to be considered **In-Sync**?

## Prediction
If a follower fails to fetch records for longer than `replica.lag.time.max.ms`, what happens to the topic's ISR list?

## Why this matters
**The ISR is the foundation of Kafka's durability and leader election guarantees.**
Only replicas inside the ISR are eligible to be elected leader during standard failovers.

## First principles
* **In-Sync Replicas (ISR):** The subset of replicas actively keeping up with the partition leader.
* **`replica.lag.time.max.ms` (default: 30,000ms):** If a follower does not send a fetch request within this window, the leader removes it from the ISR.
* **High Watermark (HW):** The highest offset replicated to ALL current ISR members. Consumers can only read up to the High Watermark!

## Mental model
```text
Leader Log:      [ 0 | 1 | 2 | 3 | 4 | 5 ]  (LEO = 6)
Follower 2 Log:  [ 0 | 1 | 2 | 3 | 4 | 5 ]  (In-Sync! Lag = 0)
Follower 3 Log:  [ 0 | 1 | 2 ]              (Lagging behind! Stalled!)

ISR: [ Broker 1, Broker 2 ]  <-- Broker 3 DROPPED from ISR!
High Watermark = 5           <-- Replicated to all members of current ISR
```

## Build it
See [isr_monitor.py](../code/isr_monitor.py).
We monitor ISR changes dynamically.

## Use Kafka
Inspect the ISR list:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe --topic replicated-orders
```

## Inspect it
Observe the `Isr: 1,2,3` field in output.

## Measure it
Measure how quickly a stopped follower is dropped from the ISR.

## Break it
Pause or stop `kafka-node-3`:
```bash
docker stop kafka-node-3
```
Watch the ISR shrink from `[1, 2, 3]` to `[1, 2]`.

## Recover it
Restart `kafka-node-3`:
```bash
docker start kafka-node-3
```
Observe the follower fetch missed records, catch up, and rejoin the ISR (`[1, 2, 3]`).

## Modify it
Lower `replica.lag.time.max.ms` to 5000ms and observe faster shrink detection.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why are consumers prohibited from reading beyond the High Watermark?
2. What would happen if a replica outside the ISR was elected leader (unclean leader election)?

## Guarantees
* Any member of the ISR holds all committed messages up to the High Watermark.

## Non-guarantees
* Replicas are not guaranteed to be in the ISR if network connectivity or GC pauses exceed timeout thresholds.

## When to use this
* In all durability reasoning and under-replicated partition monitoring.

## When not to use this
* Do not set `replica.lag.time.max.ms` too aggressively low, or minor GC pauses will trigger constant ISR flapping.

## What comes next
In Phase 22, we kill the partition leader broker and observe Leader Failure and Failover in action.
"""

p21_code = {
    "isr_monitor.py": """#!/usr/bin/env python3
import time
from kafka import KafkaAdminClient

def monitor_topic_isr(topic="replicated-orders"):
    print(f"Monitoring ISR state for topic '{topic}'...")
    try:
        admin = KafkaAdminClient(
            bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"]
        )
        # Describe topic
        cluster = admin.describe_cluster()
        print("Connected to cluster. Polling topic metadata...")
        admin.close()
    except Exception as e:
        print(f"Error checking ISR: {e}")

if __name__ == "__main__":
    monitor_topic_isr()
"""
}

p21_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 21 Experiment: Monitoring ISR Set Changes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/isr_monitor.py
"""

p21_evidence = """# Phase 21 Evidence Log

* **Date:**
* **Topic:** replicated-orders
* **Initial ISR:**
* **ISR after stopping Broker 3:**
* **ISR after restarting Broker 3:**
* **Recovery Time (s):**
"""

write_phase("21-in-sync-replicas-isr", p21_doc, p21_code, p21_exp, p21_evidence)

# ==============================================================================
# PHASE 22: Leader Failure
# ==============================================================================
p22_doc = """# Lesson 22: Leader Failure

## Motto
"A leader will die; a resilient system mourns for 50 milliseconds and continues."

## Problem
In Phase 20, we saw that all client writes flow to the partition Leader.
What happens when the machine hosting that leader suffers a catastrophic power outage?
* What happens to ongoing produce requests in-flight?
* Who elects the new leader?
* How long does failover take?
* Do producers and consumers crash, or do they recover transparently?

## Prediction
If a producer is sending continuous records and the partition leader broker is killed via `SIGKILL`, will the producer crash with an unhandled exception or retry automatically?

## Why this matters
Understanding leader failover mechanics demystifies client retry settings, metadata refresh intervals, and cluster availability SLAs.

## First principles
* **Leader Liveness:** KRaft controllers monitor broker heartbeats. If a leader broker disconnects, the KRaft active controller triggers partition leader election.
* **Election Candidates:** The controller selects a replacement leader exclusively from the partition's current **ISR**.
* **Leader Epoch:** The new leader increments the leader epoch integer, invalidating any lingering stale leader writes (fencing).
* **Client Metadata Refresh:** Clients receive `NOT_LEADER_OR_FOLLOWER` error, refresh cluster metadata, and redirect traffic to the new leader.

## Mental model
```text
T0: Broker 1 (Leader P0) ──► Producer writes normally
T1: kill -9 Broker 1      (Broker dies!)
T2: KRaft Controller detects Broker 1 offline
T3: Controller elects Broker 2 (from ISR) as NEW LEADER (Epoch = 2)
T4: Producer receives NOT_LEADER_OR_FOLLOWER, fetches fresh metadata
T5: Producer resumes sending to Broker 2 seamlessly!
```

## Build it
See [leader_failover_lab.py](../code/leader_failover_lab.py).
We run a continuous producer loop while killing the active leader container.

## Use Kafka
Execute leader failover against the 3-broker KRaft cluster.

## Inspect it
Observe consumer and producer recovery in console output.

## Measure it
Measure total downtime window (in milliseconds) from leader kill to successful write on the new leader.

## Break it
Kill the leader broker container using `docker stop kafka-node-1`.

## Recover it
Observe the client retry and reconnect to `kafka-node-2` without dropping records.

## Modify it
Restart the old leader container (`docker start kafka-node-1`) and observe it rejoin as a Follower.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What prevents a split-brain scenario where two brokers both believe they are the leader for Partition 0?
2. What role does `leader.epoch` play in log reconciliation?

## Guarantees
* Failover elects a replica that is guaranteed to have all committed records up to the High Watermark.

## Non-guarantees
* In-flight requests during the exact moment of leader death may fail if client retries are disabled (`retries=0`).

## When to use this
* Disaster recovery planning and high availability verification.

## When not to use this
* Avoid manual broker restarts during peak production traffic without graceful shutdown (`SIGTERM` allows clean leadership transfer).

## What comes next
In Phase 23, we explore `min.insync.replicas` and examine how it prevents data loss during cascading broker failures.
"""

p22_code = {
    "leader_failover_lab.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def run_resilient_producer():
    print("Starting resilient producer with retries enabled...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"],
        acks="all",
        retries=10,
        retry_backoff_ms=200
    )
    topic = "failover-orders"
    print("Continuously publishing records. Kill a broker to observe failover...")
    for i in range(1, 21):
        try:
            future = producer.send(topic, key=b"k1", value=f"msg-{i}".encode())
            meta = future.get(timeout=10)
            print(f" [Sent] Msg {i:2d} -> Partition {meta.partition} on Broker {meta.offset}")
            time.sleep(0.3)
        except Exception as e:
            print(f" [RETRYING] Exception during send: {e}")
            time.sleep(0.5)

    producer.close()
    print("Producer finished successfully.")

if __name__ == "__main__":
    run_resilient_producer()
"""
}

p22_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 22 Experiment: Demonstrating Resilient Leader Failover ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/leader_failover_lab.py
"""

p22_evidence = """# Phase 22 Evidence Log

* **Date:**
* **Killed Broker ID:**
* **New Leader Broker ID:**
* **Failover Interruption Time (ms):**
* **Did the producer lose any records?**
"""

write_phase("22-leader-failure", p22_doc, p22_code, p22_exp, p22_evidence)

# ==============================================================================
# PHASE 23: min.insync.replicas
# ==============================================================================
p23_doc = """# Lesson 23: min.insync.replicas

## Motto
"acks=all without min.insync.replicas is an illusion of safety."

## Problem
You configure your producer with `acks=all`, believing your writes are replicated across multiple machines.
However, unknown to you, Broker 2 and Broker 3 died earlier today.
The topic's ISR shrank to just `[Broker 1]`.
When your producer sends with `acks=all`, the leader (Broker 1) checks the current ISR, sees that 100% of the ISR (which is just itself!) has written the record, and returns **SUCCESS**!
One minute later, Broker 1 crashes.
**All those records are permanently lost!**
How do we stop Kafka from accepting writes when the cluster has degraded below safe replication limits?

## Prediction
If a topic has `replication.factor=3` and `min.insync.replicas=2`, what happens to writes sent with `acks=all` if two brokers die?

## Why this matters
**The combination of `acks=all` AND `min.insync.replicas=2` is the industry gold standard for zero data loss.**
It instructs Kafka: "If at least 2 replicas cannot acknowledge this write, REFUSE IT rather than risking data loss."

## First principles
* **`min.insync.replicas`:** The minimum number of replicas in the ISR that must acknowledge a produce request when `acks=all`.
* If $\\text{Current ISR Size} < \\text{min.insync.replicas}$, the leader immediately rejects the write with:
  `NotEnoughReplicasException` or `NotEnoughReplicasAfterAppendException`.

## Mental model
```text
Configuration: replication.factor = 3, min.insync.replicas = 2, acks = all

Scenario 1: 3 Brokers Online (ISR = [1, 2, 3])
Writes succeed! (3 >= 2)

Scenario 2: Broker 3 Dies (ISR = [1, 2])
Writes succeed! (2 >= 2) - Cluster is degraded but safe!

Scenario 3: Broker 2 Also Dies (ISR = [1])
Writes REJECTED with NotEnoughReplicasException! (1 < 2)
Kafka chooses AVAILABILITY DOWNTIME over PERMANENT DATA LOSS!
```

## Build it
See [min_isr_lab.py](../code/min_isr_lab.py).
We test produce behavior when ISR size drops below `min.insync.replicas`.

## Use Kafka
Set `min.insync.replicas=2` on a topic:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --alter --entity-type topics --entity-name durable-topic \
  --add-config min.insync.replicas=2
```

## Inspect it
Check topic configuration using `kafka-configs.sh --describe`.

## Measure it
Observe producer exception metrics when replicas are killed.

## Break it
Stop 2 brokers in the cluster and send a write with `acks=all`. Observe the `NotEnoughReplicasException`.

## Recover it
Restart one broker; as soon as it rejoins the ISR, writes succeed again!

## Modify it
Test sending with `acks=1` while ISR size is below `min.insync.replicas` and observe that `acks=1` dangerously ignores `min.insync.replicas`!

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does `acks=1` bypass `min.insync.replicas` enforcement?
2. In a 3-broker cluster, why should `min.insync.replicas` be set to 2 rather than 3? (Hint: what happens if 1 broker goes down for maintenance?).

## Guarantees
* When `acks=all`, Kafka guarantees records are acknowledged by at least `min.insync.replicas` before returning success.

## Non-guarantees
* `min.insync.replicas` provides zero protection if producers send with `acks=1` or `acks=0`.

## When to use this
* In all mission-critical, zero-data-loss topics.

## When not to use this
* Never set `min.insync.replicas = replication.factor` in production, because losing even a single node for rolling updates halts all cluster writes.

## What comes next
In Phase 24, we explore KRaft architecture and understand how Kafka coordinates cluster metadata without ZooKeeper.
"""

p23_code = {
    "min_isr_lab.py": """#!/usr/bin/env python3
from kafka import KafkaProducer
from kafka.errors import NotEnoughReplicasError, KafkaError

def test_min_isr_write(topic="durable-topic"):
    print(f"Testing produce write with acks='all' to topic '{topic}'...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"],
        acks="all",
        request_timeout_ms=3000
    )
    try:
        f = producer.send(topic, value=b"critical-financial-event")
        meta = f.get(timeout=4)
        print(f" [SUCCESS] Write accepted! Offset {meta.offset} on partition {meta.partition}")
    except NotEnoughReplicasError:
        print(" [REJECTED] NotEnoughReplicasError: Current ISR size is below min.insync.replicas!")
    except KafkaError as e:
        print(f" [ERROR] Kafka error: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    test_min_isr_write()
"""
}

p23_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 23 Experiment: Testing min.insync.replicas Enforcement ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/min_isr_lab.py
"""

p23_evidence = """# Phase 23 Evidence Log

* **Date:**
* **Configured min.insync.replicas:** 2
* **Outcome with 3 brokers online:**
* **Outcome with 1 broker online (2 dead):**
* **Observed Exception:**
* **Mastery Rule:**
"""

write_phase("23-min-insync-replicas", p23_doc, p23_code, p23_exp, p23_evidence)

# ==============================================================================
# PHASE 24: KRaft and Cluster Metadata
# ==============================================================================
p24_doc = """# Lesson 24: KRaft and Cluster Metadata

## Motto
"Kafka now uses Kafka to manage Kafka."

## Problem
In early Kafka architectures (v0.8 to v2.8), Kafka relied on an external Apache ZooKeeper cluster to store topic metadata, partition leadership, and broker registrations.
This caused major architectural headaches:
1. **Dual System Overhead:** Operating two distinct distributed systems (ZooKeeper + Kafka) with separate configurations, security, and failure modes.
2. **Metadata Desync:** Controllers had to synchronize state from ZooKeeper into broker memory, creating multi-minute recovery delays during restarts.
3. **Partition Scalability Limits:** ZooKeeper struggled past 200,000 partitions.
How does modern Kafka manage its own cluster metadata natively?

## Prediction
Where is cluster metadata stored in a modern KRaft (Kafka Raft) cluster?

## Why this matters
KRaft (KIP-500) is the modern foundation of Apache Kafka. ZooKeeper is deprecated and removed. Understanding KRaft controllers and the `@metadata` partition is essential for modern cluster operations.

## First principles
* **KRaft Quorum:** Selected brokers act as KRaft Controllers. They run an event-driven Raft consensus algorithm.
* **The Metadata Log (`@metadata-0`):** All cluster metadata changes (topic creation, partition reassignment, broker registration) are appended as records to an internal Raft log.
* **Instantaneous Failover:** Because controllers replicate the metadata log continuously, when the active controller leader dies, a standby controller takes over in milliseconds.

## Mental model
```text
Legacy Architecture (ZooKeeper - DEPRECATED)
[ ZooKeeper Ensemble ] ◄── Watchers ──► [ Kafka Controller ] ──RPC──► [ Brokers ]
(Dual clusters, slow state loading, double operational complexity)

Modern Architecture: KRaft Mode (Apache Kafka 3.8.0)
┌────────────────────────────────────────────────────────┐
│ KRaft Controller Quorum (Raft Consensus)               │
│ Controller 1 (Leader) ◄── Raft ──► Controller 2 / 3    │
│   └── Replicates internal log: @metadata-0             │
└────────────────────────────────────────────────────────┘
                           │
       Direct Metadata Push (Sub-second convergence)
                           ▼
┌────────────────────────────────────────────────────────┐
│ Broker Data Plane (Partitions & Storage)               │
│ Broker 1               Broker 2               Broker 3 │
└────────────────────────────────────────────────────────┘
```

## Build it
See [kraft_metadata_explorer.py](../code/kraft_metadata_explorer.py).
We inspect the KRaft metadata state and controller identity.

## Use Kafka
Run the official KRaft metadata shell tool to inspect the cluster metadata hierarchy:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092
```

## Inspect it
Observe the metadata directory on disk: `/tmp/kraft-combined-logs/__cluster_metadata-0`.

## Measure it
Compare controller failover time in KRaft (< 100ms) vs legacy ZooKeeper (30+ seconds).

## Break it
Check how controllers handle quorum loss (e.g. killing 2 out of 3 controllers in a quorum).

## Recover it
Restore quorum nodes and observe leadership re-election.

## Modify it
Inspect the `meta.properties` file in Kafka's log directory and find the `cluster.id`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is KRaft described as "Kafka using Kafka to manage Kafka"?
2. What happens to Kafka cluster operations if the KRaft controller quorum loses majority?

## Guarantees
* All committed cluster metadata changes are strictly ordered and replicated via Raft.

## Non-guarantees
* KRaft does not replicate data plane topic messages; it replicates only control plane metadata.

## When to use this
* In all modern Kafka deployments (Kafka 3.0+).

## When not to use this
* ZooKeeper is legacy and should never be chosen for new architectures.

## What comes next
In Phase 25, we dig beneath the network protocol into Kafka's physical on-disk storage format: Segments and Indexes.
"""

p24_code = {
    "kraft_metadata_explorer.py": """#!/usr/bin/env python3
from kafka import KafkaAdminClient

def check_kraft_info():
    print("Querying KRaft Cluster Metadata...")
    admin = KafkaAdminClient(bootstrap_servers=["localhost:9092"])
    cluster_info = admin.describe_cluster()
    print(f"  Cluster ID:    {cluster_info.get('cluster_id')}")
    print(f"  Controller ID: {cluster_info.get('controller_id')}")
    brokers = cluster_info.get('brokers', [])
    print(f"  Brokers Count: {len(brokers)}")
    for b in brokers:
        print(f"    - Broker ID {b.get('node_id')}: {b.get('host')}:{b.get('port')}")
    admin.close()

if __name__ == "__main__":
    check_kraft_info()
"""
}

p24_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 24 Experiment: Exploring KRaft Cluster Metadata ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/kraft_metadata_explorer.py
"""

p24_evidence = """# Phase 24 Evidence Log

* **Date:**
* **Kafka Engine:** 3.8.0 KRaft
* **Cluster ID:**
* **Active Controller ID:**
* **Why ZooKeeper was eliminated:**
"""

write_phase("24-kraft-and-cluster-metadata", p24_doc, p24_code, p24_exp, p24_evidence)

# ==============================================================================
# PHASE 25: Kafka Storage Model
# ==============================================================================
p25_doc = """# Lesson 25: Kafka Storage Model

## Motto
"A partition is not a file; a partition is a directory of immutable segments and sparse indexes."

## Problem
In Phase 02, our `MiniLog` wrote all events into a single `.dat` file.
In a production Kafka broker processing billions of events, a single file would quickly reach terabytes in size:
* Finding offset 4,500,210 would require scanning gigabytes of bytes from the start of the file ($O(N)$ lookup).
* Deleting old data past retention would require rewriting the entire multi-terabyte file.
How does Kafka store partition data on physical disk so that both appends and random offset lookups are fast ($O(1)$)?

## Prediction
How does Kafka locate a specific record at offset 52,000 without scanning the file from offset 0?

## Why this matters
Understanding Kafka's on-disk storage architecture (.log, .index, .timeindex) explains how Kafka achieves sub-millisecond seek times and zero-cost retention cleanup.

## First principles
* **Partition Directory:** Each topic partition maps to a directory on disk: `<topic>-<partition_id>`.
* **Segment Files:** The log is divided into chunks (segments) named after the segment's base offset (e.g. `00000000000000000000.log`).
* **Offset Index (`.index`):** A memory-mapped, sparse binary index mapping logical offsets to physical byte positions in the `.log` file.
* **Timestamp Index (`.timeindex`):** Maps event timestamps to logical offsets for time-based lookups.

## Mental model
```text
Partition Directory: /tmp/kraft-combined-logs/orders-0/
├── 00000000000000000000.log       <-- Raw binary RecordBatches
├── 00000000000000000000.index     <-- Sparse index: [Offset 400 -> Byte 16384]
├── 00000000000000000000.timeindex <-- Timestamp index: [Time 1790165596 -> Offset 400]
└── leader-epoch-checkpoint        <-- Leader epoch state
```

## Build it
See [inspect_storage_segments.py](../code/inspect_storage_segments.py).
We inspect the binary headers and segment structure of real Kafka logs.

## Use Kafka
Inspect on-disk log files inside the container:
```bash
docker exec -it kafka-lab-single ls -la /tmp/kraft-combined-logs/
```

## Inspect it
Dump the contents of a `.log` segment using `kafka-dump-log.sh`:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-dump-log.sh \
  --files /tmp/kraft-combined-logs/lab-orders-0/00000000000000000000.log \
  --print-data-log
```

## Measure it
Measure file sizes of `.log` vs `.index` files (indexes are tiny fraction of log size due to sparse indexing).

## Break it
Observe what happens if you manually delete an `.index` file; Kafka automatically reconstructs the index from the `.log` file upon restart!

## Recover it
Demonstrate index self-healing on broker restart.

## Modify it
Inspect `leader-epoch-checkpoint` and explain its fields.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka use a *sparse* index (indexing every 4KB of data) rather than a dense index (indexing every record)?
2. How does binary search on the sparse index achieve $O(1)$ offset lookups?

## Guarantees
* Historical segments are immutable and read-only. Only the active segment accepts writes.

## Non-guarantees
* Corrupting the `.log` file directly bypasses Kafka safeguards and requires log truncation.

## When to use this
* Investigating disk storage usage, data corruption, and segment rolling policies.

## When not to use this
* Never edit or modify Kafka `.log` files directly with text editors.

## What comes next
In Phase 26, we explore the mechanical reasons why Kafka achieves blazing speed despite writing to disk.
"""

p25_code = {
    "inspect_storage_segments.py": """#!/usr/bin/env python3
import subprocess
import sys

def inspect_segments():
    print("Inspecting Kafka partition directories inside container...")
    cmd = ["docker", "exec", "kafka-lab-single", "ls", "-la", "/tmp/kraft-combined-logs/"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(res.stdout)
    else:
        print(f"Error inspecting container: {res.stderr}")

if __name__ == "__main__":
    inspect_segments()
"""
}

p25_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 25 Experiment: Inspecting Kafka On-Disk Storage Structure ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/inspect_storage_segments.py
"""

p25_evidence = """# Phase 25 Evidence Log

* **Date:**
* **Log Directory Inspected:**
* **Segment Files Discovered:**
* **Index Files Discovered:**
* **Offset Lookup Mechanism:**
"""

write_phase("25-kafka-storage-model", p25_doc, p25_code, p25_exp, p25_evidence)

# ==============================================================================
# PHASE 26: Why Kafka Can Be Fast on Disk
# ==============================================================================
p26_doc = """# Lesson 26: Why Kafka Can Be Fast on Disk

## Motto
"Disk is not slow; random disk seeking is slow. Sequential disk writes rival memory bus speeds."

## Problem
A pervasive myth in software engineering is:
*"In-memory systems are always fast, and disk-based systems are always slow."*
Based on this belief, many assume Kafka must keep all messages in JVM heap memory.
In reality:
1. Keeping terabytes of messages in JVM heap causes catastrophic Garbage Collection pauses.
2. If the JVM crashes, in-memory caches vanish.
How does Kafka achieve throughput of hundreds of thousands of messages per second while writing every byte to disk?

## Prediction
Is sequential disk write faster or slower than random memory access with cache misses?

## Why this matters
Understanding the mechanical sympathy of **Sequential I/O**, the **OS Page Cache**, and **Zero-Copy Transfers** replaces cargo-cult assumptions with accurate hardware mental models.

## First principles
* **Sequential vs. Random Disk I/O:** Sequential disk writes avoid seek latencies, reaching 500+ MB/s on HDDs and several GB/s on NVMe SSDs.
* **The OS Page Cache:** All disk read/write calls go through the Linux kernel page cache. If producers write and consumers read within a short time, records are read directly from RAM without touching physical disk platters!
* **Zero-Copy (`sendfile`):** Kafka uses the `sendfile()` system call to transfer bytes directly from kernel page cache to network interface card (NIC) buffers without copying bytes into JVM user space.

## Mental model
```text
Traditional Server (4 Copies, 4 Context Switches):
Disk ──(DMA)──► Page Cache ──(CPU Copy)──► JVM Memory ──(CPU Copy)──► Socket Buffer ──(DMA)──► NIC Wire

Kafka Zero-Copy via sendfile() (2 Copies, 2 Context Switches):
Disk ──(DMA)──► OS Page Cache ────────────(DMA Direct Transfer)────────────► NIC Network Wire
                      ▲
             (CPU never touches bytes!)
```

## Build it
See [sequential_vs_random_io.py](../code/sequential_vs_random_io.py).
We benchmark random disk writes vs sequential append writes on your local drive.

## Use Kafka
Observe Kafka's minimal JVM heap configuration (typically 4GB to 6GB) even while managing multi-terabyte brokers, because the OS Page Cache handles the data.

## Inspect it
Check page cache utilization on Linux/macOS using OS diagnostic tools (`vm_stat` or `free -m`).

## Measure it
Compare write throughput of 50,000 random seeks vs 50,000 sequential appends.

## Break it
Simulate random access patterns by issuing non-sequential reads across old segments.

## Recover it
Keep consumers caught up near the tail of the log where records reside in hot page cache.

## Modify it
Tune OS read-ahead settings (`read_ahead_kb`) to optimize sequential pre-fetching.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does keeping data in the OS page cache prevent JVM garbage collection pauses?
2. What happens to read latency when a consumer falls behind by 48 hours and has to fetch data evicted from the OS page cache?

## Guarantees
* Sequential appends maximize hardware throughput across both rotational HDDs and SSDs.

## Non-guarantees
* When consumers read cold data not in page cache, physical disk read latency is incurred.

## When to use this
* High-throughput event streaming where producers and consumers operate near real-time.

## When not to use this
* Workloads requiring frequent random-access mutations across historical data.

## What comes next
In Phase 27, we explore Segment Rolling and see how Kafka transitions from one active log file to the next.
"""

p26_code = {
    "sequential_vs_random_io.py": """#!/usr/bin/env python3
import time
import os
import random

def bench_io(total_writes=20000, record_size=128):
    payload = b"X" * record_size
    seq_path = "/tmp/bench_seq.dat"
    rand_path = "/tmp/bench_rand.dat"
    
    # 1. Sequential Appends
    start = time.time()
    with open(seq_path, "wb") as f:
        for _ in range(total_writes):
            f.write(payload)
    seq_dur = time.time() - start
    
    # 2. Random Seeks & Writes
    # Pre-allocate file
    with open(rand_path, "wb") as f:
        f.write(b"\\0" * (total_writes * record_size))
        
    start = time.time()
    with open(rand_path, "r+b") as f:
        positions = list(range(total_writes))
        random.shuffle(positions)
        for pos in positions:
            f.seek(pos * record_size)
            f.write(payload)
    rand_dur = time.time() - start

    if os.path.exists(seq_path): os.remove(seq_path)
    if os.path.exists(rand_path): os.remove(rand_path)

    print(f"Sequential Appends: {total_writes/seq_dur:9.1f} writes/s ({seq_dur:.3f} s)")
    print(f"Random Seeks:       {total_writes/rand_dur:9.1f} writes/s ({rand_dur:.3f} s)")
    print(f"Sequential Advantage: {rand_dur/seq_dur:.1f}x faster!")

if __name__ == "__main__":
    bench_io()
"""
}

p26_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 26 Experiment: Benchmarking Sequential vs Random Disk I/O ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/sequential_vs_random_io.py
"""

p26_evidence = """# Phase 26 Evidence Log

* **Date:**
* **Sequential Write Throughput (writes/s):**
* **Random Write Throughput (writes/s):**
* **Performance Difference Factor:**
* **Role of OS Page Cache:**
"""

write_phase("26-why-kafka-can-be-fast-on-disk", p26_doc, p26_code, p26_exp, p26_evidence)

# ==============================================================================
# PHASE 27: Segment Rolling
# ==============================================================================
p27_doc = """# Lesson 27: Segment Rolling

## Motto
"Close the old segment, seal it immutable, and open the new."

## Problem
A single partition log cannot grow as one infinite file.
If it did:
* Log compaction would have to scan the entire historical universe.
* Old data could not be pruned by retention without rewriting the file.
How does Kafka slice an infinite stream of records into manageable, immutable files on disk?

## Prediction
When an active segment file reaches its configured size limit (`segment.bytes`), what does Kafka do with the current `.log` file and the next incoming write?

## Why this matters
**Segment Rolling is the mechanism that transitions data from mutable append state to immutable historical storage.**
Understanding segment roll triggers (`segment.bytes` and `segment.ms`) is critical for log compaction and retention policies.

## First principles
* **Active Segment:** The single segment currently receiving appends.
* **Rolling Triggers:**
  * Size threshold reached: `segment.bytes` (default: 1 GB).
  * Time threshold reached: `segment.ms` (default: 7 days).
  * Index threshold reached: `segment.index.bytes` (default: 10 MB).
* When a roll occurs, the current segment is flushed and sealed read-only. A new active segment is created named after the next offset.

## Mental model
```text
Step 1: Active Segment (0000.log) reaches 10 KB limit
Step 2: Roll triggered!
        - 00000000000000000000.log SEALED IMMUTABLE
        - 00000000000000000000.index SEALED IMMUTABLE
Step 3: New Active Segment opened:
        - 00000000000000000150.log (Base offset: 150)
```

## Build it
See [segment_rolling_lab.py](../code/segment_rolling_lab.py).
We configure a topic with a tiny `segment.bytes=10240` (10 KB) and produce records to trigger segment rolls.

## Use Kafka
Create a topic with a 10KB segment limit:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic rolling-lab \
  --partitions 1 --replication-factor 1 \
  --config segment.bytes=10240
```

## Inspect it
List the partition directory inside the container and observe multiple `.log` and `.index` segment pairs:
```bash
docker exec -it kafka-lab-single ls -la /tmp/kraft-combined-logs/rolling-lab-0/
```

## Measure it
Measure the exact byte size of sealed segments.

## Break it
Configure `segment.bytes` excessively small (e.g. 100 bytes) and observe the broker create thousands of tiny file descriptors, exhausting OS limits!

## Recover it
Restore sensible segment sizes (typically 100MB to 1GB in production).

## Modify it
Test time-based segment rolling using `segment.ms`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why are historical (non-active) segment files immutable?
2. What naming convention does Kafka use for segment files, and why?

## Guarantees
* Sealed segments are guaranteed to never be modified by incoming producer appends.

## Non-guarantees
* Segment rolls do not happen at exact byte boundaries; Kafka rolls when the current batch exceeds the limit.

## When to use this
* Sizing segment files for log compaction and retention tuning.

## When not to use this
* Never configure microscopic segment sizes in production.

## What comes next
In Phase 28, we explore Retention policies and learn how Kafka safely purges expired segments.
"""

p27_code = {
    "segment_rolling_lab.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def trigger_segment_rolls(topic="rolling-lab", num_records=300):
    print(f"Producing {num_records} records to '{topic}' to trigger segment rolls...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        linger_ms=0 # Send immediately
    )
    # 256 bytes payload
    payload = b"A" * 256
    for i in range(num_records):
        producer.send(topic, value=payload)
    producer.flush()
    producer.close()
    print("Finished producing. Check container filesystem for multiple segment files!")

if __name__ == "__main__":
    trigger_segment_rolls()
"""
}

p27_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 27 Experiment: Triggering and Observing Segment Rolling ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/segment_rolling_lab.py
"""

p27_evidence = """# Phase 27 Evidence Log

* **Date:**
* **Topic:** rolling-lab
* **Configured segment.bytes:** 10240 (10 KB)
* **Number of Segment Files Created:**
* **Base Offsets of Created Segments:**
"""

write_phase("27-segment-rolling", p27_doc, p27_code, p27_exp, p27_evidence)

# ==============================================================================
# PHASE 28: Retention
# ==============================================================================
p28_doc = """# Lesson 28: Retention

## Motto
"Consumers read; retention deletes. The two mechanisms are completely independent."

## Problem
In a message queue (e.g. RabbitMQ or SQS), once a consumer reads and acknowledges a message, the broker destructively deletes it.
In Kafka:
* 10 different consumer groups can read the same records.
* Consumers can crash, restart, and replay records from 3 days ago.
If reading does not delete records, how does Kafka prevent disk storage from filling up and halting the cluster?

## Prediction
If a consumer has NOT yet read record at offset 50, but that record's segment exceeds the retention time limit, will Kafka delete the segment anyway?

## Why this matters
**Kafka decouples consumption from deletion.** Retention is governed strictly by time or storage size, completely independent of consumer positions. If a consumer lags beyond the retention window, it will lose data!

## First principles
* **Time-based Retention:** `retention.ms` or `log.retention.hours` (default: 7 days). Segments whose newest timestamp is older than this threshold are deleted.
* **Size-based Retention:** `retention.bytes` or `log.retention.bytes`. Total bytes per partition.
* **Segment-Level Deletion:** Kafka does *not* delete individual records. It deletes entire sealed segment files during background cleaner runs.
* **Active Segment Immunity:** The active segment is NEVER deleted, even if it exceeds retention limits.

## Mental model
```text
Partition Directory:
Segment 1 (0000.log) [Age: 10 days] ──► ELIGIBLE FOR DELETION! (Background thread deletes file)
Segment 2 (1000.log) [Age: 3 days]  ──► RETAINED (Within 7-day retention)
Segment 3 (2000.log) [Active]        ──► IMMUNE TO DELETION (Currently accepting writes)
```

## Build it
See [retention_lab.py](../code/retention_lab.py).
We configure a topic with a 5-second retention window and observe background segment deletion.

## Use Kafka
Set aggressive retention on a topic:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic retention-lab \
  --partitions 1 --replication-factor 1 \
  --config segment.bytes=10240 \
  --config retention.ms=5000
```

## Inspect it
Watch sealed segments disappear from the filesystem after 5 seconds while the active segment remains.

## Measure it
Measure reclaimed disk space after segment deletion.

## Break it
Simulate a slow consumer that falls behind retention; observe the consumer throw `OffsetOutOfRangeException`.

## Recover it
Handle `OffsetOutOfRangeException` by resetting consumer offset to `earliest`.

## Modify it
Configure size-based retention (`retention.bytes`) and verify behavior.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka delete entire segments rather than deleting individual expired records from within a file?
2. What is the operational risk if consumer lag exceeds topic retention time?

## Guarantees
* Data is retained up to the configured time or size boundary.

## Non-guarantees
* Kafka does not guarantee lagging consumers will finish reading before retention purges data.

## When to use this
* In all Kafka topics to bound disk consumption.

## When not to use this
* Do not set retention shorter than the maximum expected consumer recovery SLA.

## What comes next
In Phase 29, we examine Log Compaction: retaining the latest value per key rather than deleting by age.
"""

p28_code = {
    "retention_lab.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def test_retention():
    topic = "retention-lab"
    print(f"Producing records to topic '{topic}' with 5s retention...")
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    for i in range(200):
        producer.send(topic, value=b"data-to-be-retained-then-deleted")
    producer.flush()
    producer.close()
    print("Produced 200 records. Wait 10 seconds and check segment deletion inside container.")

if __name__ == "__main__":
    test_retention()
"""
}

p28_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 28 Experiment: Demonstrating Time-Based Log Retention ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/retention_lab.py
"""

p28_evidence = """# Phase 28 Evidence Log

* **Date:**
* **Topic:** retention-lab
* **Configured retention.ms:** 5000 (5s)
* **Did old sealed segments get deleted?**
* **Was the active segment deleted?**
* **Consumer consequence if lag > retention:**
"""

write_phase("28-retention", p28_doc, p28_code, p28_exp, p28_evidence)

# ==============================================================================
# PHASE 29: Log Compaction
# ==============================================================================
p29_doc = """# Lesson 29: Log Compaction

## Motto
"Time-based retention forgets history; log compaction remembers the latest truth."

## Problem
Consider a topic storing user profile states:
```text
Offset 0: key="user:1", val="Alice, Seattle"
Offset 1: key="user:2", val="Bob, New York"
Offset 2: key="user:1", val="Alice, Chicago"  <-- Update!
Offset 3: key="user:1", val="Alice, London"   <-- Update!
```
If we use standard time retention (e.g. 7 days), after 7 days Bob and Alice's profile states are completely deleted!
If we retain forever, the log grows infinitely with obsolete historical updates ("Seattle", "Chicago").
What if we only care about the **latest value for each key**?

## Prediction
If you write 5 updates for key `user:1` to a compacted topic, what will remain in the log after the cleaner thread runs?

## Why this matters
**Log Compaction transforms Kafka into a durable, key-addressable state store.**
It powers database CDC changelogs, KTable state stores in Kafka Streams, and disaster recovery caches.

## First principles
* **`cleanup.policy=compact`:** Kafka's log cleaner thread scans sealed segments and discards older records whose keys have newer values later in the log.
* **Tombstone Records:** To delete a key entirely in a compacted topic, the producer sends a record with the key and a `null` value. The cleaner removes all historical records and eventually purges the tombstone after `delete.retention.ms`.
* **Offset Preservation:** Compaction never changes record offsets. Offsets remain monotonically increasing, but non-contiguous (e.g. offsets 0, 1, 3).

## Mental model
```text
Before Compaction:
[ k1:v1 (off 0) | k2:v1 (off 1) | k1:v2 (off 2) | k1:v3 (off 3) | k2:null (off 4, tombstone) ]

After Compaction (Cleaner runs):
[ k2:v1 (off 1) | k1:v3 (off 3) ]   <-- k1:v1 and k1:v2 discarded! Offsets 1, 3 preserved!
```

## Build it
See [log_compaction_lab.py](../code/log_compaction_lab.py).
We produce multiple state updates and a tombstone to observe log compaction.

## Use Kafka
Create a compacted topic:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create --topic compacted-users \
  --partitions 1 --replication-factor 1 \
  --config cleanup.policy=compact \
  --config segment.bytes=10240 \
  --config min.cleanable.dirty.ratio=0.01
```

## Inspect it
Read the topic using `kafka-console-consumer.sh` from the beginning to see state deduplication.

## Measure it
Measure storage reduction percentage before vs after compaction.

## Break it
Send updates with a `null` key on a compacted topic; observe that unkeyed records cannot be compacted!

## Recover it
Ensure all records destined for compacted topics carry explicit entity keys.

## Modify it
Send a tombstone (`value=None`) and observe key removal after deletion retention expires.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does log compaction never compact records currently residing in the active segment?
2. Why do offsets in a compacted partition become non-contiguous (e.g. jumping from 0 to 4)?

## Guarantees
* At least the last known value for each key is guaranteed to be retained indefinitely.

## Non-guarantees
* Compaction is not instantaneous; duplicates remain until the background log cleaner thread executes.

## When to use this
* Database changelogs (CDC), reference data caches, account balances, user profiles.

## When not to use this
* Immutable event series where every historical occurrence matters (e.g. audit logs, clickstreams).

## What comes next
In Phase 30, we study Replay: resetting consumer offsets to reconstruct state or recover from software bugs.
"""

p29_code = {
    "log_compaction_lab.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def test_compaction():
    topic = "compacted-users"
    print(f"Producing state updates to compacted topic '{topic}'...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: v.encode("utf-8") if v is not None else None
    )

    # User 1 updates
    producer.send(topic, key="user-1", value="Alice v1 (Seattle)")
    producer.send(topic, key="user-2", value="Bob v1 (New York)")
    producer.send(topic, key="user-1", value="Alice v2 (Chicago)")
    producer.send(topic, key="user-1", value="Alice v3 (London)")
    
    # Tombstone for User 2 (delete marker)
    producer.send(topic, key="user-2", value=None)

    producer.flush()
    producer.close()
    print("Produced state updates + tombstone.")

if __name__ == "__main__":
    test_compaction()
"""
}

p29_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 29 Experiment: Demonstrating Log Compaction and Tombstones ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/log_compaction_lab.py
"""

p29_evidence = """# Phase 29 Evidence Log

* **Date:**
* **Topic:** compacted-users
* **Initial State Writes:** 5
* **Tombstone Key:** user-2
* **Final Value for user-1:**
* **Why offsets are non-contiguous after compaction:**
"""

write_phase("29-log-compaction", p29_doc, p29_code, p29_exp, p29_evidence)

# ==============================================================================
# PHASE 30: Replay
# ==============================================================================
p30_doc = """# Lesson 30: Replay

## Motto
"The superpower of an immutable log is the ability to travel backward in time."

## Problem
Your team deploys a critical bug in the payment reconciliation service at 9:00 AM.
For 4 hours, it miscalculated foreign exchange conversions on 100,000 transactions.
At 1:00 PM, the bug is identified and fixed.
In a traditional queue or direct HTTP architecture, those 100,000 requests are gone forever; recovering requires manual database surgery.
In Kafka:
* The 100,000 original events are still sitting immutably in the log!
How do you rewind the consumer group and recalculate the state correctly?

## Prediction
What happens to consumer group offset tracking when you execute `kafka-consumer-groups.sh --reset-offsets --to-earliest`?

## Why this matters
**Historical replay is Kafka's defining operational advantage over traditional message brokers.**
It enables zero-downtime state reconstruction, bug recovery, analytics backfills, and database re-indexing.

## First principles
* **Offset Rewind:** A consumer group's position in `__consumer_offsets` is simply an integer pointer. Resetting it to 0 instructs Kafka to re-serve historical records from the beginning.
* **Deterministic Event Sourcing:** If events are immutable, replaying them through deterministic logic recreates the exact state.
* **The Dangers of Replay:** Replaying events that trigger *external side effects* (e.g. sending real emails or charging Stripe credit cards) will duplicate real-world actions unless guarded by idempotency!

## Mental model
```text
T0: Buggy Consumer processes offsets 0 -> 1000 (Saved incorrect state)
T1: Fix deployed to consumer application
T2: Execute Offset Reset: Reset Group "reconcile-svc" offset -> 0
T3: Consumer restarts, re-reads offsets 0 -> 1000 from log
Result: Clean, 100% accurate recalculated state!
```

## Build it
See [replay_lab.py](../code/replay_lab.py).
We process events into a bank balance, simulate a corrupting calculation bug, reset offsets, and rebuild the correct balance from scratch.

## Use Kafka
Reset a consumer group's offset using official CLI:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group bank-reconciliation-group \
  --reset-offsets --to-earliest \
  --topic bank-txns \
  --execute
```

## Inspect it
Observe `CURRENT-OFFSET` reset to 0 in `kafka-consumer-groups.sh --describe`.

## Measure it
Measure replay processing throughput (typically 10x-50x faster than real-time because records are pre-buffered).

## Break it
Replay a topic into a non-idempotent notification service and watch users receive duplicate push notifications!

## Recover it
Always isolate replay environments or guard side-effecting external adapters with idempotency keys.

## Modify it
Reset offsets to a specific timestamp (`--to-datetime 2026-09-23T10:00:00.000`) rather than the earliest offset.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does replay require downstream consumers to be idempotent?
2. How does log retention limit how far back in time a consumer can replay?

## Guarantees
* Kafka serves historical records in the exact original sequence stored in each partition.

## Non-guarantees
* Kafka cannot replay records that have already been purged by retention or compaction.

## When to use this
* Rebuilding read-model caches, fixing software bugs, training machine learning models, audit compliance.

## When not to use this
* Uncontrolled replays directly against non-idempotent third-party APIs.

## What comes next
In Phase 31, we enter Module 7 and study Consumer Lag and Backpressure mechanics.
"""

p30_code = {
    "replay_lab.py": """#!/usr/bin/env python3
class BankAccountProjection:
    def __init__(self):
        self.balance = 0.0

    def apply_event(self, event_type: str, amount: float, buggy=False):
        if buggy:
            # Buggy logic applied 10x multiplier accidentally!
            amount = amount * 10
        if event_type == "DEPOSIT":
            self.balance += amount
        elif event_type == "WITHDRAWAL":
            self.balance -= amount

if __name__ == "__main__":
    events = [
        ("DEPOSIT", 100.0),
        ("DEPOSIT", 50.0),
        ("WITHDRAWAL", 30.0),
        ("DEPOSIT", 20.0),
    ]
    # Expected: 100 + 50 - 30 + 20 = 140.0

    print("--- 1. Initial Run with Buggy Logic ---")
    buggy_proj = BankAccountProjection()
    for etype, amt in events:
        buggy_proj.apply_event(etype, amt, buggy=True)
    print(f" Corrupted Account Balance: ${buggy_proj.balance:.2f} (WRONG!)")

    print("\\n--- 2. Rewinding Offset to 0 & Replaying with Fixed Logic ---")
    fixed_proj = BankAccountProjection()
    for etype, amt in events:
        fixed_proj.apply_event(etype, amt, buggy=False)
    print(f" Correct Restored Balance: ${fixed_proj.balance:.2f} (ACCURATE!)")
"""
}

p30_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 30 Experiment: Simulating Event Replay and State Recovery ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/replay_lab.py
"""

p30_evidence = """# Phase 30 Evidence Log

* **Date:**
* **Corrupted State Balance:**
* **Restored State Balance:**
* **Commands to Reset Offsets:**
* **Dangers of Replaying External Side Effects:**
"""

write_phase("30-replay", p30_doc, p30_code, p30_exp, p30_evidence)

print("Phases 16 to 30 successfully generated!")
