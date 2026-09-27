# Phases 124 – 136: Kubernetes in Production & Operating Realities

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phases 124 – 128: Linux Cgroups, Quotas & OOM Mechanics

### CPU Requests vs Limits & CFS Quotas (Phase 125 & 126)
* In Linux, CPU limits are enforced by CFS Bandwidth Control (`cpu.cfs_quota_us` and `cpu.cfs_period_us`).
* If a container has a 500m limit, it is permitted 50ms of CPU runtime every 100ms.
* If a multi-threaded process spins 4 threads for 15ms ($4 \times 15 = 60\text{ms}$), it exhausts its quota in 15ms and is **frozen by the Linux kernel for the remaining 85ms!**
* **The Production Result**: Latency spikes to 85ms while CPU utilization metrics report only 25% busy!

### Memory Limits & OOMKilled (Exit Code 137) (Phase 127)
* Memory has no throttling mechanism. When a container requests 1 byte more than its limit, the Linux kernel invokes `out_of_memory()`.
* The kernel scans `/proc/[pid]/oom_score` and terminates the process with `SIGKILL`.
* `128 + 9 (SIGKILL) = 137`.

---

## Phases 129 – 133: Autoscaling Lag & Disruption Budgets

### The HPA Lag Cliff (Phase 130)
```text
Traffic Spike (0s)  ──►  Prometheus Scrape (30s)  ──►  HPA Evaluate (45s)
                                                              │
                                                              ▼
Pod Scheduled (60s) ◄── Image Pull (75s) ◄── Container Start (90s)
         │
         ▼
Cache Pre-Warmed & Traffic Accepted (120s)
```
Autoscaling takes up to **2 minutes** to bring new capacity online. Always maintain at least 30–40% warm headroom!

### Topology Spread Constraints (Phase 133)
Ensure replicas are evenly distributed across availability zones:
```yaml
topologySpreadConstraints:
  - maxSkew: 1
    topologyKey: topology.kubernetes.io/zone
    whenUnsatisfiable: DoNotSchedule
    labelSelector:
      matchLabels:
        app: checkout-service
```
Prevents all 3 replicas from being co-located on a single node or failing zone!

---

## Phases 134 – 136: Collector Deployment Patterns in Kubernetes

### DaemonSet vs Gateway Topology (Phase 136)
* **DaemonSet (Agent Pattern)**: Runs 1 Collector pod per node. Applications export via `localhost:4317` over high-speed node loopback. Collector enriches telemetry with `k8s.pod.name` and node metadata.
* **Gateway (Cluster Collector)**: StatefulSet behind a Service for heavy processing, tail-based sampling, and centralized credential management.
* **Production Standard**: Hybrid topology (DaemonSet agents forward to Gateway collectors).
