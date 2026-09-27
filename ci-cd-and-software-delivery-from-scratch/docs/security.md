# Pipeline Security & Software Supply-Chain Architecture

> "Treating CI/CD security as an afterthought turns your most trusted automation system into your primary attack vector."

---

## 1. Threat Modeling the Delivery Pipeline

A typical software delivery pipeline possesses high-value privileges:
- It can read proprietary source code.
- It holds tokens to publish packages and container images.
- It possesses credentials to deploy software into production clusters.

Attackers target the pipeline because compromising the build system allows them to inject malicious code into trusted downstream artifacts that pass through firewalls and reach end users.

```text
Threat 1: Untrusted PR ──► Attacker submits code that dumps CI environment variables.
Threat 2: Dependency ──► Malicious post-install script in npm/pip package exfiltrates AWS keys.
Threat 3: Workflow Action ──► Compromised third-party action steals repository write token.
Threat 4: Image Tampering ──► Untracked container pushed to registry without signature or SBOM.
```

---

## 2. Workload Identity Federation (OIDC) vs Permanent Secrets

### The Vulnerability of Static Secrets
Storing long-lived cloud credentials (such as `AWS_SECRET_ACCESS_KEY` or `GCP_SA_KEY`) in repository secrets introduces multiple failure modes:
1. **Never Expire**: If printed to a verbose log or stolen via a malicious dependency, the token remains valid indefinitely until manually rotated.
2. **Broad Scope**: Teams often configure one central IAM credential with excessive privileges shared across 50 workflows.
3. **No Dynamic Provenance**: The cloud audit log only shows "CI-User executed an action," with zero cryptographic proof of which workflow run, branch, or commit initiated it.

### The OIDC Solution Architecture
With OpenID Connect (OIDC), the CI platform acts as an identity provider:

```text
1. Runner requests JWT from GitHub Token Service.
2. GitHub generates signed JWT with verified claims:
   - repository: "binarydevelop/ci-cd-and-software-delivery-from-scratch"
   - ref: "refs/heads/main"
   - workflow: "deploy.yml"
3. Runner passes JWT to Cloud Security Token Service (STS) (AssumeRoleWithWebIdentity).
4. Cloud verifies signature against GitHub's public OIDC keys (JWKS).
5. Cloud checks IAM Trust Policy (e.g., must match repository AND branch).
6. Cloud issues temporary STS credentials (TTL: 15 minutes).
```

Zero static cloud credentials exist in the repository settings. If a runner VM is compromised after job completion, the temporary session is already expired.

---

## 3. Fork and Pull Request Security Boundaries

### The Danger of `pull_request_target`
GitHub Actions provides two primary triggers for pull requests:
1. **`on: pull_request`**: Runs in the security context of the **fork** (untrusted). It has read-only permissions and **no access to repository secrets**. This is safe for running linters and unit tests.
2. **`on: pull_request_target`**: Runs in the security context of the **base repository** (trusted). It has access to repository secrets and write permissions.

**The Fatal Vulnerability**: If a workflow triggers on `pull_request_target` and executes:
```yaml
- uses: actions/checkout@v4
  with:
    ref: ${{ github.event.pull_request.head.sha }} # DANGEROUS!
- run: pytest
```
An attacker on the internet can open a PR that adds malicious code to `test_something.py`. Because the workflow runs under `pull_request_target`, the attacker's code executes with access to all repository production secrets!

**Mandatory Rule**: Never checkout or execute untrusted PR code in a workflow that holds access to secrets or write permissions.

---

## 4. Software Supply-Chain Verification: SBOM & SLSA

To achieve verifiable supply-chain integrity:
1. **Software Bill of Materials (SBOM)**: Generate a machine-readable CycloneDX or SPDX manifest during the build phase recording all direct and transitive libraries, versions, and cryptographic hashes.
2. **SLSA Provenance Attestation**: Produce an in-toto attestation statement recording the exact source commit SHA, builder identity, and input dependencies.
3. **Cryptographic Signing (Sigstore / Cosign)**: Sign the container image digest and attestation using keyless OIDC identity. Production clusters verify the signature via policy engines (Kyverno, Gatekeeper) before allowing pod scheduling.
