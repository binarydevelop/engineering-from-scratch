# The Kubernetes Debugging Playbook: Systematic Triage

When a workload or cluster fails, engineers who do not understand Kubernetes internals randomly restart pods, edit manifests haphazardly, or paste random `kubectl` commands found on web forums.

In this curriculum, you follow a **strict 11-step diagnostic sequence**:

```text
OBJECT ──► STATUS ──► CONDITIONS ──► EVENTS ──► OWNER ──► POD ──► CONTAINER ──► LOGS ──► NETWORK ──► CONFIG ──► STORAGE
```

---

## Step 1: Does the Object Exist? (OBJECT)

Before asking why something isn't working, verify the API object actually exists:
```bash
kubectl get deployment,replicaset,statefulset,daemonset,pod,svc -n <namespace>
```
- **If missing**: Check `kubectl apply` exit code, verify namespace, verify typos in manifest names.

---

## Step 2: What is the Object Status? (STATUS)

Inspect the high-level status summary:
```bash
kubectl get pod <pod-name> -n <namespace> -o wide
```
Look at the `STATUS` column:
- `Pending`: The Pod cannot be scheduled onto any node, or images are downloading.
- `CrashLoopBackOff`: The container started, exited, and kubelet is backing off before restarting it.
- `ImagePullBackOff` / `ErrImagePull`: Image name does not exist, registry requires authentication, or network timeout.
- `CreateContainerConfigError`: Missing ConfigMap or Secret referenced by the container.
- `Terminating`: Pod received SIGTERM, waiting for graceful termination grace period or stuck on finalizer.
- `OOMKilled` (Exit Code 137): Container exceeded its cgroup memory limit.

---

## Step 3: What do the Conditions Report? (CONDITIONS)

Detailed health lives in `status.conditions`. Never rely on `STATUS` alone:
```bash
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{range .status.conditions[*]}{.type}{"\t"}{.status}{"\t"}{.reason}{"\t"}{.message}{"\n"}{end}'
```
Inspect the 4 core conditions:
1. `PodScheduled`: Did kube-scheduler assign the Pod to a node?
2. `Initialized`: Did all `initContainers` complete successfully?
3. `ContainersReady`: Did all application containers pass their readiness probes?
4. `Ready`: Is the Pod eligible to receive traffic through a Service?

---

## Step 4: What do the Control Plane Events Say? (EVENTS)

Events are the chronological timeline of actions taken by controllers, the scheduler, and kubelet:
```bash
# Events specifically related to the failing pod:
kubectl describe pod <pod-name> -n <namespace> | grep -A 20 Events:

# Or chronological cluster events:
kubectl get events -n <namespace> --sort-by='.metadata.creationTimestamp'
```
Events tell you:
- `FailedScheduling`: Why no node could fit the Pod (e.g. `0/3 nodes available: 3 Insufficient memory`).
- `Pulled` / `Failed`: Image download status.
- `Unhealthy`: Failed liveness or readiness probes with exact HTTP status codes or error messages.
- `FailedMount`: Unable to attach or mount PVC.

---

## Step 5: Who Owns this Workload? (OWNER)

Inspect the ownership chain to identify which controller is managing this Pod:
```bash
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.metadata.ownerReferences[*].kind}{" "}{.metadata.ownerReferences[*].name}{"\n"}'
```
- If owned by a `ReplicaSet`: Inspect the ReplicaSet with `kubectl describe rs <name>`.
- If owned by a `StatefulSet`: Check ordinal ordering rules (`db-1` will not start until `db-0` is ready).
- If empty: The Pod is standalone (unmanaged); deleting it will delete it forever!

---

## Step 6: Is the Pod Assigned to a Healthy Node? (POD)

Verify node health:
```bash
NODE=$(kubectl get pod <pod-name> -n <namespace> -o jsonpath='{.spec.nodeName}')
kubectl get node "$NODE" -o wide
kubectl describe node "$NODE"
```
Look for:
- `MemoryPressure: True`
- `DiskPressure: True`
- `PIDPressure: True`
- `Ready: False`

---

## Step 7: What State is the Container In? (CONTAINER)

Inspect the exact container termination state and exit codes:
```bash
kubectl get pod <pod-name> -n <namespace> -o jsonpath='{range .status.containerStatuses[*]}{.name}{"\tState: "}{.state}{"\tLastState: "}{.lastState}{"\trestarts: "}{.restartCount}{"\n"}{end}'
```
Key Exit Codes:
- `Exit Code 0`: Clean exit. For a service, this means your application process terminated unexpectedly without looping.
- `Exit Code 1`: General application error (uncaught exception).
- `Exit Code 137`: Process killed by `SIGKILL` ($128 + 9$). Usually Linux kernel OOM-killer enforcing `resources.limits.memory`.
- `Exit Code 143`: Process killed by `SIGTERM` ($128 + 15$). Graceful shutdown signal from kubelet.

---

## Step 8: What do the Application Logs Report? (LOGS)

Inspect stdout and stderr of the container:
```bash
# Current container logs
kubectl logs <pod-name> -n <namespace> -c <container-name>

# CRITICAL: Logs of the previous (crashed) instance!
kubectl logs <pod-name> -n <namespace> -c <container-name> --previous
```
> [!IMPORTANT]
> If a pod is in `CrashLoopBackOff`, running `kubectl logs` without `--previous` often yields empty output because the newly spawned container hasn't reached the crash point yet!

---

## Step 9: Does the Network Path Work? (NETWORK)

If the pod is running but clients cannot reach it:
1. Verify the Service has active endpoints:
   ```bash
   kubectl get endpoints <service-name> -n <namespace>
   kubectl get endpointslices -l kubernetes.io/service-name=<service-name>
   ```
   **If endpoints list is `<none>`**: The Service selector does NOT match the Pod's labels, or the Pod is failing its readiness probe!
2. Test DNS resolution inside the cluster:
   ```bash
   kubectl run test-dns --rm -it --image=busybox:1.36 -- nslookup <service-name>.<namespace>.svc.cluster.local
   ```
3. Check for blocking NetworkPolicies:
   ```bash
   kubectl get networkpolicy -n <namespace>
   ```

---

## Step 10: Is Configuration Correctly Injected? (CONFIG)

1. Verify referenced ConfigMaps and Secrets exist:
   ```bash
   kubectl get configmap,secret -n <namespace>
   ```
2. Verify keys match the manifest:
   ```bash
   kubectl get configmap <name> -o yaml
   ```
3. Shell into the running container or an ephemeral debug container:
   ```bash
   kubectl exec -it <pod-name> -n <namespace> -- env
   ```

---

## Step 11: Is Storage Successfully Bound and Mounted? (STORAGE)

If a workload with persistent volumes hangs in `ContainerCreating`:
1. Check PVC status:
   ```bash
   kubectl get pvc -n <namespace>
   ```
   Must be `Bound`. If `Pending`, inspect with `kubectl describe pvc <name>`.
2. Check StorageClass:
   ```bash
   kubectl get storageclass
   ```
3. Check volume mount permissions:
   Did the container run as a non-root user (e.g. UID 1000) while the host volume was created as root (UID 0)?
