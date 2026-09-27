# GitOps: Declarative Delivery, Reconciliation, and Drift Control

> "GitOps is not about storing YAML in Git. GitOps is an operational pattern where the desired state of your runtime system is declaratively version-controlled, and an automated software agent continuously reconciles actual state toward desired state."

---

## 1. Push vs Pull Deployment Models

### The Traditional Push-Based Delivery Model
In push-based CI/CD:
1. The CI runner builds and tests the container image.
2. The CI runner acquires cluster credentials (e.g. `KUBECONFIG` with cluster-admin token).
3. The runner executes `kubectl apply -f deployment.yaml` directly against the Kubernetes API.

```text
[ Developer Commit ] ──► [ CI Runner ] ──(Pushes with Admin Credentials)──► [ Production Cluster ]
```

**Fatal Flaws in the Push Model**:
1. **Security Vulnerability**: The CI runner is an external system with wide internet egress and arbitrary shell execution. Giving it direct cluster administrative tokens makes it the primary attack vector for cluster compromise.
2. **Silent Drift**: If an engineer logs into the cluster and modifies a resource manually (`kubectl edit deployment`), the CI runner has no knowledge of it. Cluster state drifts away from version control.
3. **Firewall & Network Ingress**: Push-based deployment requires the production Kubernetes API server to be accessible from the CI platform's IP addresses.

---

### The Pull-Based (GitOps) Model
In GitOps:
1. The CI runner builds the container, runs tests, and updates a Git repository containing the environment manifests.
2. An agent running **inside** the Kubernetes cluster (e.g. Argo CD) polls or listens for Git changes.
3. The cluster agent compares the Git state with the live cluster state, detects differences (drift), and pulls the updates into the cluster.

```text
[ CI Runner ] ──► Updates Manifest in Git (Config Repo)
                         ▲
                         │ (Watches Git via HTTPS/SSH)
                         ▼
             [ In-Cluster Reconciler (Argo CD) ]
                         │
                         ▼ (Reconciles Local State)
               [ Kubernetes Cluster ]
```

**Benefits**:
- **No Cluster Credentials in CI**: The CI system only needs write access to a Git repository, never cluster credentials.
- **Continuous Drift Remediation**: If someone alters the live cluster manually, the in-cluster reconciler detects the drift and restores the Git definition automatically.
- **Firewall Friendly**: The cluster only makes outbound connections to Git; no inbound ports are exposed to external CI runners.

---

## 2. Application Repository vs Configuration Repository

Should application code and deployment YAML live in the same repository?

| Strategy | Monorepo / Single Repo | Separate Application & Config Repos |
|:---|:---|:---|
| **Structure** | `app/` and `deploy/` in same Git repo | `repo-app` (source) + `repo-deploy` (manifests) |
| **CI Trigger Loops** | **High Risk**: Updating image tag creates a Git commit, which triggers the CI pipeline again in an infinite loop! | **Zero Risk**: CI in `repo-app` triggers only on source; CI updates `repo-deploy` without triggering source builds. |
| **Access Control** | All developers have write access to deployment manifests. | Fine-grained RBAC: Developers merge code; only release automation or tech leads merge to production branch in config repo. |
| **Audit Log Cleanliness** | Git log is noisy with automated image tag bumps mixed with feature commits. | Clean Git log: Config repo commit history is a pure ledger of production release versions. |

**Recommended Pattern**: Separate Application and Configuration repositories for production services.

---

## 3. Argo CD Operational Architecture & Drift Lifecycles

In Argo CD, application status is evaluated across two primary axes:

```text
                  ┌──────────────────────────────────────────────┐
                  │              Synchronization Status          │
                  ├──────────────────────┬───────────────────────┤
                  │     [ Synced ]       │    [ OutOfSync ]      │
┌─────────────────┼──────────────────────┼───────────────────────┤
│    [ Healthy ]  │ Normal Operation     │ Rollout in Progress   │
│ Health  ────────┼──────────────────────┼───────────────────────┤
│ Status [ Degraded]│ Misconfiguration   │ Pod CrashLoop / Outage│
└─────────────────┴──────────────────────┴───────────────────────┘
```

1. **Synced & Healthy**: Live cluster matches Git, and all pods are ready.
2. **OutOfSync & Healthy**: A new Git commit bumped the image tag, but reconciliation has not executed yet.
3. **Synced & Degraded**: Argo CD successfully applied the manifest from Git, but the container is crashing (`CrashLoopBackOff`). **Crucial Insight**: Automation faithfully deploying a bad desired state is still an outage!

---

## 4. Dangerous Sync Options: What Current Documentation Warns

Modern Argo CD provides powerful synchronization options. However, certain flags must be treated as hazardous:

### The `--replace` / `SyncOptions=Replace=true` Hazard
- Standard reconciliation executes `kubectl apply` (client-side or server-side merge patch).
- When `Replace=true` or `--force` is enabled, Argo CD deletes the live Kubernetes resource and creates a brand new one from scratch.
- **Production Consequence**: Deleting the Deployment instantly destroys all active pod replicas. Customer requests drop immediately, turning a zero-downtime rolling update into an unplanned service outage.
- **Rule**: Never use `Replace=true` on Deployments, StatefulSets, or Services serving live traffic. Reserve it strictly for immutable CustomResourceDefinitions (CRDs) that cannot be patched.
