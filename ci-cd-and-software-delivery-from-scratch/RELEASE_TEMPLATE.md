# Release Specification: [Release Name / Version]

> "A release is an immutable, cryptographically verifiable distribution package produced from a specific commit. It represents software intended for deployment across environments."

---

## Version
- **Semantic Version**: `vMAJOR.MINOR.PATCH` (e.g., `v2.4.1`)
- **Release Track**: `alpha` | `beta` | `release-candidate` | `stable` | `hotfix`
- **Git Tag Name**: `refs/tags/v2.4.1` (annotated and cryptographically signed)

---

## Commit
- **Full Commit SHA**: 40-character SHA-1 (or 64-character SHA-256) of the released source revision
- **Target Branch**: Branch from which the release was cut (e.g., `main` or `release/2.4`)
- **Tree Hash**: Exact Git tree hash corresponding to the committed file state

---

## Artifact
- **Artifact Name**: `delivery-service:2.4.1` / `delivery-service-2.4.1.tar.gz`
- **Artifact Type**: OCI Container Image / Wheel Package / Standalone Executable
- **Registry Location**: `ghcr.io/binarydevelop/delivery-service:2.4.1`
- **Immutability Guarantee**: Tag is write-protected in registry; re-pushing same tag is rejected

---

## Artifact Digest
- **Primary Content Digest**: `sha256:7f9b8c31e428a1...`
- **Digest Verification Command**:
  ```bash
  docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/binarydevelop/delivery-service:2.4.1
  ```
- **Integrity Status**: Matches recorded checksum in release manifest

---

## SBOM
- **SBOM Format**: CycloneDX v1.5 JSON / SPDX v2.3
- **Generation Tool**: `syft dir:. -o cyclonedx-json=sbom.json`
- **Artifact File**: `outputs/release-v2.4.1/sbom.cdx.json`
- **Vulnerability Scan Summary**: 0 Critical, 0 High vulnerabilities detected

---

## Provenance / Attestation
- **SLSA Level**: SLSA Build Level 2 / Level 3
- **Attestation Predicate**: `https://slsa.dev/provenance/v1`
- **Signing Authority**: Sigstore Cosign / GitHub Actions Workload Identity
- **Verification Command**:
  ```bash
  cosign verify --certificate-identity-regexp "https://github.com/..." ghcr.io/binarydevelop/delivery-service@sha256:...
  ```

---

## Changes
- **Key Features Added**:
  - Feature 1: Description and user impact
  - Feature 2: Description and user impact
- **Bug Fixes**:
  - Issue #104: Description of fix
- **Internal / Architectural Changes**:
  - Performance optimization in batch database loader

---

## Compatibility Notes
- **API Backward Compatibility**: Full backward compatibility with v2.3.x clients
- **Deprecations**: Flagged endpoints or configuration keys slated for removal in v3.0.0
- **Client Impact**: None; zero-downtime client transition supported

---

## Migration Requirements
- **Database Migrations Needed**: `db/migrations/003_add_order_status.sql`
- **Migration Strategy**: Expand phase only (column added with default value; existing application reads without error)
- **Execution Timing**: Pre-deployment migration required before rolling container update

---

## Rollback Constraints
- **Rollback Feasibility**: Fully reversible to v2.4.0 within 48 hours
- **Data Invariants**: New column `order_status` can be safely ignored by previous v2.4.0 application code
- **Point of No Return**: Contract phase (dropping legacy columns) will execute only after v2.4.1 has run safely in production for 7 days

---

## Verification
- **Automated Smoke Test Suite**: `tests/smoke/test_health_and_traffic.py`
- **Staging Verification Log**: Link to successful staging smoke test run
- **SLO Compliance Check**: Error rate < 0.01%, p95 latency < 50ms verified in staging load test

---

## Release Owner / Workflow
- **Originating CI Workflow**: `.github/workflows/release.yml (Run #412)`
- **Triggered By**: Tag push event by release coordinator (`@release-team`)
- **Audit Trail**: Recorded in repository releases table and immutable deployment ledger
