# Part XII: Software Supply Chain (Phases 84–91)

## Motto
> "A software artifact cannot be trusted merely because it sits in your private registry. You must be able to prove cryptographically what source produced it, what dependencies went into it, and which runner built it."

---

## Delivery Problem
A critical zero-day vulnerability (similar to Log4Shell or SolarWinds) is announced in a popular utility library. The CTO asks: *"Which of our 100 running production services contain this vulnerable package?"*

Because the team does not generate Software Bills of Materials (SBOMs) or provenance records during builds, the answer requires two weeks of manual codebase inspections, manual container layer extractions, and guesswork. In the meantime, unpatched services remain exposed.

---

## Prediction
1. An attacker can tamper with artifacts in transit or compromise package registries if cryptographic signatures and checksums are omitted.
2. Generating machine-readable SBOMs at build time enables instantaneous vulnerability querying across the entire fleet.
3. SLSA Build Provenance proves that an artifact was built by an authorized CI system from an exact Git commit SHA.

---

## First Principles
1. **The Software Supply Chain Flow**:
   Every stage of the delivery pipeline introduces supply-chain trust dependencies:
   ```text
   Source ──► Dependencies ──► Build Runner ──► Artifact ──► Registry ──► Production
   ```
   A vulnerability or malicious injection at any single link compromises all downstream consumers.
2. **Software Bill of Materials (SBOM)**:
   A formal, structured inventory (in CycloneDX or SPDX format) identifying all direct and transitive libraries, versions, purls (package URLs), and cryptographic hashes included in a packaged application.
3. **SLSA (Supply-chain Levels for Software Artifacts)**:
   - **SLSA Level 1**: Build process is automated and generates provenance.
   - **SLSA Level 2**: Provenance is authenticated and generated on a hosted build platform.
   - **SLSA Level 3**: Build platform isolates jobs, prevents tampering, and signs provenance cryptographically using ephemeral keys (Sigstore/Cosign).

---

## Manual Process (Phases 85, 86, 87)
Generate and verify SBOM and SLSA Provenance manually:

```bash
# 1. Generate CycloneDX SBOM
python3 security-labs/sbom_provenance_generator.py \
    --mode sbom \
    --artifact outputs/release-v1.0.0/delivery-service-1.0.0.tar.gz \
    --output outputs/release-v1.0.0/sbom.json

# 2. Generate SLSA Provenance Attestation
python3 security-labs/sbom_provenance_generator.py \
    --mode provenance \
    --artifact outputs/release-v1.0.0/delivery-service-1.0.0.tar.gz \
    --output outputs/release-v1.0.0/provenance.json

# 3. Cryptographically Verify Provenance
python3 security-labs/sbom_provenance_generator.py \
    --mode verify \
    --artifact outputs/release-v1.0.0/delivery-service-1.0.0.tar.gz \
    --provenance outputs/release-v1.0.0/provenance.json
```

---

## Mental Model

```text
[ Source Git Commit SHA ]
          │
          ▼
   [ Build Runner ] ──► Compiles Binary (Digest: sha256:7041b28e...)
          │
          ├────────────────────────┬────────────────────────┐
          ▼                        ▼                        ▼
 [ Immutable Artifact ]   [ CycloneDX SBOM ]     [ SLSA Attestation ]
 (Container / Tarball)    (Full Component List)  (Signed Build Lineage)
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   │
                                   ▼
          [ Production Admission Controller (Kyverno / Gatekeeper) ]
          - Validates Cosign signature
          - Rejects unsigned or unverified images
```

---

## Automate It (Phase 88: GitHub Actions Artifact Attestation)

```yaml
# .github/workflows/release.yml
- name: Attest Build Provenance (SLSA v1.0)
  uses: actions/attest-build-provenance@v1.3.2
  with:
    subject-path: 'outputs/delivery-service-${{ steps.release_info.outputs.version }}.tar.gz'
```

---

## Run It
Run `security-labs/sbom_provenance_generator.py` to inspect the generated CycloneDX SBOM:

```bash
python3 security-labs/sbom_provenance_generator.py \
    --mode sbom \
    --artifact outputs/delivery-service-1.0.0.tar.gz \
    --output /tmp/test-sbom.json
cat /tmp/test-sbom.json
```

---

## Break It (Phase 85: Artifact Tampering)
1. Tamper with a packaged artifact:
   ```bash
   echo "tampered-content" >> outputs/release-v1.0.0/delivery-service-1.0.0.tar.gz
   ```
2. Re-run provenance verification:
   ```bash
   python3 security-labs/sbom_provenance_generator.py \
       --mode verify \
       --artifact outputs/release-v1.0.0/delivery-service-1.0.0.tar.gz \
       --provenance outputs/release-v1.0.0/provenance.json
   ```
3. Observe how verification immediately detects the hash mismatch and halts execution!

---

## Debug It
When attestation verification fails:
- Check whether the artifact was modified or re-packaged after provenance generation.
- Ensure the runner certificate identity matches the expected workflow and repository URL.

---

## Security
- Use **Sigstore Cosign** keyless signing: instead of storing private signing keys on the runner, Cosign leverages the runner's ephemeral OIDC token to issue a short-lived signing certificate logged into the Rekor transparency ledger.

---

## Optimize It
- Generate SBOMs directly from final runtime container layers to avoid including build-time-only compilation tools in the inventory.

---

## Deployment Implication
Deploying an admission controller (such as Kyverno or Gatekeeper) in Kubernetes blocks un-attested or tampered container images from ever running in production.

---

## Recovery
If a supply-chain vulnerability is detected in a running service:
1. Query your central SBOM database for all services depending on the vulnerable package.
2. Update the lockfile, rebuild with fresh provenance, and execute canary rollout.

---

## Practical Exercises (Part XII)
1. **Exercise 12.1**: Parse a CycloneDX 1.5 JSON SBOM in Python and list all component names and versions.
2. **Exercise 12.2**: Simulate artifact tampering by appending a comment to an archive and observe the SHA-256 mismatch.
3. **Exercise 12.3**: Generate an in-toto v1.0 Statement linking an artifact digest to a Git commit SHA.
4. **Exercise 12.4**: Write a policy script that verifies whether an artifact was built on GitHub Actions vs an unauthorized workstation.
5. **Exercise 12.5**: Pin all dependencies in a sample requirements file with exact SHA-256 hashes (`--require-hashes`).
6. **Exercise 12.6**: Inspect an OCI image attestation layer using `cosign download attestation`.
7. **Exercise 12.7**: Compare SLSA Level 1 vs Level 2 vs Level 3 requirements for build isolation and non-falsifiability.
8. **Exercise 12.8**: Write an admission webhook simulation that rejects Kubernetes Pods whose container image lacks a valid signature.

---

## Questions for Mastery
1. *Why is having an SBOM generated from source files less reliable than generating it from the final built container image?*
2. *How does Sigstore Cosign's keyless signing model eliminate the operational headache of private key management?*
3. *What is the difference between verifying an artifact's checksum and verifying its build provenance?*

---

## What Comes Next
In **Part XIII (Phases 92–96)**, we explore Continuous Delivery: delivery pipelines, manual vs automated deployment, post-deployment verification, smoke tests, and deployment audit records.
