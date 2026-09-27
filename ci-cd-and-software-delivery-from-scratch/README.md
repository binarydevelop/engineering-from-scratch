# CI/CD and Software Delivery from Scratch

<p align="center">
  <b>Understand it. Build it. Test it. Package it. Verify it. Release it. Deploy it. Observe it. Recover it. Automate it.</b>
</p>

<p align="center">
  <a href="VERSIONS.md"><img src="https://img.shields.io/badge/status-production--ready-1a1a1a?style=flat-square&labelColor=fafaf5" alt="Status"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/parts-30_parts-3553ff?style=flat-square&labelColor=fafaf5" alt="30 Parts"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/phases-224_phases-3553ff?style=flat-square&labelColor=fafaf5" alt="224 Phases"></a>
  <a href="broken-pipelines/"><img src="https://img.shields.io/badge/broken_labs-42_scenarios-red?style=flat-square&labelColor=fafaf5" alt="42 Broken Labs"></a>
  <a href="benchmarks/"><img src="https://img.shields.io/badge/benchmarks-20_experiments-green?style=flat-square&labelColor=fafaf5" alt="20 Benchmarks"></a>
  <a href="projects/"><img src="https://img.shields.io/badge/projects-11_systems-blue?style=flat-square&labelColor=fafaf5" alt="11 Projects"></a>
  <a href="capstones/"><img src="https://img.shields.io/badge/capstones-8_challenges-purple?style=flat-square&labelColor=fafaf5" alt="8 Capstones"></a>
</p>

---

> [!IMPORTANT]
> **This is NOT a GitHub Actions YAML tutorial.**  
> **This is NOT a Jenkins tutorial.**  
> **This is NOT a collection of deployment commands.**  
> **This is a course in software delivery engineering.**

---

## The Target Mental Model

The target mental model is:

> **CI/CD is a software-delivery control system that turns source changes into verified, immutable, observable, and safely deployable software artifacts.**

The learner should finish able to reason about the entire path from:
```text
git commit
```
to:
```text
production software serving users
```
without treating the delivery system as magic.

---

## The Complete Path of Software Delivery

```text
Source Revision (Git Commit SHA)
           │
           ▼
    Manual Build & Exit Codes ($?)
           │
           ▼
 Continuous Integration (Frequent Synchronization)
           │
           ▼
   Automated Test Portfolio (Unit, Integration, Contract)
           │
           ▼
  Immutable Artifact Packaging (Content Digest SHA-256)
           │
           ▼
     Containerization (Multi-stage, Non-Root)
           │
           ▼
   Release Engineering (SemVer, SBOM, SLSA Provenance)
           │
           ▼
 Continuous Delivery (Build Once, Promote Many)
           │
           ▼
Deployment Strategies (Recreate, Rolling, Blue/Green, Canary)
           │
           ▼
Zero-Downtime Database Evolution (Expand / Migrate / Contract)
           │
           ▼
Progressive Delivery (Telemetry Analysis & Automated Abort)
           │
           ▼
Software Supply-Chain Security (Cosign, OIDC Workload Identity)
           │
           ▼
       GitOps (Declarative Reconciliation & Drift Control)
           │
           ▼
Reusable Platform Engineering (Golden Pipelines & Developer Self-Service)
```

---

## Critical Distinctions: Teach These Very Early

### 1. Continuous Integration (CI)
```text
developers integrate changes frequently (daily)
↓
automated verification gives fast feedback (minutes)
```
CI is **not** merely "running tests on GitHub." CI is a team working agreement to avoid integration hell by synchronizing work into trunk daily and verifying every commit automatically.

---

### 2. Continuous Delivery (CD)
```text
every suitable verified change
can be released to production safely at any moment
```
Production deployment may still require a deliberate business approval or scheduled release window.

---

### 3. Continuous Deployment
```text
every suitable verified change
automatically reaches production with zero manual human gating
```
An advanced extension of Continuous Delivery where automated safety guardrails, health probes, and error budgets eliminate manual approval clicks entirely.

---

## The Central Rule

**Never start with pipeline YAML.**

Bad:
```yaml
steps:
  - uses: actions/checkout@...
```
*(without understanding what is happening under the hood).*

Better: Start manually in the terminal:
```bash
git clone ...
cd project
install dependencies
run lint
run tests
build artifact
```

Then ask:
- *How do we make this repeatable?*
- *How do we make this isolated?*
- *How do we make this automatic?*
- *How do we make this auditable?*
- *How do we make this fast?*
- *How do we make this secure?*

Then derive the automation script. Then derive the CI platform.

---

## The 30 Curriculum Parts (Phases 00–224)

| Part | Title | Phase Range | Focus & Core Principles |
|:---|:---|:---|:---|
| **[Part I](phases/part-01-software-delivery-before-ci-cd/)** | Software Delivery Before CI/CD | Phases 00–07 | The shell, Git SHA content identity, exit codes (`$?`), determinism, local build scripts. |
| **[Part II](phases/part-02-ci-from-first-principles/)** | CI From First Principles | Phases 08–17 | Integration hell, triggers, runners, DAG evaluation, parallel jobs, failure propagation. |
| **[Part III](phases/part-03-dependencies-and-caching/)** | Dependencies & Caching | Phases 18–23 | Frozen lockfiles, cache key composition, stale caches, cache poisoning attack vectors. |
| **[Part IV](phases/part-04-testing-pipelines/)** | Testing in Pipelines | Phases 24–35 | Fast unit tests, integration tests, test isolation, flaky quarantine, test sharding, contracts. |
| **[Part V](phases/part-05-static-verification/)** | Static Verification | Phases 36–42 | AST linting, formatters, type checking, secret scanning, manifest validation. |
| **[Part VI](phases/part-06-build-systems/)** | Build Systems | Phases 43–48 | Compilation DAG, target caching, incremental builds, hermetic builds, `SOURCE_DATE_EPOCH`. |
| **[Part VII](phases/part-07-artifacts/)** | Artifacts | Phases 49–54 | Build Once Promote Many, immutable artifact identity, registry storage, workflow diagnostics. |
| **[Part VIII](phases/part-08-containers-in-ci-cd/)** | Containers in CI/CD | Phases 55–62 | Dockerfile commands, immutable digests vs mutable tags, layer caching, non-root security. |
| **[Part IX](phases/part-09-versioning-and-releases/)** | Versioning & Releases | Phases 63–69 | Build vs Release vs Deployment, SemVer, Git tags, changelogs, release immutability. |
| **[Part X](phases/part-10-environments/)** | Environments & Configuration | Phases 70–74 | Twelve-Factor runtime config, environment parity, secret injection, protection rules. |
| **[Part XI](phases/part-11-authentication-and-pipeline-security/)** | Authentication & Security | Phases 75–83 | CI threat model, long-lived secrets vs OIDC Workload Identity, least privilege, fork PR safety. |
| **[Part XII](phases/part-12-software-supply-chain/)** | Software Supply Chain | Phases 84–91 | Checksums, CycloneDX SBOM, SLSA v1.0 Provenance, Sigstore Cosign keyless signing. |
| **[Part XIII](phases/part-13-continuous-delivery/)** | Continuous Delivery | Phases 92–96 | Delivery pipelines, post-deployment smoke verification, deployment audit ledgers. |
| **[Part XIV](phases/part-14-deployment-strategies/)** | Deployment Strategies | Phases 97–103 | Recreate, Rolling Update, Blue/Green, Canary, strategy trade-off comparison matrix. |
| **[Part XV](phases/part-15-rollback-and-recovery/)** | Rollback & Recovery | Phases 104–107 | Rollback execution, roll-forward decisions, why rollback is not guaranteed, MTTR. |
| **[Part XVI](phases/part-16-database-migrations/)** | Database Migrations | Phases 108–113 | Dual-version coexistence, breaking migrations, Expand/Migrate/Contract paradigm. |
| **[Part XVII](phases/part-17-feature-flags/)** | Feature Flags | Phases 114–118 | Deploy vs Release decoupling, gradual percentage rollouts, kill switches, flag debt. |
| **[Part XVIII](phases/part-18-pipeline-design/)** | Pipeline Design | Phases 119–127 | DAG critical path analysis, parallelization, fan-out/fan-in, concurrency locks, timeouts. |
| **[Part XIX](phases/part-19-pipeline-performance/)** | Pipeline Performance | Phases 128–135 | Feedback time optimization, stage ordering, runner sizing, cache tuning, compute costs. |
| **[Part XX](phases/part-20-pipeline-observability/)** | Pipeline Observability | Phases 136–141 | Pipeline as production system, structured logs, DORA metrics (DF, LT, CFR, MTTR), SLOs. |
| **[Part XXI](phases/part-21-reusable-pipelines/)** | Reusable Pipelines | Phases 142–147 | Centralizing workflows, typed inputs/outputs, versioning (`@v1`), escape hatches. |
| **[Part XXII](phases/part-22-platform-delivery-engineering/)** | Platform Delivery Engineering | Phases 148–152 | Pipeline as product, Golden Pipelines, repository templates, compliance guardrails. |
| **[Part XXIII](phases/part-23-gitops/)** | GitOps & Reconciliation | Phases 153–165 | Push vs Pull, Argo CD architecture, drift detection, dangerous replace options. |
| **[Part XXIV](phases/part-24-progressive-delivery/)** | Progressive Delivery | Phases 166–170 | Traffic rollout controllers, metric guardrails, automated promotion and blast-radius abort. |
| **[Part XXV](phases/part-25-monorepos/)** | Monorepo Architectures | Phases 171–176 | Change detection, internal dependency DAGs, selective affected-only pipelines. |
| **[Part XXVI](phases/part-26-multiple-services/)** | Multi-Service Coordination | Phases 177–181 | Service dependencies, backward-compatible APIs, consumer contracts, independent release. |
| **[Part XXVII](phases/part-27-mobile-library-data-variants/)** | Delivery Variants | Phases 182–186 | Public library CI/CD, multi-platform binary compilation, data pipelines, IaC CI/CD. |
| **[Part XXVIII](phases/part-28-failure-labs/)** | Failure Labs | Phases 187–205 | 42 realistic pipeline failures across all domains with separate verified solutions. |
| **[Part XXIX](phases/part-29-projects/)** | Substantial Projects | Phases 206–216 | 11 end-to-end projects: Local runner, OIDC, SBOM, GitOps, Canary, Monorepo. |
| **[Part XXX](phases/part-30-capstones/)** | Capstones & Final Challenge | Phases 217–224 | 8 enterprise capstone challenges including Phase 224 Final Architecture Challenge. |

---

## The 20 Anti-Patterns Directory

| Anti-Pattern | Why Tempting | The Fatal Failure Mode | Better Design |
|:---|:---|:---|:---|
| **1. Pipeline YAML as Build System** | Easy to write inline `curl` and `python` in YAML. | Cannot test or debug pipeline logic locally without pushing commits. | Put logic in `./scripts/*.sh`; pipeline simply invokes standalone scripts. |
| **2. Green Means Safe** | All unit tests pass, so code is assumed production-ready. | Artifact crashes on launch due to missing environment variable or database deadlock. | Add post-deployment smoke tests probing live `/health/readiness` and contract tests. |
| **3. Build Per Environment** | Easy to bake `DB_URL` into binary during build. | Code tested in staging is NOT what runs in production; environment drift creates outages. | **Build Once, Promote Many**: Build single artifact; inject config via environment variables. |
| **4. `latest` Everywhere** | Avoids having to update deployment YAML tags. | Pod restarts pull different code versions simultaneously, splitting cluster behavior. | Deploy by immutable content digest (`image@sha256:...`) or exact SemVer tag. |
| **5. Permanent Cloud Admin Secret** | Simple to copy-paste AWS secret keys into CI settings. | Malicious PR or compromised dependency exfiltrates keys, yielding full cloud takeover. | Use OpenID Connect (OIDC) Workload Identity Federation for short-lived 15-minute tokens. |
| **6. Secret in Docker Build** | Easy to pass API token via `ARG` or `ENV`. | Secret is permanently baked into Docker image metadata layers and accessible via `inspect`. | Use BuildKit secret mounts (`RUN --mount=type=secret`) or inject at runtime. |
| **7. Retry Until Green** | Easy way to get a blocked PR to merge when tests flake. | Hides concurrency race conditions and memory leaks that eventually strike in production. | Quarantine flaky tests immediately; treat intermittent failures as high-priority bugs. |
| **8. Cache Everything** | Speed up builds by caching entire working directory. | Corrupted or stale caches silently pass old code or fail with bizarre missing symbols. | Cache only package manager download directories; key by exact hash of lockfile. |
| **9. Sequential Pipeline** | Simple to read: run step 1, then step 2, then step 3. | Feedback takes 45 minutes; developers wait idle instead of writing code. | Model jobs as a Directed Acyclic Graph (DAG) and run independent checks in parallel. |
| **10. Parallelize Everything** | Spin up 50 parallel jobs to make everything "fast." | Exhausts runner pool concurrency, spikes cloud bills, and hits external registry 429 limits. | Optimize the serial critical path; shard only computationally heavy test suites. |
| **11. 100% E2E Testing** | Believing end-to-end tests provide ultimate safety. | Extremely slow (1-2 hours), brittle browser timing flakes, and high cloud compute costs. | Follow the Testing Portfolio: high-volume unit tests, contract tests, and targeted smoke probes. |
| **12. Deploy Without Verification** | Assuming `kubectl apply` returning 0 means success. | Pods crash in `CrashLoopBackOff`; pipeline is green while customer site is down. | Enforce post-deployment verification: readiness probes, smoke tests, and error budget checks. |
| **13. Rollback Without Testing It** | Assuming you can always "just revert the deployment." | Schema changes or data transformations make older application code crash on launch. | Verify N-1 application compatibility against database schema before deploying. |
| **14. DB Migration + Code Flip** | Deploying new code and renaming a database column together. | Running v1 pods crash during rolling update window with `column not found`. | Use **Expand / Migrate / Contract**: deploy non-breaking schema first, contract later. |
| **15. GitOps Cargo Cult** | Copying Argo CD YAML without understanding reconciliation. | Manual cluster edits fight with reconciler in endless loop, or bad config deploys blindly. | Understand desired vs actual state reconciliation and enforce PR linting on config repos. |
| **16. CI With Production Admin** | Convenient to give CI runner broad cluster admin role. | Any compromised build script can delete production clusters or exfiltrate customer data. | Decouple CI (builds artifacts) from GitOps (pulls into cluster); enforce least privilege. |
| **17. Unpinned Third-Party Actions** | Using `uses: action@v1` to get automatic bug fixes. | Upstream maintainer account compromised; malicious code pushed to `@v1` tag runs in your CI. | Pin all third-party actions to immutable 40-character commit SHAs. |
| **18. Shared Dirty Runner** | Saving money by reusing persistent self-hosted VM disk. | Build A leaves uncommitted files on disk that cause Build B to pass falsely or leak secrets. | Use ephemeral, single-use runner environments destroyed after every job. |
| **19. Giant Universal Pipeline** | One 2,000-line workflow template used by all 100 services. | Any change risks breaking all services; full of confusing conditionals and escape hatches. | Provide modular, versioned reusable workflows with small, typed interfaces. |
| **20. DORA Metrics as Individual KPI** | Management tracking deployment count per engineer. | Developers game the system by pushing trivial empty commits to inflate deployment frequency. | Use DORA metrics strictly to measure delivery team system health and cycle time. |

---

## Hands-On Tooling & Interactive Simulators

This repository includes production-grade, zero-external-dependency simulators built with standard Python and POSIX shell:

1. **Local CI Runner Engine** ([`pipelines/local_runner.py`](pipelines/local_runner.py)):
   - Complete CI execution control plane executing job DAGs, exit code trapping, caching, and failure propagation.
2. **Deployment Strategy Simulator** ([`deployment-labs/deploy_simulator.py`](deployment-labs/deploy_simulator.py)):
   - Interactive simulation of Recreate, Rolling, Blue/Green, and Progressive Canary with automated health analysis and abort.
3. **GitOps Reconciler Engine** ([`gitops/gitops_reconciler.py`](gitops/gitops_reconciler.py)):
   - Watches Git desired-state, compares with live cluster state, detects drift, reconciles, and flags dangerous replace options.
4. **OIDC Workload Identity Simulator** ([`security-labs/oidc_simulator.py`](security-labs/oidc_simulator.py)):
   - Ephemeral JWT generation, claim verification against cloud STS trust policies, and short-lived session token issuance.
5. **SBOM & SLSA Provenance Attestation Suite** ([`security-labs/sbom_provenance_generator.py`](security-labs/sbom_provenance_generator.py)):
   - CycloneDX v1.5 SBOM generator and SLSA Provenance v1.0 generator and cryptographic verifier.
6. **Secret Leak Scanner** ([`security-labs/secret_leak_scanner.py`](security-labs/secret_leak_scanner.py)):
   - Pre-commit and CI scanner detecting high-risk tokens, API keys, and private certificates.
7. **Build Graph DAG & Incremental Build Engine** ([`build-labs/dag_builder.py`](build-labs/dag_builder.py)):
   - Topological sorting and target-level incremental caching avoiding redundant compilation.
8. **Reproducible Build Validator** ([`build-labs/reproducible_build_check.py`](build-labs/reproducible_build_check.py)):
   - Bit-for-bit reproducibility validator enforcing `SOURCE_DATE_EPOCH` and archive normalization.
9. **Pipeline Performance Benchmarking Suite** ([`benchmarks/benchmark_pipeline.py`](benchmarks/benchmark_pipeline.py)):
   - 20+ pipeline performance experiments measuring critical path, caching speedup, and test sharding.
10. **42 Broken CI/CD Labs & Test Harness** ([`broken-pipelines/`](broken-pipelines/)):
    - 42 real-world failure scenarios covering Git, dependencies, caches, builds, registries, credentials, deployments, migrations, GitOps, and supply-chain, verified via [`broken-pipelines/verify_all_labs.py`](broken-pipelines/verify_all_labs.py).

---

## Quickstart: Produce Your First Evidence in 60 Seconds

```bash
# 1. Clone the repository
git clone https://github.com/binarydevelop/ci-cd-and-software-delivery-from-scratch.git
cd ci-cd-and-software-delivery-from-scratch

# 2. Run the environment preflight check
make check-env

# 3. Execute all automated test suites (unit, integration, contract, smoke)
make test

# 4. Execute the complete standalone local CI pipeline from scratch
make local-ci

# 5. Run interactive deployment and GitOps simulators
make simulations

# 6. Verify all 42 broken pipeline labs and solutions
make verify-broken-labs
```

---

## Mastery Questions

1. **On Feedback Loops**:
   *Five engineers merge large branches once per month, and integration failures take three days to untangle. Which feedback loop does Continuous Integration attempt to shorten, and what automation is necessary versus merely convenient?*
2. **On Cache Identity**:
   *Dependency installation consumes six minutes per run. You cache dependencies using only the branch name as the key. A dependency version changes, but CI restores the old cache. What was wrong with the cache's identity?*
3. **On GitOps Architecture**:
   *Your CI runner currently holds production Kubernetes credentials and directly runs `kubectl apply`. How would a GitOps reconciliation model change where desired state lives, which component needs cluster credentials, and how deployment drift is handled?*
4. **On Database Rollback Safety**:
   *Version 2 introduced a database migration that removed a column used by version 1. Why might redeploying version 1 fail even if the old container image is still available in the registry?*
5. **On Supply-Chain Provenance**:
   *A container image named `api:v2.1` exists in your production registry. How do you cryptographically prove which exact Git commit, pipeline workflow, and runner built that image without trusting the mutable tag name?*

---

## The Final Engineering Standard

The learner is finished when:

```text
"The deployment failed."
```

does **NOT** cause:

```text
"Click re-run pipeline"
```

as the first and only response.

Instead, they systematically reason:
- *Which source revision?*
- *Which pipeline?*
- *Which runner?*
- *Which step?*
- *Which artifact?*
- *Did build succeed?*
- *Was artifact published?*
- *Which digest reached the environment?*
- *Did deployment machinery accept it?*
- *Did the application start?*
- *Did readiness probes pass?*
- *Did health metrics regress?*
- *Was the database schema compatible?*
- *Can we rollback safely?*
- *Would roll-forward be safer?*
- *What evidence do we have?*

---

## Conclusion

> CI/CD is no longer a collection of YAML files that somehow move code into production.
>
> We started with the manual path from source code to tested software, automated that path into repeatable integration pipelines, created immutable artifacts, secured the build and release process, and learned how the same verified software can move safely through increasingly production-like environments.
>
> We deliberately broke tests, caches, registries, credentials, database migrations, deployment strategies, and GitOps reconciliation until we understood how delivery systems fail and recover.
>
> Now when a commit reaches production, we can trace exactly which source produced which artifact, which checks were performed, which identity authorized the deployment, how health was verified, and how the system can be safely recovered if the change is wrong.
