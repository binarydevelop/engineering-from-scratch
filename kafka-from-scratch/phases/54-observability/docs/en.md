# Lesson 54: Observability

## Motto
"If you cannot measure it, your cluster is already failing in secret."

## Problem
In a busy Kafka cluster, thousands of metrics are emitted: JMX MBeans, broker stats, network counters, client metrics.
When an incident strikes:
* Which 5 metrics actually matter?
* Which metrics indicate imminent data loss?
* Which metrics reveal consumer bottlenecks?
How do you build a focused, actionable observability suite for Apache Kafka?

## Prediction
What is the single most critical broker metric that indicates data loss risk?

## Why this matters
Wading through thousands of useless metrics during an outage delays resolution. Focusing on the **Golden Metrics** enables instant triage.

## First principles
**The 6 Golden Kafka Metrics:**
1. **`UnderReplicatedPartitions` (URP):** Partitions where $\text{ISR Size} < \text{Replication Factor}$. **Must be 0.** If $> 0$, brokers are failing or network is degraded!
2. **`OfflinePartitionsCount`:** Partitions with NO active leader. **Must be 0.** If $> 0$, data is completely unavailable!
3. **`ActiveControllerCount`:** In KRaft, exactly ONE active controller leader must exist. If 0, metadata is frozen; if $> 1$, split-brain!
4. **`ConsumerLag`:** Records unread by consumer groups.
5. **`IsrShrinksPerSec` / `IsrExpandsPerSec`:** Replicas flapping in and out of ISR due to GC or network stalls.
6. **`BytesInPerSec` / `BytesOutPerSec`:** Cluster network throughput volume.

## Mental model
```text
The Operations Dashboard (Triage Hierarchy):
[ OfflinePartitionsCount > 0 ]      ──► P0 EMERGENCY! System Down! Partitions unreachable!
[ UnderReplicatedPartitions > 0 ]   ──► P1 HIGH ALERT! Durability degraded! Broker down!
[ ConsumerLag Growing Monotonically ]──► P2 ALERT! Consumers falling behind reality!
[ Disk Utilization > 80% ]          ──► P2 ALERT! Disk exhaustion within 48 hours!
```

## Build it
See [cluster_metrics_collector.py](../code/cluster_metrics_collector.py).
We collect and display the core health metrics from our cluster.

## Use Kafka
Query cluster health and monitor partition replication metrics.

## Inspect it
Observe broker health status in clean terminal table output.

## Measure it
Simulate an outage and watch `UnderReplicatedPartitions` spike from 0 to 3.

## Break it
Stop `kafka-node-3`; observe the URP counter spike immediately.

## Recover it
Start `kafka-node-3`; observe URP return to 0 as follower syncs.

## Modify it
Add threshold alerting rules for Prometheus / Alertmanager.

## Evidence
Record output in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is `UnderReplicatedPartitions > 0` an immediate operational alarm?
2. If `OfflinePartitionsCount > 0`, what happens to producers attempting to write to that partition?

## Guarantees
* JMX and broker metrics provide real-time status of internal cluster data structures.

## Non-guarantees
* Metrics describe cluster symptoms; diagnosing root causes still requires log inspection.

## When to use this
* In all production monitoring and alerting setups.

## When not to use this
* Alerting on every minor fluctuation (avoid alert fatigue; focus on the Golden Metrics).

## What comes next
In Phase 55, we conduct formal Performance Testing and benchmark throughput across configurations.
