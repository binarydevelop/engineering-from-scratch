# The Complete Curriculum Roadmap: kubernetes-from-scratch

**Motto:** *Understand it. Build it. Schedule it. Observe it. Break it. Reconcile it. Recover it. Scale it. Ship it.*

This roadmap outlines all **121 Phases** of the curriculum, organized into 16 conceptual tiers of distributed systems mastery.

---

## Progress Overview

- [ ] **Tier 01: Foundations & Orchestration Invariants** (Phases 00 – 05)
- [ ] **Tier 02: Workload Atoms & Pod Architecture** (Phases 06 – 09)
- [ ] **Tier 03: Scheduling, Cgroups & Constraints** (Phases 10 – 15)
- [ ] **Tier 04: Controllers, Replication & Zero-Downtime Rollouts** (Phases 16 – 23)
- [ ] **Tier 05: The Networking Dataplane, Services & Virtual IPs** (Phases 24 – 35)
- [ ] **Tier 06: Configuration, Secrets & Persistent Storage** (Phases 36 – 45)
- [ ] **Tier 07: Specialized Workloads: Daemons & Batch Jobs** (Phases 46 – 48)
- [ ] **Tier 08: Multi-Tenancy, RBAC & Policy Governance** (Phases 49 – 59)
- [ ] **Tier 09: Dynamic Autoscaling & Termination Lifecycles** (Phases 60 – 67)
- [ ] **Tier 10: Telemetry, Observability & Systematic Debugging Labs** (Phases 68 – 74)
- [ ] **Tier 11: Control Plane Internals & Node Mechanics** (Phases 75 – 82)
- [ ] **Tier 12: Extensibility, Custom Operators & Manifest Packaging** (Phases 83 – 88)
- [ ] **Tier 13: Observability Stacks & Hardened Cluster Security** (Phases 89 – 99)
- [ ] **Tier 14: Failure Engineering & Disaster Recovery Drills** (Phases 100 – 103)
- [ ] **Tier 15: Systems Architecture, Capacity Planning & Anti-Patterns** (Phases 104 – 108)
- [ ] **Tier 16: Capstone Deployments, Mini-K8s & Final Mental Model** (Phases 109 – 120)

---

## Tier 01: Foundations & Orchestration Invariants

- [ ] **Phase 00: Local Kubernetes Lab** — Set up reproducible multi-node kind cluster on v1.37.0; inspect API client vs server split.
- [ ] **Phase 01: Why Kubernetes Exists** — Run raw containers manually; observe machine failure, port conflicts, and derive orchestration pain.
- [ ] **Phase 02: Desired State** — Build pure Python `mini_controller.py`; contrast declarative declarations with imperative commands.
- [ ] **Phase 03: Reconciliation Loops** — Implement continuous feedback loop: $\Delta = \text{Desired} - \text{Actual}$; kill processes and watch automated healing.
- [ ] **Phase 04: Kubernetes API** — Deconstruct the myth that "Kubernetes is YAML"; trace JSON payloads over HTTP REST endpoints.
- [ ] **Phase 05: etcd Concept** — Study distributed consensus (Raft), atomic compare-and-swap, watches, and persistent cluster state.

---

## Tier 02: Workload Atoms & Pod Architecture

- [ ] **Phase 06: Pods From First Principles** — Deconstruct why a Pod is the smallest atomic unit; explore Linux namespaces (net, ipc, uts).
- [ ] **Phase 07: Pod Lifecycle** — Map status transitions (Pending, Running, Succeeded, Failed, CrashLoopBackOff) and container exit codes.
- [ ] **Phase 08: Multi-Container Pods** — Sidecars and ambassadors sharing localhost loopback networking and shared emptyDir volumes.
- [ ] **Phase 09: Nodes** — Explore worker node responsibilities: kubelet heartbeats, NodeLeases, allocatable capacity vs total capacity.

---

## Tier 03: Scheduling, Cgroups & Constraints

- [ ] **Phase 10: Scheduling From Scratch** — Implement `scheduler_sim.py`; derive the 3-stage pipeline (Filter, Score, Bind).
- [ ] **Phase 11: kube-scheduler** — Trace unscheduled pods (`spec.nodeName == ""`) and observe the binding subresource.
- [ ] **Phase 12: Requests and Limits** — Contrast scheduling accounting (`requests`) with Linux cgroup enforcement (`limits`).
- [ ] **Phase 13: OOM and CPU Throttling** — Differentiate compressible CPU CFS throttling from non-compressible memory exhaustion (Exit Code 137).
- [ ] **Phase 14: Labels** — The multidimensional loose-coupling metadata substrate connecting independent objects.
- [ ] **Phase 15: Selectors** — Equality-based and set-based filtering forming dynamic workload sets.

---

## Tier 04: Controllers, Replication & Zero-Downtime Rollouts

- [ ] **Phase 16: ReplicaSet From First Principles** — Maintain integer replica counts; observe selector ownership and orphan adoption.
- [ ] **Phase 17: Controllers** — Informers, Lister indexers, workqueues, and level-triggered reconciliation loops.
- [ ] **Phase 18: Deployments** — Declarative management of ReplicaSets, rollouts, pauses, and rollbacks.
- [ ] **Phase 19: Rollouts** — Trace zero-downtime rolling updates using `maxSurge` and `maxUnavailable` algorithms.
- [ ] **Phase 20: Rollback** — Recovering from broken software releases in seconds using `kubectl rollout undo`.
- [ ] **Phase 21: Readiness Probes** — Isolate booting or unready containers from receiving live user traffic.
- [ ] **Phase 22: Liveness Probes** — Detect internal process deadlocks and trigger automated container restarts.
- [ ] **Phase 23: Startup Probes** — Guard slow-starting legacy applications against premature liveness terminations.

---

## Tier 05: The Networking Dataplane, Services & Virtual IPs

- [ ] **Phase 24: Pod IPs and Ephemeral Identity** — Observe IP address churn during pod recreation; motivate stable identities.
- [ ] **Phase 25: Service From First Principles** — Build stable virtual endpoint abstraction decoupling clients from ephemeral pod IPs.
- [ ] **Phase 26: ClusterIP** — Internal layer-4 virtual IP routing and kernel packet translation (DNAT).
- [ ] **Phase 27: Kubernetes DNS** — CoreDNS resolution mechanics, `/etc/resolv.conf`, and `ndots:5` search path.
- [ ] **Phase 28: Service Discovery** — Short names vs fully qualified domain names across namespaces.
- [ ] **Phase 29: NodePort** — Expose services on dedicated node ports (30000–32767) across all worker nodes.
- [ ] **Phase 30: LoadBalancer Service** — Cloud Controller Manager integration and public external IP routing.
- [ ] **Phase 31: Ingress / Gateway Concepts** — Layer 7 HTTP/HTTPS reverse proxying, path routing, and Gateway API evolution.
- [ ] **Phase 32: Traffic Path** — Hop-by-hop packet trace: Client -> LB -> Ingress -> Service VIP -> iptables -> veth -> socket.
- [ ] **Phase 33: Kubernetes Networking Mental Model** — The flat IP model: all pods can talk to all pods without NAT.
- [ ] **Phase 34: CNI Concept** — Container Network Interface plugins (kindnet, Calico, Cilium) configuring host namespaces.
- [ ] **Phase 35: Network Debugging** — Isolate DNS failures, selector typos, targetPort mismatches, and socket binding traps.

---

## Tier 06: Configuration, Secrets & Persistent Storage

- [ ] **Phase 36: ConfigMap** — Decouple runtime plaintext configuration from container images.
- [ ] **Phase 37: Secrets** — API-governed sensitive configuration, tmpfs memory mounts, and debunking the Base64 myth.
- [ ] **Phase 38: Environment Configuration** — Promoting single immutable images across environments via configuration overlays.
- [ ] **Phase 39: Volumes** — Container filesystem ephemerality vs pod-level storage lifecycles.
- [ ] **Phase 40: emptyDir** — Pod-lifetime scratch storage and sidecar data sharing.
- [ ] **Phase 41: PersistentVolume Concept** — Decouple storage lifecycle from Pods: PersistentVolume vs PersistentVolumeClaim.
- [ ] **Phase 42: StorageClass** — Dynamic on-demand volume provisioning with CSI storage drivers.
- [ ] **Phase 43: Stateful Applications** — Unique requirements of clustered databases: identity, ordered boot, persistent disks.
- [ ] **Phase 44: StatefulSet** — Deterministic ordinal indexing (`app-0`, `app-1`), dedicated PVC templates, ordered scaling.
- [ ] **Phase 45: Headless Services** — `clusterIP: None` direct DNS A-records for peer-to-peer database clustering.

---

## Tier 07: Specialized Workloads: Daemons & Batch Jobs

- [ ] **Phase 46: DaemonSet** — Run exactly one copy of a Pod on every worker host for logging and monitoring agents.
- [ ] **Phase 47: Jobs** — Run-to-completion batch execution with retries (`backoffLimit`) and parallelism.
- [ ] **Phase 48: CronJobs** — Recurring scheduled batch jobs, concurrency policies (Allow, Forbid, Replace), and idempotence.

---

## Tier 08: Multi-Tenancy, RBAC & Policy Governance

- [ ] **Phase 49: Namespaces** — Logical scoping, multi-tenant grouping, and administrative boundaries.
- [ ] **Phase 50: ResourceQuota** — Enforce hard aggregate ceilings on namespace CPU, memory, and pod counts.
- [ ] **Phase 51: LimitRange** — Set container-level request/limit defaults and validation bounds.
- [ ] **Phase 52: RBAC From First Principles** — Subject -> RoleBinding -> Role (Verbs on Resources).
- [ ] **Phase 53: ServiceAccounts** — Workload API identities and projected short-lived JWT tokens.
- [ ] **Phase 54: Admission Control** — Mutating and validating admission webhooks intercepting requests before etcd persistence.
- [ ] **Phase 55: NetworkPolicy** — Pod-level packet firewalling restricting east-west lateral traffic movement.
- [ ] **Phase 56: Scheduling Constraints** — Guiding placement via `nodeSelector`, `nodeAffinity`, `podAffinity`, and `podAntiAffinity`.
- [ ] **Phase 57: Taints and Tolerations** — Repelling workloads from dedicated nodes (e.g. GPU, batch) with taint effects.
- [ ] **Phase 58: Topology Spread Constraints** — Spreading replicas evenly across failure domains (nodes, availability zones).
- [ ] **Phase 59: PodDisruptionBudget** — Protecting service availability during voluntary administrative disruptions (`kubectl drain`).

---

## Tier 09: Dynamic Autoscaling & Termination Lifecycles

- [ ] **Phase 60: Horizontal Pod Autoscaler** — Feedback-based horizontal scaling driven by CPU and custom metrics.
- [ ] **Phase 61: Metrics Server** — Lightweight metrics aggregation via kubelet Summary APIs.
- [ ] **Phase 62: Vertical Scaling Concepts** — Right-sizing CPU/memory requests based on historical usage (VPA).
- [ ] **Phase 63: Cluster Autoscaling Concept** — Provisioning and terminating physical/virtual nodes to accommodate pending pods.
- [ ] **Phase 64: Deployment Strategies** — Comparing RollingUpdate, Recreate, Blue/Green, and Canary rollout strategies.
- [ ] **Phase 65: Canary Deployment** — Shifting a percentage of production traffic to a new version to validate error budgets.
- [ ] **Phase 66: Graceful Shutdown** — Handling SIGTERM, draining in-flight requests, and `terminationGracePeriodSeconds`.
- [ ] **Phase 67: PreStop and Termination Grace** — Synchronizing application shutdown with iptables endpoint removal to prevent 502s.

---

## Tier 10: Telemetry, Observability & Systematic Debugging Labs

- [ ] **Phase 68: Kubernetes Events** — The chronological event stream of the control plane; reading causes of failure.
- [ ] **Phase 69: Logs** — Container stdout/stderr, `--previous` logs of crashed instances, multi-container logging.
- [ ] **Phase 70: exec and port-forward** — Interactive shell inspection and local port tunnels for developer triage.
- [ ] **Phase 71: Debugging Workflow** — Internalizing the 11-step diagnostic workflow (`OBJECT -> ... -> STORAGE`).
- [ ] **Phase 72: Broken Pod Labs** — 7 real-world incident simulations: ImagePullBackOff, CrashLoop, OOM, missing configs.
- [ ] **Phase 73: Broken Networking Labs** — 6 incident simulations: selector typos, wrong targetPort, localhost traps, network policies.
- [ ] **Phase 74: Broken Storage Labs** — 4 incident simulations: PVC pending, non-root permission denied, ephemeral loss.

---

## Tier 11: Control Plane Internals & Node Mechanics

- [ ] **Phase 75: Control Plane Components** — Architectural deep-dive: API Server, Scheduler, Controller Manager, etcd.
- [ ] **Phase 76: kube-apiserver** — REST handlers, OpenAPI validation, authentication, authorization, etcd serialization.
- [ ] **Phase 77: Controller Manager** — Monolithic binary running dozens of independent control loops.
- [ ] **Phase 78: Scheduler Internals Conceptually** — Scheduling queue (activeQ, backoffQ), priority queues, and binding cycles.
- [ ] **Phase 79: kubelet** — Node daemon, PLEG (Pod Lifecycle Event Generator), syncLoop, and status reporting.
- [ ] **Phase 80: Container Runtime and CRI** — CRI gRPC API, containerd, runc, and removal of legacy dockershim.
- [ ] **Phase 81: kube-proxy / Service Dataplane** — iptables NAT tables (PREROUTING, KUBE-SERVICES), IPVS, and eBPF maps.
- [ ] **Phase 82: etcd Failure and Importance** — Raft consensus quorum ($2N+1$), split-brain protection, control plane read-only degradation.

---

## Tier 12: Extensibility, Custom Operators & Manifest Packaging

- [ ] **Phase 83: Custom Resources** — Extending the Kubernetes API with CustomResourceDefinitions (CRDs).
- [ ] **Phase 84: Build a Tiny Controller** — Writing `webapp_controller.py` in Python to reconcile Custom Resources into child Deployments.
- [ ] **Phase 85: Operators** — The Operator Pattern: $\text{CRD} + \text{Controller} + \text{Operational Domain Logic}$.
- [ ] **Phase 86: Helm From First Principles** — Manifest parameterization, Go templating, values, and release management.
- [ ] **Phase 87: Kustomize** — Template-free declarative manifest customization with base and overlays.
- [ ] **Phase 88: GitOps Concept** — Git as single source of truth; automated synchronization and drift detection.

---

## Tier 13: Observability Stacks & Hardened Cluster Security

- [ ] **Phase 89: Observability** — The 4 pillars: Metrics, Logs, Traces, and Events in distributed architectures.
- [ ] **Phase 90: Prometheus** — Pull-based time-series scraping of `/metrics` endpoints and PromQL queries.
- [ ] **Phase 91: Application Metrics** — RED method (Rate, Errors, Duration) instrumentation in container code.
- [ ] **Phase 92: Resource Metrics** — Measuring cgroup working set memory vs RSS and CPU throttle ratios.
- [ ] **Phase 93: Alerts** — Alerting on user symptoms (high error rate, crash loops) rather than noisy infrastructure causes.
- [ ] **Phase 94: Security Fundamentals** — Defense in depth across images, identities, networks, and runtimes.
- [ ] **Phase 95: Pod Security Standards** — Enforcing `baseline` and `restricted` profiles; rejecting root and privileged containers.
- [ ] **Phase 96: Image Security** — Immutable SHA256 digests, minimal distroless base images, vulnerability scanning.
- [ ] **Phase 97: Resource Security** — Least privilege across RBAC, ServiceAccounts, Secrets, and NetworkPolicies.
- [ ] **Phase 98: Cluster Upgrades Concept** — Version skew policies (N-3), kubeadm upgrade workflow, node cordon/drain.
- [ ] **Phase 99: High Availability Control Plane** — 3-member etcd quorum, load-balanced API servers, active-standby controllers.

---

## Tier 14: Failure Engineering & Disaster Recovery Drills

- [ ] **Phase 100: Multi-Node Failure Lab** — Killing a worker node; observing node heartbeats, eviction timeouts, and rescheduling.
- [ ] **Phase 101: Application Failure Lab** — Crashing cascading microservice dependencies and observing controller healing.
- [ ] **Phase 102: Deployment Failure Lab** — Triggering broken rollout, observing `ProgressDeadlineExceeded`, and rolling back.
- [ ] **Phase 103: Stateful Failure Lab** — Crashing a StatefulSet replica and verifying PVC volume reattachment and zero data loss.

---

## Tier 15: Systems Architecture, Capacity Planning & Anti-Patterns

- [ ] **Phase 104: Capacity Planning** — Calculating required cluster CPU and memory headroom based on aggregate requests.
- [ ] **Phase 105: Bin Packing & Node Sizing** — Running `bin_packing_sim.py`; comparing many small nodes vs few large nodes.
- [ ] **Phase 106: Cost Thinking** — Cloud cost drivers: unallocated requests, idle node headroom, overprovisioned disks.
- [ ] **Phase 107: Kubernetes Anti-Patterns** — The 18 catastrophic anti-patterns and their underlying failure modes.
- [ ] **Phase 108: When Kubernetes Is the Wrong Tool** — 6 scenarios where VMs, serverless, or Docker Compose are vastly superior.

---

## Tier 16: Capstone Deployments, Mini-K8s & Final Mental Model

- [ ] **Phase 109: Project: Stateless Web App** — End-to-end production deployment: Ingress, probes, HPA, rollout, anti-affinity.
- [ ] **Phase 110: Project: App + Redis** — Multi-tier caching architecture with service discovery and dependency resilience.
- [ ] **Phase 111: Project: App + PostgreSQL** — Stateful relational database with PVC, Secrets, and persistence recovery test.
- [ ] **Phase 112: Project: Background Worker System** — Asynchronous task consumer with graceful SIGTERM termination.
- [ ] **Phase 113: Project: Stateful Application** — Clustered StatefulSet with stable ordinals, headless DNS, and dedicated PVCs.
- [ ] **Phase 114: Project: Multi-Service Application** — Multi-namespace distributed system with cross-namespace DNS discovery.
- [ ] **Phase 115: Production-Like Cluster Project** — Complete hardened deployment: PSS restricted, PDB, HPA, NetworkPolicy, non-root UID.
- [ ] **Phase 116: Failure Day Drills** — Executing the 8 chaos engineering drills and diagnosing with the 11-step playbook.
- [ ] **Phase 117: Build Mini Kubernetes** — Pure Python distributed orchestrator (`mini_k8s.py`): API, Controller, Scheduler, Kubelet.
- [ ] **Phase 118: Write a Custom Controller** — Building a live Kubernetes operator reconciling Custom Resources (`webapp_controller.py`).
- [ ] **Phase 119: Kubernetes in System Design** — 18-point architectural scrutiny across 8 production case studies.
- [ ] **Phase 120: Final Mental Model** — Tracing `kubectl apply -f deployment.yaml` to the kernel socket and self-healing reconciliation.
