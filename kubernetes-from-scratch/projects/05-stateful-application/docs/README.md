# Project 05: StatefulSet with Stable Ordinals and Dedicated PVCs

This project explores why stateful distributed databases cannot use simple Deployments.

---

## Deployment vs. StatefulSet Comparison

| Attribute | Deployment | StatefulSet |
|---|---|---|
| **Pod Naming** | Random hash suffix (`web-769b8-z4x5l`) | Predictable ordinal index (`vault-0`, `vault-1`, `vault-2`) |
| **Storage Binding** | All pods share the same PVC or use emptyDir | Each ordinal pod gets its own dedicated PVC (`data-vault-X`) |
| **Startup Order** | Concurrent / unordered by default | Sequential: `vault-0` must report Ready before `vault-1` starts |
| **Teardown Order** | Concurrent | Reverse sequential: `vault-2` terminates before `vault-1` |
| **Network Identity** | Transient IP address | Stable DNS hostname (`vault-0.vault-internal`) |

---

## Headless Service DNS Resolution

Because `vault-internal` has `clusterIP: None`, CoreDNS creates direct A-records pointing to each pod's IP:

```text
vault-0.vault-internal.default.svc.cluster.local -> 10.244.1.15
vault-1.vault-internal.default.svc.cluster.local -> 10.244.2.19
vault-2.vault-internal.default.svc.cluster.local -> 10.244.1.20
```

---

## Verification & Resilience Drill

```bash
# 1. Apply StatefulSet
kubectl apply -f projects/05-stateful-application/manifests/

# 2. Watch sequential creation
kubectl get pods -l app=vault -w

# 3. Inspect dynamically created PVCs
kubectl get pvc -l app=vault

# 4. Write data to vault-1
kubectl exec -it vault-1 -- redis-cli set cluster_key "secret_token_123"

# 5. Fault Injection: Delete vault-1
kubectl delete pod vault-1

# 6. Verify vault-1 is recreated with the identical name and retains data
kubectl wait --for=condition=Ready pod/vault-1 --timeout=60s
kubectl exec -it vault-1 -- redis-cli get cluster_key
# Output must be: "secret_token_123"
```
