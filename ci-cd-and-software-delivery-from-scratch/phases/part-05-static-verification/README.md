# Part V: Static Verification (Phases 36–42)

## Motto
> "Catch defects before executing code. Static analysis, secret scanning, and manifest validation are your cheapest and fastest feedback loops."

---

## Delivery Problem
A developer accidentally commits an AWS access key and pushes it to GitHub. Within 4 minutes, automated scrapers on the public internet detect the key and spin up 50 unauthorized cryptocurrency mining instances, accumulating an $18,000 cloud bill before anyone notices.

Meanwhile, an unvalidated Kubernetes YAML manifest with a typo in the `namespace` field is applied in production, deploying services to the default namespace and knocking out existing routing rules.

---

## Prediction
1. Static analysis checks run in sub-second time without needing external databases or runtimes.
2. Secret scanners operating in pre-commit hooks and CI prevent permanent credential leaks.
3. Validating Kubernetes manifest syntax alone does not prove that the Kubernetes API server will accept the resource semantically.

---

## First Principles
1. **Static vs Dynamic Verification**:
   - **Static Verification**: Analyzes source code, syntax trees (AST), dependencies, and manifests without executing the code. Fast, deterministic, zero side-effects.
   - **Dynamic Verification**: Executes the compiled binary in an environment and observes runtime behavior (unit tests, integration tests, fuzzing).
2. **Scanner Result ≠ Exploitability Proof**:
   A dependency scanner (Trivy, Snyk) reporting a CVE does not automatically mean your service is vulnerable. The vulnerable function or code path may never be invoked. Triage must evaluate real-world exploitability in context.
3. **Secret Entropy & Pattern Matching**:
   Secret scanners combine regular expression pattern matching (known prefixes like `AKIA...`) with Shannon entropy analysis to detect high-randomness strings (passwords, private keys).

---

## Manual Process
Run static verification by hand:

```bash
# 1. Bytecode & Syntax Compilation
python3 -m py_compile sample-apps/delivery-service/app.py

# 2. Secret Scanning (Phase 41)
python3 security-labs/secret_leak_scanner.py --scan-dir sample-apps

# 3. IaC Manifest Semantic Validation (Phase 42)
python3 -c "
import json
with open('gitops/desired-state/delivery-service.json') as f:
    spec = json.load(f)
assert spec.get('apiVersion') == 'apps/v1'
assert 'replicas' in spec['spec']
print('✓ Manifest schema valid!')
"
```

---

## Mental Model

```text
[ Developer Commit ]
         │
         ▼
[ Stage 1: Pre-Execution Static Gate (< 5 seconds) ]
   ├── Formatter & Linter        (Consistency & Common Bug Patterns)
   ├── Type Checker              (Type Safety & Signature Matching)
   ├── Secret Leak Scanner       (Credentials & Private Keys)
   ├── Dependency CVE Scanner    (Known Vulnerability Databases)
   └── Manifest Validator        (Kubernetes / Terraform Schema Check)
         │
         ▼ (Pass)
[ Stage 2: Dynamic Execution (Tests & Builds) ]
```

---

## Automate It
Here is how secret scanning and static bytecode compilation run in CI:

```yaml
- name: Static Verification
  run: |
    python3 -m py_compile sample-apps/delivery-service/app.py
    python3 security-labs/secret_leak_scanner.py --scan-dir sample-apps
```

---

## Run It
Execute the secret scanner across the repository:

```bash
python3 security-labs/secret_leak_scanner.py --scan-dir sample-apps
```

---

## Break It (Phase 41: Secret Scanning)
1. Run broken lab `14-secret-printed-to-pipeline-logs`:
   ```bash
   python3 broken-pipelines/14-secret-printed-to-pipeline-logs/reproduce_failure.py
   ```
2. Run broken lab `36-iac-manifest-syntax-valid-but-semantically-rejected`:
   ```bash
   python3 broken-pipelines/36-iac-manifest-syntax-valid-but-semantically-rejected/reproduce_failure.py
   ```
3. Observe how a syntactically valid JSON manifest fails semantic validation when required fields are missing.

---

## Debug It
When a linter or secret scanner fails:
- Check line number and file path reported by the tool.
- If it's a false positive secret detection, use explicit nosec annotations (`# nosec: safe-demo-secret`) rather than disabling the scanner entirely.

---

## Security
- Never bypass secret scanning in CI using `--no-verify`.
- If a secret is committed to Git history, simply deleting the commit or file is insufficient; the credential must be rotated and revoked immediately because Git history retains past commits.

---

## Optimize It
- Run static checks on developer machines via Git pre-commit hooks so broken commits are blocked before hitting the network.
- Cache linter cache directories (e.g. `.ruff_cache`, `.eslintcache`) across CI runs.

---

## Deployment Implication
Static verification is the cheapest gatekeeper. Catching a typo or invalid manifest in CI takes 2 seconds; catching it in production takes hours of incident triage.

---

## Recovery
If a secret is leaked:
1. Immediately revoke and rotate the secret in the cloud IAM console.
2. Invalidate any active sessions.
3. Review cloud audit logs (CloudTrail, GCP Audit Logs) for unauthorized API calls during the exposure window.

---

## Practical Exercises (Part V)
1. **Exercise 5.1**: Add a new regex pattern to `security-labs/secret_leak_scanner.py` that detects GitHub fine-grained personal access tokens (`github_pat_...`).
2. **Exercise 5.2**: Write a pre-commit hook script in `.git/hooks/pre-commit` that runs `secret_leak_scanner.py` before allowing a commit.
3. **Exercise 5.3**: Commit a dummy AWS key (`AKIAIOSFODNN7EXAMPLE`) to a scratch branch and verify that the scanner fails with non-zero exit code.
4. **Exercise 5.4**: Write a schema validator that parses Kubernetes Deployment manifests and asserts that `securityContext.runAsNonRoot` is set to `true`.
5. **Exercise 5.5**: Benchmark the execution time of running a static type checker against running the full integration test suite.
6. **Exercise 5.6**: Write a script that scans `Dockerfile` files and warns if any image uses `:latest` instead of a pinned version tag.
7. **Exercise 5.7**: Implement Shannon entropy calculation in Python to detect randomly generated strings that look like cryptographic tokens.
8. **Exercise 5.8**: Configure a manifest validator that checks for resource `limits` (CPU and Memory) on every container specification.

---

## Questions for Mastery
1. *Why is committing a secret and then deleting it in a subsequent commit still a severe security compromise?*
2. *Why does validating YAML syntax with a generic parser fail to catch Kubernetes schema errors?*
3. *How should an engineering team handle a CVE report in a transitive dependency that has no available patch?*

---

## What Comes Next
In **Part VI (Phases 43–48)**, we investigate Build Systems: compilation pipelines, incremental builds, build graph DAGs, parallel builds, hermetic builds, and reproducible builds.
