# The Seven Core Mental Models of Software Delivery Engineering

> "CI/CD is not a directory of YAML files that somehow moves code into production. CI/CD is a software-delivery control system that turns source changes into verified, immutable, observable, and safely deployable software artifacts."

---

## Mental Model 1: The Delivery Control System

Engineers often view CI/CD as an external utility that "runs tests on GitHub." This mental model leads to fragile pipelines, brittle build scripts, and production outages.

In reality, a delivery pipeline is a **closed-loop control system**:

```text
  [ Developer Change ]
           │
           ▼
     [ Controller ] ◄────── Feedback Signals (Lint, Test, Security, SLOs)
           │
           ▼
       [ Actuator ] ──────► Transforms Source to Immutable Artifact
           │
           ▼
        [ Plant ]   ──────► Production Runtime Serving Users
```

If any sensor (test, linter, health check) fails, the control loop halts actuation immediately. The pipeline's primary purpose is not to deploy code; its primary purpose is to **prevent defective code from reaching users while minimizing the lead time for verified changes**.

---

## Mental Model 2: Build Once, Promote Many

A catastrophic anti-pattern in software delivery is rebuilding the application for each environment:
- Building image `app:staging` in the staging branch.
- Building image `app:production` in the production branch.

Even if built from the identical Git commit, two separate builds can resolve different network dependencies, embed different build timestamps, or execute under different compiler environments. You are testing binary A in staging, but deploying untested binary B to production.

```text
Anti-Pattern:
Git Commit ──► Build Staging ──► Artifact A ──► Deployed to Staging
           ──► Build Prod    ──► Artifact B ──► Deployed to Production (Untested!)

Correct Principle:
Git Commit ──► Build ONCE ──► Immutable Artifact A (Digest: sha256:7f9b...)
                                       │
                    ┌──────────────────┴──────────────────┐
                    ▼                                     ▼
           Deploy to Staging                     Promote to Production
           (Inject Staging Config)               (Inject Production Config)
```

The artifact is **immutable**. Only the runtime configuration (Twelve-Factor App) changes between environments.

---

## Mental Model 3: Content Addressability & Immutability

Mutable tags like `myapp:latest`, `myapp:staging`, or `myapp:v1` are human pointers, not content identities. If someone pushes a new image with the same tag, your deployment manifests point to different code without any Git or manifest diff.

In production delivery, every artifact must have an immutable identity:
1. **Source Identity**: 40-character Git commit SHA (`e4b3c2a1...`)
2. **Artifact Identity**: 64-character SHA-256 content digest (`sha256:7041b28e...`)

Given any container running in production, an engineer must be able to trace backward without ambiguity:
`Running Container -> Artifact Digest -> Release Manifest -> Build Pipeline -> Git Commit SHA -> Developer Pull Request`.

---

## Mental Model 4: The CI Runner as an Unprivileged Worker Process

A pipeline definition (YAML) does not execute commands. The CI platform control plane receives a repository event, places a job on an internal message queue, and allocates a runner process.

The runner is simply a physical or virtual machine running an execution daemon:
1. It creates an isolated workspace directory.
2. It fetches the Git repository at the exact commit SHA.
3. It spawns child operating system processes (`bash`, `python3`, `docker`) to execute steps.
4. It reads process standard output (`stdout`), standard error (`stderr`), and the process **exit code** (`$?`).

If a step process exits with `0`, the runner proceeds. If it exits with any non-zero code (`1-255`), the runner halts the job. Modern CI is built entirely on standard POSIX process execution primitives.

---

## Mental Model 5: GitOps as Continuous Desired-State Reconciliation

Traditional push-based deployment gives the CI runner direct administrative access to the production Kubernetes cluster:

```text
Push Model:
CI Runner ──(Holds Production Admin Token)──► kubectl apply ──► Cluster
```

Problems:
- The runner is high-privilege attack surface.
- Manual cluster edits (`kubectl edit`) cause silent configuration drift.
- Rollback requires re-running external CI pipelines.

The GitOps model inverts this relationship using a pull-based reconciler:

```text
Pull Model (GitOps):
Git Repo (Desired State) ◄────── Reconciler (Argo CD) ──────► Cluster (Live State)
                                     │
                             Continual Diff Check
```

1. Desired infrastructure and application versions are declared declaratively in Git.
2. An in-cluster controller (Argo CD) continuously compares desired state in Git against live cluster state.
3. If drift occurs (e.g. an operator manually deletes a pod or modifies a replica count), the controller automatically re-applies the Git definition.

---

## Mental Model 6: Zero-Downtime Database Schema Evolution

You cannot roll back a database migration simply by redeploying the previous container image. If version 2 drops a column that version 1 requires, reverting the application will cause version 1 to crash immediately.

All production schema changes must follow the **Expand / Migrate / Contract** three-phase lifecycle:

```text
Stage 1: EXPAND
Add new column or table with defaults. Both App v1 and App v2 can run simultaneously.

Stage 2: MIGRATE
Deploy App v2. App v2 writes to new schema. Backfill historical records in background batches.

Stage 3: CONTRACT
Wait until App v2 has run safely in production for days and all rollback windows expire.
Drop legacy columns/tables in a separate, isolated release.
```

Application releases and destructive database schema changes must **never** occur in the same deployment step.

---

## Mental Model 7: Progressive Delivery & Blast Radius Management

Deployment and Release are separate operational events:
- **Deployment**: Installing software binaries onto production servers and verifying their readiness. (Users do not necessarily see it).
- **Release**: Exposing the deployed software to real customer traffic and business transactions.

Progressive delivery decouples deployment from release using traffic steering and automated health analysis:

```text
1% Traffic (Canary)  ──► Automated Health Guardrails (Error rate < 0.1%, p95 < 50ms)
         │
         ▼ (Pass)
10% Traffic          ──► Telemetry Analysis
         │
         ▼ (Pass)
50% Traffic          ──► Full Synthetic Load Verification
         │
         ▼ (Pass)
100% Full Promotion
```

If metrics degrade at the 1% or 10% stage, traffic is cut immediately. The blast radius is restricted to a tiny fraction of users, and recovery takes seconds rather than hours.
