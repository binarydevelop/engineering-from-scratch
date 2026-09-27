# Tooling and Platform Version Discipline

> "Never use `latest` casually in production examples. Pin exact versions, understand their deprecation timelines, and verify your tools against current platform APIs."

In CI/CD and software delivery, version ambiguity is the primary cause of pipeline drift, irreproducible builds, and catastrophic supply-chain poisoning. This document records the canonical pinned versions used across all lessons, labs, scripts, and workflows in this repository.

---

## 1. Core Runtimes & Operating System Environments

| Component | Pinned Version | Minimum Version | Notes |
|:---|:---|:---|:---|
| **Python** | `3.12.5` | `3.10.0` | Tested through Python `3.14.x`. Standard library used for all zero-dependency simulators. |
| **Bash** | `5.2.x` / `3.2.57` | `3.2.0` | Scripts are written to POSIX/Bash 3.2 compatibility to run natively on macOS default terminals as well as modern Linux environments. |
| **Git** | `2.45.2` | `2.34.0` | Requires support for detached HEAD checks, commit hash signing, and sparse checkouts. |
| **Docker Engine** | `27.1.1` | `24.0.0` | BuildKit enabled by default (`DOCKER_BUILDKIT=1`). OCI Image Specification v1.0 & v1.1. |
| **Runner OS** | `ubuntu-24.04` / `ubuntu-22.04` | Ephemeral | Standard hosted runner environments. |

---

## 2. GitHub Actions: Official Actions & Pinned Releases

All workflow examples in this repository pin to major version tags with specific commit SHAs recommended for immutable production pipelines.

| Action Name | Publisher | Pinned Version | Exact Immutable SHA Reference | Purpose |
|:---|:---|:---|:---|:---|
| `actions/checkout` | GitHub | `v4.1.7` | `actions/checkout@692973e3d937129bcbf40652eb9f2f61becf3332` | Clone repository at exact commit SHA |
| `actions/setup-python` | GitHub | `v5.1.1` | `actions/setup-python@f677139bbe7f9c59b41e40162b753c062f5d49a3` | Install deterministic Python runtime |
| `actions/cache` | GitHub | `v4.0.2` | `actions/cache@0c45773b623bea8c8e75f6c82b208c3cf94ea4f9` | Cache package dependencies across runs |
| `actions/upload-artifact`| GitHub | `v4.3.4` | `actions/upload-artifact@0b2256b8c012f0828dc542b3febcab082c67f72b` | Upload workflow diagnostic artifacts |
| `actions/download-artifact`| GitHub | `v4.1.8` | `actions/download-artifact@fa0a91b85d4f404e444e00e005971372dc801d16` | Download workflow build outputs |
| `actions/attest-build-provenance`| GitHub | `v1.3.2` | `actions/attest-build-provenance@c074443f1a5fb4aee83904702322ec473452e779`| Generate cryptographic build provenance |
| `docker/setup-buildx-action` | Docker | `v3.4.0` | `docker/setup-buildx-action@d70bba72b1f3ed2234483607fb52fe634910e78a` | Configure multi-platform Docker BuildKit |
| `docker/login-action` | Docker | `v3.2.0` | `docker/login-action@0d4c965ea7674fdb4c1b525f771f661da14c4c77` | Authenticate with container registry |
| `docker/build-push-action` | Docker | `v6.3.0` | `docker/build-push-action@15563696e9cbce104480a0f372670a8d4b8e749f` | Build and push OCI container images |

---

## 3. Kubernetes & Orchestration

| Tool | Pinned Version | API Version | Deprecation Notes |
|:---|:---|:---|:---|
| **Kubernetes** | `v1.30.3` | `apps/v1`, `batch/v1`, `networking.k8s.io/v1` | `extensions/v1beta1` and older `apps/v1beta*` are long removed. Ensure all Deployment specs use `apps/v1`. |
| **KinD (Kubernetes in Docker)** | `v0.24.0` | Node image: `kindest/node:v1.30.2` | Used for local integration clusters. |
| **Helm** | `v3.15.3` | Chart format: `v2` (Helm 3 native) | Helm v2 (with Tiller) is completely obsolete and insecure. |
| **Kustomize** | `v5.4.2` | `kustomize.config.k8s.io/v1beta1` | Standalone Kustomize engine. |

---

## 4. GitOps Controllers

| Tool | Pinned Version | API Group / Version | Critical Operational Safeguards |
|:---|:---|:---|:---|
| **Argo CD** | `v2.11.4` | `argoproj.io/v1alpha1` | **DANGEROUS OPTIONS FLAGGED**: Current Argo CD documentation strictly advises against default use of `SyncOptions=Replace=true` or `--force`. These flags delete and recreate live resources, destroying running pod replicas and causing sudden traffic outages. |

---

## 5. Software Supply-Chain & Attestation Frameworks

| Standard / Tool | Pinned Version | Specification Schema | Purpose |
|:---|:---|:---|:---|
| **SLSA (Supply-chain Levels for Software Artifacts)** | `v1.0` | `https://slsa.dev/provenance/v1` | Verifiable provenance describing source, builder, and inputs. |
| **in-toto** | `v1.0` | `https://in-toto.io/Statement/v1` | Generic attestation statement wrapper. |
| **Cosign (Sigstore)** | `v2.4.0` | Keyless & Keypair OIDC signing | Cryptographic image signing and Rekor transparency log entry. |
| **Syft** | `v1.9.0` | CycloneDX `v1.5` / SPDX `v2.3` | Software Bill of Materials (SBOM) generator. |
| **Trivy** | `v0.53.0` | Standalone vulnerability database | CVE vulnerability scanner for filesystems and container layers. |

---

## 6. Deprecated CI Features & Anti-Patterns (Do NOT Use)

Modern pipelines frequently break because developers copy outdated StackOverflow answers. Here are syntax rules enforced across this curriculum:

1. **`set-output` is Forbidden**:
   - *Deprecated*: `echo "::set-output name=result::$VALUE"` (Disabled in GitHub Actions since 2022).
   - *Current Standard*: `echo "result=$VALUE" >> "$GITHUB_OUTPUT"`.

2. **`save-state` is Forbidden**:
   - *Deprecated*: `echo "::save-state name=KEY::$VALUE"`.
   - *Current Standard*: `echo "KEY=$VALUE" >> "$GITHUB_STATE"`.

3. **`upload-artifact@v3` and earlier**:
   - Uses legacy upload protocol which has been deprecated. Always pin `actions/upload-artifact@v4`. Note that v4 artifacts are immutable: attempting to upload to the same artifact name across different jobs without `overwrite: true` will fail by design.

4. **Long-lived Cloud Access Keys in CI Secrets**:
   - Storing permanent AWS `AWS_SECRET_ACCESS_KEY` or GCP Service Account JSON keys in repository secrets is marked as an anti-pattern. Workload Identity Federation / OIDC (Phase 77, Phase 211) is the required standard.

5. **Mutable Docker Image Tags in Production**:
   - Deploying `myapp:latest` or `myapp:main` is forbidden in production labs. All deployments must target immutable digest references:
     `myapp@sha256:7f9b8c31...` or strictly tagged semantic versions: `myapp:1.4.2`.
