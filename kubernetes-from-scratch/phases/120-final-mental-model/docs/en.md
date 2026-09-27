# Phase 120: The Final Mental Model: End-to-End Systems Trace

You have reached the culmination of **kubernetes-from-scratch**.

At this point, you no longer look at Kubernetes as a collection of YAML templates to copy-paste. You understand Kubernetes as an **API-driven distributed control system that continuously reconciles declared desired state with observed cluster state.**

---

## The Master Trace 01: `kubectl apply -f deployment.yaml`

Trace the complete chain of distributed events when you declare a new Deployment:

```text
1. CLIENT (kubectl)
   ├── Serializes manifest from YAML to JSON.
   └── Issues HTTP POST /apis/apps/v1/namespaces/default/deployments over TLS.

2. API SERVER (kube-apiserver)
   ├── Authentication: Validates client TLS certificate or bearer token.
   ├── Authorization: Evaluates RBAC permissions (Does subject have 'create' on 'deployments'?).
   ├── Mutating Webhooks: Injects default labels, settings, or sidecars.
   ├── Schema Validation: Checks types against the OpenAPI v3 specification.
   └── Validating Webhooks: Evaluates security policies (Pod Security Standards).

3. PERSISTENCE (etcd)
   └── kube-apiserver commits the new Deployment record to etcd via Raft consensus.

4. DEPLOYMENT CONTROLLER (kube-controller-manager)
   ├── Observes new Deployment via watch stream.
   ├── Computes diff: Desired Deployment exists, but matching ReplicaSet does not.
   └── Issues POST /apis/apps/v1/namespaces/default/replicasets (spec.replicas = 3, ownerReferences -> Deployment).

5. REPLICASET CONTROLLER (kube-controller-manager)
   ├── Observes new ReplicaSet.
   ├── Computes diff: Desired replicas = 3, Actual running pods = 0.
   └── Issues 3x POST /api/v1/namespaces/default/pods.
       Note: Pods are created with spec.nodeName = "" (UNSCHEDULED).

6. SCHEDULER (kube-scheduler)
   ├── Watches API for unscheduled Pods (spec.nodeName == "").
   ├── For each pod:
   │   ├── Filtering: Discards nodes lacking CPU, RAM, or matching taints.
   │   ├── Scoring: Ranks surviving nodes (balanced allocation, spreading).
   │   └── Binding: Writes Binding object (spec.nodeName = "worker-01") to API server.

7. NODE AGENT (kubelet on worker-01)
   ├── Watches API server for Pods where spec.nodeName == "worker-01".
   ├── Calls CNI plugin: Allocates IP address and configures Linux network namespace.
   ├── Calls CRI runtime (containerd): Pulls image layers, sets up cgroups, executes runc.
   ├── Mounts volumes, ConfigMaps, and Secrets.
   └── Starts container process (PID 1) and monitors health probes.

8. STATUS RECONCILIATION
   ├── kubelet updates status.phase = Running and Ready = True via API server.
   ├── EndpointSliceController observes ready Pod; adds Pod IP to Service EndpointSlice.
   └── kube-proxy programs local iptables / IPVS / eBPF rules.
   └── User traffic begins flowing to the new container socket!
```

---

## The Master Trace 02: A Container Crashes

What happens when an application process throws an uncaught exception and terminates?

```text
1. Container process exits (e.g. exit code 1).
2. Linux kernel sends SIGCHLD to containerd / runc shim.
3. Kubelet's PLEG (Pod Lifecycle Event Generator) detects process termination.
4. Kubelet inspects the Pod's restartPolicy:
   ├── If 'Always' or 'OnFailure':
   │   ├── Kubelet increments containerStatuses[0].restartCount.
   │   ├── Enforces exponential backoff delay (10s, 20s, 40s... up to 5m).
   │   └── Instructs containerd to restart the container process.
   └── Note: The Pod object itself was never deleted; its identity and IP remain unchanged.
```

---

## The Master Trace 03: A Physical Node Dies

What happens when an entire worker server suffers catastrophic hardware failure?

```text
1. Physical machine loses power. Kubelet ceases sending NodeLease heartbeats.
2. NodeController in kube-controller-manager notices missed heartbeats (after node-monitor-grace-period ~40s).
3. NodeController marks node status: Ready: False or Unknown.
4. NodeController applies taints: node.kubernetes.io/unreachable:NoExecute.
5. Eviction timer expires: NodeController marks Pods on that node for deletion.
6. ReplicaSetController observes deficit: Desired = 3, Alive = 2.
7. ReplicaSetController issues POST /api/v1/pods for a replacement Pod.
8. Scheduler notices unscheduled replacement Pod, binds it to a surviving healthy node.
9. Kubelet on the healthy node starts the new container.
10. EndpointSliceController removes the dead node's pod IP and adds the new pod IP.
11. Cluster returns to steady state (Delta = 0).
```

---

## The Final Mastery Statement

> Kubernetes is no longer YAML and magic controllers.
>
> We started with processes and containers, discovered the problems of scheduling and failure recovery, built reconciliation loops, introduced Pods and controllers, added stable networking and persistent storage, and then studied the control plane that continuously coordinates the cluster.
>
> Now when a Kubernetes object appears in an architecture, we can reason about the problem it solves, the controller that owns it, the state it declares, the failure modes it introduces, and whether Kubernetes is even necessary for the workload.
