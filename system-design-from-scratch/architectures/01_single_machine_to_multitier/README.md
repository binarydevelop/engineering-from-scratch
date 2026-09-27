# Evolution 01: Single-Machine Monolith to Multi-Tier Architecture

## 1. Architectural Thesis
> Trace the architectural evolution from an in-process SQLite monolith to a stateless web tier with dedicated, connection-pooled database storage.

In system design, no architecture is born complex. Systems evolve under the relentless pressure of traffic, latency bounds, data volume, and availability requirements. This study illustrates the exact transition point, the bottleneck that forced the evolution, the mechanism implemented, and the resulting engineering tradeoffs.

## 2. The Problem & Initial State
- **Problem Statement**: Single-process architecture couples web serving, business logic, and disk I/O. File locking prevents concurrency, CPU-heavy tasks block database queries, and the service cannot scale beyond one machine.
- **Pressure Trigger**: Traffic reaches 1,500 req/sec. SQLite disk locking leads to 'database is locked' errors (500 Internal Server Error) and CPU spikes to 100%.
- **The Core Question**: What breaks first, why does it break, and how do we evolve the architecture without unnecessary complexity?

## 3. The Architecture Evolution

```text
=== BEFORE (Simpler Architecture) ===
[Clients] ---> [Monolithic / Single Node / Synchronous Component]
                     |
            (Saturated Bottleneck)

=== EVOLUTION PRESSURE ===
* Traffic threshold breached: Traffic reaches 1,500 req/sec. SQLite disk locking leads to 'database is locked' errors (500 Internal Server Error) and CPU spikes to 100%.
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
Decouple into an horizontally scalable stateless compute tier behind a round-robin load balancer, communicating with a centralized database engine over network sockets with connection pooling.

## 5. Architectural Tradeoffs
| Dimension | Simpler State | Evolved State | Engineering Justification |
| :--- | :--- | :--- | :--- |
| **Operational Overhead** | Low (single component) | Moderate to High | Justified by eliminating the hard scalability ceiling |
| **Consistency Guarantee** | Strong / Immediate | Eventual or Partitioned | Required to achieve horizontal read/write scale |
| **Failure Domain** | Single Point of Failure (SPOF) | Isolated & Redundant | Node failure does not cause complete system outage |

### Key Tradeoffs Explored:
- Network hop latency (+1-2ms per query) vs horizontal compute elasticity
- Operational complexity (managing separate processes/hosts) vs isolated failure domains
- Connection pool exhaustion risk vs bounded memory on DB server

## 6. Runnable Implementation
Review and execute `main.py` in this directory to observe the before-and-after behavioral benchmarks:

```bash
python main.py
```

Run verification tests:
```bash
pytest tests/
```
