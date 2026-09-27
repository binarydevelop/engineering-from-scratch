# Kubernetes From Scratch: First-Principles Glossary

This glossary defines Kubernetes concepts from the perspective of distributed systems and control theory, rather than describing them as YAML tags.

---

## 1. Control Theory & System Primitives

### Desired State
The target condition of the system declared by human operators or automated pipelines (encoded in the `spec` field of Kubernetes API objects). It describes *what* the system should look like, not *how* to achieve it.

### Observed (Actual) State
The live condition of running workloads and cluster infrastructure discovered through health checks, kernel status, and agent heartbeats (encoded in the `status` field of Kubernetes API objects).

### Reconciliation Loop
An infinite control loop that continuously executes the feedback formula:
$$\Delta = \text{Desired State} - \text{Actual State}$$
If $\Delta \neq 0$, the controller executes actions to drive the actual state toward the desired state until $\Delta = 0$.

### Level-Triggered vs. Edge-Triggered
- **Edge-Triggered**: The system reacts only to state change events (e.g. "pod X died"). If an event notification is dropped or lost, the system remains in an incorrect state.
- **Level-Triggered**: The system continuously inspects the current *level* (state) regardless of how it got there. If a network blip occurs, the next loop iteration observes the difference and reconciles anyway. Kubernetes is fundamentally level-triggered.

### Idempotence
The mathematical property where executing an operation once produces the exact same outcome as executing it multiple times ($f(f(x)) = f(x)$). In Kubernetes, controllers must be idempotent: applying a manifest that matches current state produces zero side-effects.

---

## 2. Control Plane Architecture

### `kube-apiserver`
The central HTTP REST gateway and validation brain of the cluster. It authenticates requests, authorizes permissions (via RBAC), applies admission control, and persists objects to `etcd`. It is the only component in the cluster that talks directly to `etcd`.

### `etcd`
A distributed, strongly consistent (Raft consensus) key-value store used to hold all cluster metadata and desired specifications. It provides watch mechanisms so components can be notified of key updates.

### `kube-scheduler`
An autonomous control-plane process that searches for Pods without an assigned node (`spec.nodeName == ""`). It filters candidate nodes based on resource capacity, taints, and affinity rules, scores the survivors, and writes a `Binding` object assigning the Pod to the winning node.

### `kube-controller-manager`
A monolithic binary running dozens of independent controller reconciliation loops (DeploymentController, ReplicaSetController, NodeController, EndpointSliceController, etc.). Each loop monitors a specific resource type and reconciles differences.

---

## 3. Node Architecture & Runtime

### `kubelet`
The primary node agent running as a system daemon on every worker machine. It watches the API server for Pods assigned to its node (`spec.nodeName == $(hostname)`), calls the local container runtime via CRI to start/stop containers, configures volumes, and reports pod/node status back to the API server.

### Container Runtime Interface (CRI)
A gRPC specification allowing `kubelet` to communicate with container runtimes without needing runtime-specific code compiled into Kubernetes. Modern standard: `containerd` or `CRI-O`. (Dockershim was permanently removed in v1.24).

### Container Network Interface (CNI)
A standardized plugin interface for configuring Linux network namespaces when containers are created and destroyed. It allocates IP addresses to Pods and programs host routing tables or eBPF maps. Examples: Kindnet, Calico, Cilium.

### Container Storage Interface (CSI)
A standardized plugin interface allowing third-party storage vendors (cloud block stores, NFS, Ceph) to attach, mount, and provision volumes dynamically without modifying core Kubernetes code.

### `kube-proxy`
A network agent running on each node that implements the Kubernetes `Service` virtual IP abstraction. Depending on mode (`iptables`, `ipvs`, or bypassed by eBPF runtimes), it translates virtual cluster IPs into real backend Pod IPs via packet manipulation (DNAT).

---

## 4. Workload Abstractions

### Pod
The smallest atomic schedulable workload unit in Kubernetes. A Pod is a collection of one or more tightly coupled containers that share the same Linux network namespace (same IP address, port space, and `localhost`), IPC namespace, and shared storage volumes.

### ReplicaSet
A controller whose sole job is to maintain a specified integer count of identical Pod replicas matching a selector at all times. If a Pod crashes or is deleted, the ReplicaSet creates a replacement.

### Deployment
A declarative manager for ReplicaSets and Pods. It enables declarative updates (rollouts), pauses, rollbacks, and canary transitions by creating a new ReplicaSet and gradually shifting replica counts between old and new ReplicaSets.

### StatefulSet
A workload controller tailored for stateful applications requiring:
1. Stable, unique network identifiers (e.g. `db-0`, `db-1`, `db-2`).
2. Stable, persistent storage bound to each replica ordinal across restarts.
3. Ordered, graceful deployment, scaling, and rolling updates.

### DaemonSet
A controller ensuring that an exact single copy of a specified Pod runs on all (or selected) worker nodes. Used for host-level logging agents, monitoring exporters, and storage/network daemons.

### Job & CronJob
- **Job**: A controller that creates one or more Pods and ensures a specified number of them run to successful completion (exit code 0) rather than running infinitely.
- **CronJob**: A controller that creates Jobs on a recurring schedule defined by standard 5-field cron syntax.

---

## 5. Networking & Discovery

### Service
An abstract way to expose an application running on a set of Pods as a network service with a single, stable virtual IP (ClusterIP) and DNS name, decoupling consumers from ephemeral Pod IPs.

### Endpoints / EndpointSlice
API objects tracking the live IP addresses and ports of Pods that match a Service's label selector and have passed their readiness checks.

### Ingress & Gateway API
- **Ingress**: An API object managing external HTTP/HTTPS routing into cluster Services (host-based and path-based routing).
- **Gateway API**: The modern, extensible evolution of Ingress providing expressive, role-oriented routing (GatewayClass, Gateway, HTTPRoute, TCPRoute).

### NetworkPolicy
A packet-filtering specification that controls which Pods and IP CIDR blocks can communicate with each other (ingress and egress firewall rules within the cluster network namespace).

---

## 6. Storage & Configuration

### ConfigMap
An API object used to store non-confidential configuration key-value pairs, decoupling application configuration from container images.

### Secret
An API object used to store sensitive data (tokens, certificates, passwords). Stored in `etcd`, accessible only to authorized ServiceAccounts, and mounted as files or environment variables. (Base64 encoding is serialization, not encryption).

### PersistentVolume (PV)
A piece of durable storage provisioned in the cluster (e.g. local disk, NFS share, cloud block store) that exists independently of any Pod lifecycle.

### PersistentVolumeClaim (PVC)
A request for storage by a user/workload. It specifies size, access modes (ReadWriteOnce, ReadWriteMany), and StorageClass. Kubelet binds a matching PV to the PVC.

### StorageClass
A dynamic storage provisioner definition that allows PersistentVolumes to be created on demand when a user creates a PersistentVolumeClaim.

---

## 7. Security & Identity

### ServiceAccount
An identity provisioned inside Kubernetes for processes running inside a Pod to authenticate against the `kube-apiserver`.

### Role & RoleBinding
- **Role**: Namespaced rule set defining allowed verbs (`get`, `list`, `watch`, `create`, `delete`) on API resources (`pods`, `services`, `deployments`).
- **RoleBinding**: Grants the permissions defined in a Role to a subject (user, group, or ServiceAccount) within a specific namespace.

### ClusterRole & ClusterRoleBinding
Cluster-wide counterparts to Role and RoleBinding, used for non-namespaced resources (Nodes, PVs) or cluster-wide authorization.

### Pod Security Standards (PSS)
Modern built-in security policies replacing deprecated PSP. Defines three tiers: `privileged`, `baseline`, and `restricted`, enforced through namespace labels.
