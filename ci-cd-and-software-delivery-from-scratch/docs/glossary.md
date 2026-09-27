# Software Delivery Engineering Glossary

> "Precise language creates clear mental models. Ambiguous terminology leads to fragile delivery architectures."

---

| Term | What People Say / Common Misconception | Precise Engineering Definition |
|:---|:---|:---|
| **Continuous Integration (CI)** | "Running automated tests on GitHub." | An engineering practice where developers integrate code into a shared repository frequently (at least daily), and each integration is verified by automated builds and tests to detect integration errors within minutes. |
| **Continuous Delivery (CD)** | "Deploying code automatically to production on every commit." | A software delivery discipline where every suitable change is automatically tested, packaged, and verified so that it *can* be released to production safely at any moment. Production deployment may still involve human authorization. |
| **Continuous Deployment** | Often conflated with Continuous Delivery. | An advanced extension of Continuous Delivery where every change that passes all automated release verification stages is deployed automatically to production with zero manual human gating. |
| **Build Artifact** | "The compiled files in the build folder." | An immutable, versioned, and content-addressed software package (e.g. OCI container image, tarball, wheel, binary) produced from a specific source commit that is promoted unchanged across environments. |
| **Dependency Cache** | "Where our artifacts live." | A temporary, disposable local storage mechanism used to speed up subsequent pipeline runs by avoiding redundant network downloads. Caches can be purged without impacting build correctness. |
| **Directed Acyclic Graph (DAG)** | "Workflow steps." | A mathematical graph of nodes (jobs or tasks) connected by directional edges representing dependency relationships, with no closed loops or circular dependencies. |
| **Detached HEAD** | "Git is broken." | A state in Git where the working tree points directly to a specific commit SHA rather than to a named branch reference. Standard state for CI runner checkouts. |
| **Exit Code ($?)** | "Some status code." | A standard integer (0–255) returned to the operating system by a terminating process. Code `0` indicates successful execution; any non-zero value indicates an error condition. |
| **GitOps** | "Using Git to store Kubernetes YAML." | An operational model where the entire desired state of an environment is stored declaratively in version control, and an automated agent continuously reconciles the actual live state toward the desired state. |
| **Reconciler / Controller**| "A deployment script." | A persistent software daemon that continuously observes live runtime state, compares it to declared desired state, and executes actions to eliminate drift. |
| **Configuration Drift** | "Someone changed something." | The discrepancy between the declared desired state in version control and the actual state running in the live infrastructure or cluster. |
| **OIDC (OpenID Connect)** | "Another password for CI." | An identity protocol allowing a CI runner to generate short-lived, cryptographically signed JSON Web Tokens (JWTs) that cloud providers exchange for temporary, least-privilege cloud credentials. |
| **SLSA** | "Security certification." | Supply-chain Levels for Software Artifacts. A security framework providing standards and verifiable specifications (SLSA Build Level 1, 2, 3) to protect the integrity of software build pipelines. |
| **SBOM** | "A list of dependencies." | Software Bill of Materials. A formal, machine-readable inventory of software components, direct and transitive dependencies, licenses, and checksums (e.g. CycloneDX, SPDX). |
| **Canary Deployment** | "A test deployment." | A progressive delivery technique where a new software release is exposed to a tiny fraction of live user traffic (e.g. 1%) while automated monitoring compares health metrics against a baseline before promoting. |
| **Blue/Green Deployment** | "Having two servers." | A deployment strategy where two identical environments (Blue and Green) exist, allowing instant traffic cutover at the router level and near-instantaneous rollback if defects are discovered. |
| **Expand / Migrate / Contract** | "Database migration." | A three-phase database evolution pattern that ensures zero-downtime schema migrations by maintaining backward compatibility with prior running application versions across releases. |
| **DORA Metrics** | "Developer performance scores." | Four key metrics defined by DevOps Research and Assessment: Deployment Frequency (DF), Lead Time for Changes (LT), Change Failure Rate (CFR), and Mean Time to Recovery (MTTR). Used to measure delivery team throughput and stability. |
