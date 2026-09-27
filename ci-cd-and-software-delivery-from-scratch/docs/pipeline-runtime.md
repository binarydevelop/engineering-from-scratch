# Tracing the CI/CD Pipeline Runtime: From Git Event to Production

> "Do not treat the delivery system as magic. A pipeline is a sequence of operating system processes running inside an isolated worker environment orchestrated by an event control plane."

---

## 1. The Complete Path from Commit to Production

```text
1. Developer Commits Code
       │
       ▼
2. Git Push / PR Created
       │
       ▼
3. Git Webhook Event ────────► CI Control Plane (GitHub / GitLab)
                                      │
                                      ▼
4. Job Evaluation & DAG Graph ──► Job Placed in Runner Queue
                                      │
                                      ▼
5. Runner Allocation ─────────► Ephemeral Virtual Machine or Container Spun Up
                                      │
                                      ▼
6. Repository Checkout ───────► git clone & git checkout <EXACT_COMMIT_SHA>
                                      │
                                      ▼
7. Dependency Resolution ─────► Restore Cache or Download via Lockfile
                                      │
                                      ▼
8. Static Verification ───────► Linter, Formatter, Type Checker, Secret Scanner
                                      │
                                      ▼
9. Automated Tests ───────────► Unit Tests (Fast) ──► Integration Tests (DB)
                                      │
                                      ▼
10. Deterministic Build ──────► Compile Source ──► Immutable Artifact
                                      │
                                      ▼
11. Supply Chain Attestation ─► Generate CycloneDX SBOM & SLSA Provenance
                                      │
                                      ▼
12. Registry Publication ─────► Push Image to OCI Registry with Immutable Digest
                                      │
                                      ▼
13. Staging Deployment ───────► Deploy to Staging ──► Smoke & Contract Tests
                                      │
                                      ▼
14. Production Gate ──────────► Environment Protection / Automated Approvals
                                      │
                                      ▼
15. Progressive Canary ───────► 1% ──► 10% ──► 50% ──► 100% Traffic Promotion
                                      │
                                      ▼
16. Post-Deploy Observation ──► SLO & Health Verification ──► Done or Rollback
```

---

## 2. Deconstructing Each Runtime Phase

### Phase A: Event Ingestion & Webhook Dispatch
When a developer executes `git push origin feature-branch`:
1. The remote Git repository server updates the Git reference in `.git/refs/heads/feature-branch`.
2. The server constructs an HTTP POST payload containing:
   - Repository name (`binarydevelop/ci-cd-and-software-delivery-from-scratch`)
   - Event type (`push`)
   - Before SHA and After SHA (`c477286...`)
   - Committer identity and commit message
3. The server signs the payload using an HMAC-SHA256 secret (`X-Hub-Signature-256`) and dispatches it to the CI webhook endpoint.

### Phase B: Control Plane & Job Directed Acyclic Graph (DAG)
1. The CI server validates the cryptographic signature of the webhook.
2. It locates the pipeline definition file in `.github/workflows/` at the triggering commit SHA.
3. It validates YAML syntax and constructs the execution DAG:
   - Identifies root jobs with zero upstream dependencies (`needs: []`).
   - Identifies jobs that can execute concurrently.
4. Jobs are enqueued into an internal message broker.

### Phase C: Runner Provisioning & Workspace Setup
1. A runner worker daemon polls the queue or receives an assignment.
2. The runner environment is provisioned:
   - **Hosted Ephemeral**: A brand new cloud VM is launched. Pristine disk, zero residual state. Destroyed immediately after the job finishes.
   - **Self-Hosted Persistent**: An on-premise or cluster node worker. Reuses disk and container daemons. (Carries risk of workspace contamination if uncleaned).
3. The runner executes the checkout step:
   ```bash
   git init
   git remote add origin https://github.com/org/repo.git
   git fetch --depth=1 origin <COMMIT_SHA>
   git checkout --force <COMMIT_SHA>
   ```
   **Critical Insight**: The runner is now in a **detached HEAD** state pointing at the exact commit SHA.

### Phase D: Step Execution & Process Control
Within each job, the runner executes steps sequentially:
1. Environment variables defined at workflow, job, and step levels are merged into the runner process environment (`os.environ`).
2. For every `run:` step, the runner spawns a child shell process:
   ```bash
   /bin/bash -e -u -o pipefail -c "<step_command>"
   ```
3. The runner captures standard output (`stdout`) and standard error (`stderr`), streaming lines in real-time to the web interface.
4. When the child process terminates, the runner checks `$?`:
   - `exit 0`: Step marked green. Proceed to next step.
   - `exit 1-255`: Step marked red. Job execution halts. If `if: always()` steps exist (like uploading test logs), they are executed now. Subsequent normal steps are skipped.

### Phase E: Artifact Upload & State Teardown
1. If the job produced diagnostic outputs (JUnit XML reports, coverage HTML, crash dumps), the upload action posts them to object storage.
2. If dependency caches were updated, directory trees are compressed and uploaded under the computed cache key.
3. Temporary credential tokens are invalidated.
4. If running on ephemeral infrastructure, the entire virtual machine is terminated and purged from disk.
