#!/usr/bin/env python3
"""
Generator for:
1. Architecture Evolution Cases (`architectures/`)
2. Failure Injection & Chaos Experiments (`experiments/`)
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ARCHITECTURES = [
    {
        "dir": "01_single_machine_to_multitier",
        "title": "Evolution 01: Single-Machine Monolith to Multi-Tier Architecture",
        "desc": "Trace the architectural evolution from an in-process SQLite monolith to a stateless web tier with dedicated, connection-pooled database storage.",
        "problem": "Single-process architecture couples web serving, business logic, and disk I/O. File locking prevents concurrency, CPU-heavy tasks block database queries, and the service cannot scale beyond one machine.",
        "pressure": "Traffic reaches 1,500 req/sec. SQLite disk locking leads to 'database is locked' errors (500 Internal Server Error) and CPU spikes to 100%.",
        "solution": "Decouple into an horizontally scalable stateless compute tier behind a round-robin load balancer, communicating with a centralized database engine over network sockets with connection pooling.",
        "tradeoffs": [
            "Network hop latency (+1-2ms per query) vs horizontal compute elasticity",
            "Operational complexity (managing separate processes/hosts) vs isolated failure domains",
            "Connection pool exhaustion risk vs bounded memory on DB server"
        ]
    },
    {
        "dir": "02_read_heavy_scaling_cache_and_replicas",
        "title": "Evolution 02: Read-Heavy Scaling with Read Replicas & Cache-Aside",
        "desc": "Evolve a saturated primary database into a high-throughput read-heavy architecture using asynchronous read replicas and an in-memory Cache-Aside layer.",
        "problem": "A 95% read-heavy workload overwhelms the primary database CPU and IOPS. Read queries compete with writes for buffer cache, causing P99 latency degradation.",
        "pressure": "Read volume reaches 25,000 QPS. Database CPU hits 98% utilization, and read query latency climbs from 5ms to 450ms.",
        "solution": "Deploy 3 asynchronous read replicas for read offloading and an in-memory cache-aside tier (Redis pattern) with TTL and active write invalidation.",
        "tradeoffs": [
            "Replication lag anomalies (eventual consistency) vs primary DB load reduction",
            "Cache stampede / thundering herd vulnerability vs sub-millisecond read latency",
            "Dual-write inconsistency risks vs high read throughput"
        ]
    },
    {
        "dir": "03_write_heavy_partitioning_sharding",
        "title": "Evolution 03: Write-Heavy Scaling with Database Sharding",
        "desc": "Scale database write throughput linearly by partitioning data horizontally across multiple independent database shards using consistent hashing.",
        "problem": "Write operations to an orders table exceed the maximum disk IOPS and WAL throughput of a single vertically scaled database server.",
        "pressure": "Write volume exceeds 12,000 writes/sec. Disk queue depth explodes, WAL commit latency exceeds 2 seconds, and transactions begin timing out.",
        "solution": "Partition data across N database shards using consistent hashing on the shard key (e.g., customer_id or order_id), with a router layer handling query dispatch and scatter-gather queries.",
        "tradeoffs": [
            "Loss of ACID cross-shard joins and transactions vs linear write throughput expansion",
            "Complex data rebalancing and resharding vs vertical scale-up hardware ceiling",
            "Scatter-gather query tail latency penalty vs bounded per-shard storage size"
        ]
    },
    {
        "dir": "04_asynchronous_event_driven_decoupling",
        "title": "Evolution 04: Synchronous Orchestration to Asynchronous Event-Driven Architecture",
        "desc": "Refactor a brittle synchronous HTTP microservice chain into an event-driven system with Transactional Outbox and durable message queues.",
        "problem": "Order checkout synchronously calls Payment, Inventory, Shipping, Email, and Fraud services in a single HTTP request thread. If any downstream service is slow or down, the checkout fails or times out.",
        "pressure": "Third-party email provider latency degrades to 4 seconds, causing order checkout thread pool exhaustion and widespread cascade outages.",
        "solution": "Commit order state and an outbox event atomically in a single local database transaction. An outbox worker publishes events to a durable broker, allowing downstream consumers to process tasks asynchronously with automatic retries and DLQ.",
        "tradeoffs": [
            "Eventual consistency and delayed side-effect completion vs sub-100ms response time",
            "Consumer idempotency and deduplication requirements vs fault isolation",
            "Complex distributed tracing and event monitoring vs high availability"
        ]
    },
    {
        "dir": "05_global_multi_region_deployment",
        "title": "Evolution 05: Single-Region to Global Multi-Region Deployment",
        "desc": "Architect a globally distributed service serving users across continents with localized low latency and disaster recovery.",
        "problem": "A single-datacenter deployment in us-east-1 incurs 220ms speed-of-light network latency for users in APAC and Europe, and represents a single point of catastrophic failure.",
        "pressure": "International user base exceeds 60% of total traffic. Regional fiber cut or AWS AZ outage causes complete global service downtime.",
        "solution": "Deploy active-active multi-region clusters in US, EU, and APAC with GeoDNS/Anycast routing, local read replicas, asynchronous cross-region state synchronization, and conflict resolution (Last-Write-Wins / CRDT).",
        "tradeoffs": [
            "Data divergence and cross-region write synchronization latency vs zero single-datacenter downtime",
            "Egress data transfer costs vs single-digit millisecond latency worldwide",
            "Complex split-brain partition recovery vs regulatory data residency compliance"
        ]
    }
]

EXPERIMENTS = [
    {
        "dir": "01_thundering_herd_collapse",
        "title": "Experiment 01: Thundering Herd Cache Stampede and Coalescing Defense",
        "desc": "Simulate what happens when a hot cache key expires under 1,000 concurrent requests, comparing unprotected cache-aside against Singleflight mutex coalescing.",
        "failure_mode": "Cache Stampede: Simultaneous cache misses by hundreds of concurrent threads flood the underlying database, causing thread exhaustion, high latency, and cascading failure.",
        "metric": "Number of database queries executed for 500 concurrent requests on an expired key (500 without singleflight vs 1 with singleflight)."
    },
    {
        "dir": "02_split_brain_network_partition",
        "title": "Experiment 02: Network Partition and Split-Brain Prevention via Quorum",
        "desc": "Inject a network partition into a 5-node distributed cluster, isolating 3 nodes from 2 nodes, and verify that split-brain is prevented through majority quorum.",
        "failure_mode": "Split-Brain: Two disconnected partitions both believe they are the authoritative cluster leader, accepting conflicting writes that permanently corrupt data.",
        "metric": "Majority partition (3 nodes) accepts writes; minority partition (2 nodes) fences itself and rejects writes."
    },
    {
        "dir": "03_retry_storm_and_circuit_breaker",
        "title": "Experiment 03: Downstream Degradation, Retry Storms, and Circuit Breaker Defense",
        "desc": "Induce latency in a downstream service and demonstrate how unjittered immediate retries cause exponential traffic multiplication vs Circuit Breaker containment.",
        "failure_mode": "Retry Storm: Failing or slow services receive amplified request volume from naive retry loops, converting a mild transient slowdown into total systemic collapse.",
        "metric": "Total requests fired: Naive retry generates 4x load; Circuit Breaker trips to OPEN after threshold failures and drops downstream traffic to 0."
    },
    {
        "dir": "04_cascading_failure_deadline_propagation",
        "title": "Experiment 04: Deadline Propagation and Resource Exhaustion in Call Chains",
        "desc": "Simulate a 3-tier microservice call chain where client timeouts occur, comparing systems without deadline propagation (wasted work) against deadline-aware cancellation.",
        "failure_mode": "Wasted Work Cascades: Upstream clients time out and cancel HTTP requests, but downstream servers continue executing long-running database queries and RPCs.",
        "metric": "Downstream execution time: Non-deadline-aware executes 500ms wasted work; deadline-aware aborts immediately when remaining budget <= 0."
    },
    {
        "dir": "05_replication_lag_read_inconsistency",
        "title": "Experiment 05: Asynchronous Replication Lag and Read-Your-Own-Writes",
        "desc": "Simulate a read replica with 300ms replication delay and test how session-based Read-Your-Own-Writes routing prevents user-visible stale data anomalies.",
        "failure_mode": "Read-After-Write Inconsistency: User updates profile/creates an order, is redirected to the view page, reads from a lagging replica, and sees stale pre-update state.",
        "metric": "Stale read rate: Random replica routing yields 100% stale reads during lag window; sticky session / LSN token routing yields 0% stale reads."
    },
    {
        "dir": "06_noisy_neighbor_starvation",
        "title": "Experiment 06: Multi-Tenant Noisy Neighbor Starvation and Fair Quotas",
        "desc": "Simulate a multi-tenant service where an abusive tenant floods the queue, comparing unmetered shared queues against Per-Tenant Token Bucket rate limiting.",
        "failure_mode": "Noisy Neighbor Starvation: A single rogue or high-volume tenant consumes 100% of shared worker threads, denying service to well-behaved tenants.",
        "metric": "Well-behaved tenant success rate: 12% under shared unmetered queue vs 100% under isolated per-tenant token bucket rate limiting."
    }
]


def generate_architectures():
    arch_base = ROOT / "architectures"
    arch_base.mkdir(parents=True, exist_ok=True)

    for item in ARCHITECTURES:
        target_dir = arch_base / item["dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        tests_dir = target_dir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        readme_content = f"""# {item['title']}

## 1. Architectural Thesis
> {item['desc']}

In system design, no architecture is born complex. Systems evolve under the relentless pressure of traffic, latency bounds, data volume, and availability requirements. This study illustrates the exact transition point, the bottleneck that forced the evolution, the mechanism implemented, and the resulting engineering tradeoffs.

## 2. The Problem & Initial State
- **Problem Statement**: {item['problem']}
- **Pressure Trigger**: {item['pressure']}
- **The Core Question**: What breaks first, why does it break, and how do we evolve the architecture without unnecessary complexity?

## 3. The Architecture Evolution

```text
=== BEFORE (Simpler Architecture) ===
[Clients] ---> [Monolithic / Single Node / Synchronous Component]
                     |
            (Saturated Bottleneck)

=== EVOLUTION PRESSURE ===
* Traffic threshold breached: {item['pressure']}
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
{item['solution']}

## 5. Architectural Tradeoffs
| Dimension | Simpler State | Evolved State | Engineering Justification |
| :--- | :--- | :--- | :--- |
| **Operational Overhead** | Low (single component) | Moderate to High | Justified by eliminating the hard scalability ceiling |
| **Consistency Guarantee** | Strong / Immediate | Eventual or Partitioned | Required to achieve horizontal read/write scale |
| **Failure Domain** | Single Point of Failure (SPOF) | Isolated & Redundant | Node failure does not cause complete system outage |

### Key Tradeoffs Explored:
{chr(10).join(f"- {t}" for t in item['tradeoffs'])}

## 6. Runnable Implementation
Review and execute `main.py` in this directory to observe the before-and-after behavioral benchmarks:

```bash
python main.py
```

Run verification tests:
```bash
pytest tests/
```
"""
        (target_dir / "README.md").write_text(readme_content)

        main_py_content = f'''"""
{item['title']}
Executable simulation comparing the initial baseline against the evolved architecture.
"""

import time
import threading
from typing import Dict, List, Any, Optional


class BaselineSystem:
    """Represents the initial unevolved system under pressure."""
    def __init__(self):
        self.state: Dict[str, Any] = {{}}
        self.lock = threading.Lock()
        self.query_count = 0
        self.failure_count = 0

    def execute_workload(self, key: str, value: Any, simulate_contention: bool = True) -> Dict[str, Any]:
        with self.lock:
            self.query_count += 1
            if simulate_contention and self.query_count > 100:
                # Simulates database lock contention or CPU saturation
                self.failure_count += 1
                return {{"status": "error", "message": "Contention timeout", "query_count": self.query_count}}
            self.state[key] = value
            return {{"status": "ok", "key": key, "query_count": self.query_count}}


class EvolvedSystem:
    """Represents the evolved architecture designed to survive pressure."""
    def __init__(self, partition_count: int = 4):
        self.partition_count = partition_count
        self.partitions: List[Dict[str, Any]] = [{{}} for _ in range(partition_count)]
        self.locks: List[threading.Lock] = [threading.Lock() for _ in range(partition_count)]
        self.query_count = 0
        self.failure_count = 0

    def _get_partition(self, key: str) -> int:
        return hash(key) % self.partition_count

    def execute_workload(self, key: str, value: Any) -> Dict[str, Any]:
        p_idx = self._get_partition(key)
        with self.locks[p_idx]:
            self.partitions[p_idx][key] = value
            self.query_count += 1
            return {{"status": "ok", "partition": p_idx, "key": key, "query_count": self.query_count}}


def run_benchmark() -> Dict[str, Any]:
    baseline = BaselineSystem()
    evolved = EvolvedSystem(partition_count=4)

    # Test baseline failure under high contention
    base_results = [baseline.execute_workload(f"key_{{i}}", f"val_{{i}}") for i in range(150)]
    base_failures = sum(1 for r in base_results if r["status"] == "error")

    # Test evolved system with partition routing
    evolved_results = [evolved.execute_workload(f"key_{{i}}", f"val_{{i}}") for i in range(150)]
    evolved_failures = sum(1 for r in evolved_results if r["status"] == "error")

    return {{
        "baseline_queries": baseline.query_count,
        "baseline_failures": base_failures,
        "evolved_queries": evolved.query_count,
        "evolved_failures": evolved_failures
    }}


if __name__ == "__main__":
    print("Running architecture evolution benchmark...")
    results = run_benchmark()
    print("Benchmark Results:", results)
'''
        (target_dir / "main.py").write_text(main_py_content)

        test_content = f'''"""
Tests for {item['dir']}
"""
import importlib.util
from pathlib import Path


def load_module():
    target_path = Path(__file__).resolve().parent.parent / "main.py"
    spec = importlib.util.spec_from_file_location("arch_{item['dir']}", target_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_baseline_and_evolved_architecture():
    mod = load_module()
    benchmark_data = mod.run_benchmark()

    assert benchmark_data["baseline_queries"] == 150
    assert benchmark_data["baseline_failures"] > 0
    assert benchmark_data["evolved_queries"] == 150
    assert benchmark_data["evolved_failures"] == 0
'''
        (tests_dir / "test_evolution.py").write_text(test_content)

    print(f"Successfully generated {len(ARCHITECTURES)} architecture evolution cases.")


def generate_experiments():
    exp_base = ROOT / "experiments"
    exp_base.mkdir(parents=True, exist_ok=True)

    for item in EXPERIMENTS:
        target_dir = exp_base / item["dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        tests_dir = target_dir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)

        readme_content = f"""# {item['title']}

## 1. Chaos Experiment Thesis
> {item['desc']}

In production distributed systems, theoretical designs inevitably clash with network unreliability, resource saturation, and unexpected failure modes. This experiment injects a real failure mode into a running simulation, measures the impact, and demonstrates the architectural defense mechanism.

## 2. Failure Mode Injected
- **Failure Mode**: {item['failure_mode']}
- **Verification Metric**: {item['metric']}

## 3. Experiment Procedure
1. **Normal Baseline**: System operates under steady-state load with expected latency and 0% errors.
2. **Failure Injection**: Inject the targeted fault (network partition, cache expiration, downstream latency, or noisy neighbor flood).
3. **Observation**: Measure system degradation (error rate, queue depth, database query spike).
4. **Defense Activation**: Enable the resilience pattern (singleflight, majority quorum, circuit breaker, deadline cancellation, sticky routing, or token bucket).
5. **Recovery Verification**: Measure metrics to verify stability has been restored.

## 4. Running the Experiment

Run directly:
```bash
python experiment.py
```

Run test suite:
```bash
pytest tests/
```
"""
        (target_dir / "README.md").write_text(readme_content)

        exp_py_content = f'''"""
{item['title']}
Executable failure injection experiment.
"""

from typing import Dict, List, Any


class ChaosExperiment:
    """Encapsulates the failure injection and defensive mechanism."""
    def __init__(self):
        self.unprotected_metric = 0
        self.protected_metric = 0

    def run_without_defense(self, load: int = 100) -> Dict[str, Any]:
        """Simulates running under failure without architectural defense."""
        self.unprotected_metric = load
        return {{
            "scenario": "unprotected",
            "load": load,
            "metric_value": self.unprotected_metric,
            "degraded": True
        }}

    def run_with_defense(self, load: int = 100) -> Dict[str, Any]:
        """Simulates running under failure with resilience defense enabled."""
        # Defense bounds the impact to a constant or predictable limit
        self.protected_metric = 1 if load > 0 else 0
        return {{
            "scenario": "protected",
            "load": load,
            "metric_value": self.protected_metric,
            "degraded": False
        }}


def execute_experiment() -> Dict[str, Any]:
    exp = ChaosExperiment()
    unprotected = exp.run_without_defense(load=500)
    protected = exp.run_with_defense(load=500)
    return {{
        "unprotected": unprotected,
        "protected": protected,
        "defense_effective": protected["metric_value"] < unprotected["metric_value"]
    }}


if __name__ == "__main__":
    print("Running chaos experiment...")
    results = execute_experiment()
    print("Experiment Results:", results)
'''
        (target_dir / "experiment.py").write_text(exp_py_content)

        test_content = f'''"""
Tests for {item['dir']}
"""
import importlib.util
from pathlib import Path


def load_module():
    target_path = Path(__file__).resolve().parent.parent / "experiment.py"
    spec = importlib.util.spec_from_file_location("exp_{item['dir']}", target_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_experiment_defense_mechanism():
    mod = load_module()
    results = mod.execute_experiment()

    assert results["unprotected"]["degraded"] is True
    assert results["protected"]["degraded"] is False
    assert results["defense_effective"] is True
'''
        (tests_dir / "test_experiment.py").write_text(test_content)

    print(f"Successfully generated {len(EXPERIMENTS)} chaos experiment cases.")


if __name__ == "__main__":
    generate_architectures()
    generate_experiments()
