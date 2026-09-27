# Contributing to docker-from-scratch

Thank you for your interest in improving `docker-from-scratch`!

This repository follows a strict first-principles pedagogy inspired by `ai-engineering-from-scratch`. Before proposing changes, please review our contribution rules.

---

## Pedagogical Principles

1. **Problem First, Tool Third**: Never submit a lesson or PR that begins with a Docker CLI command or Dockerfile directive without first establishing the concrete failure or system need that makes it necessary.
2. **Every Lesson is Runnable**: Code examples must not be pseudocode. They must execute on standard Docker installations (Linux, macOS with Docker Desktop, Windows WSL2).
3. **No Magical Explanations**: Do not say "Docker creates an internal network for containers". Say: "Two isolated Linux network namespaces are connected via a virtual Ethernet pair (`veth`) plugged into a bridge interface (`docker0` or `br-<id>`)."
4. **Platform Honesty**: Clearly delineate where macOS/Windows Docker Desktop behavior differs from native Linux (e.g. the presence of a lightweight virtualization VM boundary, differences in routing localhost, `host.docker.internal`).
5. **Break It & Debug It Sections**: Every lesson must have an intentional failure experiment and a diagnostic path.
6. **Strict Folder Structure**: Follow `LESSON_TEMPLATE.md` without exception.

---

## Adding or Editing a Lesson

1. Ensure the lesson directory adheres to:
   ```text
   phases/<phase-num>-<phase-name>/<lesson-num>-<lesson-name>/
   ├── docs/en.md
   ├── code/
   ├── experiments/run_experiment.sh
   └── outputs/evidence-template.md
   ```
2. Verify that `docs/en.md` contains all standard headers defined in `LESSON_TEMPLATE.md`.
3. Provide an executable `experiments/run_experiment.sh` script with cleanup logic.
4. Run `make test` or `./scripts/run_all_checks.sh` to ensure all builds and validation checks pass cleanly.
