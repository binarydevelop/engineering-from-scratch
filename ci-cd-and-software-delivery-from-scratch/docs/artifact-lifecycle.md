# The Artifact Lifecycle: From Source Commit to Production Runtime

> "Software delivery succeeds when any running production process can be unambiguously traced back to the exact Git commit, pipeline run, builder identity, and cryptographic digest that produced it."

---

## 1. The Lineage Chain

```text
[ Git Commit SHA: e4b3c2a1... ]
               │
               ▼
[ Build Process: Deterministic Compilation ]
               │
               ▼
[ Content Digest: sha256:7041b28e... ] ◄── Immutable Content Identity
               │
       ┌───────┴──────────────────┐
       ▼                          ▼
[ CycloneDX SBOM ]     [ SLSA v1.0 Provenance ]
(Software Bill of      (Builder, Commit, Inputs,
 Materials Inventory)   Signed with Cosign / Sigstore)
       │                          │
       └───────┬──────────────────┘
               │
               ▼
[ OCI Container Registry: ghcr.io/org/service@sha256:... ]
               │
               ▼
[ Promotion Stage 1: Staging Environment ]
- Health Probes (/health/liveness, /health/readiness)
- Automated API Contract Tests
- End-to-End Smoke Tests
               │
               ▼ (Approved)
[ Promotion Stage 2: Production Environment ]
- Progressive Canary Rollout (1% -> 10% -> 50% -> 100%)
- Live Telemetry & Error Budget Monitoring
               │
               ▼
[ Running Container Process ]
- Exposes /version endpoint with commit SHA and artifact digest
- Read-only root filesystem
```

---

## 2. Artifact vs Cache: The Critical Distinction

A common beginner confusion is mixing build artifacts with dependency caches:

| Dimension | Dependency Cache | Software Artifact |
|:---|:---|:---|
| **Purpose** | Optimization to speed up subsequent builds | The actual product of the build meant for distribution and deployment |
| **Integrity Requirement** | Disposable. If lost or invalidated, build re-downloads dependencies without impacting correctness | Critical and immutable. Must be retained for rollbacks, compliance, and disaster recovery |
| **Storage Destination** | Ephemeral CI runner cache storage | Secure artifact registry (OCI, Artifactory, Nexus, S3) |
| **Trust Boundary** | Restored inside internal CI worker | Deployed into privileged staging and production clusters |

---

## 3. The Reverse Provenance Audit

When an incident occurs in production, an on-call engineer must never wonder: *"What version of the code is actually running on this server?"*

To trace any running container backward:

### Step 1: Query the Running Process
Execute a request against the service's introspection endpoint:
```bash
curl -s http://production.internal:8080/version
```
```json
{
  "service": "delivery-service",
  "version": "1.0.0",
  "commit_sha": "c477286c99d56c965cd1afddc5862b17ce5661ad",
  "artifact_digest": "sha256:7041b28e74403e789f88bbf6cc2474c8fd7995b283c62819f80b4165b0fb47f0",
  "build_timestamp": "2026-09-27T08:30:00Z",
  "environment": "production"
}
```

### Step 2: Query the Container Runtime
Verify that the running container image digest matches the reported digest:
```bash
docker inspect --format='{{index .RepoDigests 0}}' delivery-service
# Output: ghcr.io/org/delivery-service@sha256:7041b28e74403e789f88bbf6cc2474c8fd7995b283c62819f80b4165b0fb47f0
```

### Step 3: Verify Cryptographic Provenance
Verify the SLSA attestation signed by the build runner:
```bash
python3 security-labs/sbom_provenance_generator.py \
    --mode verify \
    --artifact outputs/release-v1.0.0/delivery-service-1.0.0.tar.gz \
    --provenance outputs/release-v1.0.0/provenance.json
```

### Step 4: Locate the Git Source State
Inspect the exact Git commit that produced this artifact:
```bash
git show c477286c99d56c965cd1afddc5862b17ce5661ad
```

Every line of running code is accounted for. There are zero untracked local edits, zero mystery patches, and zero ambiguous dependencies.
