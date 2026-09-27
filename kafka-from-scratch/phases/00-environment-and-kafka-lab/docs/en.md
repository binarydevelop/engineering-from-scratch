# Lesson 00: Environment and Kafka Lab

## Motto
"Before you can reason about distributed logs, you must prove your client can talk to the server process across a raw network socket."

## Problem
Many engineers treat Kafka as a monolithic cloud utility or a mysterious CLI suite. When a client throws `ConnectionRefusedError` or `NoBrokersAvailable`, they guess randomly. We must establish a minimal, completely transparent, reproducible local Kafka lab and verify our ability to inspect its socket and state directly.

## Prediction
1. What process is actually running when we start Kafka in modern KRaft mode?
2. How does a client running on the host OS communicate with a broker running inside a container on port 9092?

## Why this matters
Kafka is a standard user-space server process written in Java/Scala that listens on TCP ports and appends bytes to disk files. If you understand its host-port binding, listener mapping, and process lifecycle, distributed system configuration stops being mysterious.

## First principles
Kafka operates strictly as a network service:
* **Server Process:** A single JVM instance running `kafka.Kafka`.
* **KRaft Quorum:** Eliminates external ZooKeeper; broker and controller state run inside the same or dedicated processes.
* **TCP Listeners:** Brokers bind to network sockets (e.g. `0.0.0.0:9092`) and advertise reachable hostnames to clients.

## Mental model
```text
Host Machine (macOS / Linux)
┌────────────────────────────────────────────────────────┐
│ Python Client / CLI                                    │
│ (kafka-python-ng / confluent-kafka)                    │
└────────────────────────────────────────────────────────┘
                           │ TCP Connection
                           ▼ (localhost:9092)
┌────────────────────────────────────────────────────────┐
│ Docker Engine (Container: kafka-lab-single)            │
│   └── Java JVM Process: kafka.Kafka                    │
│         ├── Port 9092 (PLAINTEXT client traffic)       │
│         ├── Port 9093 (CONTROLLER internal Raft quorum)│
│         └── Storage: /tmp/kraft-combined-logs          │
└────────────────────────────────────────────────────────┘
```

## Build it
See [verify_lab.py](../code/verify_lab.py) for a direct socket probe and metadata query script.

```python
import socket

def test_socket(host='localhost', port=9092):
    s = socket.create_connection((host, port), timeout=3)
    s.close()
    return True
```

## Use Kafka
Launch the container and query cluster metadata:

```bash
make up
docker exec kafka-lab-single /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server localhost:9092
```

## Inspect it
Check the running JVM process inside the container:
```bash
docker exec kafka-lab-single ps aux
```

## Measure it
Measure ping latency and TCP connection establishment time to port 9092.

## Break it
Stop the container and observe the exact error raised by Python clients.

## Recover it
Run `make up` and re-verify connectivity.

## Modify it
Change the advertised listener in `docker-compose.yml` to an invalid IP and observe the connection failure.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Kafka require distinct `listeners` and `advertised.listeners` configurations?
2. What role does the controller port (9093) play in a KRaft cluster?

## Guarantees
* A running, unfenced KRaft broker responds to metadata requests over PLAINTEXT.

## Non-guarantees
* Having port 9092 open does not guarantee the cluster is ready to accept writes if the KRaft quorum is partitioned.

## When to use this
* During local development, integration testing, and protocol debugging.

## When not to use this
* Single-broker setups should never run in production environments requiring high availability.

## What comes next
In Phase 01, we examine the fundamental architectural failure of point-to-point synchronous architectures that led to the creation of Kafka.
