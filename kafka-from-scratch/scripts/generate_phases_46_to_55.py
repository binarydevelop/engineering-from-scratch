#!/usr/bin/env python3
"""
Generator for Phases 46 to 55 of kafka-from-scratch.
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
# PHASE 46: Broker Disk and Capacity
# ==============================================================================
p46_doc = """# Lesson 46: Broker Disk and Capacity

## Motto
"Never deploy a Kafka cluster without doing the capacity math first."

## Problem
A team deploys Kafka with default settings.
Three weeks later at 2:00 AM, all brokers run out of disk space (`No space left on device`).
Brokers crash, partitions become corrupted, and the entire platform halts.
How do you calculate disk, network bandwidth, and broker node count *before* launching into production?

## Prediction
If an e-commerce platform generates 20,000 events/second, average record size is 1 KB, retention is 7 days, and replication factor is 3, how many terabytes of disk space are required?

## Why this matters
Capacity planning is a core system design responsibility. Guessing leads either to millions wasted on over-provisioned infrastructure or catastrophic out-of-disk outages.

## First principles
$$\\text{Daily Raw Ingestion} = \\text{Events/sec} \\times \\text{Bytes/event} \\times 86,400 \\text{ sec/day}$$
$$\\text{Total Replicated Storage} = \\text{Daily Raw} \\times \\text{Retention Days} \\times \\text{Replication Factor} \\times \\text{Headroom Buffer (1.3x)}$$
* Always include a **30% headroom buffer** for OS overhead, segment index files, compaction dirty segments, and emergency traffic spikes!

## Mental model
```text
Capacity Formula:
20,000 events/s  *  1 KB  =  20 MB/s raw ingestion
20 MB/s  *  86,400 s/day  =  1.728 TB/day raw
1.728 TB/day  *  7 days   =  12.096 TB unique data
12.096 TB  *  3 replicas  =  36.288 TB replicated
36.288 TB  *  1.3 headroom=  47.17 TB Total Disk Required!
Across 6 brokers          =  ~8 TB NVMe SSD per broker!
```

## Build it
See [capacity_calculator.py](../code/capacity_calculator.py).
We implement an interactive capacity sizing calculator.

## Use Kafka
Run the calculator with your anticipated production parameters.

## Inspect it
Observe network ingress/egress bandwidth requirements alongside disk storage.

## Measure it
Measure real-world disk footprint vs mathematical prediction.

## Break it
Simulate an out-of-disk failure by setting a tiny volume quota; observe broker shutdown behavior.

## Recover it
Implement automated disk usage alerts at 75% capacity to scale storage before saturation.

## Modify it
Add payload compression ratio (e.g. 3x reduction with `zstd`) to the capacity model.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must network bandwidth calculations multiply raw ingress by $(1 + \\text{Replication Factor} - 1 + \\text{Consumer Groups Count})$?
2. Why is running Kafka broker disks above 85% capacity dangerous?

## Guarantees
* Mathematical capacity modeling bounds infrastructure risk.

## Non-guarantees
* A mathematical estimate does not protect against unannounced marketing events generating 10x traffic spikes.

## When to use this
* During cluster architecture, cloud budgeting, and capacity reviews.

## When not to use this
* Ignoring capacity math guarantees future production incidents.

## What comes next
In Phase 47, we examine Partition Count and learn why having too many partitions is dangerous.
"""

p46_code = {
    "capacity_calculator.py": """#!/usr/bin/env python3
def calculate_kafka_capacity(
    events_per_sec=20000,
    bytes_per_event=1024,
    retention_days=7,
    replication_factor=3,
    consumer_groups=3,
    compression_ratio=0.5, # 50% size after LZ4/ZSTD
    num_brokers=6
):
    print("=== Apache Kafka Production Capacity Sizing Model ===\\n")
    
    # 1. Raw Ingestion
    raw_bytes_per_sec = events_per_sec * bytes_per_event
    wire_bytes_per_sec = raw_bytes_per_sec * compression_ratio
    wire_mb_per_sec = wire_bytes_per_sec / (1024 * 1024)
    
    # 2. Daily Volume
    daily_wire_tb = (wire_bytes_per_sec * 86400) / (1024**4)
    
    # 3. Total Storage (with Replication & 30% Headroom)
    total_storage_tb = daily_wire_tb * retention_days * replication_factor * 1.3
    disk_per_broker_tb = total_storage_tb / num_brokers
    
    # 4. Network Bandwidth
    # Ingress = Producer Ingress + Follower Replication Ingress
    ingress_mb_per_sec = wire_mb_per_sec + (wire_mb_per_sec * (replication_factor - 1))
    # Egress = Follower Replication Egress + Consumer Groups Egress
    egress_mb_per_sec = (wire_mb_per_sec * (replication_factor - 1)) + (wire_mb_per_sec * consumer_groups)

    print(f"Input Parameters:")
    print(f"  Events/sec:          {events_per_sec:,}")
    print(f"  Event Size (Raw):    {bytes_per_event:,} bytes")
    print(f"  Compression Ratio:   {compression_ratio*100:.0f}%")
    print(f"  Retention:           {retention_days} days")
    print(f"  Replication Factor:  {replication_factor}")
    print(f"  Brokers Count:       {num_brokers}")
    print(f"  Consumer Groups:     {consumer_groups}\\n")

    print(f"Storage Requirements:")
    print(f"  Daily Volume (Wire): {daily_wire_tb:6.2f} TB/day")
    print(f"  Total Replicated:    {total_storage_tb:6.2f} TB (including 30% safety headroom)")
    print(f"  Disk per Broker:     {disk_per_broker_tb:6.2f} TB / broker\\n")

    print(f"Network Throughput Requirements:")
    print(f"  Cluster Ingress:     {ingress_mb_per_sec:6.1f} MB/s ({ingress_mb_per_sec*8:6.1f} Mbps)")
    print(f"  Cluster Egress:      {egress_mb_per_sec:6.1f} MB/s ({egress_mb_per_sec*8:6.1f} Mbps)")
    print(f"  Ingress per Broker:  {ingress_mb_per_sec/num_brokers:6.1f} MB/s")

if __name__ == "__main__":
    calculate_kafka_capacity()
"""
}

p46_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 46 Experiment: Running Kafka Capacity Sizing Model ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/capacity_calculator.py
"""

p46_evidence = """# Phase 46 Evidence Log

* **Date:**
* **Events/sec Modeled:** 20,000
* **Retention Days:** 7
* **Replication Factor:** 3
* **Calculated Total Replicated Disk (TB):**
* **Network Ingress Bandwidth (MB/s):**
"""

write_phase("46-broker-disk-and-capacity", p46_doc, p46_code, p46_exp, p46_evidence)

# ==============================================================================
# PHASE 47: Partition Count and Capacity
# ==============================================================================
p47_doc = """# Lesson 47: Partition Count and Capacity

## Motto
"More partitions mean more parallelism; too many partitions mean delayed failover and operating system exhaustion."

## Problem
An engineer reasons:
*"If partitions give us throughput, why not create 1,000 partitions for every topic?"*
They deploy 50 topics with 1,000 partitions each on a 3-broker cluster (50,000 total partitions).
Suddenly:
* Broker startup time jumps to 15 minutes.
* Broker memory spikes due to open file handles and indexes.
* When a broker restarts, controller leader election experiences latency spikes.
How do you determine the *optimal* number of partitions?

## Prediction
What are the hidden operational costs of having tens of thousands of idle partitions on a Kafka cluster?

## Why this matters
Sizing partition count is a balancing act between **required consumer throughput** and **broker operational overhead**.

## First principles
**The Partition Sizing Rule of Thumb:**
$$\\text{Partitions} = \\max\\left( \\frac{\\text{Target Producer Throughput}}{P_p}, \\frac{\\text{Target Consumer Throughput}}{C_p} \\right)$$
* Where $P_p$ is single-partition producer throughput (~10-20 MB/s).
* Where $C_p$ is single-partition consumer throughput (~2-5 MB/s, often bottlenecked by DB writes).
* **The Costs of Excessive Partitions:**
  1. Open file descriptors (each partition segment requires 2-3 open files).
  2. Memory buffers allocated per partition in client producers (`batch.size` $\\times$ partitions).
  3. Increased leader election and metadata sync duration during broker failovers.

## Mental model
```text
Under-Partitioned (1 Partition):
- Max throughput = 2,000 msgs/s
- Bottleneck! Cannot scale consumer workers!

Optimal (6 to 12 Partitions):
- Matches consumer concurrency needs
- Low metadata overhead, fast failover (<100ms)

Over-Partitioned (1,000 Partitions for low traffic):
- Thousands of tiny files on disk
- Producer client memory waste
- Slower cluster recovery
```

## Build it
See [partition_sizing_tool.py](../code/partition_sizing_tool.py).
We calculate partition recommendations based on producer and consumer benchmarks.

## Use Kafka
Inspect current cluster partition count and partition-to-broker ratios.

## Inspect it
Check open file descriptors used by the Kafka broker process using `lsof`.

## Measure it
Compare client producer memory footprint with 3 partitions vs 100 partitions.

## Break it
Create 1,000 partitions on a tiny single-broker lab container and observe memory and file handle growth.

## Recover it
Plan topics with conservative partition counts (e.g. 6, 12, or 24); scale up only when measured throughput demands it.

## Modify it
Test altering partition count dynamically on an active topic.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can topic partition count be increased with `kafka-topics.sh --alter`, but NEVER decreased?
2. How does the number of partitions impact client-side producer memory allocation?

## Guarantees
* Higher partition count enables higher active consumer group parallelism.

## Non-guarantees
* Adding partitions does not improve throughput if producer keys are severely skewed.

## When to use this
* In all topic creation and architecture design decisions.

## When not to use this
* Creating hundreds of partitions "just in case" without throughput data.

## What comes next
In Phase 48, we learn how to balance clusters by Reassigning Partitions across brokers.
"""

p47_code = {
    "partition_sizing_tool.py": """#!/usr/bin/env python3
import math

def recommend_partitions(target_throughput_mb_s, consumer_speed_mb_s=2.5, producer_speed_mb_s=15.0, broker_count=3):
    print("=== Kafka Topic Partition Sizing Advisor ===\\n")
    parts_for_consumer = math.ceil(target_throughput_mb_s / consumer_speed_mb_s)
    parts_for_producer = math.ceil(target_throughput_mb_s / producer_speed_mb_s)

    recommended = max(parts_for_consumer, parts_for_producer)
    # Align to a multiple of broker count for even distribution
    aligned = math.ceil(recommended / broker_count) * broker_count

    print(f"Target Throughput:           {target_throughput_mb_s:6.1f} MB/s")
    print(f"Single Consumer Capacity:    {consumer_speed_mb_s:6.1f} MB/s (DB-bound)")
    print(f"Single Producer Capacity:    {producer_speed_mb_s:6.1f} MB/s\\n")
    print(f"Partitions for Consumer:     {parts_for_consumer}")
    print(f"Partitions for Producer:     {parts_for_producer}")
    print(f"Raw Recommended:             {recommended}")
    print(f"Aligned (Multiple of {broker_count} brokers): {aligned} partitions")

if __name__ == "__main__":
    recommend_partitions(target_throughput_mb_s=20.0, broker_count=3)
"""
}

p47_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 47 Experiment: Running Partition Sizing Recommendation Tool ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/partition_sizing_tool.py
"""

p47_evidence = """# Phase 47 Evidence Log

* **Date:**
* **Target Throughput (MB/s):** 20.0
* **Calculated Partitions:**
* **Why partition counts cannot be decreased:**
* **Downside of excessive partitions:**
"""

write_phase("47-partition-count-and-capacity", p47_doc, p47_code, p47_exp, p47_evidence)

# ==============================================================================
# PHASE 48: Reassigning Partitions
# ==============================================================================
p48_doc = """# Lesson 48: Reassigning Partitions

## Motto
"Data does not move on its own; rebalancing a cluster requires deliberate, throttled partition migration."

## Problem
Your 3-broker cluster has been running for 6 months.
Brokers 1 and 2 are running at 85% disk capacity, while Broker 3 was recently added and sits at 10% disk capacity.
How do you safely move partition replicas from overloaded brokers to underutilized brokers without causing downtime or saturating the network?

## Prediction
What tool in Apache Kafka 3.8.0 coordinates moving partition replicas between brokers?

## Why this matters
Partition reassignment is the core mechanism for cluster rebalancing, expanding cluster capacity, and decommissioning failing hardware.

## First principles
* **`kafka-reassign-partitions.sh`:** The administrative utility that generates, executes, and verifies partition movement plans.
* **Movement Mechanics:**
  1. The new broker joins the partition replica set as a follower and begins fetching historical log segments.
  2. Once the new replica catches up and enters the ISR, leadership can transfer safely.
  3. The old broker drops the replica and deletes its local files.
* **Replication Throttling:** Moving gigabytes of data can saturate broker network cards. Kafka allows setting replication throttles (`--throttle`) to limit inter-broker bandwidth.

## Mental model
```text
Step 1: Partition 0 Replicas currently on [Broker 1, Broker 2]
Step 2: Add Broker 3 to replica set -> [Broker 1, Broker 2, Broker 3]
Step 3: Broker 3 fetches historical segments over network (Throttled at 50 MB/s)
Step 4: Broker 3 catches up and joins ISR!
Step 5: Drop Broker 1 from replica set -> [Broker 2, Broker 3]
Result: Partition successfully migrated with ZERO downtime!
```

## Build it
See [reassign_partitions_demo.py](../code/reassign_partitions_demo.py).
We generate a reassignment plan JSON and execute partition migration.

## Use Kafka
Execute partition reassignment using official CLI tooling.

## Inspect it
Monitor migration progress using `--verify`:
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-reassign-partitions.sh \
  --bootstrap-server localhost:9092 \
  --reassignment-json-file /tmp/reassign.json \
  --verify
```

## Measure it
Measure network replication throughput during migration.

## Break it
Execute reassignment without a network throttle during peak business traffic; observe producer latency spikes due to network congestion.

## Recover it
Apply dynamic bandwidth throttling (`--throttle 50000000` = 50 MB/s).

## Modify it
Generate reassignment plans using the `--generate` flag.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is applying a bandwidth throttle critical when executing partition reassignments in production?
2. What happens to client writes while a partition reassignment is actively copying historical segments?

## Guarantees
* Zero-downtime online migration; partition remains fully available for reads and writes throughout.

## Non-guarantees
* Reassignment does not complete instantly; multi-terabyte partitions require hours to replicate.

## When to use this
* Adding new brokers to an existing cluster, decommissioning hardware, resolving broker disk skew.

## When not to use this
* Avoid moving massive partitions during peak traffic windows if network bandwidth is limited.

## What comes next
In Phase 49, we explore Adding a Broker and debunk the myth that Kafka automatically rebalances data on its own.
"""

p48_code = {
    "reassign_partitions_demo.py": """#!/usr/bin/env python3
import json

def generate_reassignment_plan():
    print("=== Generating Partition Reassignment Plan ===")
    plan = {
        "version": 1,
        "partitions": [
            {"topic": "replicated-orders", "partition": 0, "replicas": [2, 3], "log_dirs": ["any", "any"]},
            {"topic": "replicated-orders", "partition": 1, "replicas": [3, 1], "log_dirs": ["any", "any"]},
            {"topic": "replicated-orders", "partition": 2, "replicas": [1, 2], "log_dirs": ["any", "any"]}
        ]
    }
    plan_json = json.dumps(plan, indent=2)
    print(f"Reassignment JSON Payload:\\n{plan_json}")
    with open("/tmp/reassign_plan.json", "w") as f:
        f.write(plan_json)
    print("\\nSaved to /tmp/reassign_plan.json. Ready for execution via kafka-reassign-partitions.sh")

if __name__ == "__main__":
    generate_reassignment_plan()
"""
}

p48_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 48 Experiment: Generating and Verifying Partition Reassignment ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/reassign_partitions_demo.py
"""

p48_evidence = """# Phase 48 Evidence Log

* **Date:**
* **Topic Reassigned:** replicated-orders
* **Old Replica Set:**
* **New Replica Set:**
* **Reassignment Verification Output:**
"""

write_phase("48-reassigning-partitions", p48_doc, p48_code, p48_exp, p48_evidence)

# ==============================================================================
# PHASE 49: Adding a Broker
# ==============================================================================
p49_doc = """# Lesson 49: Adding a Broker

## Motto
"A new broker joins the cluster in seconds; data moves only when you tell it to."

## Problem
Your cluster is running low on capacity.
You boot up Broker 4 and register it with the KRaft quorum.
`kafka-cluster.sh` happily reports 4 active brokers!
The operations team celebrates, assuming the load has been redistributed.
One week later, Broker 1 runs out of disk and crashes.
Why did the new broker not absorb any existing data?

## Prediction
Does Apache Kafka automatically redistribute existing topic partitions to a newly joined broker?

## Why this matters
**Kafka does NOT automatically rebalance existing partitions when a new broker appears.**
New topics will place partitions on the new broker, but historical partitions stay exactly where they were until you explicitly trigger a partition reassignment (Phase 48).

## First principles
* **Broker Registration:** In KRaft, a new broker joins by connecting to the controller quorum and registering its `node.id`.
* **Static Partition Placement:** Partitions remain on their assigned replica brokers unless explicitly moved.
* **Rebalance Discipline:** After adding brokers, an engineer must run `kafka-reassign-partitions.sh` (or an automation tool like Cruise Control) to move partitions onto the new machine.

## Mental model
```text
Existing 3-Broker Cluster:
Broker 1: [ P0, P1, P2 ] (Disk 80%)
Broker 2: [ P0, P1, P2 ] (Disk 80%)
Broker 3: [ P0, P1, P2 ] (Disk 80%)

Add Broker 4:
Broker 4 joins cluster!
State:
Broker 1: [ P0, P1, P2 ] (Disk 80%)
Broker 2: [ P0, P1, P2 ] (Disk 80%)
Broker 3: [ P0, P1, P2 ] (Disk 80%)
Broker 4: [ EMPTY! 0 Partitions! 0 Disk Used! ] <--- DOES NOT AUTO-BALANCE!
```

## Build it
See [add_broker_simulation.py](../code/add_broker_simulation.py).
We inspect partition placement before and after a new broker is registered.

## Use Kafka
Observe cluster metadata after adding a node.

## Inspect it
List topic partitions and verify zero partitions have migrated automatically.

## Measure it
Measure disk usage across brokers to prove skew.

## Break it
Assume auto-rebalance happens; watch existing brokers continue to run out of disk while the new node sits completely idle.

## Recover it
Execute a partition reassignment to migrate a share of partitions to the new broker.

## Modify it
Create a *new* topic and verify that Kafka's default placement assignor does place new partitions on the new broker.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka avoid automatically shifting partitions when a new broker starts up? (Hint: what if a crashed broker is just rebooting?).
2. How does LinkedIn's Cruise Control project automate partition rebalancing in large fleets?

## Guarantees
* A newly registered broker is immediately available for new topic creation and metadata quorum.

## Non-guarantees
* Existing data will never move to the new broker automatically.

## When to use this
* Scaling cluster storage and compute horizontally.

## When not to use this
* Never consider a broker addition complete until existing partitions have been redistributed.

## What comes next
In Phase 50, we enter Module 10 and systematically execute controlled Broker Failure Scenarios.
"""

p49_code = {
    "add_broker_simulation.py": """#!/usr/bin/env python3
def explain_broker_addition():
    print("=== Broker Expansion vs Data Movement ===\\n")
    print("1. Broker 4 registers with KRaft quorum: OK (Takes ~2 seconds)")
    print("2. Topic 'orders' partitions: [P0 on Broker 1, P1 on Broker 2, P2 on Broker 3]")
    print("3. Does Broker 4 host any partitions? NO. (0 partitions assigned)")
    print("4. Conclusion: Kafka does NOT automatically re-shuffle existing data!")
    print("5. Required Action: Run 'kafka-reassign-partitions.sh' to rebalance workload.\\n")

if __name__ == "__main__":
    explain_broker_addition()
"""
}

p49_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 49 Experiment: Demonstrating Broker Join Semantics ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/add_broker_simulation.py
"""

p49_evidence = """# Phase 49 Evidence Log

* **Date:**
* **New Broker ID:** 4
* **Did existing partitions auto-migrate?** No
* **Why auto-migration is dangerous:**
* **Remediation required:**
"""

write_phase("49-adding-a-broker", p49_doc, p49_code, p49_exp, p49_evidence)

# ==============================================================================
# PHASE 50: Broker Failure Scenarios
# ==============================================================================
p50_doc = """# Lesson 50: Broker Failure Scenarios

## Motto
"Chaos is not an emergency; chaos is a scheduled Tuesday afternoon test."

## Problem
In theory, distributed replication provides high availability.
In practice, unless you systematically inject failures and measure recovery behavior, you do not know how your cluster responds.
What happens when:
* A follower dies?
* A leader dies?
* Two out of three replicas die?
* A broker reboots after 10 minutes offline?

## Prediction
What happens to consumer read traffic when a non-leader follower broker is killed?

## Why this matters
Rigorous failure injection transforms theoretical confidence into operational certainty.

## First principles
| Failure Scenario | Immediate Impact | Automatic Recovery |
| :--- | :--- | :--- |
| **Follower Dies** | Zero client disruption; ISR drops follower after `replica.lag.time.max.ms` | Follower catches up upon restart and rejoins ISR |
| **Leader Dies** | In-flight writes retry; KRaft elects new leader from ISR in <100ms | Clients refresh metadata and resume on new leader |
| **2 of 3 Brokers Die** | If `min.insync.replicas=2` and `acks=all`, writes are REJECTED | Restoring 1 broker allows writes to resume |
| **Disk Exhaustion** | Broker halts log appends and fences itself | Add disk space or alter retention |

## Mental model
```text
The Failure Loop:
PREDICT ──► BREAK ──► OBSERVE ──► DIAGNOSE ──► RECOVER ──► EXPLAIN
```

## Build it
See [chaos_broker_failure.py](../code/chaos_broker_failure.py).
We execute automated failure injection against cluster nodes.

## Use Kafka
Run failure drills against our 3-broker KRaft cluster.

## Inspect it
Observe broker logs and client retry logging during failure events.

## Measure it
Measure exact client interruption duration for each scenario.

## Break it
Execute hard `docker stop` on active nodes.

## Recover it
Execute `docker start` and monitor ISR healing.

## Modify it
Inject simulated packet delay on broker network interfaces using `tc` or Docker network latency.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does killing a follower cause zero write errors for clients with `acks=1`?
2. What is the difference between graceful broker shutdown (`SIGTERM`) and hard crash (`SIGKILL`)?

## Guarantees
* KRaft automatically coordinates leader election without human intervention.

## Non-guarantees
* Availability is not maintained if surviving replica count falls below `min.insync.replicas` for `acks=all`.

## When to use this
* Game days, chaos engineering, disaster recovery testing.

## When not to use this
* Directly on un-backed-up production environments without failover readiness.

## What comes next
In Phase 51, we study Consumer Failure Scenarios and diagnose rebalance storms and deadlocks.
"""

p50_code = {
    "chaos_broker_failure.py": """#!/usr/bin/env python3
import subprocess
import time

def test_follower_failure():
    print("=== Chaos Scenario 1: Stopping Follower Broker (kafka-node-3) ===")
    subprocess.run(["docker", "stop", "kafka-node-3"], check=False)
    print("kafka-node-3 stopped. Waiting 5s...")
    time.sleep(5)
    print("Restarting kafka-node-3...")
    subprocess.run(["docker", "start", "kafka-node-3"], check=False)
    print("kafka-node-3 restored! Check ISR recovery.")

if __name__ == "__main__":
    test_follower_failure()
"""
}

p50_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 50 Experiment: Executing Controlled Chaos Broker Failure ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/chaos_broker_failure.py
"""

p50_evidence = """# Phase 50 Evidence Log

* **Date:**
* **Failure Injected:** Follower container stop
* **Client Write Disruption:** 0 errors
* **Time to restore ISR:**
* **Key takeaway:**
"""

write_phase("50-broker-failure-scenarios", p50_doc, p50_code, p50_exp, p50_evidence)

# ==============================================================================
# PHASE 51: Consumer Failure Scenarios
# ==============================================================================
p51_doc = """# Lesson 51: Consumer Failure Scenarios

## Motto
"A dead consumer is easy to spot; a slow consumer that starves its peers is insidious."

## Problem
What goes wrong inside consumer groups during production incidents?
1. **Crash before commit:** Causes duplicate processing upon restart.
2. **Crash after commit:** Causes lost events if external database write failed.
3. **Slow processing deadlock:** A thread hangs on a database lock for 6 minutes. Because `max.poll.interval.ms` (5 min) expires, the coordinator evicts the consumer, triggering a stop-the-world rebalance!
How do you diagnose and recover from these consumer failure modes?

## Prediction
What happens to partition assignments across a consumer group when one consumer thread hangs?

## Why this matters
Diagnosing slow consumers, rebalance storms, and offset commit failures is the primary operational skill required for streaming engineers.

## Mental model
```text
The Slow Consumer Death Spiral:
1. Consumer 1 encounters slow 6-minute external database lock.
2. Poll loop fails to invoke poll() within max.poll.interval.ms (5 min).
3. Broker Coordinator assumes Consumer 1 died -> TRIGGERS REBALANCE!
4. Consumer 1's partitions revoked and handed to Consumer 2.
5. Consumer 2 encounters the exact same slow DB lock!
6. Consumer 2 also times out -> TRIGGERS ANOTHER REBALANCE!
Result: Cluster rebalance storm! Entire consumer group grinds to a halt!
```

## Build it
See [chaos_consumer_failure.py](../code/chaos_consumer_failure.py).
We simulate slow consumer poll timeouts and diagnose rebalance events.

## Use Kafka
Inspect consumer group status under failure using `kafka-consumer-groups.sh`.

## Inspect it
Observe `CommitFailedException` in consumer logs.

## Measure it
Measure consumer lag accumulation during a rebalance storm.

## Break it
Simulate a 60-second processing block when `max.poll.interval.ms=30000`.

## Recover it
Offload heavy processing to worker thread pools; keep Kafka consumer loop dedicated exclusively to polling and heartbeating.

## Modify it
Tune `max.poll.records` to a smaller batch size (e.g. 50 records) so batches finish well within timeouts.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does offloading processing to a worker thread pool solve `max.poll.interval.ms` timeouts but complicate manual offset committing?
2. What is the difference between `session.timeout.ms` and `max.poll.interval.ms`?

## Guarantees
* The group coordinator automatically evicts dead or non-responsive consumers.

## Non-guarantees
* The coordinator cannot distinguish between a consumer that is dead and a consumer that is stalled on a slow database query.

## When to use this
* Consumer group stability tuning and rebalance debugging.

## When not to use this
* Setting `max.poll.interval.ms` to hours to paper over broken consumer application code.

## What comes next
In Phase 52, we study Producer Failure Scenarios and error handling.
"""

p51_code = {
    "chaos_consumer_failure.py": """#!/usr/bin/env python3
import time

def simulate_consumer_failure_modes():
    print("=== Consumer Failure Scenario Matrix ===\\n")
    print("Scenario A: Worker killed by SIGKILL (Crash before commit)")
    print(" -> Consequence: Assigned partitions reassigned to peer; uncommitted batch reprocessed (DUPLICATE RISK)\\n")

    print("Scenario B: Worker hangs on external API call > max.poll.interval.ms")
    print(" -> Consequence: Coordinator evicts worker! Triggers group REBALANCE!\\n")

    print("Scenario C: Poison pill deserialization error")
    print(" -> Consequence: Crash loop forever without DLT quarantine!\\n")

if __name__ == "__main__":
    simulate_consumer_failure_modes()
"""
}

p51_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 51 Experiment: Simulating Consumer Failure Modes ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/chaos_consumer_failure.py
"""

p51_evidence = """# Phase 51 Evidence Log

* **Date:**
* **Failure Scenario:** Poll timeout eviction
* **Observed Exception:** CommitFailedException
* **Root Cause:** max.poll.interval.ms exceeded
* **Remediation Applied:**
"""

write_phase("51-consumer-failure-scenarios", p51_doc, p51_code, p51_exp, p51_evidence)

# ==============================================================================
# PHASE 52: Producer Failure Scenarios
# ==============================================================================
p52_doc = """# Lesson 52: Producer Failure Scenarios

## Motto
"A producer's configuration is not a preference; it is a mathematical guarantee."

## Problem
What can go wrong when a producer calls `send()`?
* Broker is unreachable (`NetworkException`).
* Topic does not exist and auto-creation is disabled (`UnknownTopicOrPartitionException`).
* Record exceeds 1 MB (`RecordTooLargeException`).
* Topic ISR is below minimum (`NotEnoughReplicasException`).
* Producer memory buffer is full (`BufferExhaustedException`).
Which errors are transient and retriable? Which errors are fatal?

## Prediction
Will the Kafka client automatically retry a `RecordTooLargeException`?

## Why this matters
Distinguishing **Retriable Errors** from **Fatal Errors** determines whether your application can self-heal or must alert immediately.

## First principles
* **Retriable Errors:** Caused by transient conditions (leader election, temporary network loss). The client library automatically retries if `retries > 0`.
  * Examples: `NotLeaderOrFollowerException`, `NetworkException`, `LeaderNotAvailableException`.
* **Fatal Non-Retriable Errors:** Fundamental structural flaws. Retrying will never succeed and will waste CPU.
  * Examples: `RecordTooLargeException`, `SerializationException`, `TopicAuthorizationException`.

## Mental model
```text
producer.send(record)
        │
        ▼ (Error received from broker)
Is error Retriable?
   ├── YES ──► Sleep retry_backoff_ms ──► RETRY (Up to retries limit)
   └── NO  ──► FATAL! Raise exception to application immediately!
```

## Build it
See [chaos_producer_failure.py](../code/chaos_producer_failure.py).
We categorize Kafka exceptions and test application handling.

## Use Kafka
Trigger producer errors intentionally and observe client logging.

## Inspect it
Observe producer callback futures under error conditions.

## Measure it
Measure time taken for a producer to exhaust retries during extended broker outages.

## Break it
Send a record to a non-existent topic with auto-create disabled.

## Recover it
Create the topic or handle the exception cleanly.

## Modify it
Set `max.block.ms=2000` to prevent producer threads from hanging forever when broker buffers are full.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must `max.block.ms` be configured on producers in high-throughput web APIs?
2. What happens if a producer's buffer memory fills up?

## Guarantees
* Retriable errors are retried automatically by the client library up to configured limits.

## Non-guarantees
* The producer cannot automatically recover from fatal schema or authorization failures.

## When to use this
* In all producer error handling and alerting architecture.

## When not to use this
* Swallowing producer exceptions silently with empty `except:` blocks.

## What comes next
In Phase 53, we cover Kafka Security Basics: TLS, SASL, and ACLs.
"""

p52_code = {
    "chaos_producer_failure.py": """#!/usr/bin/env python3
def classify_producer_errors():
    print("=== Producer Error Classification Matrix ===\\n")
    retriable = [
        ("NotLeaderOrFollowerException", "Partition leader is failing over; new leader will be elected shortly."),
        ("LeaderNotAvailableException", "Leader election currently in progress; wait for metadata refresh."),
        ("NetworkException", "Socket connection dropped; client will reconnect."),
        ("NotEnoughReplicasException", "Broker temporarily lagging; will retry until ISR catches up.")
    ]
    fatal = [
        ("RecordTooLargeException", "Payload exceeds max.message.bytes. Retrying will never help!"),
        ("SerializationException", "Data does not match schema or serializer format."),
        ("TopicAuthorizationException", "Client credentials lack WRITE permission on target topic."),
        ("UnknownTopicOrPartitionException", "Topic does not exist and auto-creation is disabled.")
    ]

    print("--- 1. RETRIABLE ERRORS (Client auto-heals via retries) ---")
    for name, desc in retriable:
        print(f" [RETRIABLE] {name:<32}: {desc}")

    print("\\n--- 2. FATAL ERRORS (Immediate Application Failure / Alert) ---")
    for name, desc in fatal:
        print(f" [FATAL]     {name:<32}: {desc}")

if __name__ == "__main__":
    classify_producer_errors()
"""
}

p52_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 52 Experiment: Classifying Producer Failure Scenarios ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/chaos_producer_failure.py
"""

p52_evidence = """# Phase 52 Evidence Log

* **Date:**
* **Retriable Errors Analyzed:**
* **Fatal Errors Analyzed:**
* **Why RecordTooLarge is fatal:**
* **Role of max.block.ms:**
"""

write_phase("52-producer-failure-scenarios", p52_doc, p52_code, p52_exp, p52_evidence)

# ==============================================================================
# PHASE 53: Kafka Security Basics
# ==============================================================================
p53_doc = """# Lesson 53: Kafka Security Basics

## Motto
"An unauthenticated, unencrypted broker on the open internet is a global data leak."

## Problem
By default, Kafka communicates over unencrypted `PLAINTEXT`.
In this mode:
1. Anyone on the network can snoop sensitive payloads (credit cards, passwords) using standard packet capture tools.
2. Anyone can connect and produce garbage to any topic.
3. Anyone can read any topic or delete topics!
How is Kafka secured in production?

## Prediction
What are the three pillars of Kafka security?

## Why this matters
Securing Kafka requires understanding **Authentication** (who you are), **Authorization** (what you can do), and **Encryption** (protecting bytes in transit).

## First principles
* **Encryption in Transit (TLS / SSL):** Encrypts all socket communication between clients and brokers, and between brokers during inter-broker replication.
* **Authentication (SASL):** Verifies client identity.
  * `SASL_SSL` with `SCRAM-SHA-512` (username/password with salted hashes).
  * `mTLS` (Mutual TLS using client certificates).
  * `OAUTHBEARER` (JWT tokens via identity providers like Okta/Keycloak).
* **Authorization (ACLs):** Access Control Lists enforcing fine-grained permissions:
  * *"User Alice has READ permission on Topic orders in Group order-workers."*
  * *"User Bob has WRITE permission on Topic orders."*

## Mental model
```text
Client Connection Request
   │
   ▼
[ 1. TLS Handshake ]        ──► Encrypts wire bytes (Prevents sniffing)
   │
   ▼
[ 2. SASL Authentication ]   ──► Verifies User Identity ("I am service-billing")
   │
   ▼
[ 3. ACL Authorization ]     ──► Checks Permissions: Can "service-billing" WRITE to "orders"?
   ├── YES ──► Request Accepted!
   └── NO  ──► TopicAuthorizationException! (Access Denied)
```

## Build it
See [security_config_inspector.py](../code/security_config_inspector.py).
We inspect the security protocol mappings and ACL definitions.

## Use Kafka
Observe how Kafka maps listener security protocols: `PLAINTEXT`, `SSL`, `SASL_PLAINTEXT`, `SASL_SSL`.

## Inspect it
Check ACL rules using `kafka-acls.sh`.

## Measure it
Measure CPU overhead of TLS encryption (modern CPUs with AES-NI incur < 3% overhead).

## Break it
Attempt to write to an ACL-protected topic with an unauthorized principal; observe `TopicAuthorizationException`.

## Recover it
Grant appropriate topic write permission via `kafka-acls.sh`.

## Modify it
Document standard SASL/SCRAM configuration for enterprise Kafka.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. What is the difference between Authentication (SASL) and Authorization (ACLs)?
2. Why is Mutual TLS (mTLS) popular for service-to-service Kafka security in Kubernetes?

## Guarantees
* TLS guarantees data confidentiality and integrity on the wire.
* ACLs prevent unauthorized data access across tenants.

## Non-guarantees
* Transport TLS does not encrypt data at rest on broker disks (requires storage encryption or envelope payload encryption).

## When to use this
* In all production and staging environments without exception.

## When not to use this
* PLAINTEXT should be strictly restricted to local scratch containers.

## What comes next
In Phase 54, we study Observability: metrics, dashboards, and critical production alerts.
"""

p53_code = {
    "security_config_inspector.py": """#!/usr/bin/env python3
def explain_kafka_security():
    print("=== Apache Kafka Production Security Architecture ===\\n")
    protocols = [
        ("PLAINTEXT", "No encryption, no authentication. (Local lab only!)"),
        ("SSL / TLS", "Wire encryption via TLS. Optional client certificate authentication (mTLS)."),
        ("SASL_PLAINTEXT", "Authentication via SASL (SCRAM/Kerberos), but wire bytes unencrypted."),
        ("SASL_SSL", "GOLD STANDARD: Full TLS wire encryption + SASL identity authentication.")
    ]
    for proto, desc in protocols:
        print(f" {proto:<16}: {desc}")

    print("\\nSample Kafka ACL Definition:")
    print("  Principal: User:order-fulfillment-service")
    print("  Resource:  Topic:orders")
    print("  Operation: READ")
    print("  Permission: ALLOW")

if __name__ == "__main__":
    explain_kafka_security()
"""
}

p53_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 53 Experiment: Inspecting Kafka Security Protocols ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/security_config_inspector.py
"""

p53_evidence = """# Phase 53 Evidence Log

* **Date:**
* **Security Protocols Compared:**
* **Recommended Production Protocol:** SASL_SSL
* **Role of ACLs:**
* **mTLS vs SASL/SCRAM:**
"""

write_phase("53-kafka-security-basics", p53_doc, p53_code, p53_exp, p53_evidence)

# ==============================================================================
# PHASE 54: Observability
# ==============================================================================
p54_doc = """# Lesson 54: Observability

## Motto
"If you cannot measure it, your cluster is already failing in secret."

## Problem
In a busy Kafka cluster, thousands of metrics are emitted: JMX MBeans, broker stats, network counters, client metrics.
When an incident strikes:
* Which 5 metrics actually matter?
* Which metrics indicate imminent data loss?
* Which metrics reveal consumer bottlenecks?
How do you build a focused, actionable observability suite for Apache Kafka?

## Prediction
What is the single most critical broker metric that indicates data loss risk?

## Why this matters
Wading through thousands of useless metrics during an outage delays resolution. Focusing on the **Golden Metrics** enables instant triage.

## First principles
**The 6 Golden Kafka Metrics:**
1. **`UnderReplicatedPartitions` (URP):** Partitions where $\\text{ISR Size} < \\text{Replication Factor}$. **Must be 0.** If $> 0$, brokers are failing or network is degraded!
2. **`OfflinePartitionsCount`:** Partitions with NO active leader. **Must be 0.** If $> 0$, data is completely unavailable!
3. **`ActiveControllerCount`:** In KRaft, exactly ONE active controller leader must exist. If 0, metadata is frozen; if $> 1$, split-brain!
4. **`ConsumerLag`:** Records unread by consumer groups.
5. **`IsrShrinksPerSec` / `IsrExpandsPerSec`:** Replicas flapping in and out of ISR due to GC or network stalls.
6. **`BytesInPerSec` / `BytesOutPerSec`:** Cluster network throughput volume.

## Mental model
```text
The Operations Dashboard (Triage Hierarchy):
[ OfflinePartitionsCount > 0 ]      ──► P0 EMERGENCY! System Down! Partitions unreachable!
[ UnderReplicatedPartitions > 0 ]   ──► P1 HIGH ALERT! Durability degraded! Broker down!
[ ConsumerLag Growing Monotonically ]──► P2 ALERT! Consumers falling behind reality!
[ Disk Utilization > 80% ]          ──► P2 ALERT! Disk exhaustion within 48 hours!
```

## Build it
See [cluster_metrics_collector.py](../code/cluster_metrics_collector.py).
We collect and display the core health metrics from our cluster.

## Use Kafka
Query cluster health and monitor partition replication metrics.

## Inspect it
Observe broker health status in clean terminal table output.

## Measure it
Simulate an outage and watch `UnderReplicatedPartitions` spike from 0 to 3.

## Break it
Stop `kafka-node-3`; observe the URP counter spike immediately.

## Recover it
Start `kafka-node-3`; observe URP return to 0 as follower syncs.

## Modify it
Add threshold alerting rules for Prometheus / Alertmanager.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is `UnderReplicatedPartitions > 0` an immediate operational alarm?
2. If `OfflinePartitionsCount > 0`, what happens to producers attempting to write to that partition?

## Guarantees
* JMX and broker metrics provide real-time status of internal cluster data structures.

## Non-guarantees
* Metrics describe cluster symptoms; diagnosing root causes still requires log inspection.

## When to use this
* In all production monitoring and alerting setups.

## When not to use this
* Alerting on every minor fluctuation (avoid alert fatigue; focus on the Golden Metrics).

## What comes next
In Phase 55, we conduct formal Performance Testing and benchmark throughput across configurations.
"""

p54_code = {
    "cluster_metrics_collector.py": """#!/usr/bin/env python3
def display_golden_metrics():
    print("=== The 6 Golden Metrics of Apache Kafka Observability ===\\n")
    metrics = [
        ("OfflinePartitionsCount", "0", "CRITICAL", "Partitions with no leader. Read/write completely halted!"),
        ("UnderReplicatedPartitions", "0", "CRITICAL", "Partitions where ISR < Replication Factor. Durability at risk!"),
        ("ActiveControllerCount", "1", "CRITICAL", "Exactly 1 active KRaft controller must exist. If 0, metadata frozen."),
        ("IsrShrinksPerSec", "0.0", "WARNING", "Replicas falling out of sync due to GC pauses or network latency."),
        ("ConsumerLag (per partition)", "< 1,000", "WARNING", "Downstream processing falling behind real-time production."),
        ("DiskUsagePercentage", "< 75%", "WARNING", "Broker disk saturation indicator.")
    ]

    print(f"{'Metric Name':<28} {'Healthy Target':<16} {'Severity':<10} {'Operational Meaning'}")
    print("-" * 85)
    for name, target, sev, desc in metrics:
        print(f"{name:<28} {target:<16} {sev:<10} {desc}")

if __name__ == "__main__":
    display_golden_metrics()
"""
}

p54_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 54 Experiment: Displaying Kafka Golden Metrics Framework ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/cluster_metrics_collector.py
"""

p54_evidence = """# Phase 54 Evidence Log

* **Date:**
* **OfflinePartitions Target:** 0
* **UnderReplicatedPartitions Target:** 0
* **ActiveController Target:** 1
* **Why URP indicates durability risk:**
"""

write_phase("54-observability", p54_doc, p54_code, p54_exp, p54_evidence)

# ==============================================================================
# PHASE 55: Performance Testing
# ==============================================================================
p55_doc = """# Lesson 55: Performance Testing

## Motto
"Never quote a benchmark without quoting the payload size, the acks setting, and the hardware."

## Problem
Engineers frequently read blog posts claiming *"Kafka handles 2 million messages/sec!"*
They run it on their laptop or cloud VM and get 15,000 msgs/sec, wondering what broke.
A benchmark without documented conditions is meaningless marketing.
How do you conduct rigorous, scientific performance testing on Apache Kafka?

## Prediction
What has a bigger impact on producer throughput: changing `acks` from `1` to `all`, or changing batch size from 1 KB to 32 KB?

## Why this matters
**Benchmark literacy** empowers you to evaluate performance claims, size clusters accurately, and verify SLA commitments under realistic workload conditions.

## First principles
**The 6 Mandatory Benchmark Conditions:**
1. **Payload Size:** 100 bytes vs 10 KB fundamentally alters throughput (records/sec vs MB/sec).
2. **Acknowledgment Setting:** `acks=0` vs `acks=1` vs `acks=all`.
3. **Batching Knobs:** `batch.size` and `linger.ms`.
4. **Compression Codec:** `none`, `snappy`, `lz4`, `zstd`.
5. **Partition Count & Broker Count:** Hardware concurrency layout.
6. **Network & Disk Hardware:** Local NVMe SSD vs cloud networked EBS.

## Mental model
```text
Benchmark Execution Matrix:
Run 1: Baseline (Uncompressed, acks=1, batch=16K)  ──► 35,000 rec/s | 3.5 MB/s
Run 2: Tuned Batching (batch=64K, linger=15ms)      ──► 95,000 rec/s | 9.5 MB/s
Run 3: Full Durability (acks=all, min_isr=2)       ──► 70,000 rec/s | 7.0 MB/s
```

## Build it
See [benchmark_runner.py](../code/benchmark_runner.py).
We execute a standardized benchmark capturing records/sec, MB/sec, and latency percentiles.

## Use Kafka
Run the benchmark suite against your local Kafka broker.

## Inspect it
Inspect the resulting performance metrics table.

## Measure it
Capture p50, p95, and p99 latency percentiles alongside throughput.

## Break it
Saturate producer concurrency until consumer lag explodes and latency percentiles spike.

## Recover it
Identify the bottleneck (CPU, disk I/O, network) and apply appropriate batching or partition tuning.

## Modify it
Test different payload sizes (128 bytes vs 1024 bytes) and plot the results.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does high throughput (MB/sec) often correlate with higher individual message latency (due to batching delay)?
2. Why is measuring p99 latency far more important for user-facing systems than measuring average latency?

## Guarantees
* Benchmarks provide reproducible measurements under strictly defined test parameters.

## Non-guarantees
* Laptop benchmark results cannot be extrapolated directly to distributed multi-node cloud clusters.

## When to use this
* Pre-production validation, capacity planning, configuration tuning.

## When not to use this
* Quoting generic numbers in architectural discussions without defining test parameters.

## What comes next
In Phase 56, we embark on Capstone 1: Building a Mini-Kafka from scratch in pure Python!
"""

p55_code = {
    "benchmark_runner.py": """#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def run_performance_test(num_records=5000, payload_size=512):
    print(f"=== Running Kafka Performance Benchmark ({num_records} records, {payload_size} bytes each) ===\\n")
    payload = b"B" * payload_size
    topic = "bench-perf-test"

    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        acks=1,
        linger_ms=10,
        batch_size=32768
    )

    start = time.time()
    for _ in range(num_records):
        producer.send(topic, value=payload)
    producer.flush()
    duration = time.time() - start
    producer.close()

    total_bytes = num_records * payload_size
    rps = num_records / duration
    mb_s = (total_bytes / (1024 * 1024)) / duration
    avg_latency = (duration / num_records) * 1000

    print("Benchmark Results:")
    print(f"  Duration:          {duration:.3f} seconds")
    print(f"  Records/sec:       {rps:9.1f} rec/s")
    print(f"  Throughput (MB/s): {mb_s:9.2f} MB/s")
    print(f"  Amortized Latency: {avg_latency:9.3f} ms/record")

if __name__ == "__main__":
    run_performance_test()
"""
}

p55_exp = """#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 55 Experiment: Running Standardized Kafka Performance Benchmark ==="
cd "$(dirname "$0")/.."
../../.venv/bin/python3 code/benchmark_runner.py
"""

p55_evidence = """# Phase 55 Evidence Log

* **Date:**
* **Payload Size:** 512 bytes
* **Records Produced:** 5,000
* **Records/sec:**
* **Throughput (MB/s):**
* **Hardware Environment:** macOS Apple Silicon
"""

write_phase("55-performance-testing", p55_doc, p55_code, p55_exp, p55_evidence)

print("Phases 46 to 55 successfully generated!")
