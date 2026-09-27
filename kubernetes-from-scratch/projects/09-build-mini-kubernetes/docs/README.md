# Project 09: Building Mini-Kubernetes in Python

Capstone 2: Implements an educational distributed orchestrator in pure Python from first principles.

---

## Architectural Mapping: Mini-K8s vs. Real Kubernetes

| Component in `mini_k8s.py` | Real Kubernetes Architecture | Responsibility in the System |
|---|---|---|
| `ApiServer` | `kube-apiserver` + `etcd` | In-memory thread-safe store for desired state declarations |
| `DeploymentController` | `kube-controller-manager` | Infinite loop calculating $\Delta = \text{desired} - \text{actual}$ |
| `Scheduler` | `kube-scheduler` | Matches unscheduled Tasks (`spec.nodeName == None`) to Nodes |
| `Kubelet` | Node `kubelet` daemon | Spawns and monitors local OS worker processes via `subprocess` |
| `SimulatedNode` | Worker Node / Kernel | Encapsulates capacity constraints and failure domains |

---

## Code Walkthrough

See [mini_k8s.py](../code/mini_k8s.py).

### 1. Declaring Desired State
```python
cluster = MiniCluster()
cluster.api.apply_deployment(app="web-api", replicas=3)
```

### 2. The Reconciliation Tick
```python
def tick(self):
    self.controller.reconcile() # Creates Task declarations
    self.scheduler.schedule()   # Binds Tasks to Nodes
    for kubelet in self.kubelets.values():
        kubelet.sync()          # Starts OS worker processes
```

### 3. Fault Injection & Self-Healing
```python
# Intentionally kill one worker process using Linux SIGKILL
os.kill(killed_task.pid, signal.SIGKILL)

# On the next tick:
# 1. Kubelet notices process exit code -9, marks Task "Failed"
# 2. DeploymentController observes desired (3) > actual (2), spawns replacement Task
# 3. Scheduler binds replacement Task to available Node
# 4. Kubelet spawns new OS worker process
```

---

## Running the Automated Test

```bash
python3 projects/09-build-mini-kubernetes/code/mini_k8s.py --test
# Or via Makefile:
make test-mini-k8s
```
