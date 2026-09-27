# Lesson 46: Broker Disk and Capacity

## Motto
"Never deploy a Kafka cluster without doing the capacity math first."

## Problem
A team deploys Kafka with default settings.
Three weeks later at 2:00 AM, all brokers run out of disk space (`No space left on device`).
Brokers crash, partitions become corrupted, and the entire platform halts.
How do you calculate disk, network bandwidth, and broker node count *before* launching into production?

## Prediction
If an e-commerce platform generates 20,000 events/second, average record size is 1 KB, retention is 7 days, and replication factor is 3, how many terabytes of disk space are required?

## Why this matters
Capacity planning is a core system design responsibility. Guessing leads either to millions wasted on over-provisioned infrastructure or catastrophic out-of-disk outages.

## First principles
$$\text{Daily Raw Ingestion} = \text{Events/sec} \times \text{Bytes/event} \times 86,400 \text{ sec/day}$$
$$\text{Total Replicated Storage} = \text{Daily Raw} \times \text{Retention Days} \times \text{Replication Factor} \times \text{Headroom Buffer (1.3x)}$$
* Always include a **30% headroom buffer** for OS overhead, segment index files, compaction dirty segments, and emergency traffic spikes!

## Mental model
```text
Capacity Formula:
20,000 events/s  *  1 KB  =  20 MB/s raw ingestion
20 MB/s  *  86,400 s/day  =  1.728 TB/day raw
1.728 TB/day  *  7 days   =  12.096 TB unique data
12.096 TB  *  3 replicas  =  36.288 TB replicated
36.288 TB  *  1.3 headroom=  47.17 TB Total Disk Required!
Across 6 brokers          =  ~8 TB NVMe SSD per broker!
```

## Build it
See [capacity_calculator.py](../code/capacity_calculator.py).
We implement an interactive capacity sizing calculator.

## Use Kafka
Run the calculator with your anticipated production parameters.

## Inspect it
Observe network ingress/egress bandwidth requirements alongside disk storage.

## Measure it
Measure real-world disk footprint vs mathematical prediction.

## Break it
Simulate an out-of-disk failure by setting a tiny volume quota; observe broker shutdown behavior.

## Recover it
Implement automated disk usage alerts at 75% capacity to scale storage before saturation.

## Modify it
Add payload compression ratio (e.g. 3x reduction with `zstd`) to the capacity model.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why must network bandwidth calculations multiply raw ingress by $(1 + \text{Replication Factor} - 1 + \text{Consumer Groups Count})$?
2. Why is running Kafka broker disks above 85% capacity dangerous?

## Guarantees
* Mathematical capacity modeling bounds infrastructure risk.

## Non-guarantees
* A mathematical estimate does not protect against unannounced marketing events generating 10x traffic spikes.

## When to use this
* During cluster architecture, cloud budgeting, and capacity reviews.

## When not to use this
* Ignoring capacity math guarantees future production incidents.

## What comes next
In Phase 47, we examine Partition Count and learn why having too many partitions is dangerous.
