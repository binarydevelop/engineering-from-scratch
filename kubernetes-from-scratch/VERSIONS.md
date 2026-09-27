# Kubernetes & Tooling Versions

To guarantee reproducibility and prevent "works on my machine" friction, all lessons, manifests, and experiments in **kubernetes-from-scratch** are pinned to verified, stable tool versions.

---

## Pinned Baseline Matrix

| Component | Pinned Version | Scope / Role | Verification Command |
| :--- | :--- | :--- | :--- |
| **Kubernetes Server** | `v1.37.0` | Cluster Control Plane & Kubelet | `kubectl version` |
| **kubectl Client** | `v1.36.1+` | CLI API Client | `kubectl version --client` |
| **kind (K8s in Docker)** | `v0.33.0` | Local multi-node cluster runner | `kind version` |
| **kindest/node Image** | `kindest/node:v1.37.0` | Node filesystem, containerd, kubelet | `docker images \| grep kindest` |
| **Container Runtime** | `containerd v2.3.4` | CRI implementation inside nodes | `kubectl get nodes -o wide` |
| **Docker Engine** | `29.7.x+` (Docker Desktop 4.87+) | Host container runner for kind nodes | `docker version` |
| **Python** | `3.11+` (Verified on 3.14) | Reconcilers, simulators & controllers | `python3 --version` |
| **Helm** | `v4.3.0` | Manifest templating & packaging | `helm version` |

---

## Active Kubernetes API Version Reference

Every manifest in this repository conforms to modern, non-deprecated Kubernetes API groups. Deprecated APIs will fail validation in modern clusters.

| Abstraction | API Group & Version | Current Status | Note / Deprecation History |
| :--- | :--- | :--- | :--- |
| **Pod** | `v1` (core) | GA / Stable | Fundamental atomic workload unit |
| **Service** | `v1` (core) | GA / Stable | Stable endpoint abstraction |
| **ConfigMap** | `v1` (core) | GA / Stable | Decoupled plaintext configuration |
| **Secret** | `v1` (core) | GA / Stable | API-governed sensitive configuration |
| **PersistentVolume** | `v1` (core) | GA / Stable | Cluster-level storage resource |
| **PersistentVolumeClaim**| `v1` (core) | GA / Stable | Workload storage request |
| **Namespace** | `v1` (core) | GA / Stable | Logical multi-tenant grouping |
| **ResourceQuota** | `v1` (core) | GA / Stable | Hard namespace resource boundary |
| **LimitRange** | `v1` (core) | GA / Stable | Pod/Container min/max & defaults |
| **ServiceAccount** | `v1` (core) | GA / Stable | Pod identity for Kubernetes API |
| **Deployment** | `apps/v1` | GA / Stable | `extensions/v1beta1` removed since v1.16 |
| **ReplicaSet** | `apps/v1` | GA / Stable | `extensions/v1beta1` removed since v1.16 |
| **StatefulSet** | `apps/v1` | GA / Stable | `apps/v1beta1` removed since v1.16 |
| **DaemonSet** | `apps/v1` | GA / Stable | `extensions/v1beta1` removed since v1.16 |
| **Job** | `batch/v1` | GA / Stable | Run-to-completion batch execution |
| **CronJob** | `batch/v1` | GA / Stable | `batch/v1beta1` removed since v1.25 |
| **Ingress** | `networking.k8s.io/v1` | GA / Stable | `extensions/v1beta1` removed since v1.22 |
| **NetworkPolicy** | `networking.k8s.io/v1` | GA / Stable | East-west traffic filtering rules |
| **Gateway API** | `gateway.networking.k8s.io/v1` | GA / Stable | Modern expressive routing evolution |
| **HorizontalPodAutoscaler** | `autoscaling/v2` | GA / Stable | `autoscaling/v2beta1` removed since v1.25 |
| **PodDisruptionBudget** | `policy/v1` | GA / Stable | `policy/v1beta1` removed since v1.25 |
| **StorageClass** | `storage.k8s.io/v1` | GA / Stable | Dynamic volume provisioning driver |
| **CRD** | `apiextensions.k8s.io/v1` | GA / Stable | `apiextensions.k8s.io/v1beta1` removed |
| **Role / RoleBinding** | `rbac.authorization.k8s.io/v1` | GA / Stable | Namespaced RBAC authorization |
| **ClusterRole / Binding** | `rbac.authorization.k8s.io/v1` | GA / Stable | Cluster-wide RBAC authorization |

---

## Critical Ecosystem Distinctions

### 1. Pod Security Policy (PSP) is Removed
`PodSecurityPolicy` (`policy/v1beta1`) was deprecated in v1.21 and **completely removed** in v1.25. 
This curriculum exclusively teaches modern **Pod Security Standards (PSS)** enforced via namespace labels:
```yaml
metadata:
  labels:
    pod-security.kubernetes.io/enforce: baseline # or restricted, privileged
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

### 2. Dockershim is Removed
The legacy `dockershim` component inside `kubelet` was deprecated in v1.20 and **completely removed** in v1.24. 
Kubelet communicates exclusively through the **Container Runtime Interface (CRI)** to runtimes such as `containerd` or `CRI-O`. 
Running `kind` uses `containerd` inside its node containers.

### 3. Kubernetes API Semantics vs. CNI / Dataplane Implementations
Kubernetes defines the *semantic contract* (e.g. "Pods can communicate across nodes without NAT", "Services balance traffic across endpoints"). 
How that contract is realized depends on the CNI plugin (e.g. Kindnet, Calico, Cilium) and dataplane proxy (kube-proxy iptables, IPVS, or eBPF). 
Throughout this repository, we explicitly distinguish the specification from implementation-specific quirks.
