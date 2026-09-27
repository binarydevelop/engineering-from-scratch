# Part 11: Kubernetes in Production (Phases 124 – 136)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 11 assumes basic Kubernetes knowledge and focuses entirely on the production operating consequences: cgroups CPU throttling, OOMKilled mechanics, HPA lag, PodDisruptionBudgets, and OpenTelemetry Collector topologies.

---

## Key Production Realities

### 1. Resource Requests vs Limits (Phase 125 & 126)
* **Requests**: Used by kube-scheduler to place pods on nodes.
* **CPU Limits**: Enforced by the Linux Completely Fair Scheduler (CFS) quota. If a container exceeds its CPU limit in a 100ms window, the kernel throttles its execution, causing severe latency spikes even when overall host CPU is low!
* **Production Best Practice**: Set accurate CPU requests; carefully evaluate whether CPU limits introduce unnecessary CFS throttling.

### 2. The Linux OOM Killer (Phase 127)
When a container exceeds its `memory.limit_in_bytes`, the Linux kernel triggers the Out-Of-Memory (OOM) killer. The kernel selects the process with the highest `oom_score`, sends `SIGKILL` (`kill -9`), and Kubernetes reports `OOMKilled` (Exit Code 137).

### 3. Horizontal Pod Autoscaler (HPA) Lag (Phase 129 & 130)
Traffic spikes arrive in milliseconds; Kubernetes autoscaling takes minutes:
1. Metrics pipeline scrape delay (15–30s).
2. HPA evaluation interval (15s).
3. Container image pull and pod initialization (30–60s).
4. Application cache warming (10–30s).
**Total Lag**: 1.5 to 2.5 minutes! You cannot rely on autoscaling for sudden burst protection; you must maintain warm headroom.

### 4. PodDisruptionBudgets (PDBs) (Phase 132)
Guarantees that cluster upgrades, node drains, or automated autoscaler downsizings never terminate more than an allowable percentage of replicas simultaneously:
```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: checkout-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app: checkout-service
```
