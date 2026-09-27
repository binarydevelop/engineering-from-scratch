# Kubernetes Mental Models: Systems Architecture in Diagrams

This document collects the foundational mental models and ASCII architectural diagrams for reasoning about Kubernetes as a distributed control system.

---

## 1. The Cluster Boundary: Control Plane vs. Worker Nodes

```text
                        THE KUBERNETES CONTROL PLANE
         ┌────────────────────────────────────────────────────────┐
         │                                                        │
         │   Human / CI/CD (kubectl)                              │
         │             │                                          │
         │             ▼ HTTPS (Port 6443)                        │
         │   ┌──────────────────────────────────────────────┐     │
         │   │               kube-apiserver                 │     │
         │   │ (Authentication, RBAC, Admission, Schema)    │     │
         │   └───────┬──────────────────────────────┬───────┘     │
         │           │                              │             │
         │           ▼ Raft Protocol                ▼ Watch API   │
         │   ┌───────────────┐          ┌───────────────────────┐ │
         │   │     etcd      │          │     kube-scheduler    │ │
         │   │ (Cluster DB)  │          │ (Filters & Scores)    │ │
         │   └───────────────┘          └───────────────────────┘ │
         │                                          ▲             │
         │                                          │ Watch API   │
         │                              ┌───────────┴───────────┐ │
         │                              │kube-controller-manager│ │
         │                              │(Deployment, RS, Node) │ │
         │                              └───────────────────────┘ │
         └──────────────────────────┬─────────────────────────────┘
                                    │
                         Kubernetes HTTPS API Wire
                                    │
       ┌────────────────────────────┴───────────────────────────┐
       ▼                                                        ▼
WORKER NODE 01                                           WORKER NODE 02
┌───────────────────────────────┐                        ┌───────────────────────────────┐
│ kubelet (Node Agent)          │                        │ kubelet (Node Agent)          │
│   │ gRPC CRI                  │                        │   │ gRPC CRI                  │
│   ▼                           │                        │   ▼                           │
│ containerd (Container Runtime)│                        │ containerd (Container Runtime)│
│   │ fork/exec                 │                        │   │ fork/exec                 │
│   ▼                           │                        │   ▼                           │
│ Pod A-1      Pod B-1          │                        │ Pod A-2      Pod C-1          │
│ [App+CGroup] [App+CGroup]     │                        │ [App+CGroup] [App+CGroup]     │
│                               │                        │                               │
│ kube-proxy (iptables / IPVS)  │                        │ kube-proxy (iptables / IPVS)  │
│ CNI Plugin (kindnet / veth)   │                        │ CNI Plugin (kindnet / veth)   │
└───────────────────────────────┘                        └───────────────────────────────┘
```

---

## 2. The Fundamental Reconciliation Control Loop

Every controller in the Kubernetes ecosystem executes this feedback equation:

$$\Delta = \text{Desired State (spec)} - \text{Actual State (status)}$$

```text
       ┌────────────────────────────────────────────────────────┐
       │               DECLARED DESIRED STATE                   │
       │         (e.g., spec.replicas = 3 in etcd)              │
       └──────────────────────────┬─────────────────────────────┘
                                  │
                                  ▼
                     CONTROLLER RECONCILIATION LOOP
                     ┌───────────────────────────────┐
                     │ 1. WATCH: Receive API update  │
                     │ 2. OBSERVE: Count live Pods   │
                     │ 3. COMPARE: Calculate diff    │
                     └───────────────┬───────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
             If Replicas < 3                   If Replicas > 3
             (Actual = 2)                      (Actual = 4)
                    ▼                                 ▼
         POST /api/v1/pods                 DELETE /api/v1/pods/x
         (Create Replacement)              (Evict / Terminate)
                    │                                 │
                    └────────────────┬────────────────┘
                                     ▼
       ┌────────────────────────────────────────────────────────┐
       │                 ACTUAL OBSERVED STATE                  │
       │              (Cluster approaches Δ = 0)                │
       └────────────────────────────────────────────────────────┘
```

---

## 3. The Lifecycle of a Request: From `kubectl apply` to Running Pod

What happens under the hood when you apply a Deployment:

```text
STEP 1: CLIENT
  User runs: kubectl apply -f deployment.yaml
  kubectl sends HTTP POST/PUT to /apis/apps/v1/namespaces/default/deployments

STEP 2: API SERVER ADMISSION CHAIN
  kube-apiserver receives request:
  ├── 1. Authentication: Extracts TLS client cert or bearer token (Identifies user/SA).
  ├── 2. Authorization: Queries RBAC (Can this user 'create' 'deployments' in 'default'?).
  ├── 3. Mutating Admission: Injects default values, sidecars, or labels.
  ├── 4. Schema Validation: Validates manifest types against OpenAPI schema.
  └── 5. Validating Admission: Runs security checks (Pod Security Standards).

STEP 3: STORAGE
  kube-apiserver writes Deployment object to etcd.

STEP 4: DEPLOYMENT CONTROLLER
  DeploymentController in kube-controller-manager observes new Deployment.
  Creates a ReplicaSet (spec.replicas = 3, ownerReferences -> Deployment).
  Writes ReplicaSet to kube-apiserver -> persisted in etcd.

STEP 5: REPLICASET CONTROLLER
  ReplicaSetController observes new ReplicaSet.
  Observes desired = 3, actual = 0.
  Issues 3x POST /api/v1/namespaces/default/pods.
  Note: Pods are created with spec.nodeName = "" (UNSCHEDULED).

STEP 6: SCHEDULER
  kube-scheduler watches for Pods where spec.nodeName == "".
  For each unscheduled Pod:
  ├── 1. Filtering: Removes nodes without enough CPU/RAM, or with unmatched taints.
  ├── 2. Scoring: Ranks surviving nodes (least requested resources, spreading).
  └── 3. Binding: Writes Binding object (spec.nodeName = "worker-01") to API server.

STEP 7: KUBELET & CONTAINER RUNTIME
  kubelet on "worker-01" watches API for Pods assigned to "worker-01".
  Observes new Pod assignment:
  ├── 1. Calls CNI plugin to set up network namespace and allocate Pod IP.
  ├── 2. Calls CRI runtime (containerd) to pull container images.
  ├── 3. Calls containerd to create and start container processes with cgroup limits.
  ├── 4. Mounts volumes, ConfigMaps, and Secrets into container mount points.
  └── 5. Updates Pod status (status.phase = Running, Ready = True) back to API server.
```

---

## 4. The Scheduling Pipeline: Filter -> Score -> Bind

```text
                  UNSCHEDULED POD (spec.nodeName = "")
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │            PRE-FILTER / FILTER            │
             │ Does node have enough allocatable CPU?    │
             │ Does node have enough allocatable Memory? │
             │ Does node have required labels?           │
             │ Can Pod tolerate node's taints?           │
             └─────────────────────┬─────────────────────┘
                                   │
                           Surviving Nodes
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │              SCORE / PRIORITIZE           │
             │ NodeResourcesBalancedAllocation           │
             │ ImageLocalityPriority (image cached?)     │
             │ PodTopologySpread (spread across zones?)  │
             │ NodeAffinityPriority                      │
             └─────────────────────┬─────────────────────┘
                                   │
                              Highest Score
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │             RESERVE & PERMIT              │
             │ Atomic check on remaining node capacity   │
             └─────────────────────┬─────────────────────┘
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │                   BIND                    │
             │ Write Binding: spec.nodeName = "node-2"   │
             └───────────────────────────────────────────┘
```

---

## 5. The Service Dataplane & Virtual IPs

Services are not processes. A Service `ClusterIP` is a virtual IP that exists only inside node packet-filtering tables:

```text
CLIENT POD (10.244.1.5)
      │
      │ 1. Connects to http://payments:8080 (ClusterIP: 10.96.25.100:8080)
      ▼
NODE KERNEL PACKET FILTER (iptables / IPVS / eBPF managed by kube-proxy)
      │
      │ 2. Intercepts packet destined for 10.96.25.100:8080
      │ 3. Looks up EndpointSlice for 'payments' Service:
      │    [10.244.1.12:80, 10.244.2.8:80, 10.244.2.9:80]
      │ 4. Performs DNAT (Destination Network Address Translation):
      │    Rewrites Dest IP 10.96.25.100 -> 10.244.2.8
      ▼
LINUX ROUTING TABLE / CNI BRIDGE
      │
      │ 5. Routes packet directly to Pod B on Node 2 (10.244.2.8:80)
      ▼
BACKEND CONTAINER (10.244.2.8:80)
      │
      │ 6. Application receives packet, unaware that a virtual IP was used
```

---

## 6. The Storage Chain: PersistentVolumeClaim to Disk

```text
    DEVELOPER MANIFEST                  CLUSTER RESOURCE (Admin / Cloud)
┌─────────────────────────┐               ┌─────────────────────────┐
│ PersistentVolumeClaim   │               │ PersistentVolume        │
│ spec:                   │               │ spec:                   │
│   storageClassName: standard             │   capacity: 10Gi        │
│   resources: 5Gi        │   Binds to    │   accessModes: [RWO]    │
│   accessModes: [RWO]    │ ────────────> │   hostPath / cloud-disk │
└────────────┬────────────┘               └────────────┬────────────┘
             │                                         │
             ▼                                         ▼
   POD SPEC                                 STORAGE PROVISIONER (CSI)
┌─────────────────────────┐               ┌─────────────────────────┐
│ Pod: web-db             │               │ Dynamic Provisioner     │
│ volumes:                │               │ Watches PVCs -> calls   │
│ - name: data            │               │ cloud/local disk API -> │
│   persistentVolumeClaim:│               │ formats volume ->       │
│     claimName: my-pvc   │               │ creates PV matching PVC │
└────────────┬────────────┘               └─────────────────────────┘
             │
             ▼ Kubelet Volume Manager
┌───────────────────────────────────────────────────────────────────┐
│ Worker Node: /var/lib/kubelet/pods/<uid>/volumes/kubernetes.io~csi│
│ Bind-mounted into Container at /var/lib/postgresql/data           │
└───────────────────────────────────────────────────────────────────┘
```

---

## 7. Hop-by-Hop Traffic Path: External Client to App

```text
EXTERNAL USER (e.g. Browser or curl)
      │
      ▼ (Port 80/443 on host / Load Balancer)
INGRESS CONTROLLER (e.g. Envoy / Nginx Pod)
      │
      │ 1. Evaluates Host header (api.example.com) and Path (/v1/users)
      │ 2. Looks up Ingress routing rules
      │ 3. Proxies request to upstream Service
      ▼
SERVICE (ClusterIP Virtual IP)
      │
      │ 4. kube-proxy iptables rule selects one ready endpoint
      ▼
POD (10.244.2.14:8080)
      │
      │ 5. Traverses container veth pair into Pod Network Namespace
      ▼
CONTAINER PROCESS
      │
      │ 6. Reads socket on 0.0.0.0:8080, processes HTTP request, sends 200 OK
```
