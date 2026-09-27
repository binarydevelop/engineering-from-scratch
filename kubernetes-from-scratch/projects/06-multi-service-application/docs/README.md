# Project 06: Multi-Service Distributed Microservices System

This project ties together multi-tier architecture, organizational namespaces, and cross-namespace DNS discovery.

---

## Topology & Cross-Namespace Communication

```text
┌────────────────────────────────────────────────────────┐
│ NAMESPACE: ecommerce-web                               │
│                                                        │
│   Frontend UI (frontend-ui)                            │
│         │                                              │
│         │ Same-namespace short DNS: "http://api-svc"   │
│         ▼                                              │
│   Backend API (api-backend)                            │
│         │                                              │
└─────────┼──────────────────────────────────────────────┘
          │
          │ Cross-namespace FQDN DNS:
          │ "redis-svc.ecommerce-data.svc.cluster.local:6379"
          ▼
┌────────────────────────────────────────────────────────┐
│ NAMESPACE: ecommerce-data                              │
│                                                        │
│   Redis Datastore (redis-cache)                        │
└────────────────────────────────────────────────────────┘
```

---

## DNS Discovery Rules

1. **Within the Same Namespace**:
   Pod in `ecommerce-web` accesses Service `api-svc` simply via `http://api-svc:8080`.
2. **Across Namespaces**:
   Pod in `ecommerce-web` MUST specify the namespace qualification:
   - `<service-name>.<namespace>` (e.g. `redis-svc.ecommerce-data`)
   - Or fully qualified domain name: `<service-name>.<namespace>.svc.cluster.local`

---

## Verification Commands

```bash
# 1. Apply multi-namespace manifests
kubectl apply -f projects/06-multi-service-application/manifests/

# 2. Inspect workloads in both namespaces
kubectl get all -n ecommerce-web
kubectl get all -n ecommerce-data

# 3. Test cross-namespace DNS resolution
kubectl exec -it -n ecommerce-web $(kubectl get pod -n ecommerce-web -l app=api-backend -o jsonpath='{.items[0].metadata.name}') -- \
  nslookup redis-svc.ecommerce-data.svc.cluster.local
```
