# Kafka Mental Models & Systems Architecture

> **The Core Realization:**
> Kafka is not a message queue.
> Kafka is a distributed, replicated, partitioned append-only log with producer, consumer, storage, and coordination semantics layered around it.

---

## 1. Traditional Message Queue vs. Distributed Log

### Traditional Queue (e.g., RabbitMQ, SQS)
Records are transient work items. Consumers pop messages; upon acknowledgment, the broker destructively removes the message from the queue.

```text
Producer ───► [ M1 | M2 | M3 | M4 ] ───► Consumer A (pops M1 -> deleted)
                                     └──► Consumer B (pops M2 -> deleted)
```
* **Destructive reads:** Once read and acked, the message is gone.
* **No historical replay:** A new service cannot read historical data from 3 days ago.
* **Workload contention:** All consumers compete for the head of the same queue.

### Kafka Distributed Append-Only Log
Records are persistent, ordered events in an immutable sequence. Reading is non-destructive. Consumers merely track a pointer (offset).

```text
Topic: "orders" (Partition 0)
Offset:     0        1        2        3        4        5        6 (LEO)
         ┌────────┬────────┬────────┬────────┬────────┬────────┐
 Log:    │ Ord-01 │ Ord-02 │ Ord-03 │ Ord-04 │ Ord-05 │ Ord-06 │ ...
         └────────┴────────┴────────┴────────┴────────┴────────┘
                      ▲                          ▲
                      │                          │
             Consumer Group 2:          Consumer Group 1:
             Fraud Detection            Order Fulfillment
             (Position: Offset 2)       (Position: Offset 5)
```
* **Non-destructive reads:** Multiple independent consumer groups read at their own pace.
* **Arbitrary replay:** A consumer can reset its offset to 0 and reprocess the entire stream.
* **Time-to-Live (Retention):** Records are deleted based on age or size, completely independent of whether they have been read.

---

## 2. Topic, Partitions, and Scoped Offsets

A Topic is a logical abstraction. A Partition is the physical reality.

```text
Topic: "user-signups"
├── Partition 0:  [ 0 | 1 | 2 | 3 | 4 | 5 ]  --> Stored on Broker 1 (/var/lib/kafka/user-signups-0)
├── Partition 1:  [ 0 | 1 | 2 | 3 ]          --> Stored on Broker 2 (/var/lib/kafka/user-signups-1)
└── Partition 2:  [ 0 | 1 | 2 | 3 | 4 ]      --> Stored on Broker 3 (/var/lib/kafka/user-signups-2)
```

### Critical Rules of Partitions:
1. **Ordering is local:** Kafka guarantees total order *only within a single partition*. There is no global order across Partition 0 and Partition 1.
2. **Offsets are local:** Offset 3 in Partition 0 is completely unrelated to Offset 3 in Partition 1.
3. **Unit of scale:** Partitions allow a single logical topic to exceed the throughput, disk capacity, and network I/O of any single physical machine.

---

## 3. Producer Internal Architecture

When your application invokes `producer.send(record)`, it does *not* immediately make a blocking network call to the broker.

```text
Application Thread
   │
   ▼
[ Serializer ] ──────────► Converts Key & Value from Objects to byte[]
   │
   ▼
[ Partitioner ] ─────────► Determines Target Partition (Hash of Key or Round-Robin)
   │
   ▼
[ RecordAccumulator ] ───► In-Memory Buffer Pool (batches records per partition)
   │                       Batch 1: [R1, R2, R3] (waiting for batch.size or linger.ms)
   │
   ▼  (Background IO Thread)
[ Sender Thread ] ───────► Formats ProduceRequest socket packets
   │
   ▼ (Network Socket)
Kafka Broker Socket
```

* **`linger.ms` vs `batch.size`:** The sender thread waits up to `linger.ms` for more records to arrive to fill a buffer of `batch.size` bytes.
* **Throughput trade-off:** More batching = higher throughput + lower CPU/network overhead, at the expense of a few milliseconds of latency.

---

## 4. Partition Leadership, Followers, and High Watermark

Each partition has one designated Leader broker and zero or more Follower replicas.

```text
                         Topic: "payments", Partition 0
                         Replication Factor: 3, ISR: [1, 2]

        Broker 1 (LEADER)            Broker 2 (FOLLOWER)         Broker 3 (FOLLOWER)
      ┌─────────────────────┐      ┌─────────────────────┐     ┌─────────────────────┐
      │ Offset 0: Pay-A     │      │ Offset 0: Pay-A     │     │ Offset 0: Pay-A     │
      │ Offset 1: Pay-B     │      │ Offset 1: Pay-B     │     │ (Offline/Lagging)   │
      │ Offset 2: Pay-C (HW)│◄─────│ Offset 2: Pay-C     │     │                     │
      │ Offset 3: Pay-D(LEO)│      │ (Fetching from Ldr) │     │ [DROPPED FROM ISR]  │
      └─────────────────────┘      └─────────────────────┘     └─────────────────────┘
                 ▲
                 │ Client Writes & Reads
                 │
       Producer (acks=all)  /  Consumer (reads up to HW=2)
```

* **High Watermark (HW):** The highest offset replicated across all in-sync replicas (ISR). Consumers cannot see Offset 3 until Broker 2 fetches it. This prevents "dirty reads" of data that could vanish if Broker 1 crashes.
* **Log End Offset (LEO):** The next offset the leader will write.

---

## 5. Consumer Group Scaling & Parallelism Invariant

```text
Topic: 4 Partitions [P0, P1, P2, P3]

Scenario A: 2 Consumers in Group
┌─────────────────────────┐
│ Consumer Group "workers"│
│  Consumer 1 ──► P0, P1  │
│  Consumer 2 ──► P2, P3  │
└─────────────────────────┘

Scenario B: 4 Consumers in Group
┌─────────────────────────┐
│ Consumer Group "workers"│
│  Consumer 1 ──► P0      │
│  Consumer 2 ──► P1      │
│  Consumer 3 ──► P2      │
│  Consumer 4 ──► P3      │
└─────────────────────────┘

Scenario C: 5 Consumers in Group (Idle Consumer!)
┌─────────────────────────┐
│ Consumer Group "workers"│
│  Consumer 1 ──► P0      │
│  Consumer 2 ──► P1      │
│  Consumer 3 ──► P2      │
│  Consumer 4 ──► P3      │
│  Consumer 5 ──► (IDLE)  │ ◄─── Excess consumer cannot receive work!
└─────────────────────────┘
```

> **The Invariant:**
> Within a single consumer group, a partition can be assigned to **at most one consumer** at a time.
> Therefore: **Maximum active consumer parallelism = Number of Partitions.**

---

## 6. Why Kafka is Fast: OS Page Cache & Zero-Copy

A pervasive myth is that "Kafka is written in Java and writes to disk, so it must be slow."
In reality, Kafka relies on two operating-system level mechanisms:

### Sequential Disk Appends
Random disk I/O on HDDs or SSDs requires seek operations and incurs substantial latency.
Sequential disk I/O appends directly to the tail of the log file, achieving speeds comparable to memory bus transfers:

```text
Random Disk I/O:      Seek -> Write -> Seek -> Write  (~100-500 ops/sec on HDD)
Sequential Disk I/O:  Append -> Append -> Append      (~100-600 MB/sec on modern disks)
```

### Zero-Copy Network Transfer via `sendfile()`
In traditional server software, serving a file over the network involves 4 context switches and 3 buffer copies:

```text
Disk ──(DMA)──► Kernel Page Cache ──(CPU Copy)──► User Space Buffer (Java App)
                                                         │
Socket ◄──(DMA)── Socket Buffer ◄───(CPU Copy)───────────┘
```

Kafka utilizes the Linux `sendfile()` system call (Zero-Copy):

```text
Disk ──(DMA)──► Kernel Page Cache ──(DMA Copy directly)──► NIC Network Buffer ──► Wire
```

The data never enters user-space memory! The CPU does not touch the payload bytes during reads.

---

## 7. KRaft Cluster Architecture (No ZooKeeper)

In Apache Kafka 3.x+ (KRaft mode):

```text
┌────────────────────────────────────────────────────────┐
│                   KRaft Quorum                         │
│  Node 1 (Controller Leader) ◄── Raft Heartbeats ──►   │
│  Node 2 (Controller Follower)                          │
│  Node 3 (Controller Follower)                          │
│                                                        │
│  * Metadata is stored in internal log: @metadata-0     │
│  * Leaders elected in milliseconds (no ZK sync lag)    │
└────────────────────────────────────────────────────────┘
                           │
       Active Metadata Replication & Partition State
                           ▼
┌────────────────────────────────────────────────────────┐
│                 Broker Data Plane                      │
│   Broker 1              Broker 2            Broker 3   │
│  [P0 Leader]          [P0 Follower]       [P1 Leader]  │
└────────────────────────────────────────────────────────┘
```

* Cluster state changes (broker joins, partition reassignments, topic creations) are committed to a Raft log directly inside Kafka.
