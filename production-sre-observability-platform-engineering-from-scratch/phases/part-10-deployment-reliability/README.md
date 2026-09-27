# Part 10: Deployment Reliability & Change Safety (Phases 115 – 123)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Deployments cause over 70% of production incidents. Part 10 treats every code release as a risk event requiring verified health checks, graceful draining, progressive canary delivery, and instantaneous rollback capability.

---

## Key Deployment Patterns

### 1. Health Checks Deep Dive (Phase 116)
* **Startup Probe**: Handles slow application initialization and schema checks without Kubernetes prematurely killing the pod.
* **Readiness Probe**: Tells load balancers whether to send traffic. Fails when worker threads are saturated or database is unreachable.
* **Liveness Probe**: Tells Kubernetes when to kill and restart a deadlocked process. Must NOT fail on transient dependency hiccups!

### 2. Graceful Shutdown & Zero-Downtime Draining (Phase 117)
When Kubernetes terminates a pod:
1. Pod transitions to `Terminating` and is removed from Endpoints / Load Balancer.
2. Kernel sends `SIGTERM` to the container process.
3. Service stops accepting new requests, allows in-flight requests to complete (up to 30s), closes database connections cleanly, and exits.

### 3. Progressive Canary Releases (Phase 120)
Routing 5% of traffic to the new image version:
* Compare error rate and p99 latency between Canary and Baseline pods.
* If Canary error rate > Baseline error rate by 0.5%, abort deployment automatically.

### 4. Database Schema Migration Safety (Phase 123)
The **Expand and Contract Pattern**:
* Never rename or drop a column in the same release as application code changes.
* Phase 1: Add new column (Nullable). Both old and new code work.
* Phase 2: Deploy code writing to both columns.
* Phase 3: Backfill data.
* Phase 4: Deploy code reading exclusively from new column.
* Phase 5: Drop old column.
