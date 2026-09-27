# Capstone 1: Production-Grade Continuous Integration

## 1. Challenge Prompt
> "Build an industrial-grade CI pipeline for a backend service that optimizes feedback time while enforcing format, lint, unit tests, integration tests, secret scanning, SBOM generation, container build, and SLSA provenance."

---

## 2. Architectural Requirements & Invariants
- [ ] PR feedback under 3 minutes wall-clock time
- [ ] Parallelized unit test shards and independent integration jobs
- [ ] Zero long-lived secrets in runner environment
- [ ] Automatic cancellation of superseded runs
- [ ] Immutable artifact generation with SHA-256 digest

---

## 3. Verification Command
To verify your capstone implementation, run:
```bash
python3 capstones/01-production-grade-ci/verify.py
```
