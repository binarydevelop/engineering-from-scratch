# kubernetes-from-scratch

> **Understand it. Build it. Schedule it. Observe it. Break it. Reconcile it. Recover it. Scale it. Ship it.**

An experimental, first-principles curriculum that teaches Kubernetes deeply through implementation, experiments, inspection, failure injection, debugging, measurement, and progressively realistic distributed application deployments.

---

## The Core Mental Model

> **Kubernetes is an API-driven distributed control system that continuously reconciles declared desired state with observed cluster state.**

Most engineers begin by memorizing YAML tags:

```text
"A Deployment manages ReplicaSets."
"A Service provides stable networking."
```

This mental model breaks during the first production outage. When pods enter `CrashLoopBackOff`, services return 502s, or persistent volumes fail to mount, engineers who memorize YAML resort to cargo-culting: running `kubectl delete pod` repeatedly, editing manifests randomly, or searching for magic CLI flags.

In this repository, you will not memorize YAML. You will derive every abstraction from the real-world distributed systems problem it solves:

```text
We have 3 physical machines and 20 containers.
One process dies at 3 AM. Who notices? Who starts a replacement?
        ↓
Desired replicas = 3
Observed actual replicas = 2
        ↓
Controller calculates diff: Δ = 1
        ↓
Controller creates replacement
        ↓
Actual state approaches desired state
```

Only after building the reconciliation loop in code do we introduce the Kubernetes resource.

---

## What the Learner Eventually Understands

By completing this curriculum, whenever you look at an object in an architecture:

```text
Deployment           PersistentVolume      Job
Service              StatefulSet           HPA
Ingress / Gateway    DaemonSet             NetworkPolicy
ConfigMap            Secret                ResourceQuota
```

You will immediately explain:
1. **Why the object exists**: What acute engineering pain forced its creation?
2. **Which problem it solves**: What fails if we try to solve this with raw containers?
3. **What the control plane does with it**: How `kube-apiserver`, `etcd`, `kube-controller-manager`, and `kube-scheduler` process it.
4. **Which processes and components participate**: From the API wire to `kubelet`, `containerd`, and the Linux kernel.
5. **How traffic reaches the workload**: The exact packet path across virtual IPs, iptables/eBPF rules, and network namespaces.
6. **How the workload is restarted**: Container runtime exit codes, kubelet PLEG events, and restart backoffs.
7. **What happens when a node dies**: NodeLeases, heartbeat timeouts, taint-based evictions, and rescheduling.
8. **How desired state is reconciled**: Level-triggered feedback loops driving $\Delta = 0$.
9. **How state is stored**: Raft consensus in etcd, revision generations, and resource versions.
10. **What the failure modes are**: Diagnosing with an 11-step diagnostic workflow before searching online.
11. **When Kubernetes is unnecessary**: Recognizing when Docker Compose, VMs, or serverless are vastly superior.

---

## Architectural Progression

```text
Processes
   ↓
Containers
   ↓
Nodes
   ↓
Desired State (mini_controller.py)
   ↓
Reconciliation Loops
   ↓
Pods (Linux Namespaces & CGroups)
   ↓
Controllers (ReplicaSets & Deployments)
   ↓
Services (Virtual IPs & kube-proxy)
   ↓
Networking (CNI & Packet Flow)
   ↓
Storage (PV, PVC & CSI)
   ↓
Scheduling (Filtering & Scoring in scheduler_sim.py)
   ↓
Security (RBAC & Pod Security Standards)
   ↓
Scaling (HPA & Feedback Loops)
   ↓
Control Plane Architecture (apiserver, etcd, scheduler, kubelet)
   ↓
Disaster Recovery & Chaos Engineering (Failure Day)
   ↓
Mini-Orchestrator from Scratch (mini_k8s.py)
   ↓
Production System Design
```

---

## Pinned Baseline Tooling

To ensure 100% reproducibility and eliminate "works on my machine" issues, all manifests, scripts, and experiments are pinned:

| Tool | Pinned Version | Role / Context |
|---|---|---|
| **Kubernetes** | `v1.37.0` | Cluster Control Plane & Kubelet |
| **kubectl** | `v1.36.1+` | CLI API Client |
| **kind** | `v0.33.0` | Local multi-node cluster runner |
| **Node Image** | `kindest/node:v1.37.0` | Node OS, containerd v2.3.4, kubelet |
| **Docker** | `29.7.x+` (Docker Desktop 4.87+) | Container runner for kind node containers |
| **Python** | `3.11+` (Verified on 3.14) | Reconcilers, simulators, and controllers |
| **Helm** | `v4.3.0` | Manifest templating & packaging |

See [VERSIONS.md](VERSIONS.md) for the active API version matrix. No deprecated APIs are used (no `extensions/v1beta1`, no `PodSecurityPolicy`).

---

## The Prerequisite Boundary

This course begins where Docker ends:

> **"I can build images and run containers. Now: How do I operate hundreds of them across multiple failing servers reliably?"**

We do not spend hours re-teaching Dockerfiles or `docker run`. You should already understand processes, network ports, HTTP, and basic Linux.

---

## The 11-Step Systematic Debugging Workflow

When a workload or cluster fails, you do not randomly restart pods. You execute this diagnostic sequence:

```text
OBJECT ──► STATUS ──► CONDITIONS ──► EVENTS ──► OWNER ──► POD ──► CONTAINER ──► LOGS ──► NETWORK ──► CONFIG ──► STORAGE
```

1. **OBJECT**: Does the API object actually exist in the target namespace?
2. **STATUS**: Is it `Pending`, `CrashLoopBackOff`, `ImagePullBackOff`, `OOMKilled`, or `Terminating`?
3. **CONDITIONS**: What do `PodScheduled`, `Initialized`, `ContainersReady`, and `Ready` report?
4. **EVENTS**: What does the control plane black box recorder say (`kubectl describe pod` / `kubectl get events`)?
5. **OWNER**: Who owns this pod (`metadata.ownerReferences`: ReplicaSet, StatefulSet, or unmanaged)?
6. **POD**: Is the assigned worker node healthy (`MemoryPressure`, `DiskPressure`, `NotReady`)?
7. **CONTAINER**: What was the exact exit code (`137` = OOM, `1` = App error, `0` = Exited too soon)?
8. **LOGS**: What do container stdout/stderr report? (Check `--previous` for crashed pods!)
9. **NETWORK**: Are endpoints populated (`<none>` = selector typo or unready)? Does DNS resolve?
10. **CONFIG**: Are all referenced ConfigMaps, Secrets, and keys present?
11. **STORAGE**: Is the PVC in `Bound` status? Are volume mount permissions matching the container UID?

See [docs/kubectl-debugging.md](docs/kubectl-debugging.md) and [docs/troubleshooting.md](docs/troubleshooting.md).

---

## Quickstart: Setting Up the Local Lab

### 1. Verify Environment Prerequisites
```bash
make check
```
Verifies Docker, kind, kubectl, python3, and Helm versions.

### 2. Provision the 3-Node Local Cluster
```bash
make cluster-up
```
Provisions a 3-node Kubernetes v1.37.0 cluster (1 control plane, 2 worker nodes) using `kind`.

### 3. Inspect Cluster Health
```bash
make status
```
Inspects control-plane health, node topology, runtime versions, and system pods.

### 4. Run the Automated Python Code Suites
```bash
make test-all
```
Executes:
- Phase 02/03: Mini Reconciler (`mini_controller.py`)
- Phase 10: 3-Stage Scheduler Simulator (`scheduler_sim.py`)
- Phase 105: Capacity Planning & Bin-Packing Simulator (`bin_packing_sim.py`)
- Phase 117: Mini-Kubernetes Distributed Orchestrator (`mini_k8s.py`)

---

## Repository Structure

```text
kubernetes-from-scratch/
├── README.md                           # Master curriculum guide
├── ROADMAP.md                          # Complete 121-Phase roadmap
├── LEARNING.md                         # The 12 Invariant Rules of Study
├── LESSON_TEMPLATE.md                  # Canonical 21-section lesson template
├── VERSIONS.md                         # Pinned tool versions & active API matrix
├── CONTRIBUTING.md                     # Pedagogical & coding guidelines
├── Makefile                            # Automated build, test, and lab targets
│
├── scripts/
│   ├── check-environment.sh            # Prerequisites verifier
│   ├── create-cluster.sh               # 3-node kind cluster provisioner
│   ├── destroy-cluster.sh              # Clean cluster teardown
│   ├── cluster-status.sh               # Control plane & node health inspector
│   └── reset-lab.sh                    # Restores cluster back to baseline
│
├── docs/
│   ├── glossary.md                     # First-principles terminology
│   ├── mental-models.md                # Systems architecture in ASCII diagrams
│   ├── kubectl-debugging.md            # The 11-step debugging playbook
│   └── troubleshooting.md              # 25 common failure modes matrix
│
├── manifests/                          # Production-grade baseline manifests
├── projects/                           # 10 Capstone Projects & Chaos Drills
│   ├── 01-stateless-web-app/           # Ingress, Service, Deployment, HPA
│   ├── 02-app-plus-redis/              # Service discovery & cache resilience
│   ├── 03-app-plus-postgresql/         # Stateful DB + PVC + Secret
│   ├── 04-background-worker-system/    # Async queue + Graceful SIGTERM worker
│   ├── 05-stateful-application/        # StatefulSet + Headless DNS + PVC templates
│   ├── 06-multi-service-application/   # Multi-namespace cross-discovery
│   ├── 07-production-like-cluster/     # PSS restricted, PDB, HPA, anti-affinity
│   ├── 08-failure-day/                 # 8 Chaos Engineering failure drills
│   ├── 09-build-mini-kubernetes/       # Pure Python orchestrator (mini_k8s.py)
│   └── 10-custom-controller/           # Custom Resource Definition & operator
│
├── phases/                             # 121 Structured Curriculum Phases (00 to 120)
└── outputs/
    └── evidence-template.md            # Empirical evidence log template
```

---

## Beginning Lesson 01

Start your journey at **Phase 01**:
```bash
cat phases/01-why-kubernetes-exists/docs/en.md
```

Follow the study loop:
```text
Problem ──► Predict ──► Build ──► Inspect ──► Observe Controller ──► Break ──► Watch Reconciliation ──► Debug ──► Rebuild
```

---

## The Culmination

> Kubernetes is no longer YAML and magic controllers.
>
> We started with processes and containers, discovered the problems of scheduling and failure recovery, built reconciliation loops, introduced Pods and controllers, added stable networking and persistent storage, and then studied the control plane that continuously coordinates the cluster.
>
> Now when a Kubernetes object appears in an architecture, we can reason about the problem it solves, the controller that owns it, the state it declares, the failure modes it introduces, and whether Kubernetes is even necessary for the workload.
