# Contributing to CI/CD and Software Delivery from Scratch

Thank you for your interest in contributing to **CI/CD and Software Delivery from Scratch**.

Our mission is to teach software delivery deeply from first principles through implementation, experiments, pipeline failures, debugging, deployment simulations, rollback exercises, and release automation.

The repository motto is:
> **Understand it. Build it. Test it. Package it. Verify it. Release it. Deploy it. Observe it. Recover it. Automate it.**

---

## 1. Core Principles for Contributions

Before contributing a lesson, lab, simulator, or exercise, verify that it adheres to these core standards:

1. **Never Start with Pipeline YAML**:
   Always begin with the manual shell command, demonstrate human error and friction, explain the underlying operating system primitive or cryptographic invariant, and only then derive the automation.
2. **Local Reproducibility**:
   All core educational exercises, simulators, and broken-pipeline scenarios must be completely executable locally on a standard macOS or Linux workstation without requiring paid cloud subscriptions or proprietary CI platform tokens.
3. **Evidence-Based Learning**:
   Every lesson must produce concrete verification evidence (command, exit status, stdout/stderr, generated artifact digest, or recovery log).
4. **Deliberate Breaking & Debugging**:
   A lesson is incomplete if it only shows the happy path. Contributions must include failure injection, root-cause diagnosis, and a proven recovery path.
5. **No Magic "latest" Tags**:
   All container images, package dependencies, actions, and deployment targets must use pinned versions or immutable content digests.

---

## 2. Directory Conventions

- `phases/`: 30 chronological learning parts containing structured lesson documentation and code.
- `scripts/`: Production-ready, modular shell scripts (must use `set -euo pipefail` and POSIX/Bash compatibility).
- `sample-apps/`: Concrete application code used as the target of pipelines and deployments.
- `pipelines/`: CI runner engines and platform workflow definitions.
- `broken-pipelines/`: Hands-on failure labs with separate problem and solution directories.
- `deployment-labs/`: Interactive deployment simulators (Recreate, Rolling, Blue/Green, Canary).
- `security-labs/`: Hands-on security tooling (OIDC, SBOM, Cosign, secret scanners).
- `benchmarks/`: Performance measurement experiments and profiling tools.
- `projects/`: Substantial end-to-end projects.
- `capstones/`: Comprehensive capstone challenges.

---

## 3. Creating a New Lesson

1. Copy [`LESSON_TEMPLATE.md`](file:///Users/tushar/desktop/private/repos/ci-cd-and-software-delivery-from-scratch/LESSON_TEMPLATE.md) into the target phase directory.
2. Complete all 19 mandatory sections. Do not skip the "Break It", "Debug It", "Security", or "Evidence" sections.
3. Include runnable code in a `code/` subfolder or companion script in `scripts/`.
4. Run the code locally and verify that it executes with zero syntax errors.

---

## 4. Contributing Broken-Pipeline Labs

Broken pipeline labs are vital for teaching real-world incident response.
When adding a broken lab to `broken-pipelines/`:
1. Create a numbered folder: `broken-pipelines/XX-short-descriptive-slug/`.
2. Add a `README.md` containing:
   - Incident context and symptoms
   - Exact command to reproduce the failure
   - Key diagnostic clues
   - Guided inquiry questions
3. Add the failing script or workflow configuration.
4. Add `solution/SOLUTION.md` explaining:
   - Root-cause analysis (why did it fail?)
   - Step-by-step fix
   - Verification command proving the fix works
   - Prevention policy to prevent recurrence in production teams.

---

## 5. Coding Standards

- **Bash Scripts**:
  - Always start with `#!/usr/bin/env bash`.
  - Always include `set -euo pipefail`.
  - Quote all variables (`"$VARIABLE"`).
  - Use informative error messages on non-zero exits.
- **Python**:
  - Standard library preferred for simulators so they run without extra `pip install` hurdles.
  - Follow PEP 8 style conventions.
  - Include type annotations for public functions.

---

## 6. Pull Request Process

1. Fork the repository and create a feature branch: `git checkout -b feature/phase-xx-topic`.
2. Run the environment check and local test suite:
   ```bash
   make check-env
   make test
   make local-ci
   ```
3. Commit your changes with descriptive commit messages following Conventional Commits format (`feat:`, `fix:`, `docs:`, `test:`).
4. Open a Pull Request detailing the educational problem solved and evidence of local verification.
