# Part VII: Artifacts (Phases 49–54)

## Motto
> "Build once, promote many. Never rebuild an artifact for a different environment — change only the configuration."

---

## Delivery Problem
An engineering organization has three branches: `development`, `staging`, and `production`. When code merges into `staging`, a CI job builds `myapp:staging`. When testing passes and code merges to `production`, a separate CI job rebuilds `myapp:production`.

One Friday, an upstream library publishes a minor bug fix between the staging build and the production build. Staging was tested and verified, but the production build pulled the new library which introduced a breaking memory leak. The production site crashed within 20 minutes!

---

## Prediction
1. Rebuilding artifacts per environment breaks the guarantee that what you tested in staging is what runs in production.
2. An artifact must have an immutable identity based on cryptographic content digests.
3. Workflow diagnostic artifacts (logs, test reports) require different retention policies than production release artifacts.

---

## First Principles
1. **The Build Once Principle**:
   Source code is built and packaged exactly **once** per Git commit. That identical, immutable binary/container artifact is then promoted sequentially through testing, staging, and production.
   ```text
   Source SHA ──► Build Artifact (Digest X) ──► Staging ──► Production
   ```
2. **Configuration Injected Outside the Artifact (Twelve-Factor App)**:
   Database URLs, API credentials, and environment flags must never be baked into the artifact. They must be injected at runtime via environment variables or secret mounts.
3. **Artifact Identity Metadata**:
   Every release artifact must be accompanied by metadata:
   - Source Git commit SHA (40-char)
   - Build timestamp (ISO 8601 UTC)
   - Cryptographic SHA-256 digest
   - Builder identity (Runner ID / CI run number)

---

## Manual Process
Package an artifact and verify its metadata:

```bash
# 1. Package the artifact
bash scripts/package.sh

# 2. Inspect the immutable artifact identity
cat outputs/artifact-metadata.json
cat outputs/delivery-service-1.0.0.tar.gz.sha256
```

---

## Mental Model

```text
[ Git Commit SHA: c477286... ]
              │
              ▼ Build ONCE
[ Immutable Artifact: delivery-service-1.0.0.tar.gz ]
[ Digest: sha256:7041b28e...                       ]
              │
      ┌───────┴───────┐
      ▼               ▼
[ Deploy Staging ]  [ Promote Production ]
(Config: DB_STG)    (Config: DB_PROD)
```

---

## Automate It (Phase 54: Workflow vs Registry Artifacts)

```yaml
# Step 1: Upload temporary workflow diagnostic artifact (7 days retention)
- uses: actions/upload-artifact@v4.3.4
  with:
    name: test-results
    path: outputs/test-results/
    retention-days: 7

# Step 2: Publish production release artifact to registry
- name: Push Container to OCI Registry
  run: |
    docker push ghcr.io/org/delivery-service@sha256:7041b28e...
```

---

## Run It
Execute `scripts/package.sh` to package the build output and generate the SHA-256 digest:

```bash
bash scripts/package.sh
```

---

## Break It (Phase 51: Digest Mismatch)
1. Run broken lab `11-missing-artifact-checksum-verification`:
   ```bash
   python3 broken-pipelines/11-missing-artifact-checksum-verification/reproduce_failure.py
   ```
2. Observe how deploying an artifact without verifying its cryptographic digest allows truncated or corrupted files to enter production.

---

## Debug It
When an artifact deployment fails:
- Check whether the digest recorded in the release manifest matches `shasum -a 256 <artifact>`.
- Check if the artifact was overwritten in the registry (mutable tag anti-pattern).

---

## Security
- Store release artifacts in registries with immutable tag policies enabled.
- Verify checksums before unpacking or deploying any third-party or internal binary.

---

## Optimize It
- Separate intermediate diagnostic artifacts (JUnit XML, coverage reports, core dumps) with 7-day retention from release artifacts with long-term retention.

---

## Deployment Implication
Promoting identical artifacts eliminates the "it worked in staging but failed in production" class of bugs caused by environment-specific compilation drift.

---

## Recovery
If a bad release is deployed:
- Locate the previous known-good artifact digest in `outputs/artifact-metadata.json`.
- Execute `./scripts/rollback.sh` to switch production traffic back to the prior digest.

---

## Practical Exercises (Part VII)
1. **Exercise 7.1**: Write a script that downloads an artifact from a URL, verifies its SHA-256 checksum against a `.sha256` file, and exits with code 1 if mismatched.
2. **Exercise 7.2**: Implement a Python script that injects environment variables into a running container process at launch without modifying the underlying image.
3. **Exercise 7.3**: Construct an artifact metadata JSON record embedding Git commit SHA, build timestamp, branch name, and SHA-256 digest.
4. **Exercise 7.4**: Simulate an artifact registry retention policy script that deletes workflow artifacts older than 14 days while retaining release artifacts indefinitely.
5. **Exercise 7.5**: Verify that unpacking `delivery-service-1.0.0.tar.gz` into two different directories produces identical file checksums.
6. **Exercise 7.6**: Compare the network transfer time and storage size of an uncompressed `.tar` vs a compressed `.tar.gz` artifact.
7. **Exercise 7.7**: Demonstrate that changing the environment variable `ENVIRONMENT=production` alters application behavior without modifying the built artifact binary.
8. **Exercise 7.8**: Write an audit tool that queries `/version` on 5 simulated server instances and reports any instance running an out-of-date artifact digest.

---

## Questions for Mastery
1. *Why is building separate container images for staging and production a dangerous anti-pattern?*
2. *What is the difference between a CI workflow artifact and an artifact stored in an OCI container registry?*
3. *How does content-addressable storage guarantee artifact immutability?*

---

## What Comes Next
In **Part VIII (Phases 55–62)**, we master Containers in CI/CD: manual Docker builds, mutable tags vs immutable content digests, layer caching optimization, multi-stage builds, and non-root container security.
