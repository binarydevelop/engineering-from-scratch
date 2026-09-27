# How to Learn Software Delivery Engineering

> "Understand it. Build it. Test it. Package it. Verify it. Release it. Deploy it. Observe it. Recover it. Automate it."

---

## 1. The Core Philosophy

This curriculum is not a collection of YAML snippets copied from official documentation. It is an engineering course in software delivery systems.

In this repository, you will never start with pipeline YAML:
```text
Bad Approach:
"Paste this .github/workflows/deploy.yml and push."
Result: You treat the pipeline as magic and cannot debug it when it breaks.

Engineering Approach:
1. Run the manual shell commands.
2. Experience the friction, omissions, and human error.
3. Understand the underlying OS primitives (exit codes, file descriptors, environment variables, content digests).
4. Automate the manual process in a standalone script.
5. Derive the CI/CD pipeline control plane.
6. Deliberately break the pipeline, inspect the failure evidence, and recover.
```

---

## 2. The Core Learning Loop

Every part and lesson in this course follows this deterministic 11-step learning loop:

```text
       MANUAL PROCESS
             │  (Execute by hand; feel the friction)
             ▼
      FIRST PRINCIPLES
             │  (OS exit codes, content-addressable hashes, Merkle DAGs)
             ▼
        AUTOMATE IT
             │  (Encapsulate in standalone shell script)
             ▼
          RUN IT
             │  (Execute locally via 'scripts/local-ci.sh' or runner)
             ▼
        INSPECT IT
             │  (Inspect build manifests, SHA-256 hashes, logs)
             ▼
         BREAK IT
             │  (Deliberately inject realistic failures)
             ▼
         DEBUG IT
             │  (Apply 12-Step Framework; read evidence before rerunning)
             ▼
        SECURE IT
             │  (Least privilege, OIDC workload identity, no static keys)
             ▼
       OPTIMIZE IT
             │  (DAG critical path, test sharding, layer caching)
             ▼
        RELEASE IT
             │  (Build Once, promote same immutable artifact, SBOM, SLSA)
             ▼
        RECOVER IT
                (Verify DB backward compatibility; practice rollback)
```

---

## 3. Rules of the Course

### Rule 1: Never Click "Re-run Job" Without Evidence
Clicking "Re-run job" hoping a red pipeline turns green is cargo-cult engineering. If a pipeline fails:
1. Which exact stage failed?
2. What was the termination exit code (`$?`)?
3. What did `stderr` report?
4. Did dependencies or inputs change?
5. Is the failure deterministic or a concurrency race?

### Rule 2: Build Once, Promote Many
Never build separate container images or binaries for separate environments. Build an artifact **once** from a source commit, compute its SHA-256 digest, and promote that identical immutable binary from staging to production. Configuration belongs outside the artifact.

### Rule 3: Never Deploy Mutable Tags to Production
Deploying `myapp:latest` or `myapp:staging` is strictly forbidden. All production deployments must target immutable content digests (`image@sha256:...`) or strictly immutable semantic version tags (`v1.4.2`).

### Rule 4: Zero Permanent Cloud Credentials in CI
Never store permanent AWS Access Keys or GCP Service Account keys in CI repository secrets. Workload Identity Federation / OIDC (Phase 77) is the only acceptable enterprise standard.

### Rule 5: Rollback Is Not Guaranteed
Never assume rolling back an application image is safe without verifying database schema compatibility. If version 2 ran a destructive migration that dropped a column, rolling back to version 1 will crash. All database evolution must follow **Expand / Migrate / Contract**.

---

## 4. Keeping Evidence

A lesson is NOT complete simply because the terminal output was green. For each lesson or project, record your evidence in a personal log:

```text
Lesson / Phase:
Date & Timestamp:
Commit SHA Checked Out:
Host Environment (macOS / Linux):
Command Executed:
Process Exit Status ($?):
Generated Artifact Hash (SHA-256):
Deliberate Failure Injected:
Error Message Captured from Stderr:
Recovery Action Taken:
MTTR (Mean Time to Recovery):
Explain the stage in your own words:
```

---

## 5. Prerequisites & Environment Setup

Before starting:
1. Clone the repository:
   ```bash
   git clone https://github.com/binarydevelop/ci-cd-and-software-delivery-from-scratch.git
   cd ci-cd-and-software-delivery-from-scratch
   ```
2. Verify local tooling:
   ```bash
   make check-env
   ```
3. Run the local test suite:
   ```bash
   make test
   ```
4. Execute your first local CI pipeline from scratch:
   ```bash
   make local-ci
   ```
