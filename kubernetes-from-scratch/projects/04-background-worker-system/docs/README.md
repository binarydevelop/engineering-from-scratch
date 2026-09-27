# Project 04: Background Worker System with Graceful Termination

This project focuses on asynchronous message processing, worker scaling, and termination lifecycle management.

---

## Architecture Flow

```text
PRODUCER (API / Client)
       │
       ▼ Push tasks (LPUSH)
REDIS QUEUE: queue-svc:6379
       │
       ▼ Pull tasks (BRPOP)
WORKER POOL: task-worker Deployment (3 Pods)
       │
       └── Handles SIGTERM gracefully without dropping in-flight jobs
```

---

## Core Lessons & Lifecycle

1. **Job vs. Worker Deployment**:
   - `batch/v1 Job`: Runs a batch task to completion and exits (exit 0).
   - `apps/v1 Deployment`: Runs persistent consumer daemons that continuously poll a work queue.
2. **Termination Lifecycle & Signals**:
   When a worker pod is scaled down or evicted:
   ```text
   API Server marks Pod 'Terminating'
         │
         ▼
   Kubelet sends SIGTERM to container process (PID 1)
         │
         ▼
   Worker catches signal, finishes active task, stops taking new tasks
         │
         ▼ (Wait up to terminationGracePeriodSeconds)
   Worker exits with code 0 (or receives SIGKILL if deadline expires)
   ```

---

## Verification & Graceful Shutdown Test

```bash
# 1. Deploy worker system
kubectl apply -f projects/04-background-worker-system/manifests/

# 2. View worker processing logs
kubectl logs -l app=task-worker -f --tail=20

# 3. Trigger scale-down and observe graceful SIGTERM handling
kubectl scale deployment/task-worker --replicas=1
kubectl logs -l app=task-worker --tail=50 | grep "received SIGTERM"
```
