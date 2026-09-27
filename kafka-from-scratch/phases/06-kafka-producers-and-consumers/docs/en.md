# Lesson 06: Kafka Producers and Consumers

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
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-console-consumer.sh   --bootstrap-server localhost:9092   --topic lab-orders   --from-beginning   --property print.key=true   --property print.offset=true
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
