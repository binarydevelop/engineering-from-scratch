# Kafka Architectural & Systems Glossary

A precise, non-hand-waving glossary of Apache Kafka concepts, data structures, protocols, and invariants.

---

## A

### Acks (`acks`)
The producer configuration dictating how many partition replicas must acknowledge receipt of a record batch before the producer marks the write request as successful:
* `acks=0`: Fire-and-forget. The producer considers the record written immediately after pushing it onto the network socket. Zero durability guarantee.
* `acks=1`: Leader acknowledgment. The partition leader writes the batch to its local page cache/log and immediately replies. If the leader crashes before replicas fetch the batch, records are lost.
* `acks=-1` or `acks=all`: Quorum acknowledgment. The leader waits until all current In-Sync Replicas (meeting at least `min.insync.replicas`) have appended the batch to their logs before replying.

### Active Segment
The single log segment file (`.log`) currently open for appends in a partition directory. All prior segments in that partition are immutable and read-only.

### Append-Only Log
A sequential, immutable data structure where writes can only be appended to the end (tail), and historical data cannot be modified in place. It enables $O(1)$ write operations and maximizes sequential disk I/O throughput.

---

## B

### Backpressure
The mechanism by which a downstream consumer signals or naturally slows down upstream production when consumer processing capacity is lower than ingestion rate. Kafka does not push data to consumers; consumers pull (poll), allowing consumers to control their own backpressure.

### Batching
The technique of grouping multiple individual records into a single network payload and on-disk `RecordBatch`. Amortizes TCP packet header overhead, system call costs, compression overhead, and disk write operations.

### Broker
A server process running the Kafka engine. A broker receives records from producers, writes them to disk, serves read requests to consumers and follower replicas, and participates in cluster metadata coordination.

---

## C

### Commit (`__consumer_offsets`)
The action of recording the offset up to which a consumer group has successfully processed records for a given topic-partition. Offsets are stored in an internal, compacted Kafka topic named `__consumer_offsets`.

### Consumer Group
A logical set of consumers cooperating to read data from one or more topics. Kafka guarantees that each partition in a topic is assigned to at most one consumer within a given consumer group at any instant.

### Consumer Lag
The difference between the Log End Offset (the latest record written by producers to a partition) and the Current Offset (the latest record consumed or committed by a consumer group):
$$\text{Lag} = \text{Log End Offset (LEO)} - \text{Consumer Committed Offset}$$

### Controller
The broker node currently acting as the active leader of cluster metadata coordination. In KRaft mode, controllers form a Raft quorum to manage metadata without external ZooKeeper dependencies.

---

## D

### Dead-Letter Topic (DLT / DLQ)
A designated Kafka topic where unprocessable, malformed, or poisoned messages are published after a configured number of retries, preventing consumer threads from crashing or stalling indefinitely.

---

## E

### Epoch
A monotonic integer used to differentiate cluster terms and leadership transitions:
* **Leader Epoch:** Increments whenever a new partition leader is elected, preventing truncation anomalies and stale leader split-brains.
* **Controller Epoch:** Increments whenever a new active KRaft controller takes over.

### Exactly-Once Semantics (EOS)
In Kafka, EOS means that in a consume-transform-produce loop (reading from Kafka and publishing back to Kafka), input offsets and output records are committed together atomically within a transaction. It does *not* automatically ensure exactly-once effects on third-party non-transactional databases or external APIs.

---

## F

### Follower Replica
A broker hosting a replica of a partition that is *not* the leader. Followers fetch records continuously from the partition leader over TCP to keep their local logs in sync.

---

## G

### Group Coordinator
The specific Kafka broker responsible for managing the lifecycle of a consumer group: handling join requests, tracking heartbeats, assigning partitions via an assignor, and recording committed offsets. Determined by hashing the consumer group ID modulo the number of partitions in `__consumer_offsets`.

---

## H

### High Watermark (HW)
The highest offset in a partition log that has been replicated to all active members of the In-Sync Replica set (ISR). Consumers are only permitted to read records up to the High Watermark to guarantee that uncommitted, non-replicated data is never exposed.

### Hot Partition
A partition that receives a disproportionately large volume of traffic or disk writes compared to other partitions in the same topic, usually caused by key skew (e.g. 90% of events sharing the same tenant or user ID).

---

## I

### Idempotent Producer
A producer configured with `enable.idempotence=true`. The broker assigns each producer a 64-bit Producer ID (PID) and tracks a monotonic sequence number per topic-partition. If network retries resend a previously written batch, the broker identifies the duplicate sequence number and discards it cleanly without appending duplicates.

### In-Sync Replicas (ISR)
The subset of partition replicas that are actively caught up with the leader's log. A replica is dropped from the ISR if it fails to send heartbeat fetch requests to the leader within `replica.lag.time.max.ms`.

---

## K

### Key
An optional byte array attached to a Kafka record. When present, the default partitioner computes a hash of the key to assign the record to a specific partition, guaranteeing total ordering for all records sharing that key.

### KRaft (Kafka Raft)
The consensus subsystem introduced via KIP-500 that manages Kafka's cluster metadata directly within Kafka brokers and dedicated controller nodes, entirely replacing Apache ZooKeeper.

---

## L

### Leader
The single broker designated to handle all writes (and by default all reads) for a specific topic-partition.

### Log Compaction
A retention policy (`cleanup.policy=compact`) where Kafka retains at least the last known value for each record key within a partition, garbage-collecting older records with the same key during segment cleaning.

### Log End Offset (LEO)
The offset of the next record to be written to a partition. Represents the exact append point of the log.

---

## M

### `min.insync.replicas`
The minimum number of replicas in the ISR that must be online and acknowledge a write when a producer sends with `acks=all`. If the current ISR size falls below this threshold, the leader rejects writes with a `NotEnoughReplicasException`.

---

## O

### Offset
A monotonic 64-bit integer uniquely identifying a record within a specific partition. Offsets start at 0 and strictly increment with each append. Offsets are **partition-local**; there is no global offset across a topic.

---

## P

### Partition
The fundamental physical unit of parallelism, storage, and ordering in Kafka. A topic is divided into one or more partitions. Each partition maps directly to a directory on a broker's filesystem containing sequential log segment files.

---

## R

### Rebalance
The process by which the group coordinator redistributes partition assignments among consumers in a group when group membership changes (consumer joins, leaves, or dies) or topic partitions are altered.

### Retention
The policy governing how long data is retained in a partition before deletion. Can be time-based (`log.retention.hours` / `log.retention.ms`) or size-based (`log.retention.bytes`).

---

## S

### Segment
A chunk of a partition log on disk. Comprises a data log (`.log`), an offset index (`.index`), a timestamp index (`.timeindex`), and a leader epoch checkpoint. Once a segment reaches its size or age limit, it rolls and becomes immutable.

---

## T

### Topic
A named logical stream of records. In architecture, a topic is divided physically into one or more partitions distributed across brokers in the cluster.

### Tombstone
In log compaction, a record with a non-null key and a `null` payload. Serves as a deletion marker instructing the log cleaner to remove all historical records with that key after the delete retention window.
