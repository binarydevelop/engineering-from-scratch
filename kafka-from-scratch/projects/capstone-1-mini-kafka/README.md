# Capstone 1: Mini-Kafka Engine

A zero-magic, pure Python educational implementation of Apache Kafka's core architectural primitives.

---

## 1. Architectural Highlights

* **Length-Prefixed Log Files:** On-disk binary format using `[8 bytes: offset][4 bytes: length][payload]` format.
* **Topics & Partitions:** Dynamic directory structure (`<topic>/partition-<id>.log`).
* **Deterministic Key Routing:** CRC32 positive hash modulo partition count.
* **Consumer Group Offset Tracking:** Independent offset maps per consumer group.
* **Crash Recovery:** Recovers `next_offset` by scanning segment headers on startup.

---

## 2. Running Tests

```bash
python3 projects/capstone-1-mini-kafka/test_mini_kafka.py
```
