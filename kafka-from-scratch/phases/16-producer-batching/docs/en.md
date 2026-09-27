# Lesson 16: Producer Batching

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
