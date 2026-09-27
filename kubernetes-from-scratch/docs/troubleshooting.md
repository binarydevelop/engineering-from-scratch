# Kubernetes Troubleshooting Matrix: 25 Common Failure Modes

This document provides a symptom-to-cause diagnostic table for 25 frequent Kubernetes failure modes.

---

## Quick Reference Diagnostic Matrix

| # | Error Symptom / State | Primary Root Cause | Diagnostic Command | Remediation Action |
|---|---|---|---|---|
| **01** | `ImagePullBackOff` | Typo in image name or tag; missing image in registry | `kubectl describe pod <p> \| grep -A 5 Events` | Fix image string; verify tag exists on Docker Hub |
| **02** | `ErrImagePull (401/403)` | Private registry requires authentication secret | `kubectl describe pod <p>` (look for credentials error) | Create `kubernetes.io/dockerconfigjson` Secret and attach `imagePullSecrets` |
| **03** | `CrashLoopBackOff (Exit 1)` | Application threw uncaught exception on boot | `kubectl logs <p> --previous` | Fix missing configuration or application bug |
| **04** | `CrashLoopBackOff (Exit 0)` | Command completed and exited because process was not long-running | `kubectl describe pod <p> \| grep -A 5 Command` | Ensure command runs a continuous foreground process (e.g. web server) |
| **05** | `OOMKilled (Exit 137)` | Process exceeded `resources.limits.memory` | `kubectl describe pod <p> \| grep -i oom` | Increase memory limit or optimize application memory leak |
| **06** | `Pending (0/N nodes available: Insufficient cpu)` | Sum of Pod `requests.cpu` exceeds allocatable node CPU | `kubectl describe pod <p> \| grep -A 5 FailedScheduling` | Lower CPU requests or add more worker nodes to the cluster |
| **07** | `Pending (0/N nodes available: Insufficient memory)` | Pod `requests.memory` cannot fit on any individual node | `kubectl describe nodes \| grep -A 5 Allocatable` | Right-size memory requests or deploy larger nodes |
| **08** | `Pending (node(s) had untolerated taint)` | Node has taint (e.g. `node-role.kubernetes.io/control-plane`) | `kubectl describe nodes \| grep Taints` | Add matching toleration to Pod spec or run on worker node |
| **09** | `CreateContainerConfigError` | Referenced `ConfigMap` or `Secret` does not exist | `kubectl get pod <p> -o yaml \| grep -A 10 envFrom` | Create the missing ConfigMap or Secret before running the Pod |
| **10** | `CreateContainerConfigError (Key not found)` | ConfigMap exists but requested key name is misspelled | `kubectl describe pod <p>` | Fix the `key:` field in `configMapKeyRef` to match ConfigMap data |
| **11** | `Endpoints <none>` on Service | Service label selector does not match Pod labels | `kubectl get pods --show-labels` vs `kubectl describe svc <s>` | Align `spec.selector` in Service with `metadata.labels` in Pod |
| **12** | `Endpoints <none>` (Labels match) | Pod is failing its readiness probe; traffic withheld | `kubectl describe pod <p> \| grep -A 5 Readiness` | Fix readiness endpoint or health check logic in application |
| **13** | `Connection Refused` on Service IP | Service `targetPort` does not match container `containerPort` | `kubectl get svc <s> -o yaml` vs `kubectl get pod <p> -o yaml` | Update `targetPort` in Service to match the listening container port |
| **14** | `Connection Timeout` on Service IP | Pod application listening on `127.0.0.1` instead of `0.0.0.0` | `kubectl exec -it <p> -- netstat -tlpn` | Rebind server socket to `0.0.0.0` inside container |
| **15** | `DNS Lookup Failed` (`nslookup` error) | CoreDNS pods crashed or CNI network routing failed | `kubectl get pods -n kube-system -l k8s-app=kube-dns` | Restart CoreDNS or verify cluster network connectivity |
| **16** | `PVC Pending` | No PersistentVolume matches size/accessMode; no StorageClass | `kubectl describe pvc <pvc>` | Configure valid StorageClass or provision manual PV |
| **17** | `FailedMount (Permission Denied)` | Container runs as non-root user and cannot write to root-owned volume | `kubectl describe pod <p> \| grep FailedMount` | Set `securityContext.fsGroup` or adjust volume directory ownership |
| **18** | `Multi-Attach error for volume` | Volume with `ReadWriteOnce` attached to node A cannot attach to node B | `kubectl describe pod <p>` | Ensure old Pod terminates completely before new Pod mounts volume |
| **19** | `NetworkPolicy Silent Drop` | Default-deny NetworkPolicy active with no ingress rule for client | `kubectl get networkpolicy -n <ns>` | Add Ingress rule permitting traffic from client pod selector |
| **20** | `ProgressDeadlineExceeded` (Deployment) | Rollout failed to reach ready state within deadline (default 10m) | `kubectl rollout status deployment/<d>` | Inspect new ReplicaSet pods; run `kubectl rollout undo` |
| **21** | `StatefulSet Rollout Stuck` | Pod `app-1` waiting indefinitely for `app-0` to report Ready | `kubectl describe pod app-0` | Fix health of earlier ordinal pod to unblock subsequent pods |
| **22** | `Pod Stuck in Terminating` | Application ignoring `SIGTERM` and graceful timeout expiring | `kubectl describe pod <p>` | Implement `SIGTERM` handler in app or check finalizers (`.metadata.finalizers`) |
| **23** | `NodeNotReady` | Kubelet stopped or container runtime (containerd) unresponsive | `docker exec -it <node> systemctl status kubelet` | Restart containerd/kubelet or inspect node system logs |
| **24** | `DiskPressure: True` on Node | Container images and logs filled root disk (>85% capacity) | `df -h` inside node | Prune dangling images: `crictl rmi --prune` |
| **25** | `Forbidden (User/SA cannot ...)` | RBAC Role or RoleBinding missing required API verb/resource | `kubectl auth can-i <verb> <resource> --as=system:serviceaccount:<ns>:<sa>` | Add required verb/resource to Role and bind to ServiceAccount |
