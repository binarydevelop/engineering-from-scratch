# The 12-Step Broken Pipeline Debugging Framework

> "The least effective response to a broken pipeline is clicking 'Re-run job' without collecting evidence. CI pipelines are deterministic state machines; rerun without diagnosis is magical thinking."

---

## 1. The 12-Step Diagnostic Decision Tree

Whenever a pipeline fails, systematically trace the failure from event source to runtime health:

```text
Step 01: Did the event trigger fire? (Webhook dispatched, branch filter matched)
   │
   ▼
Step 02: Was the job created in the queue? (Concurrency limits, syntax validity)
   │
   ▼
Step 03: Did the runner allocate and start? (Worker capacity, pool saturation)
   │
   ▼
Step 04: Did repository checkout succeed? (Detached HEAD, shallow depth, auth)
   │
   ▼
Step 05: Were dependencies available? (Cache hit/miss, lockfile hash, registry 429)
   │
   ▼
Step 06: Did the step command execute? (PATH resolution, permissions, shebang)
   │
   ▼
Step 07: What exact exit status was returned? (Exit 0 vs Exit 1-255, signal 137/OOM)
   │
   ▼
Step 08: Did the output artifact exist on disk? (Path typo, compilation failure)
   │
   ▼
Step 09: Was artifact publication successful? (Registry auth, token expiration, quota)
   │
   ▼
Step 10: Did deployment machinery begin rollout? (GitOps sync trigger, RBAC)
   │
   ▼
Step 11: Did the target environment accept it? (Schema validation, resource limits)
   │
   ▼
Step 12: Did the application become healthy? (Liveness, readiness, smoke probe)
```

---

## 2. Common Failure Symptoms and Root Causes

### 1. The Disappearing Pipeline (Step 1 Failure)
- **Symptom**: Developer pushes a commit, but no pipeline runs on GitHub/GitLab.
- **Diagnostics**:
  - Check `.github/workflows/*.yml` path and branch filters (`branches: [main]` does not trigger on `feature/abc`).
  - Check YAML syntax: invalid indentation causes silent drop before job creation.
  - Check path exclusions (`paths-ignore: ['docs/**']`).

### 2. Job Terminated with Exit Code 137 (Step 7 Failure)
- **Symptom**: Step fails abruptly without an error stack trace. The last log line is `Killed` or `Exit 137`.
- **Root Cause**: **Linux OOM (Out Of Memory) Killer**. The process exceeded the runner container's memory ceiling (`128 + 9 = 137`, indicating `SIGKILL` 9).
- **Remediation**:
  - Increase runner memory limits or reduce compiler parallel thread count (`make -j2` instead of `make -j8`).
  - Pass memory limits to Node/Python/Java (`JAVA_OPTS="-Xmx2g"`).

### 3. "ModuleNotFoundError" Despite Cache Hit (Step 5 Failure)
- **Symptom**: CI logs report `Cache restored successfully from key: python-deps-v1`, but the test step crashes saying a required library is missing.
- **Root Cause**: **Stale Cache Identity**. The cache key did not include a hash of the lockfile (`requirements.lock`). A new dependency was added to code, but CI restored the older cached virtualenv without installing the new package.
- **Remediation**:
  - Invalidate cache by updating cache key prefix: `python-deps-v2-${{ hashFiles('requirements.lock') }}`.

### 4. "Readiness Probe Failed: HTTP 503" (Step 12 Failure)
- **Symptom**: Container starts up, but Kubernetes restarts it repeatedly in `CrashLoopBackOff`.
- **Root Cause**: The readiness probe queried `/health/readiness` before the database migration completed or before the connection pool was initialized.
- **Remediation**:
  - Adjust `initialDelaySeconds` and `periodSeconds` on the readiness probe spec.
  - Verify that the target database is reachable from inside the pod network namespace.

---

## 3. Evidence Collection Template

Before asking a colleague or re-running a failed job, record this evidence:

```text
Incident Timestamp:
Workflow Run URL:
Failing Step Name:
Exact Exit Code:
Standard Error (Last 10 Lines):
Was an Artifact Produced (Yes/No)?
Did a Dependency Change in this Commit?
Did the Runner Time Out (Yes/No)?
```
