# Curriculum Roadmap: All 30 Parts & 224 Phases

> "From Git Commit to Production Software Serving Users — Without Magic."

Total Curriculum Scope: **30 Parts · 224 Phases · 240+ Practical Exercises · 42 Broken Labs · 20 Benchmarks · 11 Substantial Projects · 8 Capstones · ~180 Hours of Hands-On Engineering.**

---

## High-Level Milestone Architecture

```text
Foundations (Parts I–VII)       ──► Manual delivery, Git SHA identity, exit codes, local CI, caching, build DAGs
Containers & Releases (VIII–XII) ──► OCI packaging, digests, SemVer, environments, OIDC, SBOM, SLSA provenance
Deployment & Safety (XIII–XVII) ──► Continuous Delivery, Recreate/Rolling/Blue-Green/Canary, Rollback, Expand/Contract DB
Platform Engineering (XVIII–XXIV)──► Pipeline DAG optimization, telemetry/DORA, reusable workflows, GitOps, Progressive
Enterprise Delivery (XXV–XXX)   ──► Monorepos, multi-service compatibility, 42 broken labs, projects, capstone challenge
```

---

## Detailed Part & Phase Schedule

### Part I: Software Delivery Before CI/CD (Phases 00–07)
*Estimated Duration: 4 Hours*
- **Phase 00**: Delivery Lab — The tiny service with manual build, test, and run.
- **Phase 01**: What Happens After Code Is Written? — Source to production lineage.
- **Phase 02**: Version Control as Delivery Input — Commit SHA as immutable source state.
- **Phase 03**: Build From a Commit — Recording source SHA and artifact checksum.
- **Phase 04**: Manual Verification — Format, lint, unit tests, and integration tests by hand.
- **Phase 05**: Build Script — Creating `./scripts/local-ci.sh` (CI platform != build logic).
- **Phase 06**: Exit Codes — Process exit status 0 vs non-zero as pipeline control flow.
- **Phase 07**: Determinism — Same source + same inputs = equivalent behavior and artifacts.

### Part II: Continuous Integration from First Principles (Phases 08–17)
*Estimated Duration: 6 Hours*
- **Phase 08**: Why Continuous Integration? — Merging long-lived branches vs trunk integration.
- **Phase 09**: CI Trigger — Repository events: push, pull request, tag, schedule, manual dispatch.
- **Phase 10**: Runner — Control plane, message queues, and process workers.
- **Phase 11**: Local Runner Simulation — Building a Python CI runner from scratch.
- **Phase 12**: First GitHub Actions Workflow — Deconstructing every field in YAML.
- **Phase 13**: Workflow -> Job -> Step — Mental model of hierarchical execution.
- **Phase 14**: Parallel Jobs — Concurrently executing lint and unit tests.
- **Phase 15**: Dependencies Between Jobs — Modeling DAG execution constraints (`needs:`).
- **Phase 16**: Failure Propagation — Skipping dependent downstream jobs on failure.
- **Phase 17**: Conditions — Evaluating branch filters and conditional step execution.

### Part III: Dependencies & Caching (Phases 18–23)
*Estimated Duration: 5 Hours*
- **Phase 18**: Dependency Installation — Clean runner provisioning overhead.
- **Phase 19**: Lockfiles — Generating and enforcing frozen lockfiles and hashes.
- **Phase 20**: Dependency Caching — Caching package downloads (cache != build artifact).
- **Phase 21**: Cache Keys — Designing robust keys: OS, runtime version, and lockfile hash.
- **Phase 22**: Stale Cache — Detecting and diagnosing bad cache identities.
- **Phase 23**: Cache Poisoning / Trust — Security implications of restoring untrusted caches.

### Part IV: Testing in Pipelines (Phases 24–35)
*Estimated Duration: 8 Hours*
- **Phase 24**: Unit Tests — Sub-second fast feedback tests.
- **Phase 25**: Integration Tests — Real database and persistence verification.
- **Phase 26**: Service Containers — Ephemeral network dependencies in CI.
- **Phase 27**: Test Isolation — Preventing state leakage across parallel test workers.
- **Phase 28**: Flaky Tests — Root cause analysis of non-deterministic race conditions.
- **Phase 29**: Test Retries — Diagnostic containment vs toxic normalization of broken tests.
- **Phase 30**: Test Sharding — Splitting test suites across parallel workers.
- **Phase 31**: Test Selection — Affected-test execution and coverage-based selection.
- **Phase 32**: Coverage — Code coverage as diagnostic information, not a quality vanity metric.
- **Phase 33**: Contract Tests — Verifying API schemas across service boundaries.
- **Phase 34**: End-to-End Tests — Managing slow, expensive, broad-scope integration suites.
- **Phase 35**: Testing Pyramid / Portfolio — Balancing feedback speed, confidence, and compute cost.

### Part V: Static Verification (Phases 36–42)
*Estimated Duration: 5 Hours*
- **Phase 36**: Formatting — Automated code style consistency.
- **Phase 37**: Linting — Catching common anti-patterns and bug signatures.
- **Phase 38**: Type Checking — Compile-time type inference and signature checks.
- **Phase 39**: Static Analysis — Security and code smell detection in abstract syntax trees.
- **Phase 40**: Dependency Vulnerability Scanning — CVE scanning in context.
- **Phase 41**: Secret Scanning — Detecting hardcoded API keys and private certificates.
- **Phase 42**: IaC / Manifest Validation — Validating Kubernetes and Terraform syntax semantically.

### Part VI: Build Systems (Phases 43–48)
*Estimated Duration: 6 Hours*
- **Phase 43**: Compilation Pipeline — Source to object to package.
- **Phase 44**: Incremental Builds — Target-level caching avoiding redundant compilation.
- **Phase 45**: Build Graph — Directed Acyclic Graphs (DAG) and topological sorting.
- **Phase 46**: Parallel Builds — Multi-core and distributed target compilation.
- **Phase 47**: Hermetic Build Intuition — Eliminating unpinned host state and leaks.
- **Phase 48**: Reproducible Builds — `SOURCE_DATE_EPOCH` and bit-for-bit identical hashes.

### Part VII: Artifacts (Phases 49–54)
*Estimated Duration: 5 Hours*
- **Phase 49**: What Is an Artifact? — The compiled product of a build.
- **Phase 50**: Build Once — Promoting the identical artifact through dev, staging, prod.
- **Phase 51**: Artifact Identity — Version, commit SHA, build ID, and SHA-256 digest.
- **Phase 52**: Artifact Repository — Versioned package storage and retrieval.
- **Phase 53**: Retention — Retaining release artifacts vs purging ephemeral workflow logs.
- **Phase 54**: Workflow Artifacts — Diagnostic test reports vs production release packages.

### Part VIII: Containers in CI/CD (Phases 55–62)
*Estimated Duration: 6 Hours*
- **Phase 55**: Docker Build Manually — Understanding the container engine directly.
- **Phase 56**: Image Tags — Mutable tags (`:latest`, `:staging`) vs immutable versions.
- **Phase 57**: Image Digests — Cryptographic content addressability (`@sha256:...`).
- **Phase 58**: Docker Build in CI — Running BuildKit inside CI workers.
- **Phase 59**: Registry — Authenticated push and pull across registries.
- **Phase 60**: Layer Caching — Ordering Dockerfile steps to optimize build duration.
- **Phase 61**: Multi-Stage Build — Separating builder tools from minimal runtime images.
- **Phase 62**: Container Security — Non-root users, no embedded secrets, read-only root filesystems.

### Part IX: Versioning & Releases (Phases 63–69)
*Estimated Duration: 5 Hours*
- **Phase 63**: What Is a Release? — Distinguishing build, release, and deployment.
- **Phase 64**: Versioning — Semantic Versioning (SemVer) concepts.
- **Phase 65**: Git Tags — Mapping tags to commits and release artifacts.
- **Phase 66**: Release Notes — Generating meaningful human summaries.
- **Phase 67**: Changelog — Maintaining durable, human-readable project histories.
- **Phase 68**: Automated Release — Event-driven release workflows on tag pushes.
- **Phase 69**: Release Immutability — Enforcing write-once, immutable release packages.

### Part X: Environments & Configuration (Phases 70–74)
*Estimated Duration: 5 Hours*
- **Phase 70**: Dev / Test / Staging / Production — The rationale for environment separation.
- **Phase 71**: Environment Parity — Avoiding "works in staging, fails in prod".
- **Phase 72**: Configuration — Twelve-Factor runtime environment variable injection.
- **Phase 73**: Secrets — Injecting credentials securely without baking them into images.
- **Phase 74**: CI Environments — Deployment protection rules, reviewers, and approval windows.

### Part XI: Authentication & Pipeline Security (Phases 75–83)
*Estimated Duration: 8 Hours*
- **Phase 75**: Why CI Credentials Are Dangerous — The pipeline as a high-privilege target.
- **Phase 76**: Long-Lived Secrets — Leak, rotation, and blast-radius risks.
- **Phase 77**: Workload Identity / OIDC — Short-lived token exchange with cloud STS.
- **Phase 78**: Least Privilege — Scoping runner permissions to minimal required tasks.
- **Phase 79**: Job-Level Permissions — Explicit scopes per job (`id-token: write`).
- **Phase 80**: Fork / Pull Request Security — Trust boundaries and `pull_request_target` perils.
- **Phase 81**: Third-Party Actions — Reviewing and pinning actions to 40-character commit SHAs.
- **Phase 82**: Runner Security — Ephemeral hosted vs persistent self-hosted runner risks.
- **Phase 83**: Secret Exfiltration Lab — Simulating and blocking malicious test credential theft.

### Part XII: Software Supply Chain (Phases 84–91)
*Estimated Duration: 7 Hours*
- **Phase 84**: Supply Chain Mental Model — The end-to-end dependency trust graph.
- **Phase 85**: Checksums / Digests — Cryptographic verification of downloaded inputs.
- **Phase 86**: SBOM — Software Bill of Materials generation (CycloneDX, SPDX).
- **Phase 87**: Provenance — Recording exact builder identity and source revision.
- **Phase 88**: Artifact Attestation — In-toto statements and GitHub Artifact Attestations.
- **Phase 89**: Signing Concepts — Keyless cryptographic signing using Sigstore Cosign.
- **Phase 90**: Dependency Pinning — Enforcing exact hash verification on build dependencies.
- **Phase 91**: SLSA Concepts — Supply-chain Levels for Software Artifacts (Levels 1–3).

### Part XIII: Continuous Delivery (Phases 92–96)
*Estimated Duration: 6 Hours*
- **Phase 92**: Delivery Pipeline — The path from commit to production-ready package.
- **Phase 93**: Deployment Manually — Pulling, starting, probing, and switching by hand.
- **Phase 94**: Deployment Automation — Automating the verified manual procedure.
- **Phase 95**: Post-Deployment Verification — Smoke tests, readiness probes, and telemetry checks.
- **Phase 96**: Deployment Record — Immutable deployment ledgers and audit trails.

### Part XIV: Deployment Strategies (Phases 97–103)
*Estimated Duration: 7 Hours*
- **Phase 97**: Recreate Deployment — Stopping old, starting new, observing downtime.
- **Phase 98**: Rolling Deployment — Incremental replica replacement with zero downtime.
- **Phase 99**: Blue / Green — Parallel environments, instant cutover, rapid rollback.
- **Phase 100**: Canary — Progressive traffic allocation (1% -> 10% -> 50% -> 100%).
- **Phase 101**: Strategy Comparison — Trade-off matrix: cost, rollback speed, state safety.
- **Phase 102**: Canary Health Analysis — Error rate and latency guardrail evaluation.
- **Phase 103**: Failed Canary — Automated abort cutting traffic back to stable.

### Part XV: Rollback & Recovery (Phases 104–107)
*Estimated Duration: 5 Hours*
- **Phase 104**: Rollback — Re-pointing traffic to the previous immutable release digest.
- **Phase 105**: Roll-Forward — Deploying a hotfix when rollback is precluded.
- **Phase 106**: Rollback Is Not Guaranteed — Why schema mutations make rollback fail.
- **Phase 107**: Recovery Time — Measuring Mean Time to Recovery (MTTR).

### Part XVI: Database Migrations (Phases 108–113)
*Estimated Duration: 7 Hours*
- **Phase 108**: Deployment + Schema — Dual-version coexistence during rollouts.
- **Phase 109**: Breaking Migration — Demonstrating column drops causing instant crashes.
- **Phase 110**: Expand / Migrate / Contract — Three-phase zero-downtime database evolution.
- **Phase 111**: Backfills — Decoupled asynchronous batch data transformations.
- **Phase 112**: Migration Failure — Transactional recovery from interrupted migrations.
- **Phase 113**: Migration Idempotency — Re-running migrations safely.

### Part XVII: Feature Flags (Phases 114–118)
*Estimated Duration: 5 Hours*
- **Phase 114**: Deployment vs Release — Decoupling binary installation from user exposure.
- **Phase 115**: Feature Flags — Deploying dormant code to production.
- **Phase 116**: Gradual Rollout — Percentage-based user cohort exposure.
- **Phase 117**: Kill Switch — Sub-second operational disabling of broken features.
- **Phase 118**: Flag Debt — Lifecycle management and retirement of legacy flags.

### Part XVIII: Pipeline Design (Phases 119–127)
*Estimated Duration: 6 Hours*
- **Phase 119**: Pipeline DAG — Directed Acyclic Graph topology.
- **Phase 120**: Critical Path — Calculating the longest serial path bounding duration.
- **Phase 121**: Parallelization — Moving independent jobs off the critical path.
- **Phase 122**: Fan-Out / Fan-In — Parallel matrix execution with single result aggregation.
- **Phase 123**: Matrix Builds — Multi-version and multi-OS compatibility matrices.
- **Phase 124**: Fail-Fast — Fast feedback vs diagnostic completeness.
- **Phase 125**: Pipeline Timeouts — Enforcing maximum job durations to prevent hanging runners.
- **Phase 126**: Cancellation — Cancelling superseded pipeline runs on rapid pushes.
- **Phase 127**: Concurrency Controls — Serializing deployments to prevent race conditions.

### Part XIX: Pipeline Performance (Phases 128–135)
*Estimated Duration: 6 Hours*
- **Phase 128**: Measure Pipeline Duration — Profiling queue, checkout, build, and deploy.
- **Phase 129**: Feedback Time — Minimizing time-to-first-failure for developers.
- **Phase 130**: Stage Ordering — Placing fast, high-probability failure checks first.
- **Phase 131**: Caching — Optimizing dependency restore and build layer caches.
- **Phase 132**: Test Parallelism — Sharding test suites across runner pools.
- **Phase 133**: Runner Sizing — Benchmarking CPU and memory resource allocations.
- **Phase 134**: Queue Time — Managing runner pool saturation and queue latency.
- **Phase 135**: Cost — Tracking compute minutes, runner sizes, and cache storage costs.

### Part XX: Pipeline Observability (Phases 136–141)
*Estimated Duration: 6 Hours*
- **Phase 136**: Pipeline as Production System — Treating delivery as a Tier-1 service.
- **Phase 137**: Pipeline Metrics — Tracking duration, queue time, failure, and flake rates.
- **Phase 138**: Logs — Structured logging and secret-masking best practices.
- **Phase 139**: Build Artifacts for Debugging — Persisting test reports, dumps, and traces.
- **Phase 140**: Delivery Metrics — Tracking DORA metrics (DF, LT, CFR, MTTR).
- **Phase 141**: Pipeline SLO — Establishing 95th percentile PR validation time targets.

### Part XXI: Reusable Pipelines (Phases 142–147)
*Estimated Duration: 5 Hours*
- **Phase 142**: Duplication — The cost and maintenance drift of copy-pasted YAML.
- **Phase 143**: Reusable Workflows — Centralizing delivery logic in callable workflows.
- **Phase 144**: Workflow Inputs — Defining typed, validated input parameters.
- **Phase 145**: Workflow Outputs — Exposing generated digests and metadata downstream.
- **Phase 146**: Version Reusable Workflows — Semantic versioning of shared workflows.
- **Phase 147**: Escape Hatches — Supporting custom requirements without breaking standards.

### Part XXII: Platform Delivery Engineering (Phases 148–152)
*Estimated Duration: 6 Hours*
- **Phase 148**: Pipeline as Product — Measuring internal developer adoption and friction.
- **Phase 149**: Golden Pipeline — Providing a standard, production-ready delivery pipeline.
- **Phase 150**: Repository Template — Zero-to-pipeline onboarding for new microservices.
- **Phase 151**: Central Policy — Automated compliance and governance guardrails.
- **Phase 152**: Policy vs Mechanism — Decoupling organizational rules from specific tooling.

### Part XXIII: GitOps (Phases 153–165)
*Estimated Duration: 8 Hours*
- **Phase 153**: Push-Based Deployment — The traditional model and its limitations.
- **Phase 154**: Problems With Push Deployment — Runner credentials and silent drift.
- **Phase 155**: GitOps Mental Model — Pull-based reconcilers and Git as single source of truth.
- **Phase 156**: Desired vs Actual State — Drift detection and automatic correction.
- **Phase 157**: Argo CD Introduction — Reconciler architecture and operational loops.
- **Phase 158**: Application Configuration Repository — Application repo vs Config repo.
- **Phase 159**: Sync — Transitioning from `[OutOfSync]` to `[Synced]`.
- **Phase 160**: Automated Sync — Enabling self-healing declarative reconciliation.
- **Phase 161**: Drift — Detecting manual cluster mutations out-of-band.
- **Phase 162**: Git as Audit Trail — Commits as the deployment ledger.
- **Phase 163**: GitOps Rollback — Reverting Git commits to trigger automated recovery.
- **Phase 164**: GitOps Failure — Resolving bad desired-state deployments.
- **Phase 165**: Dangerous Sync Options — The hazards of `--replace` and `--force` flags.

### Part XXIV: Progressive Delivery (Phases 166–170)
*Estimated Duration: 6 Hours*
- **Phase 166**: GitOps ≠ Progressive Delivery — Desired state vs traffic rollout analysis.
- **Phase 167**: Progressive Rollout Controllers — Incremental traffic shifting mechanisms.
- **Phase 168**: Analysis Metrics — Error budgets, latency percentiles, and SLO guardrails.
- **Phase 169**: Automated Promotion — Promoting traffic steps upon passing analysis.
- **Phase 170**: Automated Abort — Reverting traffic immediately upon metric degradation.

### Part XXV: Monorepos (Phases 171–176)
*Estimated Duration: 6 Hours*
- **Phase 171**: Monorepo Delivery Problem — Rebuilding all services on every commit.
- **Phase 172**: Change Detection — Identifying modified files via Git diffs.
- **Phase 173**: Dependency Graph — Mapping shared libraries to dependent services.
- **Phase 174**: Selective Pipelines — Running tests only for affected components.
- **Phase 175**: Monorepo Cache — Shared build caching across monorepo projects.
- **Phase 176**: Monorepo Release Strategy — Independent vs unified semantic versioning.

### Part XXVI: Multiple Services (Phases 177–181)
*Estimated Duration: 6 Hours*
- **Phase 177**: Service Dependencies — Cross-service API compatibility constraints.
- **Phase 178**: Backward-Compatible APIs — Eliminating lockstep release requirements.
- **Phase 179**: Consumer-Driven Compatibility — Testing client contracts in CI.
- **Phase 180**: Coordinated Release — Managing multi-service releases when unavoidable.
- **Phase 181**: Microservice Deployment Independence — Testing the architectural invariant.

### Part XXVII: Mobile / Library / Data Variants (Phases 182–186)
*Estimated Duration: 6 Hours*
- **Phase 182**: Library CI/CD — Semantic stability and package registry distribution.
- **Phase 183**: CLI/Binary Release — Multi-platform cross-compilation and checksums.
- **Phase 184**: Mobile Release Concepts — App Store review constraints vs instant web CD.
- **Phase 185**: Data Pipeline CI/CD — SQL testing, schema migration, and backfills.
- **Phase 186**: Infrastructure CI/CD — Plan, review, and apply workflows in Terraform/OpenTofu.

### Part XXVIII: Failure Labs (Phases 187–205)
*Estimated Duration: 15 Hours*
- **Phase 187–204**: 18 Dedicated Incident Scenarios covering tests, caches, credentials, registries, probes, migrations, GitOps, and supply-chain.
- **Phase 205**: The Complete 42 Broken CI/CD Lab Suite — Hands-on troubleshooting and fixes with separate solutions.

### Part XXIX: Substantial Projects (Phases 206–216)
*Estimated Duration: 25 Hours*
- **Phase 206**: Project 01 — Build a Local CI Runner from scratch.
- **Phase 207**: Project 02 — Full GitHub Actions CI with sharding and matrix.
- **Phase 208**: Project 03 — Immutable Container Packaging & Registry Delivery.
- **Phase 209**: Project 04 — Automated Staging Deployment & Smoke Verification.
- **Phase 210**: Project 05 — Production Delivery with Approvals & Rollback.
- **Phase 211**: Project 06 — OIDC Short-Lived Workload Identity Federation.
- **Phase 212**: Project 07 — Supply-Chain SBOM & SLSA Build Provenance.
- **Phase 213**: Project 08 — Central Reusable Workflow Platform.
- **Phase 214**: Project 09 — Monorepo Selective Delivery Engine.
- **Phase 215**: Project 10 — Declarative GitOps Delivery with Argo CD Reconciler.
- **Phase 216**: Project 11 — Progressive Canary Deployment with Automated Abort.

### Part XXX: Capstones & Architecture Challenge (Phases 217–224)
*Estimated Duration: 20 Hours*
- **Phase 217**: Capstone 1 — Production-Grade Continuous Integration.
- **Phase 218**: Capstone 2 — Continuous Delivery & Environment Promotion.
- **Phase 219**: Capstone 3 — Continuous Deployment with Automated Safety Guardrails.
- **Phase 220**: Capstone 4 — Progressive Canary Delivery with Automated Abort.
- **Phase 221**: Capstone 5 — Enterprise GitOps Platform with Argo CD.
- **Phase 222**: Capstone 6 — Internal Developer Platform & Golden Pipeline.
- **Phase 223**: Capstone 7 — Delivery Failure Day (Chaos Drill across 10 critical failures).
- **Phase 224**: Final Enterprise CI/CD Architecture Challenge (300 engineers, 100 services).
