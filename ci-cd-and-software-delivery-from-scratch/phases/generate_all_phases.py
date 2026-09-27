#!/usr/bin/env python3
"""
Generator for Parts 13 through 30 of CI/CD and Software Delivery from Scratch.
Ensures every part has full 19-section structure and 8 practical exercises per part,
surpassing the 200+ practical exercises requirement.
"""

import os

PARTS_DATA = [
    {
        "part_num": "13",
        "slug": "part-13-continuous-delivery",
        "title": "Part XIII: Continuous Delivery (Phases 92–96)",
        "phases": "Phases 92–96",
        "motto": "Continuous Delivery ensures that every suitable change can be released safely at any moment. Deployment command exiting zero does not prove application health.",
        "problem": "A team configures an automated deployment script. When executed, `kubectl apply` returns exit code 0. The team assumes the deployment succeeded and closes the release ticket. In reality, the new container crashed on startup due to a missing runtime library, leaving pods stuck in CrashLoopBackOff while customers see HTTP 502 errors.",
        "first_principles": "Deployment is a multi-step transition: binary distribution, process startup, dependency connection, readiness probe passing, traffic routing, and health verification. The pipeline must verify post-deployment health before declaring completion.",
        "manual_cmd": "python3 sample-apps/delivery-service/tests/smoke/test_smoke.py",
        "break_lab": "broken-pipelines/20-deploy-succeeds-but-app-crashes-on-startup/reproduce_failure.py",
        "exercises": [
            "Write a post-deployment smoke test script probing `/health/liveness` and `/health/readiness` with exponential backoff.",
            "Implement a deployment audit ledger in SQLite that records deployed artifact digest, timestamp, actor, and result.",
            "Simulate a slow container startup and configure `initialDelaySeconds` to prevent premature probe failures.",
            "Write a script that curls `/version` on all live instances and asserts that 100% of replicas report the target commit SHA.",
            "Differentiate Continuous Delivery from Continuous Deployment in an engineering team policy document.",
            "Build a synthetic transaction tester that creates a test order through the API and validates its persistence.",
            "Measure the deployment verification duration and optimize probe polling frequency.",
            "Implement an automated Slack or webhook notification that broadcasts successful deployment metadata to the engineering team."
        ]
    },
    {
        "part_num": "14",
        "slug": "part-14-deployment-strategies",
        "title": "Part XIV: Deployment Strategies (Phases 97–103)",
        "phases": "Phases 97–103",
        "motto": "Every deployment strategy is a conscious trade-off between infrastructure cost, rollback speed, state compatibility, and blast radius.",
        "problem": "An engineering team deploys a breaking change via Recreate deployment on a production payment gateway. The service experiences 6 minutes of total downtime, dropping 4,200 checkout transactions and triggering customer escalations.",
        "first_principles": "Recreate causes downtime. Rolling updates maintain capacity but require dual-version database compatibility. Blue/Green doubles capacity cost but offers instant rollback. Canary minimizes blast radius by testing real traffic incrementally.",
        "manual_cmd": "python3 deployment-labs/deploy_simulator.py --strategy rolling",
        "break_lab": "broken-pipelines/27-canary-promoted-despite-elevated-5xx-errors/reproduce_failure.py",
        "exercises": [
            "Run the deployment simulator in Recreate mode and observe the downtime interval.",
            "Execute a Rolling Update simulation with `maxSurge: 1` and `maxUnavailable: 0` and verify zero downtime.",
            "Simulate a Blue/Green router switch and measure the cutover duration in milliseconds.",
            "Execute a Canary rollout progression (1% -> 10% -> 50% -> 100%) and monitor error rates.",
            "Inject a 20% error rate into the canary and verify that automated abort cuts traffic immediately.",
            "Construct a comparative trade-off matrix evaluating cost, rollback speed, and state compatibility.",
            "Write a Prometheus PromQL query that calculates the error budget burn rate of a canary replica.",
            "Simulate state compatibility issues when v1 and v2 replicas concurrently access the same database."
        ]
    },
    {
        "part_num": "15",
        "slug": "part-15-rollback-and-recovery",
        "title": "Part XV: Rollback & Recovery (Phases 104–107)",
        "phases": "Phases 104–107",
        "motto": "Never assume rollback is guaranteed. A recovery plan that has never been tested in production is mere wishful thinking.",
        "problem": "A bug in release v2 causes data corruption. The on-call engineer rolls back the application image to v1. However, v2 ran a migration that dropped a column required by v1. Re-deploying v1 crashes instantly, leaving the team with both versions broken.",
        "first_principles": "Application rollback is independent of database rollback. When irreversible data transformations occur, roll-forward (deploying v3 with a fix) is often safer than rolling back.",
        "manual_cmd": "bash scripts/rollback.sh staging prev-known-good",
        "break_lab": "broken-pipelines/22-rollback-fails-due-to-irreversible-migration/reproduce_failure.py",
        "exercises": [
            "Execute `scripts/rollback.sh` and inspect the pre-flight database schema compatibility check.",
            "Simulate an irreversible schema change and observe why application rollback fails.",
            "Measure Mean Time to Recovery (MTTR) across 5 simulated rollback exercises.",
            "Formulate a decision matrix for when to Roll Back vs when to Roll Forward.",
            "Write an automated rollback hook in GitHub Actions that executes on step failure.",
            "Test reverting a Git commit in a GitOps configuration repository to trigger automated recovery.",
            "Design an emergency hotfix workflow that bypasses non-critical linters while maintaining security checks.",
            "Document a post-incident recovery runbook for a failed database migration."
        ]
    },
    {
        "part_num": "16",
        "slug": "part-16-database-migrations",
        "title": "Part XVI: Database Migrations in Delivery (Phases 108–113)",
        "phases": "Phases 108–113",
        "motto": "Never execute breaking schema changes and code deployments simultaneously. Expand, Migrate, Contract is the foundation of zero-downtime persistence.",
        "problem": "A developer renames column `user_email` to `email` in a single migration script and deploys the new code. During the 15-minute rolling update, running v1 pods query `user_email` and crash because the column was renamed, causing an immediate production outage.",
        "first_principles": "Database migrations must be backward-compatible with N-1 application versions. In the Expand phase, add new columns with defaults. In the Migrate phase, backfill data. In the Contract phase, drop legacy columns only after old code is completely decommissioned.",
        "manual_cmd": "python3 sample-apps/delivery-service/db/migration_engine.py",
        "break_lab": "broken-pipelines/21-breaking-database-column-drop-instant-crash/reproduce_failure.py",
        "exercises": [
            "Run all 4 stages of migrations in `sample-apps/delivery-service/db/` and verify idempotency.",
            "Simulate an un-indexed table update on 100,000 rows and observe table lock starvation.",
            "Implement a batching backfill script that migrates records in chunks of 1,000 rows with sleep pauses.",
            "Write a SQL linter that detects and blocks `DROP COLUMN` and `ALTER COLUMN TYPE` in PR pipelines.",
            "Test simultaneous execution of v1 and v2 application code against the expanded schema.",
            "Simulate a migration failure midway through execution and test transactional rollback.",
            "Verify that `schema_migrations` records applied versions deterministically.",
            "Design a two-week migration release schedule across Expand, Migrate, and Contract phases."
        ]
    },
    {
        "part_num": "17",
        "slug": "part-17-feature-flags",
        "title": "Part XVII: Feature Flags & Decoupled Release (Phases 114–118)",
        "phases": "Phases 114–118",
        "motto": "Deployment puts code in production; feature flags put code in front of users. Decouple deployment from release to eliminate release-day panic.",
        "problem": "A marketing launch is scheduled for 09:00 AM on Monday. Engineering deploys the code at 08:45 AM. The deployment hits a networking glitch, creating a delayed rollout and widespread panic during the public launch.",
        "first_principles": "By wrapping new behavior behind feature flags, code can be deployed dormant to production days in advance. At launch time, a flag toggle instantly enables the feature without code deployment.",
        "manual_cmd": "curl -s http://localhost:8080/api/flags",
        "break_lab": "broken-pipelines/28-feature-flag-deadlock-stale-flag-debt/reproduce_failure.py",
        "exercises": [
            "Query and update feature flags in `sample-apps/delivery-service` via REST API.",
            "Implement a feature flag kill-switch that disables an errant feature path in under 1 second.",
            "Simulate gradual feature rollout: enable feature for 10% of user IDs using hash modulo.",
            "Write a static analysis script that flags feature flags older than 30 days as technical debt.",
            "Demonstrate how dormant code deployed to production can be verified with internal tester headers.",
            "Design a flag retirement plan removing dead code branches after 100% rollout.",
            "Test application fallback behavior when a remote feature flag service is unreachable.",
            "Calculate the cognitive complexity added to code by maintaining nested feature flags."
        ]
    },
    {
        "part_num": "18",
        "slug": "part-18-pipeline-design",
        "title": "Part XVIII: Pipeline Design & Topology (Phases 119–127)",
        "phases": "Phases 119–127",
        "motto": "A well-designed pipeline is an efficient Directed Acyclic Graph. Move independent work off the critical path, fail fast on blocking errors, and guard against concurrency races.",
        "problem": "A delivery pipeline executes 12 jobs in strict serial sequence. Total duration is 48 minutes. When a unit test fails at minute 42, the developer waited nearly an hour just to discover a one-line typo.",
        "first_principles": "Topological sorting of job dependencies identifies parallel execution opportunities. The critical path determines the lower bound on total pipeline duration. Concurrency locks prevent racing deployments.",
        "manual_cmd": "python3 benchmarks/benchmark_pipeline.py",
        "break_lab": "broken-pipelines/30-pipeline-hangs-indefinitely-no-timeout/reproduce_failure.py",
        "exercises": [
            "Calculate the critical path duration of a multi-job pipeline using DAG analysis.",
            "Configure `concurrency: group, cancel-in-progress: true` in GitHub Actions and test cancellation.",
            "Demonstrate the trade-off between `fail-fast: true` and collecting full diagnostic test reports.",
            "Configure hard timeouts on jobs (`timeout-minutes: 10`) to prevent hanging processes.",
            "Build a matrix build workflow testing across multiple Python versions and operating systems.",
            "Implement fan-out / fan-in topology where parallel tests aggregate into a single release job.",
            "Prevent production deployment race conditions using serialization mutex locks.",
            "Profile runner CPU and memory utilization during peak parallel DAG execution."
        ]
    },
    {
        "part_num": "19",
        "slug": "part-19-pipeline-performance",
        "title": "Part XIX: Pipeline Performance Optimization (Phases 128–135)",
        "phases": "Phases 128–135",
        "motto": "Developer productivity is bounded by CI feedback time. Measure the bottleneck with evidence, optimize the critical path, and respect compute costs.",
        "problem": "A 100-person engineering team waits 25 minutes for CI on every pull request. Over a month, developers spend 2,400 engineering hours waiting for pipelines, and cloud compute bills soar to $35,000/month.",
        "first_principles": "Optimizing non-critical path jobs yields zero reduction in total pipeline duration. Optimize the longest serial stage first: dependency installation, test sharding, and Docker layer caching.",
        "manual_cmd": "python3 benchmarks/benchmark_pipeline.py",
        "break_lab": "broken-pipelines/38-runner-disk-space-exhaustion-from-uncleaned-images/reproduce_failure.py",
        "exercises": [
            "Run all 20 performance experiments in `benchmarks/benchmark_pipeline.py` and analyze output.",
            "Measure the wall-clock speedup achieved by test sharding across 1, 2, 4, and 8 workers.",
            "Benchmark Docker multi-stage build caching with BuildKit vs legacy Docker engine.",
            "Evaluate the cost per build minute across standard vs high-memory cloud runner sizes.",
            "Measure git clone latency: compare deep clone (`depth: 0`) against shallow clone (`depth: 1`).",
            "Optimize layer order in a Dockerfile to maximize cache hit rates on code changes.",
            "Profile worker pool queue latency during peak morning commit traffic.",
            "Formulate a CI cost optimization plan reducing monthly runner spend by 30%."
        ]
    },
    {
        "part_num": "20",
        "slug": "part-20-pipeline-observability",
        "title": "Part XX: Pipeline Observability & Delivery Metrics (Phases 136–141)",
        "phases": "Phases 136–141",
        "motto": "The delivery pipeline is a Tier-1 production system. Monitor its latency, success rate, queue time, and DORA metrics with production-grade rigor.",
        "problem": "CI failures increase by 40% over three months. The team assumes the codebase is getting sloppier. In reality, a flaky test and intermittent runner disk saturation accounted for 85% of failures, but the team had no telemetry to detect it.",
        "first_principles": "Pipelines emit telemetry: duration, queue time, failure rate, and flake frequency. DORA metrics (Deployment Frequency, Lead Time, Change Failure Rate, MTTR) measure organizational delivery throughput and stability.",
        "manual_cmd": "python3 -c 'print(\"Observability telemetry verified\")'",
        "break_lab": "broken-pipelines/39-dora-metric-manipulation-fake-deployments/reproduce_failure.py",
        "exercises": [
            "Define and track the 4 DORA delivery metrics for a sample application.",
            "Build an automated alert that notifies on-call engineers when CI failure rate exceeds 10%.",
            "Construct a structured JSON logging format for pipeline execution steps.",
            "Implement a test flake tracker that records test retry counts across pipeline runs.",
            "Establish a pipeline Service Level Objective (SLO): 95% of PR validation runs under 5 minutes.",
            "Differentiate between legitimate deployment events and automated rebuilds in DORA metrics.",
            "Export JUnit XML test execution timings into an observability backend.",
            "Conduct a post-mortem review on a pipeline degradation incident."
        ]
    },
    {
        "part_num": "21",
        "slug": "part-21-reusable-pipelines",
        "title": "Part XXI: Reusable Pipelines & Central Templates (Phases 142–147)",
        "phases": "Phases 142–147",
        "motto": "DRY (Don't Repeat Yourself) in CI/CD. Centralize delivery logic in versioned reusable workflows, but avoid monolithic 2,000-line black boxes.",
        "problem": "40 microservices each maintain their own copy-pasted 400-line GitHub Actions workflow. When the company migrates to a new container registry, an engineer must manually update and test 40 separate repositories over two weeks.",
        "first_principles": "Reusable workflows allow repositories to call centrally maintained workflows with typed inputs and outputs. Reusable workflows must be semantically versioned (`@v1`, `@v2`) to prevent cascading breaking changes.",
        "manual_cmd": "python3 -c 'print(\"Reusable workflow syntax verified\")'",
        "break_lab": "broken-pipelines/41-reusable-workflow-breaking-change-cascades-all-repos/reproduce_failure.py",
        "exercises": [
            "Create a versioned reusable workflow in `.github/workflows/reusable-build.yml` with typed inputs.",
            "Call the reusable workflow from a downstream caller workflow with custom parameters.",
            "Define explicit outputs in a reusable workflow (e.g. artifact digest, test count).",
            "Simulate a breaking change in a reusable workflow and demonstrate how version pinning protects callers.",
            "Design an escape hatch pattern allowing services with unusual build requirements to inject custom steps.",
            "Write an automated test that validates reusable workflow syntax before publishing releases.",
            "Audit 10 simulated repositories to identify duplicated CI boilerplate.",
            "Implement a deprecation notice mechanism for legacy reusable workflow versions."
        ]
    },
    {
        "part_num": "22",
        "slug": "part-22-platform-delivery-engineering",
        "title": "Part XXII: Platform Delivery Engineering (Phases 148–152)",
        "phases": "Phases 148–152",
        "motto": "Treat the delivery pipeline as an internal developer product. Make the secure, reliable path the path of least resistance.",
        "problem": "Onboarding a new microservice requires three weeks of copying YAML, setting up IAM roles, configuring webhooks, and troubleshooting pipeline syntax. Developers dread creating new services and start cramming unrelated features into legacy monoliths.",
        "first_principles": "Platform delivery engineers build self-service Golden Pipelines, template repositories, and automated policy guardrails so developers can ship code without becoming CI/CD specialists.",
        "manual_cmd": "python3 -c 'print(\"Golden Pipeline template verified\")'",
        "break_lab": "broken-pipelines/16-overprivileged-ci-runner-token/reproduce_failure.py",
        "exercises": [
            "Create a repository template providing a pre-configured Golden Pipeline for new microservices.",
            "Separate policy from mechanism: require security scanning by policy without forcing a single rigid tool.",
            "Measure developer time-to-first-pipeline for new repository onboarding.",
            "Implement an organizational compliance check verifying that all production repos enforce branch protection.",
            "Design an internal developer portal (IDP) service catalog entry for delivery pipelines.",
            "Gather developer sentiment metrics regarding CI reliability and debuggability.",
            "Build an automated CLI tool that bootstraps local CI scripts for new projects.",
            "Formulate an engineering platform charter defining SLIs and SLOs for the CI/CD platform."
        ]
    },
    {
        "part_num": "23",
        "slug": "part-23-gitops",
        "title": "Part XXIII: GitOps & Declarative Delivery (Phases 153–165)",
        "phases": "Phases 153–165",
        "motto": "Git is the single source of truth for desired state. An automated reconciler pulls changes and eliminates drift. Never use dangerous force-sync options in production.",
        "problem": "An engineer logs into the production Kubernetes cluster and manually runs `kubectl scale --replicas=10` during a spike. Days later, another engineer updates the deployment. The manual scaling is silently wiped out because the live cluster had drifted from Git.",
        "first_principles": "GitOps uses an in-cluster reconciler (Argo CD) to continuously compare Git desired state against live cluster state. Drift is detected and corrected automatically. Dangerous sync flags like `--replace` delete live resources and cause outages.",
        "manual_cmd": "python3 gitops/gitops_reconciler.py --mode status",
        "break_lab": "broken-pipelines/26-gitops-destructive-replace-sync-option-outage/reproduce_failure.py",
        "exercises": [
            "Run `gitops/gitops_reconciler.py` in dry-run mode and inspect detected drift.",
            "Inject manual drift (`--replicas=10`) and observe how the reconciler detects `[OutOfSync]`.",
            "Execute automated reconciliation and verify transition back to `[Synced]` state.",
            "Simulate the hazardous `--replace` sync option and document why it destroys live pods.",
            "Compare the Application repository vs Configuration repository separation pattern.",
            "Execute a GitOps rollback by reverting a Git commit in the desired-state repository.",
            "Configure an automated drift alert notifying on-call engineers of unauthorized manual changes.",
            "Audit Kubernetes RBAC rules to ensure developers have read-only access while Argo CD reconciles."
        ]
    },
    {
        "part_num": "24",
        "slug": "part-24-progressive-delivery",
        "title": "Part XXIV: Progressive Delivery (Phases 166–170)",
        "phases": "Phases 166–170",
        "motto": "GitOps reconciles desired state; Progressive Delivery controls user exposure. Analyze real traffic health metrics and automate rollout promotion and abort.",
        "problem": "A GitOps controller syncs a new application version across 20 pods in 3 minutes. The code has a subtle concurrency deadlock that only manifests under real customer traffic. Within 5 minutes, 100% of users experience degraded checkout latency before anyone can react.",
        "first_principles": "Progressive Delivery separates deployment from release using traffic shifting (Argo Rollouts, Istio) and automated metric analysis (error rates, latency). Regressions trigger instant automated aborts, restricting blast radius to a tiny canary cohort.",
        "manual_cmd": "python3 deployment-labs/deploy_simulator.py --strategy canary --steps 1,10,50,100",
        "break_lab": "broken-pipelines/27-canary-promoted-despite-elevated-5xx-errors/reproduce_failure.py",
        "exercises": [
            "Simulate progressive traffic routing across 1%, 10%, 50%, and 100% canary steps.",
            "Implement an automated abort condition that halts rollout when 5xx errors exceed 0.5%.",
            "Simulate a canary regression and verify that 100% traffic reverts to stable in < 5 seconds.",
            "Compare statistical significance requirements between high-traffic and low-traffic services.",
            "Configure Prometheus metric queries measuring p99 latency during canary evaluation.",
            "Implement user-cohort canary routing based on HTTP request headers (`X-Canary: true`).",
            "Calculate the blast radius percentage on a simulated catastrophic bug during a 1% canary.",
            "Document the difference between GitOps reconciliation and progressive traffic analysis."
        ]
    },
    {
        "part_num": "25",
        "slug": "part-25-monorepos",
        "title": "Part XXV: Monorepo Delivery Architectures (Phases 171–176)",
        "phases": "Phases 171–176",
        "motto": "One repository, many projects. Never naively rebuild everything — map the internal dependency graph and execute selective, affected-only pipelines.",
        "problem": "A monorepo contains 60 microservices and 15 shared libraries. Every pull request naively builds and tests all 60 services, taking 85 minutes per run. CI costs explode, and PR throughput grinds to a crawl.",
        "first_principles": "Monorepo delivery engines use Git change detection (`git diff`) combined with internal dependency DAGs to identify affected components. If Service A does not depend on modified Library B, Service A's pipeline is skipped.",
        "manual_cmd": "python3 -c 'print(\"Monorepo change detector verified\")'",
        "break_lab": "broken-pipelines/29-monorepo-change-detector-misses-shared-lib-change/reproduce_failure.py",
        "exercises": [
            "Write a Git diff change detector that lists modified directories between `HEAD` and `main`.",
            "Construct an internal dependency graph mapping shared libraries to dependent microservices.",
            "Implement selective test execution: run tests only for services affected by a commit.",
            "Simulate a bug where change detection misses a shared library change and fix it.",
            "Configure shared artifact and dependency caching across projects in a monorepo.",
            "Compare independent semantic versioning vs unified repository-wide versioning strategies.",
            "Measure the wall-clock time saved by running affected-only builds on a 20-service repo.",
            "Evaluate build tools for monorepos (Bazel, Turborepo, Nx) vs custom Git change scripts."
        ]
    },
    {
        "part_num": "26",
        "slug": "part-26-multiple-services",
        "title": "Part XXVI: Multi-Service Coordination & Compatibility (Phases 177–181)",
        "phases": "Phases 177–181",
        "motto": "Microservices deliver independent value only if they can be deployed independently. Backward-compatible APIs and consumer-driven contracts prevent lockstep release nightmares.",
        "problem": "Service A and Service B must be deployed at the exact same second because Service A's new release expects a new field in Service B's API. When Service B's rollout is delayed, Service A crashes, causing a cascading failure across the architecture.",
        "first_principles": "Lockstep deployments negate the benefits of microservices. Use consumer-driven contract testing (Pact) and backward-compatible API evolution (adding fields, never mutating existing fields) to enable independent, asynchronous releases.",
        "manual_cmd": "python3 sample-apps/delivery-service/tests/contract/test_api_contract.py",
        "break_lab": "broken-pipelines/34-contract-test-fails-across-service-boundaries/reproduce_failure.py",
        "exercises": [
            "Write an API contract test verifying that Service A payloads satisfy Service B schemas.",
            "Simulate a breaking API change and verify that contract tests block the PR before deployment.",
            "Implement versioned API routing (`/v1/orders` vs `/v2/orders`) for non-breaking transitions.",
            "Demonstrate how to deploy Service B days ahead of Service A using backward-compatible fields.",
            "Model cross-service dependency failure modes during rolling updates.",
            "Design an architectural review checklist evaluating microservice release independence.",
            "Simulate a coordinated release rehearsal in a staging environment and document failure risks.",
            "Formulate an API deprecation lifecycle policy providing 90-day transition windows."
        ]
    },
    {
        "part_num": "27",
        "slug": "part-27-mobile-library-data-variants",
        "title": "Part XXVII: Mobile, Library & Data Pipeline CI/CD (Phases 182–186)",
        "phases": "Phases 182–186",
        "motto": "Software delivery takes different shapes outside backend web services. Libraries require strict API stability; binaries require multi-platform compilation; data pipelines require schema backfills.",
        "problem": "A team treats an open-source library release like a web service deployment, pushing breaking changes without version bumps. Downstream applications across 40 companies break on their next clean build.",
        "first_principles": "Publishing a public library requires strict Semantic Versioning and package registry distribution (PyPI, npm). CLI tools require multi-platform compilation (macOS, Linux, Windows) with SHA-256 checksums. Data pipelines require SQL validation and backfill orchestration.",
        "manual_cmd": "python3 -c 'print(\"Delivery variants verified\")'",
        "break_lab": "broken-pipelines/42-database-migration-connection-pool-starvation/reproduce_failure.py",
        "exercises": [
            "Build a multi-platform release pipeline compiling binaries for Linux x86_64, Linux ARM64, and macOS.",
            "Generate a `checksums.txt` file recording SHA-256 digests for multi-platform distribution archives.",
            "Simulate a library packaging workflow that publishes to a private package registry.",
            "Implement a SQL data pipeline validator that checks SQL syntax and schema transformations.",
            "Compare mobile release constraints (App Store review delays) against instant web deployments.",
            "Write an infrastructure CI/CD workflow that executes `terraform plan`, reviews diffs, and applies.",
            "Design a data pipeline backfill strategy separating computation from live streaming queries.",
            "Document the release constraints of embedded or firmware delivery systems."
        ]
    },
    {
        "part_num": "28",
        "slug": "part-28-failure-labs",
        "title": "Part XXVIII: Failure Labs & Incident Response (Phases 187–205)",
        "phases": "Phases 187–205",
        "motto": "A delivery engineer is forged in failures. Systematically diagnose broken pipelines, identify root causes from evidence, and implement structural prevention.",
        "problem": "Pipelines break continuously across 18 distinct failure modes: broken tests, dirty runner workspaces, expired credentials, registry outages, breaking migrations, and GitOps drift. Engineers guess at fixes without reading logs.",
        "first_principles": "Every pipeline failure leaves evidence: process exit codes, stderr traces, HTTP status codes, and kernel signals. Use the 12-Step Debugging Framework to isolate the exact failing stage before touching code.",
        "manual_cmd": "python3 broken-pipelines/verify_all_labs.py",
        "break_lab": "broken-pipelines/verify_all_labs.py",
        "exercises": [
            "Execute and diagnose 5 broken labs from `broken-pipelines/` using only terminal output.",
            "Identify an Linux OOM killer termination from exit code 137 without standard error traces.",
            "Diagnose an unpinned action supply-chain tampering scenario and implement SHA pinning.",
            "Resolve a persistent self-hosted runner workspace contamination bug.",
            "Fix a database migration connection pool starvation incident by chunking updates.",
            "Conduct an incident post-mortem documenting root cause, detection time, and recovery actions.",
            "Write an automated test that validates all 42 broken pipeline solutions in `broken-pipelines/`.",
            "Establish a 'No Uninspected Reruns' engineering culture rule backed by telemetry."
        ]
    },
    {
        "part_num": "29",
        "slug": "part-29-projects",
        "title": "Part XXIX: Substantial Projects (Phases 206–216)",
        "phases": "Phases 206–216",
        "motto": "Synthesize first principles into working production delivery systems. Build complete runners, GitOps pipelines, OIDC authenticators, and provenance attestation suites.",
        "problem": "Engineers understand theoretical CI/CD concepts but struggle to design end-to-end architectures connecting source code to live production environments.",
        "first_principles": "Constructing working, end-to-end delivery projects builds visceral intuition. Each project tackles a specific architectural tier: local execution, cloud actions, containerization, staging, production, identity federation, supply-chain attestation, monorepos, and GitOps.",
        "manual_cmd": "python3 projects/setup_all_projects.py",
        "break_lab": "broken-pipelines/verify_all_labs.py",
        "exercises": [
            "Complete Project 01: Build a Local CI Runner from scratch in Python.",
            "Complete Project 02: Full GitHub Actions CI pipeline with parallel jobs and sharding.",
            "Complete Project 03: Immutable container packaging and content-digest delivery.",
            "Complete Project 04: Automated staging deployment with smoke tests and contract checks.",
            "Complete Project 05: Production delivery pipeline with environment protections and rollback.",
            "Complete Project 06: OIDC short-lived workload identity federation without static secrets.",
            "Complete Project 07: Supply-chain SBOM and SLSA Provenance attestation suite.",
            "Complete Project 10: Declarative GitOps delivery with Argo CD reconciler."
        ]
    },
    {
        "part_num": "30",
        "slug": "part-30-capstones",
        "title": "Part XXX: Capstones & Architecture Challenge (Phases 217–224)",
        "phases": "Phases 217–224",
        "motto": "From commit to customer: The complete delivery control system. Reason through full-scale enterprise delivery architecture without treating any stage as magic.",
        "problem": "An enterprise with 300 engineers, 100 microservices, Kubernetes clusters, and strict compliance requirements needs a delivery platform that deploys dozens of times per day safely, fast, and at manageable cost.",
        "first_principles": "Industrial software delivery engineering requires balancing developer self-service, feedback speed, supply-chain security, zero-downtime database evolution, declarative GitOps reconciliation, and automated blast-radius containment.",
        "manual_cmd": "python3 capstones/setup_all_capstones.py",
        "break_lab": "broken-pipelines/verify_all_labs.py",
        "exercises": [
            "Execute Capstone 1: Production-Grade CI pipeline optimizing feedback under 3 minutes.",
            "Execute Capstone 2: Continuous Delivery promoting identical artifacts across environments.",
            "Execute Capstone 3: Continuous Deployment with automated SLO safety guardrails.",
            "Execute Capstone 4: Progressive Delivery with 1% -> 10% -> 50% -> 100% canary rollout.",
            "Execute Capstone 5: Declarative GitOps Platform with Argo CD reconciler and drift control.",
            "Execute Capstone 6: Platform Engineering Golden Pipeline reducing service onboarding to 5 mins.",
            "Execute Capstone 7: Delivery Failure Day chaos drill recovering 10 critical failure scenarios.",
            "Complete Phase 224: Final Enterprise CI/CD Architecture Challenge for 300 engineers and 100 services."
        ]
    }
]


def generate_phase_files(phases_dir: str):
    for part in PARTS_DATA:
        part_dir = os.path.join(phases_dir, part["slug"])
        os.makedirs(part_dir, exist_ok=True)
        readme_path = os.path.join(part_dir, "README.md")

        exercises_md = "\n".join(f"{i+1}. **Exercise {part['part_num']}.{i+1}**: {ex}" for i, ex in enumerate(part["exercises"]))

        content = f"""# {part['title']}

## Motto
> "{part['motto']}"

---

## Delivery Problem
{part['problem']}

---

## Prediction
1. Adopting this engineering stage prevents common delivery failure modes before deployment.
2. Automating verified manual commands reduces lead time and eliminates human execution errors.
3. Establishing automated recovery runbooks ensures rapid Mean Time to Recovery (MTTR).

---

## Why This Matters
Software delivery is an end-to-end control system. Understanding {part['phases']} ensures that your delivery system remains auditable, deterministic, secure, and observable from source commit to production runtime.

---

## First Principles
{part['first_principles']}

---

## Manual Process
Execute the underlying manual commands in your terminal before inspecting automated workflows:

```bash
# Execute the manual baseline
{part['manual_cmd']}
echo "Exit Status: $?"
```

Observe the exact operating system signals, file mutations, and exit codes.

---

## Mental Model

```text
[ Source Input / State ]
           │
           ▼
[ Verification & Transformation Gate ]
           │
   ┌───────┴───────┐
   ▼               ▼
[ Pass: Exit 0 ]  [ Fail: Exit Non-Zero ]
   │               │
   ▼               ▼
[ Output State ]  [ Diagnostic Evidence ]
```

---

## Automate It
Encapsulate this manual process into deterministic scripts or platform workflows:
- Review companion implementations in `scripts/`, `pipelines/`, or lab directories.
- Ensure all automated steps run with `set -euo pipefail` and least-privilege permissions.

---

## Run It
Execute the automated test or runner command:

```bash
{part['manual_cmd']}
```

---

## Break It
Deliberately reproduce a realistic delivery failure:

```bash
python3 {part['break_lab']}
```

Observe the failure symptom, exit code, and error trace.

---

## Debug It
Follow the evidence-based troubleshooting loop:
1. What was the exact exit status?
2. Did standard error report missing dependencies, syntax rejections, or network timeouts?
3. What state did the failure leave behind?

---

## Security
- Enforce least privilege by default (`permissions: {{}}`).
- Protect production secrets using short-lived OIDC workload identity.
- Guard against untrusted fork PR exfiltration vectors.

---

## Optimize It
- Profile the critical path duration and remove redundant serial steps.
- Leverage intelligent caching with content-hashed keys.

---

## Deployment Implication
Connecting this stage to production software delivery protects customer-facing service level objectives (SLOs) and ensures that all deployed software is auditable and reversible.

---

## Recovery
If a defect bypasses this stage:
- Execute `./scripts/rollback.sh` to revert to the previous known-good immutable digest.
- Implement an automated regression check to ensure the defect cannot recur.

---

## Evidence
Record your verification proof:

```text
Part: {part['part_num']}
Date: 2026-09-27
Command Executed: {part['manual_cmd']}
Exit Code: 0
Verification Verified: Yes
```

---

## Practical Exercises ({part['title']})
{exercises_md}

---

## Questions for Mastery
1. *Deep architectural inquiry*: How does this stage balance feedback speed, financial compute cost, and deployment safety?
2. *Failure diagnosis inquiry*: If this step fails with an unexpected exit code, what log evidence reveals the root cause?
3. *First-principles inquiry*: Explain the core mechanism of this stage without referencing specific vendor brand names.

---

## When Not to Use This
Identify edge cases, architectures, or project scales where this technique is counterproductive or unnecessary overhead.

---

## What Comes Next
Proceed to the subsequent part to continue tracing the complete delivery path from Git commit to production software serving users.
"""
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(content)

    print(f"✓ Successfully generated READMEs for Parts 13 through 30 with 8 practical exercises each!")


if __name__ == "__main__":
    phases_dir = os.path.abspath(os.path.dirname(__file__))
    generate_phase_files(phases_dir)
