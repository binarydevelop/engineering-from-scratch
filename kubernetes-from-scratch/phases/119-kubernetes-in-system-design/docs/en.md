# Phase 119: Kubernetes in System Design: The 18-Point Architectural Evaluation

When designing systems at scale, senior engineers do not simply choose Kubernetes because "everyone else does." Every architectural proposal must withstand an **18-point scrutiny framework**.

---

## The 18-Point Scrutiny Framework

For every workload under consideration, you must answer:
1. **Why Kubernetes?** What specific distributed orchestration requirement mandates it?
2. **Why not VMs?** What agility or bin-packing efficiency makes raw VMs insufficient?
3. **Why not Serverless?** What cost, startup latency, or long-running connection makes Fargate/Lambda inappropriate?
4. **Workload Classification**: Is it stateless, stateful, batch, or daemon?
5. **State Ownership**: Where does persistent state live (in-cluster PVC vs external managed database)?
6. **Resource Sizing**: What are the baseline CPU/Memory requests and limits?
7. **Storage Requirements**: What access modes (RWO, RWX) and storage classes are required?
8. **Communication Pattern**: How do services discover each other (ClusterIP, Headless, Ingress, gRPC)?
9. **Failure Domain Modeling**: What topology keys (AZs, nodes) must spread replicas?
10. **Health Checks**: What exact startup, readiness, and liveness probe thresholds prevent traffic drops?
11. **Deployment Strategy**: RollingUpdate, Canary, or Recreate?
12. **Autoscaling Mechanics**: HPA metrics (CPU, requests/sec) vs KEDA custom events?
13. **RBAC Isolation**: What ServiceAccount permissions are granted under least privilege?
14. **Network Segmentation**: What NetworkPolicies restrict east-west lateral movement?
15. **Observability**: What RED metrics, distributed traces, and log pipelines are attached?
16. **Worker Node Failure Blast Radius**: If a physical host dies, what happens to latency and traffic?
17. **Control Plane Outage Behavior**: If the API server is unreachable, how long can data-plane traffic survive?
18. **Operational Burden Accepted**: What maintenance, upgrade, and debugging overhead is the team committing to?

---

## 8 Production Design Case Studies

### Case Study 1: Multi-Tenant SaaS API
- **Challenge**: 50 microservices serving 10,000 requests/sec with strict tenant data isolation.
- **Architectural Reasoning**:
  - Namespace per tenant vs unified cluster with NetworkPolicy and RBAC scoping.
  - HPA triggered on HTTP request rate via Prometheus metrics adapter.
  - Ingress controller terminating TLS and routing by hostname (`<tenant>.api.saas.com`).

### Case Study 2: Asynchronous Job Processing Pool
- **Challenge**: Processing 1,000,000 audio transcoding tasks arriving in unpredictable bursts.
- **Architectural Reasoning**:
  - Deployments vs `batch/v1 Job` with dynamic completions.
  - Autoscaling driven by Redis/RabbitMQ queue depth rather than CPU utilization.
  - Spot / Preemptible node tolerations to slash infrastructure costs by 70%.

### Case Study 3: Real-Time Stream Processor (Apache Flink / Kafka Consumer)
- **Challenge**: Stateful stream processing requiring exactly-once semantics and checkpoint storage.
- **Architectural Reasoning**:
  - StatefulSet with dedicated PVCs for RocksDB state storage.
  - Headless service for task manager discovery.
  - PodDisruptionBudget ensuring minimum available task managers during cluster maintenance.

### Case Study 4: Clustered Distributed Datastore (Elasticsearch / Cassandra)
- **Challenge**: Running a 9-node search cluster across 3 availability zones.
- **Architectural Reasoning**:
  - Pod Topology Spread Constraints (`topologyKey: topology.kubernetes.io/zone`, `maxSkew: 1`).
  - ReadWriteOnce dynamic volumes with local NVMe SSD storage classes.
  - Dedicated worker node taints to prevent noisy neighbor memory competition.

### Case Study 5: Machine Learning Inference Serving
- **Challenge**: Serving PyTorch / LLM inference models requiring GPU acceleration.
- **Architectural Reasoning**:
  - Taints and tolerations: `dedicated=gpu:NoSchedule`.
  - Resource limits requesting `nvidia.com/gpu: 1`.
  - Startup probe with 3-minute initial delay to accommodate multi-gigabyte weight loading into VRAM.

### Case Study 6: Scheduled Cron Infrastructure
- **Challenge**: Nightly financial settlement and ledger reconciliation at 00:00 UTC.
- **Architectural Reasoning**:
  - `batch/v1 CronJob` with `concurrencyPolicy: Forbid` to prevent duplicate parallel billing.
  - Strict `backoffLimit: 2` and alerting on failed job events.

### Case Study 7: Internal Developer Platform (IDP)
- **Challenge**: Enabling 200 developers to spin up ephemeral staging environments on demand.
- **Architectural Reasoning**:
  - Custom Resource Definitions (`kind: PreviewEnvironment`) managed by a custom operator.
  - Hard ResourceQuotas and LimitRanges per dynamic namespace to prevent cluster starvation.

### Case Study 8: High-Traffic E-Commerce Checkout
- **Challenge**: Black Friday traffic surges where a 500ms outage costs $100,000.
- **Architectural Reasoning**:
  - Pre-scaled minimum replicas with PodDisruptionBudget `minAvailable: 80%`.
  - Anti-affinity spreading across distinct physical nodes and availability zones.
  - `preStop` hook sleep (5 seconds) to ensure iptables endpoints are drained before process shutdown.
