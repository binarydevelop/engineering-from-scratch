# Evolution 03: Write-Heavy Scaling with Database Sharding

## 1. Architectural Thesis
> Scale database write throughput linearly by partitioning data horizontally across multiple independent database shards using consistent hashing.

In system design, no architecture is born complex. Systems evolve under the relentless pressure of traffic, latency bounds, data volume, and availability requirements. This study illustrates the exact transition point, the bottleneck that forced the evolution, the mechanism implemented, and the resulting engineering tradeoffs.

## 2. The Problem & Initial State
- **Problem Statement**: Write operations to an orders table exceed the maximum disk IOPS and WAL throughput of a single vertically scaled database server.
- **Pressure Trigger**: Write volume exceeds 12,000 writes/sec. Disk queue depth explodes, WAL commit latency exceeds 2 seconds, and transactions begin timing out.
- **The Core Question**: What breaks first, why does it break, and how do we evolve the architecture without unnecessary complexity?

## 3. The Architecture Evolution

```text
=== BEFORE (Simpler Architecture) ===
[Clients] ---> [Monolithic / Single Node / Synchronous Component]
                     |
            (Saturated Bottleneck)

=== EVOLUTION PRESSURE ===
* Traffic threshold breached: Write volume exceeds 12,000 writes/sec. Disk queue depth explodes, WAL commit latency exceeds 2 seconds, and transactions begin timing out.
* Resource limit encountered (CPU / IOPS / Disk lock / Cascade failure)

=== AFTER (Evolved Architecture) ===
[Clients] ---> [Load Balancer / Ingress Router]
                     |
       +-------------+-------------+
       |                           |
[Worker / Service Node A]    [Worker / Service Node B]
       |                           |
       +-------------+-------------+
                     |
         [Storage / Cache / Outbox Layer]
```

## 4. The Evolved Solution
Partition data across N database shards using consistent hashing on the shard key (e.g., customer_id or order_id), with a router layer handling query dispatch and scatter-gather queries.

## 5. Architectural Tradeoffs
| Dimension | Simpler State | Evolved State | Engineering Justification |
| :--- | :--- | :--- | :--- |
| **Operational Overhead** | Low (single component) | Moderate to High | Justified by eliminating the hard scalability ceiling |
| **Consistency Guarantee** | Strong / Immediate | Eventual or Partitioned | Required to achieve horizontal read/write scale |
| **Failure Domain** | Single Point of Failure (SPOF) | Isolated & Redundant | Node failure does not cause complete system outage |

### Key Tradeoffs Explored:
- Loss of ACID cross-shard joins and transactions vs linear write throughput expansion
- Complex data rebalancing and resharding vs vertical scale-up hardware ceiling
- Scatter-gather query tail latency penalty vs bounded per-shard storage size

## 6. Runnable Implementation
Review and execute `main.py` in this directory to observe the before-and-after behavioral benchmarks:

```bash
python main.py
```

Run verification tests:
```bash
pytest tests/
```
