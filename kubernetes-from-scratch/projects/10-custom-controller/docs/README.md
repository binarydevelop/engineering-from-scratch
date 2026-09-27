# Project 10: Custom Controller & Operator Pattern

Capstone 3 (Phases 84 & 118): Extends the Kubernetes control plane with custom declarative APIs and custom reconciliation loops.

---

## The Operator Formula

$$\text{Operator} = \text{CustomResourceDefinition (CRD)} + \text{Custom Controller Loop} + \text{Domain Knowledge}$$

---

## Architectural Flow

```text
HUMAN OPERATOR / CI
       │
       ▼ kubectl apply -f webapp.yaml
KUBE-APISERVER
       │
       │ Persists WebApp custom object (learning.example/v1) to etcd
       ▼
WEBAPP CONTROLLER (webapp_controller.py)
       │
       ├── 1. WATCH: Observes new WebApp 'bookstore' (replicas: 3, port: 5678)
       ├── 2. RECONCILE:
       │      Ensures child Deployment 'bookstore-deployment' exists
       │      Ensures child Service 'bookstore-service' exists
       ▼
KUBERNETES BUILT-IN CONTROLLERS
       ├── DeploymentController creates ReplicaSet
       ├── ReplicaSetController creates 3 Pods
       └── EndpointSliceController populates Service endpoints
```

---

## Execution & Verification

```bash
# 1. Install CustomResourceDefinition schema
kubectl apply -f projects/10-custom-controller/manifests/01-crd.yaml

# 2. Verify CRD registration
kubectl get crd webapps.learning.example

# 3. Create a WebApp Custom Resource instance
kubectl apply -f projects/10-custom-controller/manifests/02-instance.yaml
kubectl get webapp bookstore

# 4. Run the Python Reconciler
python3 projects/10-custom-controller/code/webapp_controller.py

# 5. Clean up
kubectl delete -f projects/10-custom-controller/manifests/02-instance.yaml
kubectl delete -f projects/10-custom-controller/manifests/01-crd.yaml
```
