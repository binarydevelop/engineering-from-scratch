# Kafka Production Failure Triage & Troubleshooting

A structured, systematic triage guide for common Kafka operational failures, distributed desynchronizations, and client exceptions.

---

## 1. The "Advertised Listeners" Connectivity Trap

### Symptom
Client throws `NoBrokersAvailable` or `ConnectionRefusedError: [Errno 61] Connection refused` even though `docker compose ps` shows Kafka is "Up".

### First Principles Mechanics
When a client connects to `bootstrap.servers` (e.g. `localhost:9092`), the broker returns its **Advertised Listeners** metadata list. All subsequent topic metadata queries, produce requests, and fetch requests are directed to the *advertised host:port*, NOT the initial bootstrap IP!

If Kafka advertises `kafka:9092` to a host client running outside Docker, the host cannot resolve `kafka`, causing instant connection failure.

### Diagnostic Command
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092
```

### Remediation
Verify dual-listener configuration in `docker-compose.yml`:
```yaml
KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
```

---

## 2. Exploding Consumer Lag

### Symptom
Lag keeps growing continuously ($LEO - \text{Offset} \gg 0$). Downstream databases or users experience delayed event processing.

### First Principles Mechanics
$$\text{Production Rate} > \text{Consumer Processing Capacity}$$
Either:
1. Producer throughput spiked.
2. Consumer processing per record took longer (slow external database query, network latency).
3. Number of consumer processes is less than partition count.
4. Partitions are skewed (one partition has 90% of the events).

### Diagnostic Commands
```bash
# Check lag per partition
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group <group-name>
```

### Remediation Matrix
* If all partitions have equal lag and consumers < partitions: **Scale consumer instances up to match partition count.**
* If only Partition 0 has massive lag while Partition 1 & 2 are 0: **Key skew detected.** Fix producer partition hashing.
* If consumer count == partition count and lag persists: **Increase partition count** and scale consumers accordingly, or implement batched DB writes in the consumer.

---

## 3. Rebalance Storms & `CommitFailedException`

### Symptom
Consumer logs frequently report `CommitFailedException: Commit cannot be completed since the group has already rebalanced and assigned the partitions to another member`.

### First Principles Mechanics
If a consumer takes longer than `max.poll.interval.ms` (default 5 minutes) to process a batch of records returned by `poll()`, the group coordinator assumes the consumer has hung or died. The coordinator evicts the consumer and initiates a rebalance.
When the consumer finally finishes its slow batch and calls `commitSync()`, its assignment has been revoked!

### Remediation
1. Reduce `max.poll.records` (e.g. from 500 to 50) so each batch can be processed well within `max.poll.interval.ms`.
2. Offload heavy CPU/network work to a separate worker thread pool, keeping the Kafka poll loop responsive.
3. Increase `max.poll.interval.ms` if long processing is unavoidable.

---

## 4. `NotEnoughReplicasException`

### Symptom
Producers with `acks=all` fail with `NotEnoughReplicasException` or `NotEnoughReplicasAfterAppendException`.

### First Principles Mechanics
Producer specified `acks=all`, and the topic has `min.insync.replicas=2`.
If 2 out of 3 brokers die, the current In-Sync Replica set has size 1.
Because $\text{ISR size} (1) < \text{min.insync.replicas} (2)$, Kafka refuses writes to protect durability rather than accepting data that cannot be replicated safely.

### Diagnostic Command
```bash
docker exec -it kafka-node-1 /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic <topic-name>
```
Look at the `Isr:` field in output.

### Remediation
* Restore crashed follower brokers so they catch up and rejoin the ISR.
* If disaster recovery demands accepting writes at reduced durability, temporarily alter topic config:
  `kafka-configs.sh --alter --entity-name <topic> --entity-type topics --add-config min.insync.replicas=1`

---

## 5. Poison Pill Record (Consumer Infinite Crash Loop)

### Symptom
Consumer crashes on record at Offset $K$ due to JSON deserialization error or unhandled exception. Upon restart, the consumer resumes from last committed offset ($K$), reads the same bad record, and crashes again forever.

### Remediation
Implement the **Dead-Letter Topic (DLT)** pattern:
```python
try:
    process_event(record.value)
except DeserializationError as ex:
    dead_letter_producer.send("orders.DLT", key=record.key, value=record.value, headers=[("error", str(ex))])
    consumer.commit()  # Move forward past the poison record!
```

---

## 6. `RecordTooLargeException`

### Symptom
Producer fails with `org.apache.kafka.common.errors.RecordTooLargeException: The message is 2097152 bytes when serialized which is larger than the maximum request size...`

### First Principles Mechanics
Default maximum record batch size in Kafka is 1 MB (`max.message.bytes` on broker, `max.request.size` on producer).

### Architectural Solution
Kafka is optimized for streaming event data, not multi-megabyte binary blobs.
Instead of ballooning Kafka's memory buffers, use the **Claim-Check Pattern**:
1. Upload large image/PDF/payload to object storage (S3 / MinIO / GCS).
2. Publish an event to Kafka containing the URI reference and metadata:
   `{"file_id": "9812", "s3_uri": "s3://bucket/reports/9812.parquet", "size_bytes": 104857600}`
