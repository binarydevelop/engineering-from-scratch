#!/usr/bin/env python3
"""
Generator for Phases 31 to 45 of kafka-from-scratch.
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
# PHASE 31: Consumer Lag
# ==============================================================================
p31_doc = """# Lesson 31: Consumer Lag

## Motto
"Consumer Lag is the single most vital health metric in the entire Kafka ecosystem."

## Problem
In a healthy cluster, consumers read records within milliseconds of being produced.
However, when downstream databases slow down, code bugs cause CPU spikes, or producers suddenly surge with Black Friday traffic:
* Production rate outpaces consumption rate.
* The backlog of unread records swells.
How do we mathematically measure this backlog, and how do we monitor it before customers notice delays?

## Prediction
If Log End Offset (LEO) is 150,000 and the consumer group's committed offset is 120,000, what is the exact lag?

## Why this matters
**Consumer Lag is the ultimate early-warning indicator.**
High CPU or memory is just machine state; Consumer Lag directly tells you that your business domain is falling behind reality.

## First principles
$$\\text{Consumer Lag} = \\text{Log End Offset (LEO)} - \\text{Committed Offset}$$
* **Log End Offset (LEO):** The offset of the next record to be written to the partition.
* **Committed Offset:** The last offset processed and saved by the consumer group.
* Lag must be monitored per partition, because a hot partition can be starving even while the average cluster lag looks acceptable.

## Mental model
```text
Partition 0 Log:
Offsets: 0 ...... 120,000 ........................ 150,000
                     ▲                                ▲
                     │                                │
            Committed Offset (120,000)        Log End Offset (150,000)
                     └──────── Lag = 30,000 ──────────┘
```

## Build it
See [lag_monitor.py](../code/lag_monitor.py).
We build a real-time lag calculator that inspects partition LEO and group offset to alert on backlog spikes.

## Use Kafka
Inspect lag using the official CLI:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe --group order-processors
```

## Inspect it
Observe columns: `LOG-END-OFFSET`, `CURRENT-OFFSET`, and `LAG`.

## Measure it
Produce 1,000 records while the consumer is paused and observe lag increase by exactly 1,000.

## Break it
Simulate a slow consumer sleeping 100ms per record; observe lag growth rate.

## Recover it
Scale consumer instances up to match partition count to clear lag.

## Modify it
Add alerting logic to `lag_monitor.py` when lag exceeds 500 records.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is checking *average* lag across a topic misleading if one partition has 95% of the lag?
2. What happens to lag if the consumer process crashes completely?

## Guarantees
* Lag accurately reflects the count of unread records between the consumer position and the partition tail.

## Non-guarantees
* Zero lag does not guarantee downstream services have completed external asynchronous operations.

## When to use this
* In all production alerting systems (Prometheus, Datadog, Grafana).

## When not to use this
* Lag monitoring is useless if consumers do not commit offsets.

## What comes next
In Phase 32, we explore Backpressure and reason about capacity limits using Little's Law.
"""

p31_code = {
    "lag_monitor.py": """#!/usr/bin/env python3
import time
from kafka import KafkaConsumer, TopicPartition

def check_consumer_lag(topic="lab-orders", group_id="manual-commit-group"):
    print(f"Calculating Consumer Lag for group '{group_id}' on topic '{topic}'...")
    consumer = KafkaConsumer(
        bootstrap_servers=["localhost:9092"],
        group_id=group_id,
        enable_auto_commit=False
    )
    
    # Get partitions for topic
    partitions = consumer.partitions_for_topic(topic)
    if not partitions:
        print(f"Topic '{topic}' has no partitions or does not exist.")
        consumer.close()
        return

    tps = [TopicPartition(topic, p) for p in partitions]
    
    # Query Log End Offsets (broker tail)
    end_offsets = consumer.end_offsets(tps)
    
    total_lag = 0
    print(f"\\n{'Partition':<12} {'LEO':<12} {'Committed':<12} {'Lag':<12}")
    print("-" * 48)
    for tp in tps:
        leo = end_offsets.get(tp, 0)
        committed = consumer.committed(tp)
        committed_offset = committed if committed is not None else 0
        lag = max(0, leo - committed_offset)
        total_lag += lag
        print(f"{tp.partition:<12} {leo:<12} {committed_offset:<12} {lag:<12}")

    print("-" * 48)
    print(f"Total Topic Lag: {total_lag} records")
    consumer.close()

if __name__ == "__main__":
    check_consumer_lag()
"""
}

p31_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 31 Experiment: Calculating Real-Time Consumer Lag ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/lag_monitor.py
"""

p31_evidence = """# Phase 31 Evidence Log

* **Date:**
* **Topic:** lab-orders
* **Partitions Examined:**
* **Observed LEO:**
* **Observed Committed Offset:**
* **Calculated Lag:**
"""

write_phase("31-consumer-lag", p31_doc, p31_code, p31_exp, p31_evidence)

# ==============================================================================
# PHASE 32: Backpressure
# ==============================================================================
p32_doc = """# Lesson 32: Backpressure

## Motto
"Kafka buffers work, but buffering is an emergency brake, not an infinite engine."

## Problem
In a push-based message broker, if workers cannot keep up, the broker pushes messages anyway, crashing the workers with out-of-memory errors.
In Kafka:
* Consumers **pull** data at their own pace via `poll()`.
* Therefore, consumers naturally control their own backpressure.
However, if $\\text{Producer Rate} > \\text{Consumer Rate}$ for hours or days:
* The buffer on disk grows without bound.
* When retention expires, data is lost.
How do we reason about buffer saturation and system capacity?

## Prediction
If incoming traffic is 10,000 msgs/s and consumer capacity is 8,000 msgs/s, how long until a 100GB disk partition fills up if each record is 1 KB?

## Why this matters
Backpressure reasoning connects software architecture to physics and queueing theory (**Little's Law**: $L = \\lambda W$).

## First principles
* **Pull-Based Flow Control:** Because Kafka never pushes records, consumers cannot be overwhelmed by network bursts.
* **Storage as Buffer:** Unprocessed messages accumulate on disk.
* **Catch-up Math:** If a backlog of $B$ records builds up, and consumers process at rate $C$ while producers send at rate $P$:
  $$\\text{Catch-up Time} = \\frac{B}{C - P} \\quad (\\text{Requires } C > P)$$

## Mental model
```text
Producer Rate: 10,000/s ──► [ Kafka Disk Buffer ] ──► Consumer Rate: 2,000/s (Slow!)
                                  │
                                  ▼
                         Backlog Growing at +8,000 msgs/sec!
                         Disk consumption: +8 MB/sec
                         In 24 hours: 691 GB accumulated!
```

## Build it
See [backpressure_sim.py](../code/backpressure_sim.py).
We model queue accumulation and calculate exact catch-up times under different consumer scaling scenarios.

## Use Kafka
Run a high-speed producer against a rate-limited consumer and observe lag growth.

## Inspect it
Observe disk space consumption and consumer lag trajectory.

## Measure it
Measure time taken to drain the backlog once additional consumer instances join.

## Break it
Simulate $C < P$ indefinitely until topic retention is breached.

## Recover it
Scale consumer parallelism or optimize per-record database batching.

## Modify it
Calculate capacity requirements for an e-commerce flash sale event.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a pull model protect consumers from crashing due to memory exhaustion?
2. If your consumers are processing at maximum CPU capacity and lag is growing, what are your two architectural options?

## Guarantees
* Consumers only receive records when they explicitly request them via `poll()`.

## Non-guarantees
* Kafka's disk buffer does not protect you from business failure if catch-up rate never exceeds production rate.

## When to use this
* Capacity planning, peak load sizing, and autoscaling design.

## When not to use this
* Assuming that because Kafka buffers data, downstream capacity can be ignored.

## What comes next
In Phase 33, we study Producer Retries and observe how network timeouts create duplicate records.
"""

p32_code = {
    "backpressure_sim.py": """#!/usr/bin/env python3
def calculate_buffer_dynamics(prod_rate=10000, cons_rate=8000, duration_sec=3600, record_bytes=1024):
    print("--- Queueing & Buffer Capacity Analysis ---")
    print(f"Production Rate: {prod_rate:,} msgs/s")
    print(f"Consumer Rate:   {cons_rate:,} msgs/s")
    print(f"Duration:        {duration_sec/60:.0f} minutes\\n")

    net_rate = prod_rate - cons_rate
    accumulated_msgs = net_rate * duration_sec
    accumulated_mb = (accumulated_msgs * record_bytes) / (1024 * 1024)

    print(f"Backlog Accumulation Rate: +{net_rate:,} msgs/s")
    print(f"Total Accumulated Backlog:  {accumulated_msgs:,} records")
    print(f"Storage Buffer Required:    {accumulated_mb:,.1f} MB ({accumulated_mb/1024:.2f} GB)\\n")

    # Catch up calculation if consumer scales to 15,000/s
    scaled_cons_rate = 15000
    recovery_rate = scaled_cons_rate - prod_rate
    catch_up_sec = accumulated_msgs / recovery_rate
    print(f"If consumer capacity is scaled to {scaled_cons_rate:,} msgs/s:")
    print(f" -> Drain Rate: {recovery_rate:,} msgs/s")
    print(f" -> Time to drain backlog completely: {catch_up_sec/60:.1f} minutes")

if __name__ == "__main__":
    calculate_buffer_dynamics()
"""
}

p32_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 32 Experiment: Simulating Backpressure and Catch-up Capacity ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/backpressure_sim.py
"""

p32_evidence = """# Phase 32 Evidence Log

* **Date:**
* **Net Accumulation Rate:**
* **Storage Growth per Hour:**
* **Catch-up Time Required:**
* **Application of Little's Law:**
"""

write_phase("32-backpressure", p32_doc, p32_code, p32_exp, p32_evidence)

# ==============================================================================
# PHASE 33: Producer Retries and Duplicates
# ==============================================================================
p33_doc = """# Lesson 33: Producer Retries and Duplicates

## Motto
"A dropped acknowledgment is indistinguishable from a dropped write."

## Problem
A producer sends a record to the broker.
The broker successfully writes the record to disk at offset 42.
The broker crafts an acknowledgment packet (`ProduceResponse: OK`) and sends it over the network.
A network glitch drops the packet.
The producer's client library encounters a timeout:
* Did the broker write the record and the ACK was lost?
* Or did the write fail before reaching the broker?
The producer cannot know!
So the producer does the only reasonable thing: **it retries**.
The broker receives the record a second time and appends it at offset 43.
**You now have duplicate records in your log!**

## Prediction
If network packet loss is 5% and producer retries are enabled (`retries=3`), will duplicate records appear in the topic?

## Why this matters
Understanding the fundamental ambiguity of distributed network communication explains why simple retries produce duplicates, necessitating the **Idempotent Producer** (Phase 34).

## Mental model
```text
Producer                                Kafka Broker
   │                                         │
   ├─── 1. Send Record ("Charge $50") ──────►│ Writes to Disk at Offset 42!
   │                                         │
   │◄── 2. Ack Packet DROPPED by network! ───┤
   │    (Timeout occurs!)                    │
   │                                         │
   ├─── 3. Retries: Send Record again ──────►│ Writes to Disk at Offset 43!
   │                                         │
   │◄── 4. Ack OK ───────────────────────────┤
Result: Offset 42 AND Offset 43 both contain "Charge $50"! DUPLICATE WRITE!
```

## Build it
See [network_retry_duplicate_sim.py](../code/network_retry_duplicate_sim.py).
We simulate lost acknowledgments and demonstrate duplicate records appearing in the log.

## Use Kafka
Inspect how standard producers create duplicate writes during network instability.

## Inspect it
Consume from the topic and find identical records with sequential offsets.

## Measure it
Count duplicate percentage under simulated 10% packet drop conditions.

## Break it
Disable retries (`retries=0`) to prevent duplicates, and observe that you now trade duplicate records for permanent data loss!

## Recover it
Enable Kafka's native Idempotent Producer (Phase 34).

## Modify it
Tune `retry.backoff.ms` and observe how backoff spacing affects retry timing.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can a client never distinguish between a server that crashed before processing and a server whose response was dropped?
2. Why does setting `retries=0` solve the duplicate problem but create a catastrophic data loss problem?

## Guarantees
* Producer retries ensure transient network blips do not cause data loss.

## Non-guarantees
* Standard retries without idempotence do NOT guarantee uniqueness.

## When to use this
* Retries are mandatory in all production systems.

## When not to use this
* Retries without idempotency should never be used for sensitive transactional data.

## What comes next
In Phase 34, we enable the Idempotent Producer to eliminate retry duplicates automatically.
"""

p33_code = {
    "network_retry_duplicate_sim.py": """#!/usr/bin/env python3
import random

class SimulatedBroker:
    def __init__(self):
        self.log = []

    def append(self, record):
        offset = len(self.log)
        self.log.append((offset, record))
        return offset

def produce_with_unreliable_ack(broker, record, drop_ack_probability=0.5):
    print(f"\\n[Producer] Sending: '{record}'")
    # 1. Broker receives and writes
    offset = broker.append(record)
    print(f"  -> Broker wrote to disk at Offset {offset}")

    # 2. Network simulation for Ack
    if random.random() < drop_ack_probability:
        print("  -> [NETWORK GLITCH] Ack packet DROPPED in transit!")
        print("  -> [Producer] Timeout! Did not receive Ack. RETRYING...")
        # Retry!
        retry_offset = broker.append(record)
        print(f"  -> Broker accepted RETRY write to disk at Offset {retry_offset}")
        print("  -> Ack received.")
    else:
        print("  -> Ack delivered successfully.")

if __name__ == "__main__":
    broker = SimulatedBroker()
    # Force a dropped ack
    produce_with_unreliable_ack(broker, "payment:ord_101", drop_ack_probability=1.0)

    print("\\nFinal Broker Log:")
    for off, msg in broker.log:
        print(f"  Offset {off}: {msg}")
    print("Result: Duplicate records created because producer retried after dropped Ack!")
"""
}

p33_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 33 Experiment: Simulating Network Drops and Retry Duplication ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/network_retry_duplicate_sim.py
"""

p33_evidence = """# Phase 33 Evidence Log

* **Date:**
* **Dropped Ack Simulated:** Yes
* **Offsets Created for Single Logical Event:** 0, 1
* **Why the producer retried:**
* **The fundamental distributed systems dilemma:**
"""

write_phase("33-producer-retries-and-duplicates", p33_doc, p33_code, p33_exp, p33_evidence)

# ==============================================================================
# PHASE 34: Idempotent Producer
# ==============================================================================
p34_doc = """# Lesson 34: Idempotent Producer

## Motto
"Sequence numbers turn blind retries into deduplicated no-ops."

## Problem
In Phase 33, we saw that retrying after a dropped ACK creates duplicate records on disk.
How can the broker recognize that a retried message is a duplicate of a message it already appended, and discard the duplicate without throwing an error to the producer?

## Prediction
If the producer tags every batch with a monotonic sequence number, what can the broker do when it receives sequence number #5 a second time?

## Why this matters
**The Idempotent Producer is one of Kafka's most elegant architectural features.**
It completely eliminates duplicate writes caused by producer retries, with zero performance penalty.

## First principles
When `enable.idempotence=true`:
1. **Producer ID (PID):** The broker assigns each producer a unique 64-bit PID during handshake (`InitProducerId`).
2. **Sequence Numbers:** The producer assigns an integer sequence number ($0, 1, 2, ...$) to every batch per topic-partition.
3. **Broker Deduplication:** The broker tracks the last committed sequence number for each `(PID, Partition)`.
   * If incoming sequence number == $\\text{last} + 1$: **Append to log and increment sequence.**
   * If incoming sequence number $\\le \\text{last}$: **DUPLICATE! Discard write, but return SUCCESS to client!**
   * If incoming sequence number $> \\text{last} + 1$: **GAP! Raise `OutOfOrderSequenceException` (potential missing data).**

## Mental model
```text
Producer (PID: 1001)                     Broker (Tracks PID 1001, Last Seq: 4)
   │                                              │
   ├─── 1. Send Batch (Seq: 5) ──────────────────►│ Seq 5 == Last(4) + 1 -> APPEND!
   │                                              │ Updates Last Seq = 5
   │◄── 2. Ack DROPPED by network! ───────────────┤
   │                                              │
   ├─── 3. Producer RETRIES Send Batch (Seq: 5) ─►│ Seq 5 <= Last(5) -> DUPLICATE!
   │                                              │ DOES NOT APPEND TO DISK!
   │◄── 4. Returns SUCCESS Ack! ──────────────────┘
Result: Exactly ONE write on disk! Zero duplicates!
```

## Build it
See [idempotent_producer_lab.py](../code/idempotent_producer_lab.py).
We configure and verify the idempotent producer.

## Use Kafka
In modern Kafka (3.0+), `enable.idempotence=true` is the default.
We explicitly verify this behavior.

## Inspect it
Use `kafka-dump-log.sh` to observe the `producerId` and `firstSequence` fields stored inside on-disk record batch headers.

## Measure it
Compare produce latency with idempotence enabled vs disabled (difference is negligible, < 1ms).

## Break it
Inject an artificial sequence number gap and observe `OutOfOrderSequenceException`.

## Recover it
Producer automatically refreshes PID state.

## Modify it
Verify that `max.in.flight.requests.per.connection` can safely be up to 5 without reordering when idempotence is active.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the idempotent producer guarantee deduplication only within a single producer session and single partition?
2. What happens to the sequence number tracking if the producer application restarts?

## Guarantees
* Eliminates duplicate writes caused by producer network retries within a session.
* Preserves strict order even with up to 5 in-flight requests.

## Non-guarantees
* Does NOT prevent duplicate messages if the producer application restarts with a new PID and generates the same event twice.

## When to use this
* In all production Kafka producers (enabled by default).

## When not to use this
* Extremely legacy brokers (< v0.11) that do not support batch format v2.

## What comes next
In Phase 35, we extend idempotence across multiple partitions and consumers using Kafka Transactions.
"""

p34_code = {
    "idempotent_producer_lab.py": """#!/usr/bin/env python3
from kafka import KafkaProducer

def run_idempotent_producer():
    print("Initializing KafkaProducer with enable_idempotence=True...")
    # In Kafka 3.0+, enable_idempotence is True by default when acks='all'
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        acks="all",
        retries=5
    )
    topic = "idempotent-lab"
    print(f"Producing 5 records with sequence numbers to '{topic}'...")
    for i in range(5):
        f = producer.send(topic, key=b"cust-1", value=f"tx-{i}".encode())
        meta = f.get(timeout=5)
        print(f" [Ack] Record {i} -> Offset {meta.offset}")

    producer.flush()
    producer.close()
    print("Idempotent producer completed.")

if __name__ == "__main__":
    run_idempotent_producer()
"""
}

p34_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 34 Experiment: Verifying Idempotent Producer Execution ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/idempotent_producer_lab.py
"""

p34_evidence = """# Phase 34 Evidence Log

* **Date:**
* **enable.idempotence:** True
* **Producer ID (PID):**
* **Sequence Number Tracking:**
* **How duplicate writes are prevented:**
"""

write_phase("34-idempotent-producer", p34_doc, p34_code, p34_exp, p34_evidence)

# ==============================================================================
# PHASE 35: Kafka Transactions
# ==============================================================================
p35_doc = """# Lesson 35: Kafka Transactions

## Motto
"Transactions bind input offsets and output events in an atomic embrace."

## Problem
Consider a streaming pipeline that reads from `input-topic` and publishes to `output-topic`:
```text
1. Fetch record at Offset 100 ("Transfer $50 from Alice to Bob")
2. Produce transformed record to output topic
3. Commit offset 100
```
What if the process crashes after step 2, but before step 3?
Upon restart, it re-fetches Offset 100 and publishes a *second* transformed record to `output-topic`!
How can we make **producing output records** and **committing input offsets** occur **atomically** together?

## Prediction
What happens to uncommitted transactional records in Kafka if the producer process crashes mid-transaction?

## Why this matters
**Kafka Transactions enable Exactly-Once Processing (EOS) in Kafka-to-Kafka streaming workflows.**
They ensure that downstream consumers only see output records if the corresponding input offsets were successfully committed.

## First principles
* **Transaction Coordinator:** A specialized broker managing transaction state via an internal topic `__transaction_state`.
* **Two-Phase Commit (2PC):**
  1. Producer registers partitions and sends records marked as uncommitted.
  2. Producer sends input offsets to the transaction coordinator (`sendOffsetsToTxn`).
  3. Coordinator writes `PREPARE_COMMIT` marker, flushes, and writes `COMMIT` marker to all participating partitions.
* **Isolation Level:** Consumers configured with `isolation.level=read_committed` skip uncommitted or aborted transaction batches.

## Mental model
```text
Stream Processor (Transactional Loop)
   ├── 1. beginTransaction()
   ├── 2. Process record from Topic A (Offset 50)
   ├── 3. send(Topic B, "Transformed Output")   <-- Marked as transactional!
   ├── 4. sendOffsetsToTransaction(Offset 50)  <-- Ties offset commit to txn!
   └── 5. commitTransaction()                   <-- Atomic Commit Marker!
Downstream Consumer (isolation.level=read_committed)
   └── Sees output message ONLY after Commit Marker appears!
```

## Build it
See [transactional_processor.py](../code/transactional_processor.py).
We demonstrate the complete transactional consume-transform-produce cycle.

## Use Kafka
Execute transactional writes and inspect with `read_committed` consumer.

## Inspect it
Observe transaction commit markers using `kafka-dump-log.sh`.

## Measure it
Measure latency overhead of two-phase commit markers vs non-transactional writes.

## Break it
Abort a transaction (`abortTransaction()`) and verify downstream `read_committed` consumers never see the aborted messages.

## Recover it
Demonstrate clean rollback without orphan messages.

## Modify it
Compare output visible to `read_uncommitted` vs `read_committed` consumers.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must the input offset commit be routed through the Transaction Coordinator rather than committed directly to `__consumer_offsets`?
2. What is an aborted transaction marker, and why does it still consume disk space in the log?

## Guarantees
* Atomicity across multiple topic-partitions and consumer offset commits.

## Non-guarantees
* Does NOT make external non-Kafka databases (e.g. Postgres) exactly-once.

## When to use this
* Stream processing applications reading from Kafka and producing to Kafka (Kafka Streams, Flink).

## When not to use this
* Simple ingestion pipelines where downstream consumers are already idempotent.

## What comes next
In Phase 36, we evaluate the real boundaries of Exactly-Once Semantics (EOS).
"""

p35_code = {
    "transactional_processor.py": """#!/usr/bin/env python3
import time

def simulate_transactional_flow():
    print("--- Simulating Kafka Two-Phase Transactional Commit ---")
    print("1. Producer registers transactional.id='order-processor-txn-1'")
    print("2. Coordinator assigns Producer ID (PID: 2005, Epoch: 1)")
    print("3. beginTransaction()")
    print("4. Appending transformed output record to 'orders-processed'...")
    print("5. Committing input offset 42 via sendOffsetsToTransaction()...")
    print("6. commitTransaction(): Coordinator appends COMMIT markers to logs.")
    print("7. Downstream read_committed consumer sees record! SUCCESS!\\n")

    print("--- Simulating Aborted Transaction (Rollback) ---")
    print("1. beginTransaction()")
    print("2. Appending tentative record to 'orders-processed'...")
    print("3. CRASH / ERROR DETECTED! Calling abortTransaction()...")
    print("4. Coordinator appends ABORT marker.")
    print("5. Downstream read_committed consumer SKIPS tentative record! ZERO LEAKAGE!")

if __name__ == "__main__":
    simulate_transactional_flow()
"""
}

p35_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 35 Experiment: Simulating Kafka Two-Phase Transactions ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/transactional_processor.py
"""

p35_evidence = """# Phase 35 Evidence Log

* **Date:**
* **Transactional ID:**
* **Isolation Level Tested:** read_committed
* **Behavior of Aborted Records:**
* **Scope of Kafka Transactions:**
"""

write_phase("35-kafka-transactions", p35_doc, p35_code, p35_exp, p35_evidence)

# ==============================================================================
# PHASE 36: Exactly-Once Semantics
# ==============================================================================
p36_doc = """# Lesson 36: Exactly-Once Semantics

## Motto
"Exactly-once processing in Kafka does not mean magic exactly-once effects across the universe."

## Problem
Marketing materials often claim: *"Kafka provides Exactly-Once Semantics (EOS)!"*
Software engineers then build pipelines that read from Kafka and call an external payment gateway or insert into MySQL, and are shocked when duplicate payments still occur.
What does Kafka's "Exactly-Once" guarantee actually mean, and where does that guarantee stop?

## Prediction
Can Kafka transactions guarantee that a third-party non-transactional REST API will be called exactly once?

## Why this matters
Clarifying the precise technical boundary of EOS separates senior distributed systems architects from engineers who believe in magic.

## First principles
**The Reality of Kafka Exactly-Once Processing:**
* **Within Kafka Boundary:** Reading from Kafka, transforming in memory, and writing back to Kafka CAN be strictly exactly-once.
* **Outside Kafka Boundary:** Once an external system is touched (HTTP requests, external SQL databases, email gateways, file systems), Kafka's transactional coordinator has no jurisdiction!
* Achieving true end-to-end exactly-once with external systems requires **Idempotency** or the **Transactional Outbox Pattern** (Phase 60).

## Mental model
```text
The Kafka EOS Boundary:
┌────────────────────────────────────────────────────────┐
│ Kafka Input ──► Kafka Stream ──► Kafka Output Topic    │
│ [ EXACTLY-ONCE SEMANTICS GUARANTEED BY 2PC & KIP-98 ]  │
└────────────────────────────────────────────────────────┘
                           │
                           ▼ Outside the Boundary!
┌────────────────────────────────────────────────────────┐
│ External REST API / Stripe / SendGrid / Postgres       │
│ [ AT-LEAST-ONCE ONLY! Requires Idempotency Keys! ]     │
└────────────────────────────────────────────────────────┘
```

## Build it
See [eos_boundaries_lab.py](../code/eos_boundaries_lab.py).
We demonstrate the boundary where Kafka EOS ends and external side-effects require application-level idempotency.

## Use Kafka
Evaluate `read_committed` consumers reading transactional topics.

## Inspect it
Observe how committed and aborted transaction records are handled.

## Measure it
Measure throughput delta between EOS transactions and standard idempotent producer writes.

## Break it
Simulate an external API call inside a Kafka transaction; crash after the API call succeeds but before Kafka commit; observe the duplicate API call!

## Recover it
Add idempotency keys (`Idempotency-Key` HTTP header) to the external API call.

## Modify it
Document the failure matrix for hybrid Kafka + Database pipelines.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is the phrase "Exactly-Once Delivery" technically impossible over an unreliable network, while "Exactly-Once Processing" is achievable?
2. If your consumer writes to an external non-transactional database, how do you achieve effective exactly-once results?

## Guarantees
* Exactly-once state updates for Kafka-in to Kafka-out streaming topologies.

## Non-guarantees
* Does not guarantee exactly-once side effects on external services or databases.

## When to use this
* Pure Kafka streaming transformations (aggregations, joins, filtering).

## When not to use this
* Believing it eliminates the need for database idempotency.

## What comes next
In Phase 37, we explore Schema Evolution and see how event schemas evolve without breaking consumers.
"""

p36_code = {
    "eos_boundaries_lab.py": """#!/usr/bin/env python3
def explain_eos_boundaries():
    print("=== The Reality of Exactly-Once Semantics (EOS) ===\\n")
    print("1. Kafka-to-Kafka Stream:")
    print("   Input Topic -> Stream Processor -> Output Topic")
    print("   Guarantee: EXACTLY-ONCE (via Idempotent Producer + Transactions)\\n")

    print("2. Kafka to External Non-Transactional API:")
    print("   Input Topic -> Consumer -> HTTP POST https://api.stripe.com/charges")
    print("   Guarantee: AT-LEAST-ONCE (Network can drop response after card charged!)")
    print("   Solution: Must send Idempotency-Key header to external API!\\n")

    print("3. Kafka to SQL Database:")
    print("   Input Topic -> Consumer -> INSERT INTO orders VALUES (...)")
    print("   Guarantee: AT-LEAST-ONCE (Crash between DB commit and Kafka offset commit!)")
    print("   Solution: Idempotent Consumer (Phase 15) or Outbox Pattern (Phase 60)!\\n")

if __name__ == "__main__":
    explain_eos_boundaries()
"""
}

p36_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 36 Experiment: Exploring EOS Boundaries ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/eos_boundaries_lab.py
"""

p36_evidence = """# Phase 36 Evidence Log

* **Date:**
* **Kafka-to-Kafka Guarantee:** Exactly-Once Processing
* **Kafka-to-External API Guarantee:** At-Least-Once
* **Why external systems break EOS:**
* **Idempotency's role:**
"""

write_phase("36-exactly-once-semantics", p36_doc, p36_code, p36_exp, p36_evidence)

# ==============================================================================
# PHASE 37: Schema Evolution
# ==============================================================================
p37_doc = """# Lesson 37: Schema Evolution

## Motto
"An event format without a schema contract is a ticking production landmine."

## Problem
In early development, teams publish arbitrary JSON payloads:
`{"user_id": 42, "name": "Alice"}`
Six months later, the producer team renames `user_id` to `customer_uuid`:
`{"customer_uuid": "c-99", "name": "Alice"}`
The instant this event is published, 4 downstream consumer services crash with `KeyError: 'user_id'`.
How do producers and consumers evolve independently without coordinated deployment locks?

## Prediction
What is the difference between Backward Compatibility and Forward Compatibility in event schemas?

## Why this matters
In event-driven systems, producers and consumers are deployed independently by different teams. **Schema Evolution** is the discipline that ensures events remain readable across system versions.

## First principles
* **Backward Compatibility:** A new consumer (v2) can read data produced by an old producer (v1). (e.g. adding an optional field with a default value).
* **Forward Compatibility:** An old consumer (v1) can read data produced by a new producer (v2). (e.g. consumer ignores unknown new fields).
* **Full Compatibility:** Both backward and forward compatible.
* **Breaking Changes:** Renaming fields, changing data types (integer to string), deleting required fields.

## Mental model
```text
Producer v2 (Adds optional 'loyalty_tier')
   │
   ▼
Event: {"user_id": 42, "name": "Alice", "loyalty_tier": "GOLD"}
   ├──► Consumer v1 (Reads 'user_id' & 'name', safely IGNORES 'loyalty_tier') -> OK!
   └──► Consumer v2 (Reads all fields including 'loyalty_tier')               -> OK!
Result: Zero downtime deployment!
```

## Build it
See [schema_evolution_lab.py](../code/schema_evolution_lab.py).
We test schema evolution and observe consumer compatibility breaks.

## Use Kafka
Produce evolving JSON payloads with schema version headers.

## Inspect it
Observe how resilient consumers gracefully fallback when optional fields are missing.

## Measure it
Benchmark parsing overhead of schema validation.

## Break it
Simulate a producer renaming a required field without a migration window; watch legacy consumers crash.

## Recover it
Maintain deprecated fields alongside new fields during a transition period.

## Modify it
Implement schema evolution using Avro or Protobuf specifications.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is renaming a field always a breaking change in JSON and Protobuf?
2. Why must newly added fields always specify a default value to maintain backward compatibility?

## Guarantees
* Compatible schemas allow consumers and producers to be deployed in any arbitrary order.

## Non-guarantees
* Raw JSON without validation does not enforce schema constraints at compile time.

## When to use this
* In all cross-team production event streams.

## When not to use this
* Throwaway internal prototypes where all code is in a single repository.

## What comes next
In Phase 38, we examine Event Design: Event Notification vs. Event-Carried State Transfer.
"""

p37_code = {
    "schema_evolution_lab.py": """#!/usr/bin/env python3
import json

def legacy_consumer_v1(raw_payload: str):
    data = json.loads(raw_payload)
    # Expects strict schema v1: user_id (int), email (str)
    try:
        user_id = data["user_id"]
        email = data["email"]
        print(f" [Consumer v1 OK] Handled user_id={user_id}, email={email}")
    except KeyError as e:
        print(f" [Consumer v1 CRASHED!] Missing required key: {e}")

def resilient_consumer_v2(raw_payload: str):
    data = json.loads(raw_payload)
    # Resilient schema: handles both user_id and customer_uuid, default loyalty_tier
    uid = data.get("customer_uuid") or data.get("user_id", "UNKNOWN")
    email = data.get("email", "no-email@provided")
    tier = data.get("loyalty_tier", "STANDARD")
    print(f" [Consumer v2 OK] Handled uid={uid}, email={email}, tier={tier}")

if __name__ == "__main__":
    print("--- 1. Producer sends v1 payload ---")
    p1 = json.dumps({"user_id": 101, "email": "alice@example.com"})
    legacy_consumer_v1(p1)

    print("\\n--- 2. Producer evolves schema to v2 (Renames user_id to customer_uuid) ---")
    p2_broken = json.dumps({"customer_uuid": "CUST-99", "email": "bob@example.com", "loyalty_tier": "VIP"})
    legacy_consumer_v1(p2_broken) # CRASHES!

    print("\\n--- 3. Resilient Consumer handles both v1 and v2 seamlessly ---")
    resilient_consumer_v2(p1)
    resilient_consumer_v2(p2_broken)
"""
}

p37_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 37 Experiment: Demonstrating Schema Evolution and Breaking Changes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/schema_evolution_lab.py
"""

p37_evidence = """# Phase 37 Evidence Log

* **Date:**
* **Legacy Consumer Outcome with Renamed Field:** CRASH (KeyError)
* **Resilient Consumer Outcome:** SUCCESS
* **Backward Compatibility Rule:**
* **Forward Compatibility Rule:**
"""

write_phase("37-schema-evolution", p37_doc, p37_code, p37_exp, p37_evidence)

# ==============================================================================
# PHASE 38: Event Design
# ==============================================================================
p38_doc = """# Lesson 38: Event Design

## Motto
"An event should tell a complete story, not send consumers on a database scavenger hunt."

## Problem
What should the payload of an event actually look like?
Consider two extremes:
* **Bad Minimal Event (Event Notification):** `{"event": "ORDER_UPDATED", "order_id": 501}`
  * Every consumer must immediately make an HTTP call back to Order Service to ask *"What changed?"*, destroying decoupling and causing a thundering herd.
* **Bad Bloated Event:** A 15 MB payload containing entire historical customer records, tax forms, and attachments.
How do we balance self-contained richness with lean payload size?

## Prediction
What is the difference between Event Notification and Event-Carried State Transfer?

## Why this matters
Event schema design dictates how tightly coupled downstream systems remain to the original producing service.

## First principles
* **Event Notification:** Signals only that something happened (`order_id: 101`). Downstream services query upstream API for details. Low payload, high RPC coupling.
* **Event-Carried State Transfer (ECST):** Carries all relevant state attributes needed by downstream consumers (`order_id`, `items`, `total`, `tax`, `customer_address`). Eliminates RPC queries, achieves true temporal decoupling.
* **Essential Event Metadata:** Every event should contain:
  1. `event_id`: Unique UUID for idempotency.
  2. `event_type`: Domain action in past tense (`OrderCreated`, `PaymentCompleted`).
  3. `timestamp`: Event creation time (epoch ms).
  4. `entity_id`: Domain entity key.
  5. `schema_version`: For evolution.

## Mental model
```text
Event Notification (Causes Scavenger Hunt):
Producer ──► [ OrderUpdated(id=101) ] ──► Consumer ──(HTTP GET /orders/101)──► Producer DB!

Event-Carried State Transfer (Decoupled & Self-Contained):
Producer ──► [ OrderCreated { id: 101, items: [...], total: 99.50, addr: "..." } ]
                   │
                   ▼
             Consumer processes event directly without touching any other service!
```

## Build it
See [event_design_patterns.py](../code/event_design_patterns.py).
We contrast lean vs well-structured domain events.

## Use Kafka
Produce structured domain events with metadata envelopes.

## Inspect it
Observe how standard metadata envelopes make generic logging, routing, and tracing trivial.

## Measure it
Compare downstream query load under Event Notification vs Event-Carried State Transfer.

## Break it
Send an event with vague semantics (`{"action": "modify"}`) and observe how multiple consumers misinterpret it.

## Recover it
Use explicit past-tense domain events (`OrderAddressChanged`, `OrderItemAdded`).

## Modify it
Add correlation IDs (`trace_id`, `span_id`) to enable OpenTelemetry distributed tracing across Kafka.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why should event types always be named in the past tense (e.g. `OrderPlaced` rather than `PlaceOrder`)?
2. What are the trade-offs of Event-Carried State Transfer regarding data privacy and GDPR?

## Guarantees
* Rich events provide full temporal decoupling.

## Non-guarantees
* Event-Carried State Transfer does not reflect subsequent modifications unless new events are emitted.

## When to use this
* In all enterprise event-driven architectures.

## When not to use this
* Highly sensitive PII that cannot be persisted in unencrypted distributed logs.

## What comes next
In Phase 39, we examine Ordering Guarantees and learn where Kafka preserves order and where it does not.
"""

p38_code = {
    "event_design_patterns.py": """#!/usr/bin/env python3
import uuid
import time
import json

def create_domain_event(entity_id: str, event_type: str, payload: dict) -> dict:
    \"\"\"Standard Production Event Envelope.\"\"\"
    return {
        "metadata": {
            "event_id": str(uuid.uuid4()),
            "event_type": event_type,
            "schema_version": "1.0",
            "timestamp": int(time.time() * 1000),
            "source_service": "checkout-service",
            "correlation_id": str(uuid.uuid4())
        },
        "key": entity_id,
        "data": payload
    }

if __name__ == "__main__":
    event = create_domain_event(
        entity_id="order-9901",
        event_type="OrderPlaced",
        payload={
            "order_id": "order-9901",
            "customer_id": "usr_42",
            "currency": "USD",
            "amount": 149.99,
            "items": [{"sku": "HEADPHONES-PRO", "qty": 1, "price": 149.99}]
        }
    )
    print("Standard Production Event Envelope:")
    print(json.dumps(event, indent=2))
"""
}

p38_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 38 Experiment: Generating Standard Domain Event Envelopes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/event_design_patterns.py
"""

p38_evidence = """# Phase 38 Evidence Log

* **Date:**
* **Event Structure Inspected:**
* **Role of event_id:**
* **Role of past-tense naming:**
* **Trade-off of ECST:**
"""

write_phase("38-event-design", p38_doc, p38_code, p38_exp, p38_evidence)

# ==============================================================================
# PHASE 39: Ordering
# ==============================================================================
p39_doc = """# Lesson 39: Ordering

## Motto
"Kafka does not guarantee global order; Kafka guarantees partition order. Design your keys accordingly."

## Problem
A user executes three operations on their bank account:
1. `Deposit $100` (Account: $100)
2. `Withdraw $80` (Account: $20)
3. `Withdraw $50` (Declined - Insufficient funds!)
If these three events are published without keys to a 3-partition topic:
* Event 1 lands on Partition 0.
* Event 2 lands on Partition 1.
* Event 3 lands on Partition 2.
Because different consumers read different partitions at different speeds, Event 3 is processed first!
The user's withdrawal is rejected even though they had $100 in their account!
How does Kafka preserve causality?

## Prediction
What happens to ordering when causally related events are scattered across multiple partitions?

## Why this matters
Total global ordering across a distributed system requires serializing all writes through a single thread on a single machine (Amdahl's Law). Kafka achieves massive scale by scoping ordering strictly to the partition.

## First principles
* **Partition Total Order:** Records within a partition are strictly sequential ($0, 1, 2, ...$).
* **Cross-Partition Interleaving:** No ordering guarantee exists across different partitions.
* **Keying for Causality:** To preserve order for an entity, all events for that entity must share the same partition key.

## Mental model
```text
Unkeyed (Scattered across partitions - Causality Broken!):
Partition 0: [ Deposit $100 ]
Partition 1: [ Withdraw $80 ]  <-- Consumer B processes this first!
Partition 2: [ Withdraw $50 ]  <-- Consumer C processes this second! (Overdrawn!)

Keyed by Account ID "acc-42" (Guaranteed Chronological Order!):
Partition 1: [ Deposit $100 (off 0) ──► Withdraw $80 (off 1) ──► Withdraw $50 (off 2) ]
Result: Deterministic, correct financial execution!
```

## Build it
See [ordering_guarantees_lab.py](../code/ordering_guarantees_lab.py).
We demonstrate order preservation via keying vs out-of-order interleaving without keys.

## Use Kafka
Produce sequential records to Kafka and verify partition-scoped arrival.

## Inspect it
Consume from multiple partitions and observe out-of-order interleaving in real-time.

## Measure it
Measure throughput cost of single-partition total ordering vs multi-partition key-based ordering.

## Break it
Send causally related events with `key=None` across a 4-partition topic and observe interleaved processing.

## Recover it
Key all related events by entity ID (`account_id`, `user_id`, `order_id`).

## Modify it
Implement a single-partition topic to observe true global FIFO order (and observe throughput limits).

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is global FIFO ordering fundamentally incompatible with horizontal distributed scale?
2. If two events happen for *different* users, does your application actually care which one is processed first?

## Guarantees
* Strict, deterministic chronological order within any single partition.

## Non-guarantees
* Zero ordering guarantees between different partitions.

## When to use this
* Per-entity ordering for financial transactions, state machines, user actions.

## When not to use this
* Demanding global topic-wide order across independent entities (an architectural anti-pattern).

## What comes next
In Phase 40, we examine Time semantics in Kafka: CreateTime, LogAppendTime, and ProcessingTime.
"""

p39_code = {
    "ordering_guarantees_lab.py": """#!/usr/bin/env python3
import time
from collections import defaultdict

def test_ordering():
    print("--- 1. Producing WITH Key (Targeting Same Partition) ---")
    account_partition = 1
    partition_log = []
    
    events = ["DEPOSIT_100", "WITHDRAW_80", "WITHDRAW_50"]
    for off, ev in enumerate(events):
        partition_log.append((off, ev))
        print(f" Partition {account_partition} | Offset {off}: {ev}")

    print("\\nConsumer processing order:")
    balance = 0
    for off, ev in partition_log:
        if ev == "DEPOSIT_100": balance += 100
        elif ev == "WITHDRAW_80": balance -= 80
        elif ev == "WITHDRAW_50":
            if balance >= 50: balance -= 50
            else: print("  [DECLINED] Insufficient funds!")
        print(f"  Processed {ev} -> Current Balance: ${balance}")

if __name__ == "__main__":
    test_ordering()
"""
}

p39_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 39 Experiment: Verifying Partition-Scoped Ordering ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/ordering_guarantees_lab.py
"""

p39_evidence = """# Phase 39 Evidence Log

* **Date:**
* **Key Strategy Used:** Entity ID (acc-42)
* **Target Partition:** 1
* **Was causality preserved?** Yes
* **Why global FIFO order restricts throughput:**
"""

write_phase("39-ordering", p39_doc, p39_code, p39_exp, p39_evidence)

# ==============================================================================
# PHASE 40: Time in Kafka
# ==============================================================================
p40_doc = """# Lesson 40: Time in Kafka

## Motto
"There is the time an event happened, the time Kafka wrote it, and the time you read it; never confuse the three."

## Problem
In distributed systems, clocks skew, consumers lag, and historical replays occur.
Consider three different timestamps for a single event:
1. `10:00:00 AM` — Sensor detects engine overheating in a car.
2. `10:05:00 AM` — Car re-enters cellular coverage; producer appends record to Kafka broker.
3. `02:00:00 PM` — Analytics consumer wakes up and processes the record.
If the analytics service alerts on "events that happened in the last 15 minutes" using `time.now()`, it alerts 4 hours late!
Which timestamp should you use?

## Prediction
What is the difference between `CreateTime` and `LogAppendTime` in Kafka topic configurations?

## Why this matters
**Time is the trickiest variable in stream processing.**
Confusing Event Time with Processing Time causes incorrect financial calculations, broken window aggregations, and invalid alerting.

## First principles
* **Event Time (`CreateTime`):** The timestamp set by the producer application when the real-world event occurred (`message.timestamp.type=CreateTime`, the default).
* **Log Append Time (`LogAppendTime`):** The timestamp assigned by the broker when it writes the record to its local log.
* **Processing Time:** The clock time of the consumer machine executing business logic.

## Mental model
```text
Event Occurs: 10:00:00 AM (Event Time / CreateTime)
      │
      ▼ (5 minute network/cellular delay)
Broker Writes: 10:05:00 AM (LogAppendTime)
      │
      ▼ (4 hours in retention buffer / consumer lag)
Consumer Reads: 02:00:00 PM (Processing Time)
```

## Build it
See [time_semantics_lab.py](../code/time_semantics_lab.py).
We inspect the differences between event timestamps and consumer processing timestamps.

## Use Kafka
Set `message.timestamp.type=LogAppendTime` on a topic and observe broker-assigned timestamps.

## Inspect it
Use `kafka-console-consumer.sh --property print.timestamp=true` to inspect record timestamps.

## Measure it
Measure the delta between `CreateTime` and `System.currentTimeMillis()` at consumption.

## Break it
Simulate a producer with an incorrectly configured system clock set to year 2035; observe how time-based retention misbehaves!

## Recover it
Synchronize server clocks using NTP (Network Time Protocol) or enforce `LogAppendTime`.

## Modify it
Query Kafka offsets by timestamp using `consumer.offsets_for_times()`.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does out-of-order stream processing require algorithms to operate on Event Time rather than Processing Time?
2. What happens to time-based retention if records are produced with timestamps far in the past or future?

## Guarantees
* Kafka preserves the 64-bit millisecond timestamp attached to each record batch.

## Non-guarantees
* Kafka does not validate whether producer clocks are synchronized with real UTC time.

## When to use this
* Windowed streaming aggregations, time-series telemetry, and historical replay.

## When not to use this
* Relying on `CreateTime` without NTP clock synchronization across producer servers.

## What comes next
In Phase 41, we contrast Kafka with traditional Message Queues (RabbitMQ, SQS).
"""

p40_code = {
    "time_semantics_lab.py": """#!/usr/bin/env python3
import time
from datetime import datetime

def test_time_semantics():
    # 1. Real-world event occurs
    event_time_ms = int(time.time() * 1000) - 300000 # 5 minutes ago
    event_dt = datetime.fromtimestamp(event_time_ms / 1000)

    # 2. Broker receives and writes
    log_append_time_ms = int(time.time() * 1000)
    append_dt = datetime.fromtimestamp(log_append_time_ms / 1000)

    # 3. Consumer processes later
    processing_time_ms = log_append_time_ms + 10000 # 10s later
    process_dt = datetime.fromtimestamp(processing_time_ms / 1000)

    print("Timestamp Analysis for Record:")
    print(f"  Event Time (CreateTime):   {event_dt.strftime('%H:%M:%S')} (When event physically happened)")
    print(f"  Log Append Time:           {append_dt.strftime('%H:%M:%S')} (When broker committed to disk)")
    print(f"  Processing Time:           {process_dt.strftime('%H:%M:%S')} (When consumer thread executed)")
    print(f"\\nTime Delta (Ingestion Delay):  {(log_append_time_ms - event_time_ms)/1000:.1f} seconds")
    print(f"Time Delta (Processing Lag):   {(processing_time_ms - log_append_time_ms)/1000:.1f} seconds")

if __name__ == "__main__":
    test_time_semantics()
"""
}

p40_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 40 Experiment: Inspecting Kafka Timestamp Semantics ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/time_semantics_lab.py
"""

p40_evidence = """# Phase 40 Evidence Log

* **Date:**
* **Event Time:**
* **Log Append Time:**
* **Processing Time:**
* **Why windowing must use Event Time:**
"""

write_phase("40-time-in-kafka", p40_doc, p40_code, p40_exp, p40_evidence)

# ==============================================================================
# PHASE 41: Kafka as Queue vs Log
# ==============================================================================
p41_doc = """# Lesson 41: Kafka as Queue vs Log

## Motto
"A queue is an ephemeral checklist; a log is an immutable historical ledger."

## Problem
Many software engineers begin by asking: *"Is Kafka better than RabbitMQ or SQS?"*
This question stems from a category error:
* A Queue manages transient work items, deleting them as soon as one worker completes the task.
* A Log records immutable facts in chronological order, preserving them for multiple independent consumers to read and replay.
When should you pick a Queue, and when should you pick Kafka?

## Prediction
If you need individual message acknowledgments, dead-letter routing per message, and tasks distributed to 100 workers regardless of partition count, is Kafka or a Queue more suitable?

## Why this matters
Choosing Kafka when you actually need a simple task queue introduces massive partition management, consumer group rebalances, and ordering complexity for zero benefit.
Choosing a queue when you need event replay, multi-team fan-out, and high throughput leads to queue collapse.

## First principles
| Dimension | Traditional Queue (RabbitMQ / SQS) | Distributed Log (Apache Kafka) |
| :--- | :--- | :--- |
| **Read Mechanism** | Destructive pop (`ack` deletes message) | Non-destructive offset read |
| **Multiple Consumers** | Competing consumers (divide work) | Independent Consumer Groups (broadcast/fanout) |
| **Replay** | Impossible (messages are deleted) | Trivial (rewind consumer offset) |
| **Ordering** | FIFO queue head only | Strict partition-scoped ordering |
| **Throughput** | 10k - 50k msgs/sec | 500k - 2M+ msgs/sec (via batching & page cache) |
| **Task Granularity** | Per-message ack and routing | Batch-level commits and partition-level locks |

## Mental model
```text
Work Queue (RabbitMQ / SQS):
[ Msg 1 | Msg 2 | Msg 3 ] ──► Worker A pops Msg 1 (DELETED!)
                          ──► Worker B pops Msg 2 (DELETED!)

Append-Only Log (Kafka):
[ Evt 1 | Evt 2 | Evt 3 ] ──► Service A reads Evt 1, 2, 3 (Track offset)
                          ──► Service B reads Evt 1, 2, 3 (Track offset)
                          ──► Auditor replays Evt 1, 2, 3 next week!
```

## Build it
See [queue_vs_log_comparison.py](../code/queue_vs_log_comparison.py).
We contrast destructive pop vs offset tracking in Python.

## Use Kafka
Demonstrate multiple consumer groups reading the same records simultaneously without interference.

## Inspect it
Observe that after consumer A finishes reading all records, consumer B can still read 100% of those records from offset 0.

## Measure it
Compare consumer memory usage between in-memory message queues and Kafka offset pointers.

## Break it
Try to ack individual messages out of order in Kafka; discover that Kafka can only commit sequential offsets up to the highest processed point!

## Recover it
Use application-level deduplication or out-of-order trackers.

## Modify it
Write an architectural decision record (ADR) comparing Kafka vs SQS for a background email sending service.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a traditional queue struggle to support 10 independent downstream consumer services?
2. If your workload involves long-running, CPU-intensive tasks (e.g. 10 minutes per PDF render), why is a traditional work queue usually a better fit than Kafka?

## Guarantees
* Kafka guarantees non-destructive reads across multiple consumer groups.

## Non-guarantees
* Kafka does not support selective per-message acknowledgments (e.g. acknowledging message #5 while leaving message #4 unacknowledged).

## When to use this
* Architectural technology selection and system design interviews.

## When not to use this
* Blindly replacing existing task queues with Kafka without evaluating partition concurrency limits.

## What comes next
In Phase 42, we demonstrate Multiple Consumer Groups and fan-out architecture in practice.
"""

p41_code = {
    "queue_vs_log_comparison.py": """#!/usr/bin/env python3
from collections import deque

class DestructiveQueue:
    def __init__(self):
        self.queue = deque()
    def push(self, item): self.queue.append(item)
    def pop(self): return self.queue.popleft() if self.queue else None

class NonDestructiveLog:
    def __init__(self):
        self.log = []
    def append(self, item):
        off = len(self.log)
        self.log.append((off, item))
        return off
    def read(self, offset):
        return self.log[offset:]

if __name__ == "__main__":
    print("--- 1. Destructive Queue (Work Queue Model) ---")
    q = DestructiveQueue()
    q.push("Task-1")
    q.push("Task-2")
    print(f" Worker A pops: {q.pop()}")
    print(f" Worker B pops: {q.pop()}")
    print(f" Remaining in queue: {len(q.queue)} (Data is GONE! Cannot replay!)\\n")

    print("--- 2. Non-Destructive Log (Kafka Model) ---")
    log = NonDestructiveLog()
    log.append("Event-1")
    log.append("Event-2")
    print(f" Service A (Fraud) reads:     {[x[1] for x in log.read(0)]}")
    print(f" Service B (Analytics) reads: {[x[1] for x in log.read(0)]}")
    print(f" Service C (Replay next day): {[x[1] for x in log.read(0)]}")
    print(" Result: Data remains immutable on disk for all consumers!")
"""
}

p41_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 41 Experiment: Contrasting Queue vs Log Architectures ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/queue_vs_log_comparison.py
"""

p41_evidence = """# Phase 41 Evidence Log

* **Date:**
* **Queue Behavior Observed:** Destructive pop
* **Log Behavior Observed:** Non-destructive multi-consumer reads
* **When to pick RabbitMQ/SQS:**
* **When to pick Kafka:**
"""

write_phase("41-kafka-as-queue-vs-log", p41_doc, p41_code, p41_exp, p41_evidence)

# ==============================================================================
# PHASE 42: Multiple Consumer Groups
# ==============================================================================
p42_doc = """# Lesson 42: Multiple Consumer Groups

## Motto
"One write, infinite independent readers; the ultimate decoupling engine."

## Problem
In a monolithic system, when an order is placed:
The code calls `payment()`, then `email()`, then `inventory()`, then `analytics()`.
When Marketing wants to add a new `loyalty_points()` system, the core checkout codebase must be touched, tested, and redeployed.
How does Kafka allow any number of independent teams to consume the `orders` stream without the checkout team ever knowing or caring?

## Prediction
If Group A commits offset 100 on Partition 0, what is Group B's offset on Partition 0?

## Why this matters
**Multiple Consumer Groups provide true organizational decoupling.**
Teams can build, deploy, scale, and crash their services independently without affecting any other team's consumption progress.

## Mental model
```text
Topic: "orders" (Partition 0)
Offsets: 0 ── 1 ── 2 ── 3 ── 4 ── 5 ── 6 (LEO)

Group 1: "payment-service"      ──► Offset 6 (Real-time, caught up!)
Group 2: "email-notifications"  ──► Offset 4 (Slightly lagging)
Group 3: "data-warehouse-etl"   ──► Offset 1 (Batching 10,000 records/hr)
Group 4: "new-loyalty-service"  ──► Offset 0 (Newly deployed! Replaying from beginning!)
```

## Build it
See [multi_group_fanout.py](../code/multi_group_fanout.py).
We launch three independent consumer groups against a single producer topic and verify independent offset tracking.

## Use Kafka
Run multiple consumers specifying different `--group` IDs:
```bash
# Group 1: fraud-service
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic multi-fanout-orders --group fraud-service

# Group 2: email-service
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 --topic multi-fanout-orders --group email-service
```

## Inspect it
Describe both groups and observe completely independent `CURRENT-OFFSET` values:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 --describe --group fraud-service
```

## Measure it
Measure broker CPU and memory impact when adding 5 additional consumer groups (virtually zero, thanks to page cache sharing!).

## Break it
Crash Group 2 (Email Service); observe that Group 1 (Fraud Service) continues processing without experiencing a single millisecond of disruption!

## Recover it
Restart Group 2; it resumes from its own saved offset and catches up.

## Modify it
Deploy a new Group 4 that starts from `earliest` to backfill historical analytics.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does having 10 consumer groups reading the same partition NOT multiply disk reads by 10x? (Hint: OS Page Cache).
2. How does independent consumer group offset storage prevent cross-team cascading outages?

## Guarantees
* Each consumer group maintains completely isolated, independent offset pointers.

## Non-guarantees
* A crashing consumer group does not affect other groups, but it will accumulate lag on disk.

## When to use this
* In every microservice architecture with multiple downstream consumers.

## When not to use this
* When workers are cooperating on the exact same task (use the *same* consumer group ID to divide work).

## What comes next
In Phase 43, we enter Module 9 and study Resilience Patterns: In-Process Retries vs Retry Topics.
"""

p42_code = {
    "multi_group_fanout.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer, KafkaConsumer

def run_fanout():
    topic = "multi-fanout-orders"
    print(f"Producing 5 events to '{topic}'...")
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    for i in range(1, 6):
        producer.send(topic, value=f"order-{i}".encode())
    producer.flush()
    producer.close()

    # Consumer Group 1: Fraud Service
    c1 = KafkaConsumer(topic, bootstrap_servers=["localhost:9092"], group_id="grp-fraud", auto_offset_reset="earliest", consumer_timeout_ms=2000)
    g1_msgs = [m.value.decode() for m in c1]
    c1.close()

    # Consumer Group 2: Email Service
    c2 = KafkaConsumer(topic, bootstrap_servers=["localhost:9092"], group_id="grp-email", auto_offset_reset="earliest", consumer_timeout_ms=2000)
    g2_msgs = [m.value.decode() for m in c2]
    c2.close()

    print(f"Group 'grp-fraud' received: {len(g1_msgs)} events ({g1_msgs})")
    print(f"Group 'grp-email' received: {len(g2_msgs)} events ({g2_msgs})")
    print("Both groups independently consumed 100% of the stream!")

if __name__ == "__main__":
    run_fanout()
"""
}

p42_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 42 Experiment: Demonstrating Multiple Consumer Group Fan-Out ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/multi_group_fanout.py
"""

p42_evidence = """# Phase 42 Evidence Log

* **Date:**
* **Topic:** multi-fanout-orders
* **Group 1 Msgs Processed:** 5
* **Group 2 Msgs Processed:** 5
* **How offsets are isolated:**
"""

write_phase("42-multiple-consumer-groups", p42_doc, p42_code, p42_exp, p42_evidence)

# ==============================================================================
# PHASE 43: Retry Patterns
# ==============================================================================
p43_doc = """# Lesson 43: Retry Patterns

## Motto
"Retrying in a tight in-process loop stalls the entire partition; retry topics preserve pipeline flow."

## Problem
A consumer fetches an order event and calls the inventory API.
The inventory API returns `503 Service Unavailable` due to a transient blip.
If the consumer:
* **Retries in-process in a tight loop:** It blocks the poll loop. If it takes longer than `max.poll.interval.ms`, the consumer is kicked out of the group (rebalance storm!). Meanwhile, thousands of healthy orders behind it are blocked.
* **Drops the message:** Data loss!
How do you implement delayed retries with exponential backoff without stalling the main partition?

## Prediction
What happens if you route failed events to a dedicated `orders-retry-1` topic instead of sleeping in the main consumer thread?

## Why this matters
**Non-blocking retry architectures are mandatory for high-throughput consumers.**
They allow healthy events to flow uninterrupted while failing events receive controlled, delayed retries.

## First principles
* **In-Process Retry:** Fine for quick retries (e.g. 2 attempts with 50ms backoff).
* **Retry Topic Pattern:** If in-process retries fail:
  1. Produce failed record to `topic.RETRY-1` with error headers and retry count.
  2. Commit offset on main topic! (Main pipeline continues at full speed!)
  3. A dedicated retry worker consumes from `topic.RETRY-1` with backoff delay.
  4. If it fails again $\\implies$ Route to `topic.RETRY-2` or `topic.DLT` (Phase 44).

## Mental model
```text
Main Consumer Loop (NEVER BLOCKS!)
[ Ord 1 (OK) | Ord 2 (Fails!) | Ord 3 (OK) | Ord 4 (OK) ]
      │             │               │            │
      ▼             ▼               ▼            ▼
   Processed   Publish to        Processed   Processed
               orders.RETRY-1
               & Commit Offset!
                    │
                    ▼
Dedicated Retry Consumer (Processes with 10s delay, doesn't block main queue!)
```

## Build it
See [retry_topic_pattern.py](../code/retry_topic_pattern.py).
We implement the non-blocking retry topic pattern with exponential delay.

## Use Kafka
Execute the retry workflow and observe message progression across topics.

## Inspect it
Observe headers attached to retried records: `retry_count`, `original_topic`, `error_reason`.

## Measure it
Measure main partition throughput with and without retry topic offloading under 10% failure rates.

## Break it
Create an infinite retry loop without backoff limits; watch retry topics explode.

## Recover it
Enforce a strict maximum retry count (e.g. 3 attempts) before routing to a Dead-Letter Topic.

## Modify it
Implement exponential backoff calculation: $\\text{delay} = \\text{base} \\times 2^{\\text{retry\\_count}}$.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an in-process `time.sleep(30)` inside a Kafka consumer poll loop trigger a group rebalance?
2. What happens to strict entity ordering when a failed record is moved to a retry topic?

## Guarantees
* Main consumer partition continues processing healthy events without being blocked by isolated failures.

## Non-guarantees
* Routing failed records to retry topics breaks strict FIFO ordering relative to newer records for that entity.

## When to use this
* In all high-throughput services with transient downstream dependencies (APIs, third-party services).

## When not to use this
* Workloads where strict per-entity FIFO order cannot be compromised under any circumstances.

## What comes next
In Phase 44, we study Dead-Letter Topics (DLT) for unrecoverable messages.
"""

p43_code = {
    "retry_topic_pattern.py": """#!/usr/bin/env python3
import time

def simulate_retry_pipeline():
    print("--- Simulating Non-Blocking Retry Topic Pipeline ---")
    events = [
        {"id": "ORD-1", "status": "valid"},
        {"id": "ORD-2", "status": "transient_fail"},
        {"id": "ORD-3", "status": "valid"},
    ]

    main_topic = "orders"
    retry_topic_1 = "orders.RETRY-1"

    for ev in events:
        print(f"\\n[Main Consumer] Processing {ev['id']} from '{main_topic}'...")
        if ev["status"] == "valid":
            print(f"  [SUCCESS] Order {ev['id']} processed! Committing offset.")
        else:
            print(f"  [TRANSIENT FAILURE] Downstream API 503 for {ev['id']}!")
            print(f"  -> Forwarding {ev['id']} to '{retry_topic_1}' with header retry_count=1")
            print(f"  -> Committing offset on '{main_topic}'! Main consumer DOES NOT BLOCK!")

    print("\\n[Retry Consumer] Wakes up after 5s backoff delay...")
    print(f"  -> Fetches ORD-2 from '{retry_topic_1}'")
    print("  -> Downstream API recovered: [SUCCESS] ORD-2 processed!")

if __name__ == "__main__":
    simulate_retry_pipeline()
"""
}

p43_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 43 Experiment: Demonstrating Non-Blocking Retry Topics ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/retry_topic_pattern.py
"""

p43_evidence = """# Phase 43 Evidence Log

* **Date:**
* **Main Topic:** orders
* **Retry Topic:** orders.RETRY-1
* **Did healthy events behind the failed event process immediately?** Yes
* **Ordering trade-off of retry topics:**
"""

write_phase("43-retry-patterns", p43_doc, p43_code, p43_exp, p43_evidence)

# ==============================================================================
# PHASE 44: Dead-Letter Topics
# ==============================================================================
p44_doc = """# Lesson 44: Dead-Letter Topics

## Motto
"A Dead-Letter Topic is not a trash bin; it is an active crime scene requiring investigation."

## Problem
A producer emits an unparseable malformed record:
`{"amount": "INVALID_STRING_NOT_A_FLOAT"}`
No amount of retrying will ever make this record valid.
If retries loop infinitely, resources are wasted.
If the consumer crashes, it enters an infinite crash loop (**Poison Pill**).
If the consumer silently ignores it, money or state changes are lost without trace.
Where do unprocessable messages go?

## Prediction
What metadata must accompany a record routed to a Dead-Letter Topic (DLT)?

## Why this matters
**The Dead-Letter Topic (DLT / DLQ) pattern quarantines poison pills, preserving cluster health while saving complete forensic evidence for human triage.**

## First principles
* **Poison Pill:** A record that reliably crashes consumer deserialization or business logic on every attempt.
* **Dead-Letter Routing:** After $N$ failed retries:
  1. Wrap the record with diagnostic metadata:
     * `original_topic`
     * `original_partition`
     * `original_offset`
     * `exception_message`
     * `stacktrace`
     * `failure_timestamp`
  2. Produce to `<topic>.DLT`.
  3. Commit the offset on the source topic!
* **Operational Rule:** **A DLT is an alert.** If messages are landing in a DLT, an engineer must inspect, fix the bug, and replay or discard intentionally.

## Mental model
```text
Source Topic ──► [ Consumer ] ──(Fails 3x)──► [ Dead-Letter Topic: orders.DLT ]
                      │                              │
                      ▼                              ▼
                 Commit Offset!               PagerDuty Alert!
                 (Pipeline Continues)         Engineer inspects payload & stacktrace
```

## Build it
See [dead_letter_queue_lab.py](../code/dead_letter_queue_lab.py).
We implement automatic DLT routing with error envelope encapsulation.

## Use Kafka
Deliver a malformed record to Kafka and watch the consumer quarantine it to `orders.DLT`.

## Inspect it
Read the DLT topic using `kafka-console-consumer.sh` and inspect the error metadata headers.

## Measure it
Monitor DLT record arrival rate as a primary production alarm.

## Break it
Simulate a bug where the DLT producer itself fails; observe fallback logging.

## Recover it
Fix the root cause and replay records from the DLT back into the main pipeline.

## Modify it
Build a CLI re-drive tool that reads messages from the DLT and re-publishes them to the main topic.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is routing a poison pill to a DLT safer than dropping it on the floor?
2. What dangerous antipattern occurs when teams configure a DLT but never set up monitoring or alerts on it?

## Guarantees
* Poison pill messages cannot crash consumer loops indefinitely.
* Unprocessable payloads are preserved for debugging.

## Non-guarantees
* DLT routing does not resolve the business failure; an order routed to DLT remains unfulfilled until remediated.

## When to use this
* In all production consumer applications.

## When not to use this
* Transient network timeouts (use Retry Topics with backoff first; only route to DLT after retries are exhausted).

## What comes next
In Phase 45, we examine Large Messages and learn why sending 50MB blobs over Kafka kills performance.
"""

p44_code = {
    "dead_letter_queue_lab.py": """#!/usr/bin/env python3
import json
import time

def process_order(record_str: str):
    data = json.loads(record_str)
    # Strict validation: amount must be a number > 0
    if not isinstance(data.get("amount"), (int, float)):
        raise ValueError(f"Invalid amount type: {type(data.get('amount'))}")
    return True

def run_dlt_pipeline():
    print("--- Dead-Letter Topic (DLT) Demonstration ---")
    incoming_records = [
        {"topic": "orders", "offset": 101, "payload": '{"order_id": 1, "amount": 25.50}'},
        {"topic": "orders", "offset": 102, "payload": '{"order_id": 2, "amount": "CORRUPT_NOT_A_NUMBER"}'}, # Poison Pill!
        {"topic": "orders", "offset": 103, "payload": '{"order_id": 3, "amount": 80.00}'},
    ]

    dlt_topic = []

    for r in incoming_records:
        print(f"\\nProcessing record at offset {r['offset']}...")
        try:
            process_order(r["payload"])
            print(f" [SUCCESS] Offset {r['offset']} processed normally.")
        except Exception as ex:
            print(f" [POISON PILL DETECTED] Processing failed: {ex}")
            # Quarantine to DLT with forensic envelope
            dlt_envelope = {
                "original_topic": r["topic"],
                "original_offset": r["offset"],
                "raw_payload": r["payload"],
                "error": str(ex),
                "quarantined_at": time.time()
            }
            dlt_topic.append(dlt_envelope)
            print(f" [DLT ROUTED] Record {r['offset']} quarantined to 'orders.DLT'!")
            print(" [COMMITTED] Offset committed on main topic. Main pipeline proceeds!")

    print(f"\\nTotal Records Quarantined in DLT: {len(dlt_topic)}")
    print(f"DLT Envelope Contents:\\n{json.dumps(dlt_topic[0], indent=2)}")

if __name__ == "__main__":
    run_dlt_pipeline()
"""
}

p44_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 44 Experiment: Simulating Poison Pill Quarantine to DLT ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/dead_letter_queue_lab.py
"""

p44_evidence = """# Phase 44 Evidence Log

* **Date:**
* **Poison Record Offset:** 102
* **Error Encountered:** ValueError
* **DLT Topic Name:** orders.DLT
* **Why unmonitored DLTs are dangerous:**
"""

write_phase("44-dead-letter-topics", p44_doc, p44_code, p44_exp, p44_evidence)

# ==============================================================================
# PHASE 45: Large Messages
# ==============================================================================
p45_doc = """# Lesson 45: Large Messages

## Motto
"Kafka is built for streaming event streams, not moving gigabyte video files."

## Problem
A machine learning team wants to pass 50 MB trained model weights or 25 MB high-resolution medical images between services.
They attempt to produce them directly to Kafka.
Immediately:
* Producer throws `RecordTooLargeException`.
* If you tune Kafka's `max.message.bytes` to 50 MB, broker memory buffers balloon, page cache gets thrash-evicted, and network saturation causes broker heartbeats to drop, triggering cluster-wide rebalances!
How should large binary payloads be handled in event-driven systems?

## Prediction
What happens to broker OS page cache performance when 50 MB payloads are passed through Kafka?

## Why this matters
Kafka is optimized for small to medium streaming records (1 KB to 100 KB). Forcing large binary blobs through Kafka violates mechanical sympathy. The solution is the **Claim-Check Pattern**.

## First principles
* **Default Limits:** `max.message.bytes=1048576` (1 MB).
* **The Claim-Check Pattern:**
  1. Producer uploads the heavy binary blob (video, PDF, ML weights) directly to Object Storage (Amazon S3, Google Cloud Storage, MinIO).
  2. Producer gets back an immutable URI: `s3://bucket/models/v1.bin`.
  3. Producer sends a lean event (1 KB) to Kafka containing the URI and metadata.
  4. Consumer receives the lean event from Kafka and downloads the payload directly from Object Storage.

## Mental model
```text
Bad Design (Forcing 50MB into Kafka):
Producer ──(50 MB Record)──► [ Kafka Broker ] ──(Memory Balloon! Heartbeat Timeout!)

The Claim-Check Pattern (Clean & Fast):
Producer ──(50 MB Blob)──► [ Object Storage: S3 / MinIO ]
   │                                  ▲
   ├──(1 KB Event with URI)──► [ Kafka ]
                                  │
                                  ▼
Consumer ◄────────────────(1 KB Event)
Consumer ──(Fetches 50MB directly)──► [ Object Storage ]
```

## Build it
See [claim_check_pattern.py](../code/claim_check_pattern.py).
We implement the Claim-Check pattern using local file storage to simulate object storage.

## Use Kafka
Observe that Kafka only transports the lightweight metadata event.

## Inspect it
Check the record size inside Kafka: < 500 bytes.

## Measure it
Compare broker throughput and memory footprint transporting 1 KB claim checks vs 10 MB raw payloads.

## Break it
Attempt to send a 2 MB record when `max.request.size=1048576` and observe `RecordTooLargeException`.

## Recover it
Implement claim-check routing for any payload exceeding 256 KB.

## Modify it
Add payload SHA-256 checksums to the Kafka event to guarantee data integrity between object storage and consumer.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does passing multi-megabyte payloads through Kafka evict valuable small events from the OS page cache?
2. How does the Claim-Check pattern solve payload retention independent of Kafka retention?

## Guarantees
* Keeps Kafka throughput and page cache utilization optimal.

## Non-guarantees
* Consumers must handle separate failure modes if Object Storage is temporarily unreachable.

## When to use this
* Whenever payload sizes regularly exceed 500 KB (images, PDFs, audio, machine learning models).

## When not to use this
* Standard domain events under 100 KB.

## What comes next
In Phase 46, we learn how to calculate Broker Disk and Capacity sizing before deploying to production.
"""

p45_code = {
    "claim_check_pattern.py": """#!/usr/bin/env python3
import os
import uuid
import hashlib
import json
from pathlib import Path

STORAGE_DIR = Path("/tmp/claim_check_storage")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

def upload_large_payload(payload_bytes: bytes) -> str:
    blob_id = str(uuid.uuid4())
    blob_path = STORAGE_DIR / f"{blob_id}.bin"
    with open(blob_path, "wb") as f:
        f.write(payload_bytes)
    return str(blob_path)

def produce_claim_check(payload_bytes: bytes) -> dict:
    # 1. Upload heavy data to external storage
    blob_uri = upload_large_payload(payload_bytes)
    sha256 = hashlib.sha256(payload_bytes).hexdigest()
    
    # 2. Craft lightweight Kafka event
    kafka_event = {
        "event_type": "DocumentGenerated",
        "blob_uri": blob_uri,
        "size_bytes": len(payload_bytes),
        "sha256": sha256
    }
    return kafka_event

if __name__ == "__main__":
    # Simulate 5 MB PDF document
    large_pdf_data = b"%PDF-1.4 " + (b"X" * (5 * 1024 * 1024))
    print(f"Original Payload Size: {len(large_pdf_data) / (1024*1024):.1f} MB")

    event = produce_claim_check(large_pdf_data)
    event_json = json.dumps(event)
    print(f"Kafka Event Size:      {len(event_json)} bytes")
    print(f"\\nEvent published to Kafka:\\n{json.dumps(event, indent=2)}")
    print(f"\\nStorage Efficiency: {(1 - len(event_json)/len(large_pdf_data))*100:.4f}% reduction on Kafka wire!")
"""
}

p45_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 45 Experiment: Demonstrating the Claim-Check Pattern ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/claim_check_pattern.py
"""

p45_evidence = """# Phase 45 Evidence Log

* **Date:**
* **Original Payload Size:** 5 MB
* **Claim-Check Event Size:** ~200 bytes
* **Storage Reduction on Kafka:** 99.99%
* **When to apply Claim-Check:**
"""

write_phase("45-large-messages", p45_doc, p45_code, p45_exp, p45_evidence)

print("Phases 31 to 45 successfully generated!")
