# Lesson 33: Producer Retries and Duplicates

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
