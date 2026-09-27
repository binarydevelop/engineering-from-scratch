# Project 02: App + Redis Stateful Caching Architecture

This project models multi-tier dependency architecture and failure handling between a stateless API and a stateful cache.

---

## Architecture Flow

```text
CLIENT
  │
  ▼ :80
SERVICE: frontend-svc (ClusterIP)
  │
  ▼
DEPLOYMENT: web-frontend (2 replicas)
  │
  │ Connects to: redis-svc:6379 (DNS)
  ▼
SERVICE: redis-svc (ClusterIP: 6379)
  │
  ▼
DEPLOYMENT / POD: redis (1 replica)
```

---

## Core Lessons & Failure Drills

1. **Service Discovery via DNS**:
   The web application does not hardcode an IP address. It connects to `redis-svc` which CoreDNS resolves to the ClusterIP virtual IP.
2. **Dependency Resilience**:
   What happens if Redis dies or is slow to boot? The web frontend must not enter `CrashLoopBackOff`; it should report degraded health until the dependency recovers.
3. **Failure Injection Drill**:
   - Delete the Redis pod: `kubectl delete pod -l app=redis`.
   - Observe how the ReplicaSet creates a replacement with a **new Pod IP**.
   - Notice that the web frontend continues communicating seamlessly because `redis-svc` updated its Endpoints automatically.

---

## Manifest Verification

```bash
kubectl apply -f projects/02-app-plus-redis/manifests/
kubectl rollout status deployment/redis
kubectl rollout status deployment/web-frontend
```
