# Pipeline and Software Supply-Chain Security Framework

> "A CI/CD runner is an execution engine that has network access, credentials, and the authority to deploy production software. Treating your delivery system as a secondary concern makes it the primary attack vector."

---

## 1. Threat Model for CI/CD Systems

Modern software supply-chain attacks rarely target production firewalls directly. Instead, attackers target the automated pipeline that has pre-authorized write access to production clusters and artifact registries.

```text
Attacker Vector              Delivery Pipeline Stage               Impact
────────────────────────────────────────────────────────────────────────────────────────
Malicious Pull Request   ──► Ephemeral CI Runner           ──► Secret Exfiltration (Env Dump)
Dependency Confusion    ──► Package Manager Resolution    ──► Malicious Code in Build Artifact
Compromised Action      ──► Hosted Workflow Step          ──► Tampered Artifact / Backdoor
Stale CI Secret Keys    ──► Permanent Cloud IAM Role      ──► Infrastructure Takeover
Untracked Build Inputs  ──► OCI Container Registry        ──► Untraceable Production Malware
```

---

## 2. Core Security Pillars

### Pillar 1: Least Privilege by Default
Pipelines must operate under the principle of minimal necessary access.
- Every workflow must explicitly define top-level permissions as empty:
  ```yaml
  permissions: {}
  ```
- Individual jobs must only request the specific scopes required for their tasks (e.g., `contents: read` for linting; `packages: write` for registry publishing; `id-token: write` for OIDC authentication).
- Build and test jobs must **never** possess credentials capable of mutating production infrastructure.

### Pillar 2: Short-Lived Identity (OIDC) vs Permanent Secrets
Static cloud credentials (e.g., AWS Access Key IDs, permanent GCP Service Account JSON keys) stored in CI secrets create massive operational liabilities:
- They never expire automatically.
- They are vulnerable to accidental printing in verbose build logs.
- They require continuous manual rotation.

**Mandatory Approach**: OpenID Connect (OIDC) Workload Identity Federation.
1. The CI runner generates a cryptographically signed JSON Web Token (JWT) identifying the exact workflow run, repository, branch, and commit.
2. The runner presents this token to the cloud provider's Security Token Service (STS).
3. The cloud provider validates the signature against GitHub's public OIDC keys (`https://token.actions.githubusercontent.com`).
4. If the claims (e.g., `repository: org/repo`, `ref: refs/heads/main`) match the trust policy, the cloud provider issues a temporary credential valid for only 15–60 minutes.

### Pillar 3: Fork and Pull Request Trust Boundaries
Public and internal forks present a severe security boundary:
- **`pull_request` event**: Runs in the context of the fork. Does **not** have access to repository secrets or write permissions.
- **`pull_request_target` event**: Runs in the context of the base repository and has access to secrets! **WARNING**: Running untrusted code (such as checking out the PR head) inside `pull_request_target` allows any external contributor to exfiltrate production secrets or deploy malicious code.
- Rule: Never checkout untrusted fork code in a workflow that holds access to credentials or write permissions.

### Pillar 4: Third-Party Action Pinning and Supply-Chain Integrity
Using floating tags like `uses: actions/checkout@v4` trusts the tag maintainer not to push malicious code to that tag.
- In security-sensitive and production release pipelines, pin actions to their full 40-character commit SHA:
  ```yaml
  uses: actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332 # v4.1.7
  ```
- Use automated dependency update tools (such as Dependabot or Renovate) to keep SHA-pinned actions updated with automated change notes.

### Pillar 5: Software Bill of Materials (SBOM) & Attestations
Every release artifact must be accompanied by:
1. **SBOM**: A complete inventory of direct and transitive libraries, licenses, and hashes (generated via Syft in CycloneDX or SPDX format).
2. **Provenance Attestation**: A verifiable statement (SLSA Level 2/3) signed via Sigstore Cosign proving that the artifact was built by an authorized runner from an exact Git commit SHA.

---

## 3. Secret Exfiltration Defense Checklist

To protect pipelines against malicious tests or dependencies that attempt to steal credentials:
- [ ] Never echo secrets or write unmasked tokens to disk.
- [ ] Do not pass production credentials into test execution environments.
- [ ] Implement runner network egress filtering to prevent data exfiltration to unrecognized IP addresses.
- [ ] Sanitize environment variables before invoking third-party build tools.
- [ ] Run automated secret scanners (Trivy, Gitleaks) on every commit to block accidental credential leaks.

---

## 4. Reporting Security Vulnerabilities

If you identify a security flaw or vulnerability within this educational repository, please report it via private security advisory on GitHub or email `security@binarydevelop.internal`. Do not file public GitHub issues for security vulnerabilities.
