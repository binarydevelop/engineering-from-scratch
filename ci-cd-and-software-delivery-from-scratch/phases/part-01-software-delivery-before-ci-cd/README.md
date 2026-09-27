# Part I: Software Delivery Before CI/CD (Phases 00–07)

## Motto
> "Never automate what you do not understand manually. Before pipeline YAML, there is only the shell, the source tree, and the process exit code."

---

## Delivery Problem
A development team commits code directly to a shared branch. When an engineer asks to deploy, another engineer manually opens a terminal, runs ad-hoc commands from memory, misses a database migration step, uses their personal laptop's compiler with uncommitted local patches, and uploads an unversioned `.tar.gz` to a server. 

The application immediately crashes. Nobody knows:
1. Which exact Git commit was deployed.
2. Why it worked on the developer's laptop but failed on the server.
3. How to recover the previously working version.

Without deterministic, reproducible delivery practices before introducing automation, adopting a CI/CD platform only accelerates the rate at which you deploy broken software.

---

## Prediction
1. Executing commands manually will introduce human typos, omitted flags, and ordering mistakes.
2. Relying on laptop state will hide missing dependencies that exist globally on the developer machine but not in production.
3. If an automated script does not check `$?` (exit code) after every command, a failed compilation will silently fall through to packaging stale binaries.

---

## Why This Matters
Software delivery is fundamentally a state transformation:
`Source Code (Git State) ──► Verified Immutable Artifact ──► Running Production System`

If you cannot perform this transformation reliably by hand with standalone shell commands, wrapping it in GitHub Actions or GitLab CI YAML creates fragile "cargo cult" pipelines that no one can debug when they fail.

---

## First Principles
1. **Operating System Exit Status**:
   Every POSIX process terminates by returning an 8-bit unsigned integer (`0` to `255`) to its parent process via the `exit()` system call.
   - `0`: Success.
   - `1–255`: Specific error condition.
   Pipelines do not possess magical AI intelligence; their control flow is governed entirely by trapping process exit codes.
2. **Git Commit SHA as Content Address**:
   A Git commit SHA (e.g. `c477286...`) is a SHA-1/SHA-256 Merkle tree hash of the exact file contents, parent commit hashes, committer identity, and timestamp. It represents the exact, immutable identity of the source input.
3. **Artifact Digest as Build Output Identity**:
   Computing the cryptographic hash (`sha256sum`) of the packaged artifact provides an immutable identity for the build output. If source SHA A always maps to artifact hash B, your build is deterministic.

---

## Manual Process (Phases 00–04)

Execute the manual delivery sequence by hand in your terminal:

```bash
# Phase 00 & 02: Check version control state
git status
git rev-parse HEAD

# Phase 04: Manual Verification
python3 -m py_compile sample-apps/delivery-service/app.py
echo "Compile Exit Code: $?"

python3 sample-apps/delivery-service/tests/unit/test_orders.py
echo "Unit Test Exit Code: $?"

python3 sample-apps/delivery-service/tests/integration/test_db.py
echo "Integration Test Exit Code: $?"

# Phase 03: Manual Build & Hash
mkdir -p outputs/manual-build
cp sample-apps/delivery-service/app.py outputs/manual-build/
tar -czf outputs/manual-build.tar.gz -C outputs/manual-build app.py
shasum -a 256 outputs/manual-build.tar.gz
```

Notice the repetition, the risk of forgetting a step, and the friction of manually verifying exit codes.

---

## Mental Model

```text
[ Phase 02: Source Git SHA ]
              │
              ▼
[ Phase 04: Verification Matrix ]
  ├── 1. Static Bytecode Check  ──► Exit 0 ?
  ├── 2. Unit Test Suite        ──► Exit 0 ?
  └── 3. Integration Tests      ──► Exit 0 ?
              │
              ▼ (All Exit 0)
[ Phase 03 & 07: Deterministic Build ]
              │
              ▼
[ Immutable Artifact + SHA-256 Digest ]
```

---

## Automate It (Phase 05: Build Script)

Instead of running commands manually, encapsulate the verified steps into a standalone, reproducible shell script:

```bash
#!/usr/bin/env bash
# scripts/local-ci.sh
set -euo pipefail

# Step 1: Preflight
bash scripts/check-environment.sh

# Step 2: Test
bash scripts/test.sh

# Step 3: Build
bash scripts/build.sh

# Step 4: Package
bash scripts/package.sh
```

**Key Architectural Rule**: The CI platform (`.github/workflows/*.yml`) should never contain complex inline build logic. The pipeline should simply invoke the same standalone shell scripts that developers can execute locally.

---

## Run It
Execute the automated harness from the repository root:

```bash
bash scripts/local-ci.sh
```

Expected output:
```text
======================================================================
  LOCAL CI PIPELINE HARNESS — FROM SCRATCH
======================================================================
▶ [STAGE] Environment Preflight
✓ [STAGE PASSED] Environment Preflight (2s)
▶ [STAGE] Automated Test Matrix
✓ [STAGE PASSED] Automated Test Matrix (1s)
▶ [STAGE] Deterministic Build
✓ [STAGE PASSED] Deterministic Build (1s)
▶ [STAGE] Artifact Packaging & Checksum Generation
✓ [STAGE PASSED] Artifact Packaging & Checksum Generation (1s)
✓ LOCAL CI PIPELINE COMPLETED SUCCESSFULLY!
```

---

## Inspect It
Inspect the generated build manifest and verify the recorded Git SHA:

```bash
cat outputs/build/build-manifest.json
cat outputs/artifact-metadata.json
```

---

## Break It (Phase 06: Exit Code Trapping)
Deliberately break a unit test:
1. Edit `sample-apps/delivery-service/tests/unit/test_orders.py` and alter line 36: change `self.assertTrue(is_valid)` to `self.assertFalse(is_valid)`.
2. Run `bash scripts/local-ci.sh`.
3. Observe how the pipeline halts immediately at the test stage with exit status `1`, refusing to execute the build or packaging stages.
4. Revert your edit.

---

## Debug It
When a script fails in Phase 06:
1. Inspect the last command executed before termination.
2. Check whether `set -e` (halt on non-zero exit) was triggered.
3. Review standard error (`stderr`) traces to diagnose the root cause.

---

## Security
- Scripts must run with least privilege. Do not execute build scripts under `sudo`.
- Environment variables containing credentials must not be logged or exposed to unmasked child processes.

---

## Optimize It
- Replace full deep Git clones with shallow clones (`git fetch --depth=1`) when history is unnecessary.
- Run independent verification checks (e.g. formatting and unit tests) in parallel rather than serially.

---

## Deployment Implication
If an artifact is packaged without verifying test exit codes, defective software will be tagged and pushed to registries, requiring emergency incident response in production.

---

## Recovery
If a broken artifact was built and published:
1. Query the artifact digest from the running server (`curl http://localhost:8080/version`).
2. Map the digest back to the failing Git commit SHA in `outputs/artifact-metadata.json`.
3. Re-deploy the previously verified artifact digest using `./scripts/rollback.sh`.

---

## Evidence
Record your execution evidence:
```text
Date: 2026-09-27
Source Commit SHA: c477286c99d56c965cd1afddc5862b17ce5661ad
Manual Command: bash scripts/local-ci.sh
Exit Code: 0
Generated Artifact Digest: sha256:7041b28e...
Verified Stages: Preflight, Static Compile, Secret Scan, Tests, Build, Package
```

---

## Practical Exercises (Part I)
1. **Exercise 1.1**: Run `git log -n 1 --format="%H %ct"` to inspect the commit SHA and UNIX commit epoch timestamp.
2. **Exercise 1.2**: Write a one-line bash command that executes `python3 sample-apps/delivery-service/tests/unit/test_orders.py` and prints `"TEST PASSED"` only if the exit code was `0`, or `"TEST FAILED"` if non-zero.
3. **Exercise 1.3**: Execute `python3 -m py_compile` on an intentionally broken Python file containing a syntax error. Observe the non-zero exit code emitted.
4. **Exercise 1.4**: Modify `scripts/build.sh` to embed the Git branch name into `outputs/build/build-manifest.json`.
5. **Exercise 1.5**: Use `shasum -a 256` to calculate the checksum of two separate text files; observe how changing a single byte completely changes the 64-character hexadecimal digest.
6. **Exercise 1.6**: Run `scripts/local-ci.sh` under `bash -x` to trace every process fork and file descriptor redirection.
7. **Exercise 1.7**: Create an isolated temporary directory and verify that `sample-apps/delivery-service/app.py` runs with a clean SQLite database.
8. **Exercise 1.8**: Write a script that checks whether the local Git working tree has uncommitted modifications (`git diff --quiet`) before allowing a build to proceed.

---

## Questions for Mastery
1. *Why is vendor pipeline YAML (e.g. GitHub Actions) not the build system itself?*
2. *If a shell script omits `set -e`, what happens when a test fails on line 12 and packaging runs on line 15?*
3. *Why does recording the Git commit SHA provide stronger identity than recording the Git branch name?*

---

## What Comes Next
In **Part II (Phases 08–17)**, we derive Continuous Integration from first principles: event triggers, runner architectures, DAG job evaluation, parallelization, and failure propagation.
