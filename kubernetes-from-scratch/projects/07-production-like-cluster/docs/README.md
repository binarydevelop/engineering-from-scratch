# Project 07: Production-Grade Hardened Cluster Workload

Capstone Project: Combines security hardening, reliability guarantees, autoscaling, and zero-downtime rolling upgrades.

---

## Production Checklist Implemented

| Category | Primitive / Feature | Security / Operational Value |
|---|---|---|
| **Security** | `pod-security.kubernetes.io/enforce: restricted` | Namespace admission rejects privileged or root containers |
| **Security** | `runAsNonRoot: true`, `readOnlyRootFilesystem: true` | Container kernel compromises cannot write to host filesystem |
| **Security** | `capabilities.drop: ["ALL"]` | Strips all Linux root capabilities (e.g. `CAP_NET_RAW`, `CAP_SYS_ADMIN`) |
| **Reliability** | `PodDisruptionBudget (minAvailable: 2)` | Protects against voluntary disruptions (e.g. `kubectl drain`) |
| **Reliability** | `PodAntiAffinity` (hostname topology) | Spreads replicas across physical/virtual worker nodes |
| **Networking** | `NetworkPolicy` (ingress restriction) | East-west packet filtering inside the Pod network namespace |
| **Governance** | `ResourceQuota` | Enforces hard ceilings on CPU, Memory, and Pod counts per namespace |
| **Autoscaling** | `HorizontalPodAutoscaler` | Dynamic scale-out from 3 to 8 replicas based on CPU demand |

---

## Verification & Eviction Test

```bash
# 1. Apply production manifests
kubectl apply -f projects/07-production-like-cluster/manifests/

# 2. Check rollout
kubectl rollout status deployment/prod-api -n production-tier

# 3. Verify security profile of running pods
kubectl get pods -n production-tier -o jsonpath='{range .items[*]}{.metadata.name}{"\tUID: "}{.spec.securityContext.runAsUser}{"\n"}{end}'

# 4. Test PDB during node drain
# When draining a worker node, PDB ensures at least 2 replicas remain online:
kubectl drain k8s-scratch-cluster-worker --ignore-daemonsets --delete-emptydir-data

# 5. Restore node
kubectl uncordon k8s-scratch-cluster-worker
```
