# Project 01: Stateless Web App Architecture

This capstone project implements an end-to-end production-grade stateless application.

---

## Architecture Flow

```text
CLIENT (curl / browser)
   │
   ▼ :8080 (NodePort / Ingress Port Forward)
SERVICE: web-app-svc (ClusterIP: 10.96.x.x:80)
   │
   ├── iptables / IPVS round-robin
   ▼
DEPLOYMENT: web-app (3 replicas)
   ├── Pod: web-app-xxxx-1 (10.244.1.x)
   ├── Pod: web-app-xxxx-2 (10.244.2.x)
   └── Pod: web-app-xxxx-3 (10.244.1.y)
         ▲
         │ (Monitored by HPA: web-app-hpa)
         │ Target CPU: 70%
```

---

## Components Included

1. **ConfigMap (`01-configmap.yaml`)**:
   Injects application environment (`APP_ENV=production`, `GREETING="Hello from Kubernetes!"`).
2. **Deployment (`02-deployment.yaml`)**:
   - 3 Replicas with `RollingUpdate` strategy (`maxSurge: 1`, `maxUnavailable: 0`).
   - Liveness Probe (`/`) & Readiness Probe (`/`).
   - Strict resource requests (`cpu: 100m`, `memory: 64Mi`) and limits (`cpu: 200m`, `memory: 128Mi`).
   - Pod Anti-Affinity ensuring replicas are spread across different worker nodes.
3. **Service (`03-service.yaml`)**:
   ClusterIP service selecting `app: web-app` on port 80.
4. **HPA (`04-hpa.yaml`)**:
   Horizontal Pod Autoscaler scaling from 3 to 10 replicas when average CPU crosses 70%.

---

## Execution & Verification

```bash
# 1. Apply all project manifests
kubectl apply -f projects/01-stateless-web-app/manifests/

# 2. Inspect rollout progress
kubectl rollout status deployment/web-app

# 3. Verify pods are scheduled across multiple worker nodes
kubectl get pods -l app=web-app -o wide

# 4. Test service endpoints
kubectl get endpoints web-app-svc

# 5. Simulate rollout update
kubectl set image deployment/web-app web=nginx:1.27.1-alpine
kubectl rollout status deployment/web-app
kubectl rollout history deployment/web-app

# 6. Simulate rollback
kubectl rollout undo deployment/web-app
```
