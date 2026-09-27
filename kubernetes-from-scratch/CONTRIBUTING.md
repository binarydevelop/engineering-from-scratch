# Contributing to kubernetes-from-scratch

Thank you for contributing to **kubernetes-from-scratch**! 

The primary goal of this repository is to teach Kubernetes from first principles as an API-driven distributed control system. We adhere to a strict pedagogical philosophy.

---

## Pedagogical Philosophy

1. **Problem First, Primitive Second, Resource Third**:
   Never start a lesson or document by introducing a Kubernetes resource definition. Always begin with the raw engineering challenge, the failure of naive solutions, the derived conceptual primitive, and only then the Kubernetes abstraction.
2. **Reconciliation Over Magic**:
   Every lesson must reveal the control loop, the controller manager actor, the status transition, and the API interaction.
3. **Intentional Fault Injection**:
   Every lesson must contain a "Break it" section where the student deliberately kills an actor, severs a network path, corrupts configuration, or starves resources.
4. **Reasoning Quizzes Only**:
   No trivia or YAML field memorization questions. All questions must test causal reasoning under failure or state transitions.

---

## Structural Standards

Every lesson must follow [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md) and include:
```text
phases/<phase>/<lesson>/
├── docs/
│   └── en.md
├── manifests/
├── code/
├── experiments/
│   └── run_experiment.sh
└── outputs/
    └── evidence-template.md
```

### Manifest Guidelines:
- Use only modern, stable Kubernetes API groups (see [VERSIONS.md](VERSIONS.md)).
- Do not use deprecated APIs (e.g. no `extensions/v1beta1`, no `PodSecurityPolicy`).
- Manifests must be formatted with 2-space indentation.
- Every field introduced must be accompanied by an explanation of *who reads it* and *what breaks if omitted*.

### Script Guidelines:
- Bash scripts must start with:
  ```bash
  #!/usr/bin/env bash
  set -euo pipefail
  ```
- Scripts must be idempotent and safe to run multiple times.
- Provide cleanup or reset mechanisms where state is modified.

### Python Code Guidelines:
- Python scripts must use standard libraries wherever possible (no unnecessary external dependencies).
- Compatible with Python 3.11+.

---

## Verification Before Submitting

Before opening a pull request:
1. Verify scripts pass syntax check:
   ```bash
   bash -n scripts/*.sh
   ```
2. Validate all manifests with `kubectl --dry-run=client`:
   ```bash
   make lint
   ```
3. Run the Python simulators to confirm execution without errors:
   ```bash
   make test-controller
   make test-mini-k8s
   ```
4. Verify tests pass on a clean local kind cluster:
   ```bash
   make cluster-up
   make cluster-status
   make cluster-down
   ```
