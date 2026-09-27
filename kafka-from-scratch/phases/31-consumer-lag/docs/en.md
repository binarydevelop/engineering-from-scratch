# Lesson 31: Consumer Lag

## Motto
"Consumer Lag is the single most vital health metric in the entire Kafka ecosystem."

## Problem
In a healthy cluster, consumers read records within milliseconds of being produced.
However, when downstream databases slow down, code bugs cause CPU spikes, or producers suddenly surge with Black Friday traffic:
* Production rate outpaces consumption rate.
* The backlog of unread records swells.
How do we mathematically measure this backlog, and how do we monitor it before customers notice delays?

## Prediction
If Log End Offset (LEO) is 150,000 and the consumer group's committed offset is 120,000, what is the exact lag?

## Why this matters
**Consumer Lag is the ultimate early-warning indicator.**
High CPU or memory is just machine state; Consumer Lag directly tells you that your business domain is falling behind reality.

## First principles
$$\text{Consumer Lag} = \text{Log End Offset (LEO)} - \text{Committed Offset}$$
* **Log End Offset (LEO):** The offset of the next record to be written to the partition.
* **Committed Offset:** The last offset processed and saved by the consumer group.
* Lag must be monitored per partition, because a hot partition can be starving even while the average cluster lag looks acceptable.

## Mental model
```text
Partition 0 Log:
Offsets: 0 ...... 120,000 ........................ 150,000
                     ▲                                ▲
                     │                                │
            Committed Offset (120,000)        Log End Offset (150,000)
                     └──────── Lag = 30,000 ──────────┘
```

## Build it
See [lag_monitor.py](../code/lag_monitor.py).
We build a real-time lag calculator that inspects partition LEO and group offset to alert on backlog spikes.

## Use Kafka
Inspect lag using the official CLI:
```bash
docker exec -it kafka-lab-single /opt/kafka/bin/kafka-consumer-groups.sh   --bootstrap-server localhost:9092   --describe --group order-processors
```

## Inspect it
Observe columns: `LOG-END-OFFSET`, `CURRENT-OFFSET`, and `LAG`.

## Measure it
Produce 1,000 records while the consumer is paused and observe lag increase by exactly 1,000.

## Break it
Simulate a slow consumer sleeping 100ms per record; observe lag growth rate.

## Recover it
Scale consumer instances up to match partition count to clear lag.

## Modify it
Add alerting logic to `lag_monitor.py` when lag exceeds 500 records.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is checking *average* lag across a topic misleading if one partition has 95% of the lag?
2. What happens to lag if the consumer process crashes completely?

## Guarantees
* Lag accurately reflects the count of unread records between the consumer position and the partition tail.

## Non-guarantees
* Zero lag does not guarantee downstream services have completed external asynchronous operations.

## When to use this
* In all production alerting systems (Prometheus, Datadog, Grafana).

## When not to use this
* Lag monitoring is useless if consumers do not commit offsets.

## What comes next
In Phase 32, we explore Backpressure and reason about capacity limits using Little's Law.
