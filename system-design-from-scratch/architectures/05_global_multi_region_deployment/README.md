# Evolution 05: Single-Region to Global Multi-Region Deployment

## 1. Architectural Thesis
> Architect a globally distributed service serving users across continents with localized low latency and disaster recovery.

In system design, no architecture is born complex. Systems evolve under the relentless pressure of traffic, latency bounds, data volume, and availability requirements. This study illustrates the exact transition point, the bottleneck that forced the evolution, the mechanism implemented, and the resulting engineering tradeoffs.

## 2. The Problem & Initial State
- **Problem Statement**: A single-datacenter deployment in us-east-1 incurs 220ms speed-of-light network latency for users in APAC and Europe, and represents a single point of catastrophic failure.
- **Pressure Trigger**: International user base exceeds 60% of total traffic. Regional fiber cut or AWS AZ outage causes complete global service downtime.
- **The Core Question**: What breaks first, why does it break, and how do we evolve the architecture without unnecessary complexity?

## 3. The Architecture Evolution

```text
=== BEFORE (Simpler Architecture) ===
[Clients] ---> [Monolithic / Single Node / Synchronous Component]
                     |
            (Saturated Bottleneck)

=== EVOLUTION PRESSURE ===
* Traffic threshold breached: International user base exceeds 60% of total traffic. Regional fiber cut or AWS AZ outage causes complete global service downtime.
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
Deploy active-active multi-region clusters in US, EU, and APAC with GeoDNS/Anycast routing, local read replicas, asynchronous cross-region state synchronization, and conflict resolution (Last-Write-Wins / CRDT).

## 5. Architectural Tradeoffs
| Dimension | Simpler State | Evolved State | Engineering Justification |
| :--- | :--- | :--- | :--- |
| **Operational Overhead** | Low (single component) | Moderate to High | Justified by eliminating the hard scalability ceiling |
| **Consistency Guarantee** | Strong / Immediate | Eventual or Partitioned | Required to achieve horizontal read/write scale |
| **Failure Domain** | Single Point of Failure (SPOF) | Isolated & Redundant | Node failure does not cause complete system outage |

### Key Tradeoffs Explored:
- Data divergence and cross-region write synchronization latency vs zero single-datacenter downtime
- Egress data transfer costs vs single-digit millisecond latency worldwide
- Complex split-brain partition recovery vs regulatory data residency compliance

## 6. Runnable Implementation
Review and execute `main.py` in this directory to observe the before-and-after behavioral benchmarks:

```bash
python main.py
```

Run verification tests:
```bash
pytest tests/
```
