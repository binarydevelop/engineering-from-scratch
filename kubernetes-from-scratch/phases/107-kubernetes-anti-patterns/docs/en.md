# Phase 107: The 18 Critical Kubernetes Anti-Patterns

This document catalogues the 18 most dangerous anti-patterns encountered in production Kubernetes clusters, detailing the naive reasoning that introduces them and the exact failure mode they cause.

---

## 1. Using Kubernetes for a Single Small App
- **The Naive Reasoning**: "Kubernetes is industry standard, so we must use it for our company blog."
- **The Underlying Failure Mode**: The operational overhead of managing etcd, CNI, ingress, and upgrades dwarfs the business value. A single VM with systemd or Docker Compose delivers 99.99% reliability with near-zero operational burden.

## 2. Omitting Resource Requests and Limits
- **The Naive Reasoning**: "We don't know how much CPU/memory the app needs, so let's leave it blank."
- **The Underlying Failure Mode**: The scheduler treats the Pod as requesting 0 CPU and 0 Memory. It packs dozens of pods onto a single node. A sudden traffic burst causes memory exhaustion, triggering the Linux kernel OOM-killer to terminate random neighbor pods.

## 3. Using `:latest` Image Tags in Production
- **The Naive Reasoning**: "We always want the newest version running automatically."
- **The Underlying Failure Mode**: Kubernetes caches images by tag (`imagePullPolicy: IfNotPresent`). Different worker nodes run different code versions under the same deployment name. Rollouts fail to trigger because the tag name hasn't changed. Rollback is impossible without immutable image digests.

## 4. Giant Multi-Process Monolithic Pods
- **The Naive Reasoning**: "Let's put Nginx, our Python API, Redis, and MySQL all in one Pod so they can talk on localhost."
- **The Underlying Failure Mode**: Defeats independent autoscaling, independent rollouts, and failure isolation. If MySQL crashes, the entire Pod restarts, terminating user HTTP sessions.

## 5. Hardcoding Pod IP Addresses
- **The Naive Reasoning**: "The Pod is running at 10.244.1.15; let's configure our client to connect there."
- **The Underlying Failure Mode**: Pods are mortal. Every rollout, rescheduling, or crash assigns a new IP address, permanently breaking client communication. (Fix: ClusterIP Services).

## 6. Using Deployments for Stateful Databases
- **The Naive Reasoning**: "Deployment has replicas: 3, so our database is now highly available."
- **The Underlying Failure Mode**: Multiple database instances mount the same volume simultaneously or write with identical IDs without clustering consensus, causing silent database index corruption and split-brain disaster. (Fix: StatefulSet + dynamic PVCs or managed DB).

## 7. Committing Secrets to Git Repositories
- **The Naive Reasoning**: "It's a private repository, and Base64 encodes it anyway."
- **The Underlying Failure Mode**: Base64 is serialization, not encryption (`echo cGFzczEyMw== | base64 -d` yields `pass123`). Git history persists credentials forever across developer laptops and CI machines.

## 8. Omitting Readiness Probes
- **The Naive Reasoning**: "The container process started, so it's ready to handle traffic."
- **The Underlying Failure Mode**: The container needs 20 seconds to establish database connections. Kube-proxy routes user HTTP traffic immediately upon container boot, causing 502/504 errors on every rolling update.

## 9. Overly Aggressive Liveness Probes
- **The Naive Reasoning**: "Check liveness every 1 second; kill the pod if it doesn't respond in 200ms."
- **The Underlying Failure Mode**: Under high user load, the app's CPU utilization rises, delaying health responses. Kubelet interprets this as death and kills healthy, working pods, triggering a catastrophic cascading cluster crash loop.

## 10. Single Replica for Critical Services (`replicas: 1`)
- **The Naive Reasoning**: "Our service doesn't need high throughput."
- **The Underlying Failure Mode**: During worker node patching or rescheduling, zero replicas are available. Outage is guaranteed.

## 11. No Pod Anti-Affinity (Colocated Replicas)
- **The Naive Reasoning**: "We have 3 replicas, so we have redundancy."
- **The Underlying Failure Mode**: The scheduler happens to place all 3 replicas on `worker-01`. When `worker-01` experiences a hardware kernel panic, the entire service goes dark simultaneously.

## 12. Omitting PodDisruptionBudgets (PDB)
- **The Naive Reasoning**: "Kubernetes handles node drains automatically."
- **The Underlying Failure Mode**: An administrator or cluster autoscaler drains nodes during a maintenance window, evicting all pods at once and breaching production SLAs.

## 13. Unrestricted RBAC Privileges (`cluster-admin` for Everyone)
- **The Naive Reasoning**: "It's annoying to configure RBAC roles for CI/CD and developers."
- **The Underlying Failure Mode**: A compromised application pod or CI runner token can delete all namespaces, read all Secrets, and wipe persistent storage.

## 14. Putting All Applications in the `default` Namespace
- **The Naive Reasoning**: "Namespaces add extra typing to kubectl commands."
- **The Underlying Failure Mode**: Inability to apply ResourceQuotas, NetworkPolicies, or RBAC boundaries. One noisy team exhausts cluster capacity.

## 15. Treating `kubectl exec` as Operational Architecture
- **The Naive Reasoning**: "Just SSH/exec into the pod and tweak the configuration file or install packages."
- **The Underlying Failure Mode**: Mutations exist only in memory. When the pod restarts, all manual changes are lost, leaving the system in an unreproducible mystery state.

## 16. Modifying Live Pods Instead of Declarative Manifests
- **The Naive Reasoning**: "Let me just quickly edit the live replica count with `kubectl edit`."
- **The Underlying Failure Mode**: The next CI/CD pipeline run applies the Git manifest, overwriting manual fixes and reverting changes unpredictably.

## 17. Treating Helm Charts as Magic Black Boxes
- **The Naive Reasoning**: "Just run `helm install stable/app` without inspecting what it provisions."
- **The Underlying Failure Mode**: The chart creates unknown cluster roles, unconstrained storage volumes, and poorly tuned resource limits that cause silent cluster degradation.

## 18. Running Kubernetes Without Observability
- **The Naive Reasoning**: "If `kubectl get pods` shows Running, everything is fine."
- **The Underlying Failure Mode**: Pods are running, but dropping 50% of requests due to internal errors or latency spikes. Without Prometheus metrics, distributed tracing, and centralized logging, outages go undetected until customers complain.
