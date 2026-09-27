# Pipeline Specification: [Pipeline Name]

> "A pipeline is a deterministic state machine that transforms source changes into verified, immutable software artifacts. It must have explicit boundaries, minimal privileges, and predictable failure behavior."

---

## Trigger
- **Event Types**: `push`, `pull_request`, `workflow_dispatch`, `schedule`, `release`
- **Branch / Tag Filters**: Specify exact branch patterns (e.g., `main`, `release/v*`)
- **Path Filters**: Specify path inclusions or exclusions (e.g., ignore docs updates for binary builds)
- **Concurrency Group**: Policy for cancelling superseded runs (e.g., `concurrency: group-${{ github.ref }}, cancel-in-progress: true`)

---

## Source Revision
- **Target Git SHA**: Exact 40-character commit hash checked out
- **Merge Commit vs Head Commit**: Explicitly state whether the pipeline runs against the head of the PR branch or the simulated GitHub merge commit (`refs/pull/:id/merge`)
- **Checkout Depth**: Shallow clone (`depth: 1`) or full history (`depth: 0` for changelog/tag calculation)

---

## Inputs
- **Environment Variables**: Required global and job-level environment variables
- **Workflow Dispatch Inputs**: Any interactive parameters (e.g., target environment, deployment percentage, debug flag)
- **Default Values**: Safe fallback defaults for all inputs

---

## Jobs
List all jobs defined in this pipeline:
1. `job-name-1`: Description of role (e.g., static linting & formatting)
2. `job-name-2`: Description of role (e.g., unit test sharding)
3. `job-name-3`: Description of role (e.g., container image build & sign)

---

## Job Dependencies
Define the execution Directed Acyclic Graph (DAG):
- Which jobs run concurrently at start?
- Which jobs depend on upstream job completion (`needs: [job-a, job-b]`)?
- What is the critical path from trigger to completion?

```text
       ┌──────────┐      ┌──────────┐
       │   lint   │      │ unit-test│
       └────┬─────┘      └─────┬────┘
            │                  │
            └────────┬─────────┘
                     ▼
             ┌───────────────┐
             │ build-artifact│
             └───────────────┘
```

---

## Commands
List the executable commands run by each step. Ensure that core logic calls standalone scripts (`./scripts/build.sh`) rather than embedding 50 lines of complex inline bash directly in YAML.

---

## Tests
- **Unit Test Execution**: Test framework, sharding parameters, timeout per shard
- **Integration Test Execution**: Dependency containers required, health probe wait logic
- **Test Reporting**: Path to JUnit XML results or test report artifacts

---

## Artifact
- **Type**: Container image, tarball, wheel, binary
- **Immutability Identifier**: SHA-256 digest or immutable tag
- **Storage Location**: Container registry (GHCR, ECR, DockerHub) or CI workflow artifact storage
- **Retention Period**: Days retained before automated garbage collection

---

## Cache
- **Cache Key Design**: Detailed hash composition (e.g., `os-runner-python-v1-${{ hashFiles('requirements.lock') }}`)
- **Restore Keys**: Fallback prefix keys for partial cache hits
- **Cache Scope & Invalidation**: How changes to dependencies bust the cache without manual intervention

---

## Credentials
- **Identity Mechanism**: GitHub Actions OIDC (Workload Identity Federation) vs encrypted repository secrets
- **Cloud Provider Audience**: `sts.amazonaws.com`, `accounts.google.com`, etc.
- **Short-Lived Token Duration**: Maximum session validity (e.g., 15 minutes)

---

## Permissions
- **Default Level**: Top-level `permissions: {}` (read-nothing / least-privilege default)
- **Job-Level Explicit Grants**:
  - `contents: read`
  - `id-token: write` (for OIDC exchange)
  - `packages: write` (for container publishing)
  - `pull-requests: read`

---

## Outputs
- **Exported Values**: Output variables passed downstream (e.g., `image_digest`, `release_tag`, `test_coverage_ratio`)
- **Published Artifact Locations**: URLs or registry endpoints for generated software

---

## Failure Behavior
- **Fail-Fast**: State whether `strategy.fail-fast` is enabled or disabled
- **Partial Failure Handling**: If a test shard fails, does the pipeline immediately cancel other shards or allow them to collect diagnostic evidence?
- **Notification Hooks**: Alert channels (Slack, PagerDuty, email) triggered on failure

---

## Retry Behavior
- **Automated Retries**: Are test retries permitted? (Rule: Never retry blindly to mask flakiness; only retry for proven network transport failures)
- **Max Retry Count**: Maximum attempts per network/transient step (e.g., 2 attempts with exponential backoff)

---

## Timeout
- **Job Timeout**: Hard cap per job (e.g., `timeout-minutes: 15`)
- **Step Timeout**: Per-step timeout for network-bound operations (e.g., `timeout: 120s`)

---

## Observability
- **Structured Log Format**: Plain text vs JSON log outputs
- **Diagnostic Artifacts**: Uploaded crash dumps, memory profiles, failed request traces
- **Pipeline Metrics**: Duration, queue time, worker resource utilization

---

## Expected Duration
- **Target Feedback Time**: Desired wall-clock time for PR validation (e.g., < 5 minutes)
- **Max Acceptable Duration**: Threshold above which pipeline is considered degraded
- **Bottleneck Analysis**: Identification of the longest running serial step

---

## Security Boundaries
- **Untrusted Code Execution**: Are pull requests from forks prevented from accessing secrets?
- **Third-Party Actions**: Are all actions pinned to full-length commit SHAs?
- **Network Egress Controls**: Does the runner have unrestricted internet access or firewall egress filtering?
