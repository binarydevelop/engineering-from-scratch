# Apache Kafka 3.8.0 CLI Command Reference

This reference documents the modern, official CLI utilities for Kafka 3.8.0.
All commands use `--bootstrap-server` (KRaft architecture).
**Do not use the deprecated `--zookeeper` flag anywhere.**

---

## 1. Running Inside Docker Container

To run any Kafka CLI tool on your local machine using the containerized Kafka broker:

```bash
docker exec -it kafka-lab-single /opt/kafka/bin/<tool-name>.sh [args]
```

---

## 2. Topic Management (`kafka-topics.sh`)

### Create a Topic
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --create \
  --topic orders \
  --partitions 3 \
  --replication-factor 1
```

### List All Topics
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --list
```

### Describe a Topic (Inspect Partitions, Leader, Replicas, ISR)
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --topic orders
```

### Alter Partition Count (Scale Up Partitions)
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --alter \
  --topic orders \
  --partitions 6
```
*(Note: Partitions can only be increased, never decreased, because removing a partition would result in immediate data loss or complex log migration).*

### Delete a Topic
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 \
  --delete \
  --topic orders
```

---

## 3. Producing Records (`kafka-console-producer.sh`)

### Send Plain String Records
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders
```

### Send Key-Value Pairs (Colon Delimited)
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-producer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders \
  --property "parse.key=true" \
  --property "key.separator=:"
```
*Example input:*
```text
user-42:{"order_id": 101, "amount": 49.99}
user-99:{"order_id": 102, "amount": 120.00}
```

---

## 4. Consuming Records (`kafka-console-consumer.sh`)

### Consume from the Beginning
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders \
  --from-beginning
```

### Consume with Keys, Timestamps, and Partition Metadata
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders \
  --from-beginning \
  --property print.key=true \
  --property print.timestamp=true \
  --property print.partition=true \
  --property print.offset=true
```

### Consume as Part of a Consumer Group
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic orders \
  --group order-processors
```

---

## 5. Consumer Group Inspection & Offsets (`kafka-consumer-groups.sh`)

### List All Active Consumer Groups
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --list
```

### Describe a Consumer Group (Inspect Lag, Current Offset, Log End Offset)
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --describe \
  --group order-processors
```

### Reset Consumer Offsets (e.g. Replay from Beginning)
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh \
  --bootstrap-server localhost:9092 \
  --group order-processors \
  --reset-offsets \
  --to-earliest \
  --all-topics \
  --execute
```

---

## 6. On-Disk Log Inspection (`kafka-dump-log.sh`)

Inspect the binary contents of an on-disk `.log` segment file, including magic byte, CRC, Producer ID, and record batches:

```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-dump-log.sh \
  --files /tmp/kraft-combined-logs/orders-0/00000000000000000000.log \
  --print-data-log \
  --deep-iteration
```

Inspect an offset index file (`.index`):
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-dump-log.sh \
  --files /tmp/kraft-combined-logs/orders-0/00000000000000000000.index \
  --verify-index-only
```

---

## 7. KRaft Cluster Management (`kafka-cluster.sh` & `kafka-metadata-shell.sh`)

### Print Cluster ID
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-cluster.sh \
  cluster-id \
  --bootstrap-server localhost:9092
```

### Interactive KRaft Metadata Shell (Explore Cluster State Tree)
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-metadata-shell.sh \
  --snapshot /tmp/kraft-combined-logs/__cluster_metadata-0/00000000000000000000.log
```
*Allows navigating the KRaft metadata state directory tree like a virtual filesystem (`ls /brokers`, `cat /topics/orders`).*
