# Project 08: Cluster Failure Day & Chaos Engineering Drills

The definitive test of Kubernetes mastery is not whether you can write YAML that boots cleanly, but whether you can systematically diagnose, isolate, and recover from real production failures.

---

## The 8 Failure Day Drills

| Scenario | Injected Failure | Primary Symptom | Controller / Component Responsible |
|---|---|---|---|
| **Drill 01** | `delete pod` on a Deployment | Transient pod missing | `ReplicaSetController` creates replacement immediately |
| **Drill 02** | Worker node failure (`docker stop`) | Node `NotReady` | `NodeController` marks node unreachable; evicts pods after taint timeout |
| **Drill 03** | Rollout with non-existent image | `ImagePullBackOff` | `DeploymentController` pauses rollout; `kubectl rollout undo` recovers |
| **Drill 04** | Broken readiness probe path | Service endpoints `<none>` | `EndpointSliceController` removes unready pod IP from Service routing |
| **Drill 05** | Service selector typo | Connection refused / timeout | Service virtual IP routes to empty endpoints |
| **Drill 06** | Corrupted ConfigMap key | `CreateContainerConfigError` | Kubelet cannot mount environment or volumes; container never starts |
| **Drill 07** | Revoked RBAC RoleBinding | API returns `403 Forbidden` | `kube-apiserver` RBAC authorization webhook denies request |
| **Drill 08** | PVC requested capacity exceeds storage | PVC stuck in `Pending` | `persistent-volume-controller` cannot find or provision matching PV |

---

## The Drill Protocol: 7 Steps for Every Failure

For every drill:
1. **PREDICT**: What will happen to user traffic, status conditions, and controller loops?
2. **BREAK**: Inject the specific fault using the provided scenario script.
3. **OBSERVE**: Watch the live status transition with `kubectl get pods -w`.
4. **INSPECT EVENTS**: Read `kubectl get events --sort-by='.metadata.creationTimestamp'`.
5. **DIAGNOSE**: Execute the 11-step diagnostic workflow (`docs/kubectl-debugging.md`).
6. **RECOVER**: Apply the root-cause fix and verify the system reaches steady state ($\Delta = 0$).
7. **EXPLAIN**: State clearly what Kubernetes handled automatically, and what required human operator intervention.
