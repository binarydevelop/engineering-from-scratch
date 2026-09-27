# Part II: Continuous Integration from First Principles (Phases 08–17)

## Motto
> "Continuous Integration is an engineering discipline of frequent synchronization and rapid automated verification. It is not merely running tests on GitHub."

---

## Delivery Problem
Five software engineers work on isolated feature branches for four weeks. Each branch modifies database models, shared utility libraries, and API routes. When the sprint ends, they all attempt to merge into `main` at once.

The result is "Integration Hell":
- 250 merge conflicts.
- Code compiles on Developer A's branch, but crashes when executed alongside Developer B's changes.
- Untangling the breakage takes four full days of developer firefighting.
- Releases are delayed, and trust between product and engineering deteriorates.

---

## Prediction
1. Integrating small changes multiple times per day shrinks the merge conflict window from days to minutes.
2. Running tests automatically on every push detects regressions immediately while the developer's context is fresh.
3. Breaking a pipeline into parallel jobs reduces wall-clock feedback time significantly compared to running everything serially.

---

## First Principles
1. **The Integration Loop**:
   Continuous Integration (CI) is defined by two requirements:
   - Developers merge their work into trunk/main frequently (at least daily).
   - An automated build and test harness verifies every integration within minutes.
2. **The CI Control Plane vs. The Runner**:
   - The **Control Plane** (hosted by GitHub, GitLab, Jenkins master) acts as an event router and state store. It receives webhooks, checks branch policies, evaluates DAGs, and queues jobs.
   - The **Runner** (worker daemon) is where execution occurs. It accepts a job description, allocates an environment, spawns OS processes, streams logs, and reports the termination code.
3. **Directed Acyclic Graphs (DAG)**:
   Jobs form a DAG where nodes are units of work and edges are dependency constraints (`needs: [lint]`). Topological sorting determines the exact execution schedule.

---

## Manual Process
Trace the trigger and execution by hand:

```bash
# 1. Inspect the triggering Git event
git log -1 --stat

# 2. Run the local runner simulation
python3 pipelines/local_runner.py
```

Observe how the runner solves the DAG:
`lint -> security-scan -> unit-tests -> integration-tests -> build`

---

## Mental Model

```text
[ Git Webhook Trigger ]
          │
          ▼
   [ CI Control Plane ]
          │
     Enqueues Jobs
          │
          ▼
    [ Runner Pool ] ────► Allocates Ephemeral Worker
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
         [ Job: Lint ]                [ Job: Security Scan ]
         (Process Worker 1)            (Process Worker 2)
                │                             │
                └──────────────┬──────────────┘
                               ▼
                       [ Job: Test Suite ]
                               │
                               ▼
                      [ Job: Build & Package ]
```

---

## Automate It (Phase 12, 13: Workflow -> Job -> Step)

Here is the declarative GitHub Actions pipeline definition:

```yaml
name: CI Pull Request Validation
on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions: {}

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4.1.7
      - run: python3 -m py_compile sample-apps/delivery-service/app.py

  test:
    needs: [lint] # Job dependency (Phase 15)
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4.1.7
      - run: bash scripts/test.sh
```

---

## Run It
Execute the local CI runner engine:

```bash
python3 pipelines/local_runner.py
```

Output:
```text
========================================================================
 EXECUTING PIPELINE: Delivery Service CI/CD
========================================================================
DAG Execution Order: lint -> security-scan -> unit-tests -> integration-tests -> build
  ▶ [JOB START] lint -> ✓ [JOB PASSED] (0.51s)
  ▶ [JOB START] security-scan -> ✓ [JOB PASSED] (0.03s)
  ▶ [JOB START] unit-tests -> ✓ [JOB PASSED] (0.04s)
  ▶ [JOB START] integration-tests -> ✓ [JOB PASSED] (0.05s)
  ▶ [JOB START] build -> ✓ [JOB PASSED] (0.10s)
========================================================================
 Total Wall-Clock Time: 0.73s
```

---

## Inspect It
Examine `.github/workflows/ci.yml`. Trace:
1. What triggers the workflow (`on: pull_request`, `on: push`).
2. Why `concurrency.cancel-in-progress: true` is configured (Phase 126).
3. How `needs: [lint-and-validate]` enforces job dependencies (Phase 15).

---

## Break It (Phase 16: Failure Propagation)
1. Inject an error in the `lint` stage of `pipelines/local_runner.py` or break a syntax file.
2. Run `python3 pipelines/local_runner.py`.
3. Notice how `lint` fails with exit code 1, and downstream jobs (`unit-tests`, `build`) are marked `[SKIPPED]`!

---

## Debug It
When a job fails:
- Check if it failed due to an error in the step command itself or because an upstream dependency failed.
- Check whether `if: always()` or `if: failure()` steps were executed.

---

## Security
- Always set top-level `permissions: {}` in workflow YAML.
- Restrict `id-token: write` only to jobs that perform authenticated OIDC exchanges.

---

## Optimize It (Phase 14: Parallel Jobs)
- Running `lint` and `security-scan` concurrently saves wall-clock time. If `lint` takes 30s and `scan` takes 30s:
  - Serial execution: 60s total.
  - Parallel execution: 30s total (2x speedup).

---

## Deployment Implication
A green CI run does not prove that code is ready for production; it proves that the change integrates cleanly with current trunk state and satisfies existing unit/integration test assertions.

---

## Recovery
If a broken commit slips past CI:
1. Identify the missing test case that failed to detect the regression.
2. Revert the commit on `main`.
3. Add the regression test before re-introducing the feature.

---

## Practical Exercises (Part II)
1. **Exercise 2.1**: Modify `pipelines/local_runner.py` to add a new job called `type-check` that runs in parallel with `lint`.
2. **Exercise 2.2**: Introduce a circular dependency in `pipelines/local_runner.py` (Job A needs Job B, Job B needs Job A) and observe the DAG cycle detection error.
3. **Exercise 2.3**: Trace how GitHub Actions cancels in-progress runs when a developer pushes three commits in rapid succession to the same PR.
4. **Exercise 2.4**: Implement a step in `local_runner.py` that evaluates the conditional expression `if: branch == 'main'`.
5. **Exercise 2.5**: Measure the wall-clock time difference between running test suites serially versus running them concurrently across multiple background worker threads.
6. **Exercise 2.6**: Explain why `set -o pipefail` is critical in pipelines when executing piped commands like `pytest | tee test.log`.
7. **Exercise 2.7**: Simulate runner queue time by introducing a worker pool limit of 2 concurrent processes in `local_runner.py`.
8. **Exercise 2.8**: Write an integration check verifying that all `.yml` workflows in `.github/workflows/` have valid YAML formatting and top-level permission declarations.

---

## Questions for Mastery
1. *Why is running tests on a weekly staging branch fundamentally different from Continuous Integration?*
2. *If Job B needs Job A, but Job A fails, why must Job B be skipped rather than executed?*
3. *What risk does `cancel-in-progress: true` introduce if applied to a production deployment workflow?*

---

## What Comes Next
In **Part III (Phases 18–23)**, we dive into Dependencies and Caching: lockfiles, package resolution, cache key design, stale caches, and cache poisoning attack vectors.
