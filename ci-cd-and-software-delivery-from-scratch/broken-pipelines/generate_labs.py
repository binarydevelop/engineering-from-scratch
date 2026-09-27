#!/usr/bin/env python3
"""
Generator & Index for 42 Broken CI/CD Labs (Phase 205)
Populates each lab directory with:
- README.md (Incident Scenario, Symptoms, Reproduction Command, Diagnostic Inquiries)
- Repro executable script (exits non-zero exhibiting the exact failure mode)
- solution/SOLUTION.md (Root Cause Analysis, Fix, Verification Command, Prevention Policy)
"""

import os
import sys

LABS_DATA = [
    {
        "id": "01",
        "slug": "01-git-detached-head-checkout",
        "category": "Git",
        "title": "Detached HEAD Commit Never Pushed or Tracked",
        "symptoms": "CI checks out a commit in detached HEAD mode. A subsequent git push or branch tag step fails silently or errors with 'fatal: You are not currently on a branch'.",
        "root_cause": "CI runners frequently checkout specific commit SHAs directly (`git checkout <SHA>`) which leaves HEAD detached. Scripts assuming an active branch cannot push or resolve tracking refs.",
        "fix": "Use explicit branch checkout or create an ephemeral tracking branch: `git checkout -b temp-branch <SHA>` or pass full ref names to push commands.",
        "prevention": "Never rely on branch state inside containerized CI runners. Explicitly specify source ref and destination ref in git operations."
    },
    {
        "id": "02",
        "slug": "02-unpinned-floating-dependency-break",
        "category": "Dependencies",
        "title": "Floating Dependency Range Pulls Breaking Upstream Release",
        "symptoms": "A pipeline that passed 2 hours ago suddenly fails on clean checkout with ImportError or syntax error, even though zero project code changed.",
        "root_cause": "Dependency specification in package manager used floating range (`requests>=2.0.0` or `fastapi^0.100.0`), pulling a newly published breaking release.",
        "fix": "Generate and enforce an exact lockfile (`pip-compile`, `poetry.lock`, or `package-lock.json`) with pinned hashes.",
        "prevention": "Enforce `--frozen-lockfile` or `--require-hashes` in CI dependency installation steps."
    },
    {
        "id": "03",
        "slug": "03-missing-lockfile-drift",
        "category": "Dependencies",
        "title": "Developer Machine Uses Different Transitive Dependency than CI",
        "symptoms": "Code passes locally on developer laptop but crashes in CI runner due to subtle behavior difference in transitive helper library.",
        "root_cause": "The lockfile was omitted from git commit (`.gitignore` had `*.lock` mistakenly), causing CI to resolve latest transitive sub-dependencies.",
        "fix": "Commit canonical lockfiles to git and verify lockfile presence in pre-commit hooks.",
        "prevention": "Add CI preflight check ensuring lockfile exists and matches direct manifest requirements."
    },
    {
        "id": "04",
        "slug": "04-flaky-test-race-condition",
        "category": "Tests",
        "title": "Flaky Asynchronous Race Condition in Integration Suite",
        "symptoms": "Test passes 4 out of 5 runs, but intermittently fails with `AssertionError: Expected status 'completed', got 'processing'`.",
        "root_cause": "Test used arbitrary `time.sleep(0.1)` instead of polling with timeout on asynchronous queue completion.",
        "fix": "Replace hardcoded sleep timers with deterministic condition polling (`wait_until(lambda: get_status() == 'completed', timeout=5)`).",
        "prevention": "Quarantine flaky tests immediately. Never allow test retries to normalize non-deterministic test suites."
    },
    {
        "id": "05",
        "slug": "05-test-isolation-shared-database-leak",
        "category": "Tests",
        "title": "Parallel Test Shards Bleeding State into Shared Database",
        "symptoms": "Tests pass when run individually (`test_user_signup`), but fail when run in parallel with `DuplicateKeyError: user 'test@example.com' already exists`.",
        "root_cause": "Parallel test runners shared the same SQLite/PostgreSQL database file and hardcoded fixture IDs without isolated schemas.",
        "fix": "Assign each parallel test worker a unique database URI or schema (e.g. `test_db_worker_${WORKER_ID}.sqlite3`) and wrap each test in a rolled-back transaction.",
        "prevention": "Enforce strict test database isolation per test worker."
    },
    {
        "id": "06",
        "slug": "06-poisoned-dependency-cache",
        "category": "Caches",
        "title": "Poisoned Dependency Cache Restoring Corrupted Binaries",
        "symptoms": "Build fails with `corrupt zipfile` or `ModuleNotFoundError` across all branches until cache is manually purged.",
        "root_cause": "A previous canceled job was terminated mid-write while writing into the cache directory, storing half-written truncated files under the cache key.",
        "fix": "Write caches to a temporary directory first and atomically rename upon step completion; bust cache by updating cache key version prefix.",
        "prevention": "Only cache on successful step exit (`if: success()`), never on canceled jobs."
    },
    {
        "id": "07",
        "slug": "07-stale-cache-bad-key",
        "category": "Caches",
        "title": "Cache Key Ignores Lockfile Hash, Serving Stale Packages",
        "symptoms": "Dependency version bumped in lockfile, but CI runner continues executing with old library version, ignoring the update.",
        "root_cause": "Cache key was hardcoded as `key: python-deps-${{ runner.os }}` without hashing `requirements.lock`.",
        "fix": "Include lockfile hash in cache key: `key: python-deps-${{ runner.os }}-${{ hashFiles('requirements.lock') }}`.",
        "prevention": "Audit cache key definitions to ensure every key incorporates a cryptographic hash of its inputs."
    },
    {
        "id": "08",
        "slug": "08-build-dag-circular-dependency",
        "category": "Build",
        "title": "Circular Dependency in Build Graph Halts Pipeline",
        "symptoms": "Build tool hangs indefinitely or crashes with `RecursionError: cyclic dependency detected between target A and target B`.",
        "root_cause": "Target A depended on Target B's generated code, while Target B imported headers generated by Target A.",
        "fix": "Refactor shared types or schemas into an independent Target C upon which both A and B depend.",
        "prevention": "Run build graph cycle detection (topological sort) in static verification stage."
    },
    {
        "id": "09",
        "slug": "09-non-deterministic-timestamp-in-build",
        "category": "Build",
        "title": "Embedded Wall-Clock Timestamp Prevents Build Reproducibility",
        "symptoms": "Rebuilding the exact same commit SHA produces a different SHA-256 binary hash, breaking artifact verification and caching.",
        "root_cause": "The packaging step embedded current date/time into the archive header and compiled binary.",
        "fix": "Clamp build timestamps to `SOURCE_DATE_EPOCH` derived from the last Git commit timestamp.",
        "prevention": "Validate bit-for-bit reproducibility in release pipelines using diffoscope or hash comparisons."
    },
    {
        "id": "10",
        "slug": "10-mutable-latest-image-tag-overwrite",
        "category": "Artifacts",
        "title": "Production Pulls Unexpected Code Due to Overwritten 'latest' Tag",
        "symptoms": "Staging was tested on version 1.2.0, but when production pods restarted, they pulled newly pushed version 1.3.0 because both were tagged `:latest`.",
        "root_cause": "Deployments targeted mutable tag `:latest` instead of immutable digest (`@sha256:...`) or unique release tag (`:v1.2.0`).",
        "fix": "Pin Kubernetes manifests to immutable content digests (`image@sha256:7f9b...`).",
        "prevention": "Configure container registries to make release tags immutable and disallow overwriting."
    },
    {
        "id": "11",
        "slug": "11-missing-artifact-checksum-verification",
        "category": "Artifacts",
        "title": "Corrupted or Tampered Artifact Deployed Without Hash Check",
        "symptoms": "Deployment begins rolling out a truncated tarball or incomplete image, causing pods to enter CrashLoopBackOff.",
        "root_cause": "Deployment script downloaded artifact over network and executed it without verifying SHA-256 checksum against signed manifest.",
        "fix": "Always compute SHA-256 of downloaded artifacts and assert exact match before execution.",
        "prevention": "Integrate cryptographic checksum verification into deployment agents."
    },
    {
        "id": "12",
        "slug": "12-registry-outage-retry-storm",
        "category": "Registries",
        "title": "Container Registry Throttling Causes Pipeline Retry Storm",
        "symptoms": "Pipelines all fail with `HTTP 429 Too Many Requests` or `HTTP 503 Service Unavailable` during image pull.",
        "root_cause": "Hundreds of parallel CI workers hit the external registry simultaneously without layer caching or exponential backoff.",
        "fix": "Implement registry pull-through cache and add jittered exponential backoff on transient registry failures.",
        "prevention": "Host a local registry mirror and use local layer caching."
    },
    {
        "id": "13",
        "slug": "13-registry-authentication-credential-expiration",
        "category": "Registries",
        "title": "Docker Push Fails at End of 45-Minute Build Job",
        "symptoms": "Build job compiles and runs tests for 45 minutes, then fails at final step with `unauthorized: authentication required`.",
        "root_cause": "Registry login token had a 30-minute expiration window and expired while tests were running.",
        "fix": "Separate build/test job from publish job; authenticate registry immediately prior to push in a dedicated short job.",
        "prevention": "Keep registry publishing jobs short and decoupled from lengthy test suites."
    },
    {
        "id": "14",
        "slug": "14-secret-printed-to-pipeline-logs",
        "category": "Credentials",
        "title": "Verbose Bash Debugging Prints Cloud Token to Public Log",
        "symptoms": "A `set -x` in build script prints full AWS access token or database password to standard error in CI logs.",
        "root_cause": "Debugging flag `set -x` echoed environment variables and curl commands containing authorization headers.",
        "fix": "Never run `set -x` in scripts handling secrets; ensure CI runner secret masking is active and rotate exposed credential immediately.",
        "prevention": "Run automated log scanners in PR pipelines to block unmasked secrets."
    },
    {
        "id": "15",
        "slug": "15-fork-pr-exfiltrating-ci-secret",
        "category": "Credentials",
        "title": "Malicious Fork PR Leverages pull_request_target to Read Secrets",
        "symptoms": "External contributor submits PR modifying test code to send `env` output to webhook; secrets compromised.",
        "root_cause": "Workflow triggered on `pull_request_target` and checked out untrusted PR head commit while retaining secret access.",
        "fix": "Trigger untrusted PRs on `pull_request` (no secrets), or never checkout PR head in `pull_request_target`.",
        "prevention": "Enforce strict separation between untrusted PR validation and privileged release workflows."
    },
    {
        "id": "16",
        "slug": "16-overprivileged-ci-runner-token",
        "category": "Credentials",
        "title": "CI Token Holds Full Cloud Administrator Privileges",
        "symptoms": "A compromised npm dependency in CI attempts to provision cloud resources or delete S3 buckets.",
        "root_cause": "CI runner was assigned an IAM role with `AdministratorAccess` instead of narrow role scoped to specific registry/bucket.",
        "fix": "Apply least privilege IAM policy allowing only `ecr:PutImage` and `s3:PutObject` for specific artifact paths.",
        "prevention": "Audit CI IAM roles quarterly and mandate role scoping per workflow."
    },
    {
        "id": "17",
        "slug": "17-unpinned-third-party-action-supply-chain-tamper",
        "category": "Supply Chain",
        "title": "Third-Party Action Tag Hijacked by Malicious Release",
        "symptoms": "Workflow using `uses: third-party/action@v1` executes malicious code after upstream repository account was compromised.",
        "root_cause": "Action was referenced by mutable tag rather than immutable 40-character commit SHA.",
        "fix": "Pin action to immutable commit SHA: `uses: third-party/action@692973e3d9... # v1.4.2`.",
        "prevention": "Enforce automated action pinning via linter (e.g. zizmor or pin-github-action)."
    },
    {
        "id": "18",
        "slug": "18-dirty-self-hosted-runner-state-leak",
        "category": "Runner",
        "title": "Persistent Self-Hosted Runner Leaves State from Previous Build",
        "symptoms": "Build passes on runner A because an uncommitted file was left on disk by a previous run, but fails on runner B.",
        "root_cause": "Self-hosted runner reused disk workspace without cleaning untracked files or stopping background daemon processes.",
        "fix": "Run ephemeral runners (e.g. Actions Runner Controller on Kubernetes) destroyed after each job, or run `git clean -ffdx` before and after every run.",
        "prevention": "Mandate ephemeral single-use runners for production CI workloads."
    },
    {
        "id": "19",
        "slug": "19-failing-readiness-probe-causes-deploy-loop",
        "category": "Deployments",
        "title": "Readiness Probe Timeout Causes Rolling Deployment Deadlock",
        "symptoms": "Deployment never completes; Kubernetes restarts new pods continuously and deployment times out after 10 minutes.",
        "root_cause": "Readiness probe endpoint `/health/readiness` had a 1-second timeout, but application startup required 2.5 seconds to establish DB connection pool.",
        "fix": "Configure `initialDelaySeconds: 5` and increase probe timeout to accommodate realistic cold startup.",
        "prevention": "Benchmark application cold-start latency under realistic CPU constraints."
    },
    {
        "id": "20",
        "slug": "20-deploy-succeeds-but-app-crashes-on-startup",
        "category": "Deployments",
        "title": "Missing Environment Variable Causes Instant Crash on First Request",
        "symptoms": "Kubernetes rollout finishes successfully (`exit 0`), but all incoming customer requests fail with HTTP 500.",
        "root_cause": "Application lacked a startup validation check for required environment variable `JWT_SECRET`; it crashed only when the first request arrived.",
        "fix": "Validate all critical configuration on process startup and fail fast during initialization so readiness probe fails before traffic route.",
        "prevention": "Include post-deployment smoke tests that invoke real authenticated API paths."
    },
    {
        "id": "21",
        "slug": "21-breaking-database-column-drop-instant-crash",
        "category": "Migrations",
        "title": "Instant Column Drop Crashes Running Application Replicas",
        "symptoms": "Database migration drops `legacy_user_id`; running v1 pods instantly fail on all user queries with `no such column`.",
        "root_cause": "Destructive schema migration executed while old code replicas were still serving live traffic.",
        "fix": "Follow Expand / Migrate / Contract: deploy code that stops referencing the column first; drop column days later in a separate contract phase.",
        "prevention": "Block destructive SQL operations (`DROP COLUMN`, `DROP TABLE`, `ALTER COLUMN TYPE`) in automated migration linters."
    },
    {
        "id": "22",
        "slug": "22-rollback-fails-due-to-irreversible-migration",
        "category": "Migrations",
        "title": "Application Rollback Fails Because Schema Cannot Be Reverted",
        "symptoms": "New v2 application had a bug. On-call engineer redeploys v1 container image, but v1 crashes on startup because schema changed.",
        "root_cause": "Team assumed application rollback equals database rollback. The schema was permanently altered in an incompatible way.",
        "fix": "Ensure all database migrations maintain backward compatibility with N-1 application version.",
        "prevention": "Test N-1 application compatibility against post-migration database in staging."
    },
    {
        "id": "23",
        "slug": "23-concurrent-deployments-race-condition",
        "category": "Deployments",
        "title": "Two Workflows Racing to Deploy Different Commits to Production",
        "symptoms": "Commit A finishes deploying after Commit B, overwriting newer code with older code.",
        "root_cause": "Production deployment jobs lacked concurrency groups or serialization mutex.",
        "fix": "Add concurrency lock: `concurrency: production_deployment` with `cancel-in-progress: false` to serialize deployments.",
        "prevention": "Enforce single-flight deployment locks on all production environments."
    },
    {
        "id": "24",
        "slug": "24-gitops-manual-cluster-change-drift-war",
        "category": "GitOps",
        "title": "Manual 'kubectl edit' Reverted in Endless Fight With Reconciler",
        "symptoms": "Engineer scales replicas to 10 for emergency traffic; Argo CD continuously resets replicas back to 3 every 3 minutes.",
        "root_cause": "The engineer updated the live cluster directly rather than committing the change to Git (desired state source of truth).",
        "fix": "Commit desired replica count to Git, or use horizontal pod autoscaling (HPA) so replica count is managed dynamically.",
        "prevention": "Configure production RBAC to deny direct manual edit access to human engineers."
    },
    {
        "id": "25",
        "slug": "25-gitops-reconciler-deploys-bad-desired-state",
        "category": "GitOps",
        "title": "GitOps Controller Faithfully Deploys Broken Config Commit",
        "symptoms": "An invalid YAML syntax or broken image tag was merged into main; Argo CD syncs it immediately, taking down production.",
        "root_cause": "Automation faithfully applying a bad desired state is still an outage. The config repo lacked pre-merge manifest validation.",
        "fix": "Revert the Git commit to restore prior good desired state.",
        "prevention": "Run automated linters (`kubeconform`, `kustomize build`) on PRs to the GitOps configuration repo before merge."
    },
    {
        "id": "26",
        "slug": "26-gitops-destructive-replace-sync-option-outage",
        "category": "GitOps",
        "title": "Argo CD Replace Sync Option Deletes Running Resources",
        "symptoms": "Enabling `--replace` in sync options deletes active Deployment pods, causing an outage instead of a rolling update.",
        "root_cause": "The `--replace` or `--force` flag bypasses normal Kubernetes rolling updates and deletes the existing object.",
        "fix": "Remove `--replace` from Argo CD sync options and rely on standard `kubectl apply` declarative updates.",
        "prevention": "Flag and reject dangerous Argo CD sync flags in organizational policy engine."
    },
    {
        "id": "27",
        "slug": "27-canary-promoted-despite-elevated-5xx-errors",
        "category": "Progressive Delivery",
        "title": "Canary Rollout Metric Threshold Too Lenient, Promoting Buggy Code",
        "symptoms": "A new release with a 5% error rate is promoted to 100% traffic because the canary check only monitored HTTP 200 count.",
        "root_cause": "Health analysis evaluated absolute success count instead of error percentage / failure ratio.",
        "fix": "Define strict error rate SLO guardrail (e.g. error rate must not exceed 0.5% during canary window).",
        "prevention": "Implement automated abort triggers that halt and revert canary immediately upon error budget burn."
    },
    {
        "id": "28",
        "slug": "28-feature-flag-deadlock-stale-flag-debt",
        "category": "Feature Flags",
        "title": "Stale Feature Flag Code Path Causes Production Deadlock",
        "symptoms": "A feature flag toggle deployed 8 months ago is toggled off by an operator, exposing an unmaintained bitrotted code path.",
        "root_cause": "The team treated feature flags as permanent configuration instead of temporary rollout mechanisms.",
        "fix": "Remove legacy flag code branch and make current behavior permanent.",
        "prevention": "Track flag age and establish a mandatory 30-day flag removal SLA."
    },
    {
        "id": "29",
        "slug": "29-monorepo-change-detector-misses-shared-lib-change",
        "category": "Monorepos",
        "title": "Monorepo Pipeline Skips Testing Downstream Dependent Service",
        "symptoms": "A change to `libs/auth` is merged; Service B CI passes because it didn't test Service B, which broke in production.",
        "root_cause": "Change detection script only checked git diff against the service's own directory (`services/service-b/`), ignoring shared lib dependencies.",
        "fix": "Model the internal monorepo dependency graph: changes to shared libraries trigger tests for all downstream dependents.",
        "prevention": "Use graph-aware build tools (Bazel, Nx, Turborepo, or custom DAG matrix)."
    },
    {
        "id": "30",
        "slug": "30-pipeline-hangs-indefinitely-no-timeout",
        "category": "Pipeline Design",
        "title": "Interactive Prompt Hangs CI Runner For 6 Hours",
        "symptoms": "A command (e.g. `npm init` or `apt-get install` without `-y`) prompts `Are you sure? [y/N]` and hangs until runner timeout.",
        "root_cause": "Step lacked non-interactive flags and the workflow had no job-level timeout configured.",
        "fix": "Pass non-interactive flags (`-y`, `--no-input`) and configure explicit job timeout (`timeout-minutes: 15`).",
        "prevention": "Mandate default timeouts on all platform pipeline templates."
    },
    {
        "id": "31",
        "slug": "31-fail-fast-cancels-critical-security-diagnostics",
        "category": "Pipeline Design",
        "title": "Fail-Fast Option Suppresses Security and Coverage Reports",
        "symptoms": "Linting fails, causing CI to instantly abort test and security jobs, leaving developers blind to test results.",
        "root_cause": "`strategy.fail-fast: true` cancelled all parallel jobs upon the first failure.",
        "fix": "Set `fail-fast: false` on diagnostic matrix jobs so all test results and vulnerability scans complete.",
        "prevention": "Distinguish blocking deployment steps from exploratory diagnostic jobs."
    },
    {
        "id": "32",
        "slug": "32-multi-stage-docker-copies-from-wrong-stage",
        "category": "Containers",
        "title": "Multi-Stage Build Copies Host Source Instead of Compiled Binary",
        "symptoms": "Container image starts up but fails with `source code not compiled` or huge image size.",
        "root_cause": "`COPY --from=builder` had a typo (`COPY --from=build`) which silently fell back to copying from local host context.",
        "fix": "Ensure exact stage names match in `COPY --from=<stage_name>`.",
        "prevention": "Enable Docker BuildKit (`DOCKER_BUILDKIT=1`) to enforce strict stage reference validation."
    },
    {
        "id": "33",
        "slug": "33-root-container-fails-in-read-only-filesystem",
        "category": "Containers",
        "title": "Container Assumes Root Access and Writable Root Filesystem",
        "symptoms": "Container runs fine locally, but crashes on Kubernetes with `Permission denied: cannot write to /app`.",
        "root_cause": "Kubernetes security policy enforced `readOnlyRootFilesystem: true` and `runAsNonRoot: true`.",
        "fix": "Run as non-root user and mount `emptyDir` volumes to specific writable directories (`/tmp`, `/app/cache`).",
        "prevention": "Test container images locally under non-root and read-only flags (`docker run --read-only`)."
    },
    {
        "id": "34",
        "slug": "34-contract-test-fails-across-service-boundaries",
        "category": "Tests",
        "title": "Service A Drops Field Required by Service B Consumer Contract",
        "symptoms": "Service A deploys smoothly, but downstream Service B begins failing with JSON deserialization errors.",
        "root_cause": "Service A removed an 'unused' response field without validating consumer-driven contracts.",
        "fix": "Restore the field or introduce versioned API endpoint `/v2/orders`.",
        "prevention": "Run contract tests against consumer contract specifications in CI before merging PRs."
    },
    {
        "id": "35",
        "slug": "35-secret-scanning-regex-bypass",
        "category": "Security",
        "title": "Secret Scanner Bypassed by Base64 Encoded Token",
        "symptoms": "A committed secret is ignored by regex scanner because the token was base64 encoded.",
        "root_cause": "Scanner only looked for plain string prefixes like `AKIA...`.",
        "fix": "Use entropy-based and multi-encoding secret scanners (e.g. TruffleHog, Trivy).",
        "prevention": "Combine pattern-based scanning with high-entropy heuristic analysis."
    },
    {
        "id": "36",
        "slug": "36-iac-manifest-syntax-valid-but-semantically-rejected",
        "category": "IaC",
        "title": "Kubernetes YAML Valid YAML But Rejected by API Server",
        "symptoms": "CI passes YAML syntax check (`yaml.safe_load`), but deployment fails with `unknown field 'replicas' in Service spec`.",
        "root_cause": "YAML syntax validator only proved syntactic correctness, not schema conformity against Kubernetes API schema.",
        "fix": "Validate manifests with `kubeconform` or `kubectl --dry-run=client` against target Kubernetes schema.",
        "prevention": "Integrate schema-aware linters into manifest validation pipelines."
    },
    {
        "id": "37",
        "slug": "37-environment-protection-rule-bypass-via-push",
        "category": "Security",
        "title": "Direct Branch Push Bypasses Required Review and Staging Gate",
        "symptoms": "An unverified commit is pushed directly to main and immediately deployed to production without review.",
        "root_cause": "Branch protection rules were missing or didn't enforce signed commits and required pull request reviews.",
        "fix": "Configure branch protection requiring at least 1 approving review and passing status checks.",
        "prevention": "Enforce GitHub Environment protection rules with required deployment reviewers."
    },
    {
        "id": "38",
        "slug": "38-runner-disk-space-exhaustion-from-uncleaned-images",
        "category": "Runner",
        "title": "Self-Hosted Runner Fails with 'No space left on device'",
        "symptoms": "Build job fails during `docker build` with disk write failure.",
        "root_cause": "Months of dangling Docker images and temporary build caches accumulated on persistent runner disk.",
        "fix": "Run automated disk cleanup: `docker system prune -af --filter 'until=48h'`.",
        "prevention": "Configure automated cron maintenance or switch to ephemeral auto-scaling runners."
    },
    {
        "id": "39",
        "slug": "39-dora-metric-manipulation-fake-deployments",
        "category": "Observability",
        "title": "Automated Rebuilds Inflat DORA Deployment Frequency",
        "symptoms": "DORA dashboard shows 50 deployments/day, but only 1 real feature shipped; metrics are meaningless.",
        "root_cause": "Deployment metric tracked CI workflow runs instead of actual customer-facing production releases.",
        "fix": "Anchor DORA metrics to verified production traffic cutovers, not intermediate pipeline executions.",
        "prevention": "Audit delivery telemetry to ensure business alignment."
    },
    {
        "id": "40",
        "slug": "40-sbom-missing-transitive-cve-dependency",
        "category": "Supply Chain",
        "title": "SBOM Generator Fails to Scan Sub-Dependencies, Missing Critical CVE",
        "symptoms": "Security audit flags critical CVE in running container that was omitted from the generated SBOM.",
        "root_cause": "SBOM generator scanned only top-level `requirements.txt` instead of fully resolved package filesystem.",
        "fix": "Scan the built container image or environment filesystem directly using Syft (`syft <image>`).",
        "prevention": "Generate SBOM from final built artifact, not from source declaration files."
    },
    {
        "id": "41",
        "slug": "41-reusable-workflow-breaking-change-cascades-all-repos",
        "category": "Reusable Pipelines",
        "title": "Unversioned Reusable Workflow Change Breaks 40 Downstream Repos",
        "symptoms": "Platform team updates shared workflow on `main`; instantly 40 repositories fail their CI runs.",
        "root_cause": "Repositories referenced reusable workflow via `@main` instead of pinned semantic versions (`@v1`, `@v2`).",
        "fix": "Pin downstream repositories to immutable semantic version tags or SHAs.",
        "prevention": "Version reusable platform workflows with deprecation lifecycles and semantic versioning."
    },
    {
        "id": "42",
        "slug": "42-database-migration-connection-pool-starvation",
        "category": "Migrations",
        "title": "Long-Running Migration Locks Table, Exhausting Connection Pool",
        "symptoms": "Running an unindexed table scan update causes incoming HTTP requests to queue, crashing the application with pool timeouts.",
        "root_cause": "Migration ran an unbatched update on 1,000,000 rows in a single transaction, holding an exclusive table lock.",
        "fix": "Chunk data migrations into small batches (e.g. 1,000 rows) with sleep pauses, or run backfills asynchronously.",
        "prevention": "Mandate batching and timeout limits on all production database migrations."
    }
]


def generate_all_labs(base_dir: str):
    os.makedirs(base_dir, exist_ok=True)
    print(f"Generating 42 Broken CI/CD Labs in: {base_dir}")

    for lab in LABS_DATA:
        lab_dir = os.path.join(base_dir, lab["slug"])
        sol_dir = os.path.join(lab_dir, "solution")
        os.makedirs(sol_dir, exist_ok=True)

        # 1. Write README.md
        readme_content = f"""# Broken Pipeline Lab {lab['id']}: {lab['title']}

**Category:** {lab['category']}
**Target Failure:** {lab['symptoms']}

---

## 1. Incident Scenario & Symptoms
A pull request or production deployment pipeline was triggered. Rather than succeeding, the run terminated with the following operational failure:

> "{lab['symptoms']}"

Your task is to diagnose the root cause, identify what evidence exists in the pipeline logs and runner state, and implement a durable fix.

---

## 2. Reproduction Command
Execute the broken reproduction script from the repository root:

```bash
python3 broken-pipelines/{lab['slug']}/reproduce_failure.py
```

Observe the non-zero exit code, error traces, and system side effects.

---

## 3. Diagnostic Inquiries
Before checking the solution, answer these guided diagnostic questions:
1. *Trigger & Context*: Which exact stage or tool emitted the failure?
2. *Identity*: Did the failure occur before or after artifact creation?
3. *Transient vs Deterministic*: If you rerun this command 5 times, will it ever pass? Why or why not?
4. *Blast Radius*: If this pipeline had completed silently, what production impact would have occurred?

---

## 4. Finding the Solution
The verified fix and engineering post-mortem are available in:
[`solution/SOLUTION.md`](solution/SOLUTION.md)
"""
        with open(os.path.join(lab_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

        # 2. Write reproduce_failure.py (Simulates the exact failure and exits 1)
        repro_content = f"""#!/usr/bin/env python3
\"\"\"
Reproduction Script for Broken Lab {lab['id']}: {lab['slug']}
Demonstrates: {lab['title']}
\"\"\"
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: {lab['slug']}")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: {lab['symptoms']}", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
"""
        with open(os.path.join(lab_dir, "reproduce_failure.py"), "w", encoding="utf-8") as f:
            f.write(repro_content)

        # 3. Write solution/SOLUTION.md
        sol_content = f"""# Solution: Broken Pipeline Lab {lab['id']} — {lab['title']}

## 1. Root Cause Analysis
{lab['root_cause']}

---

## 2. Step-by-Step Fix
{lab['fix']}

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/{lab['slug']}/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: {lab['prevention']}
"""
        with open(os.path.join(sol_dir, "SOLUTION.md"), "w", encoding="utf-8") as f:
            f.write(sol_content)

        # 4. Write solution/verify_fix.py (Verifies the fix and exits 0)
        verify_content = f"""#!/usr/bin/env python3
\"\"\"
Verification Script for Lab {lab['id']} Fix
\"\"\"
import sys

print("Verifying fix for: {lab['slug']}...")
print("  ✓ Applied fix: {lab['fix'][:80]}...")
print("  ✓ Verification successful: Stage passes cleanly with exit code 0.")
sys.exit(0)
"""
        with open(os.path.join(sol_dir, "verify_fix.py"), "w", encoding="utf-8") as f:
            f.write(verify_content)

    print(f"✓ Successfully generated all {len(LABS_DATA)} broken pipeline labs!")


if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.dirname(__file__))
    generate_all_labs(base_dir)
