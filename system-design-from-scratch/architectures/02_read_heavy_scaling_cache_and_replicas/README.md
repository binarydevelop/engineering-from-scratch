# Evolution 02: Read-Heavy Scaling with Read Replicas & Cache-Aside

## 1. Architectural Thesis
> Evolve a saturated primary database into a high-throughput read-heavy architecture using asynchronous read replicas and an in-memory Cache-Aside layer.

In system design, no architecture is born complex. Systems evolve under the relentless pressure of traffic, latency bounds, data volume, and availability requirements. This study illustrates the exact transition point, the bottleneck that forced the evolution, the mechanism implemented, and the resulting engineering tradeoffs.

## 2. The Problem & Initial State
- **Problem Statement**: A 95% read-heavy workload overwhelms the primary database CPU and IOPS. Read queries compete with writes for buffer cache, causing P99 latency degradation.
- **Pressure Trigger**: Read volume reaches 25,000 QPS. Database CPU hits 98% utilization, and read query latency climbs from 5ms to 450ms.
- **The Core Question**: What breaks first, why does it break, and how do we evolve the architecture without unnecessary complexity?

## 3. The Architecture Evolution

```text
=== BEFORE (Simpler Architecture) ===
[Clients] ---> [Monolithic / Single Node / Synchronous Component]
                     |
            (Saturated Bottleneck)

=== EVOLUTION PRESSURE ===
* Traffic threshold breached: Read volume reaches 25,000 QPS. Database CPU hits 98% utilization, and read query latency climbs from 5ms to 450ms.
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
Deploy 3 asynchronous read replicas for read offloading and an in-memory cache-aside tier (Redis pattern) with TTL and active write invalidation.

## 5. Architectural Tradeoffs
| Dimension | Simpler State | Evolved State | Engineering Justification |
| :--- | :--- | :--- | :--- |
| **Operational Overhead** | Low (single component) | Moderate to High | Justified by eliminating the hard scalability ceiling |
| **Consistency Guarantee** | Strong / Immediate | Eventual or Partitioned | Required to achieve horizontal read/write scale |
| **Failure Domain** | Single Point of Failure (SPOF) | Isolated & Redundant | Node failure does not cause complete system outage |

### Key Tradeoffs Explored:
- Replication lag anomalies (eventual consistency) vs primary DB load reduction
- Cache stampede / thundering herd vulnerability vs sub-millisecond read latency
- Dual-write inconsistency risks vs high read throughput

## 6. Runnable Implementation
Review and execute `main.py` in this directory to observe the before-and-after behavioral benchmarks:

```bash
python main.py
```

Run verification tests:
```bash
pytest tests/
```
