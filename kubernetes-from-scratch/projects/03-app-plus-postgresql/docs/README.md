# Project 03: Web API + PostgreSQL with Persistent Storage

This project explores running a stateful relational database alongside a stateless web API.

---

## Architecture Flow

```text
API CLIENT (HTTP)
   │
   ▼ :8080
SERVICE: api-svc (ClusterIP)
   │
   ▼
DEPLOYMENT: api-backend (2 replicas)
   │
   │ JDBC / TCP 5432 (postgres-svc:5432)
   ▼
SERVICE: postgres-svc (ClusterIP: 5432)
   │
   ▼
STATEFULSET / POD: postgres-0 (1 replica)
   │
   ├── Mounts PVC: postgres-data-pvc (1Gi standard)
   └── Reads Secret: postgres-credentials (user/password)
```

---

## Architectural Decision: In-Cluster DB vs. Cloud Managed DB

| Dimension | In-Cluster Database (Kubernetes) | Cloud-Managed DB (e.g. AWS RDS, GCP CloudSQL) |
|---|---|---|
| **Storage Attach Latency** | PVC attachment delays during node failover | Managed automated failover (multi-AZ replicas) |
| **Backup & Point-in-Time Recovery** | Requires external operator (e.g. CloudNativePG, Zalando) | Automated automated snapshots & managed recovery |
| **Maintenance Burden** | Team manages OS patches, disk resize, replication | Cloud provider manages maintenance windows & engine patches |
| **When Justified in K8s** | Local development, isolated integration tests, on-premise edge | High-availability production tier with strict SLA |

---

## Verification & Recovery Drill

```bash
# 1. Apply manifests
kubectl apply -f projects/03-app-plus-postgresql/manifests/

# 2. Verify PVC is Bound
kubectl get pvc postgres-data-pvc

# 3. Verify PostgreSQL pod is Running and healthy
kubectl get pods -l app=postgres

# 4. Insert data into DB
kubectl exec -it $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- \
  psql -U appuser -d appdb -c "CREATE TABLE users (id SERIAL PRIMARY KEY, name TEXT); INSERT INTO users (name) VALUES ('Alice'), ('Bob');"

# 5. Fault Injection: Kill the PostgreSQL Pod
kubectl delete pod -l app=postgres

# 6. Verify Data Persistence after Pod Recreation
kubectl wait --for=condition=Ready pod -l app=postgres --timeout=60s
kubectl exec -it $(kubectl get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}') -- \
  psql -U appuser -d appdb -c "SELECT * FROM users;"
```
