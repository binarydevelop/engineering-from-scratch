# Contributing to redis-from-scratch

Thank you for contributing to `redis-from-scratch`!

This repository aims to be the gold standard in hands-on, first-principles systems engineering education for Redis and in-memory architectures.

---

## Pedagogical Principles

Every pull request that adds or updates a lesson must uphold these tenets:

1. **Strict Version Discipline:**
   All commands and behavioral explanations must be verified against the pinned version in [VERSIONS.md](VERSIONS.md) (Redis 7.4.x / 8.x). Do not document deprecated commands or legacy internal structures (e.g. `ziplist`) as modern behavior.

2. **First Principles Before Real Features:**
   Every lesson must follow the `BUILD IT -> USE REDIS` sequence. The learner must first build or inspect a simple Python implementation of the concept before issuing the real Redis command.

3. **Quantitative Measurement & Controlled Failures:**
   Lessons must include measurable benchmarks (latency percentiles, operations per second, memory bytes) and an intentional failure mode with reproduction steps and diagnosis.

4. **Strict Structure:**
   Follow [LESSON_TEMPLATE.md](LESSON_TEMPLATE.md) exactly. Every section header (`## Motto`, `## Problem`, `## Prediction`, `## Why this matters`, `## First principles`, `## Mental model`, `## Build it`, `## Use Redis`, `## Inspect it`, `## Measure it`, `## Break it`, `## Debug it`, `## Modify it`, `## Evidence`, `## Questions for mastery`, `## When to use this`, `## When not to use this`, `## What comes next`) is required.

5. **Self-Contained Runnable Code:**
   Code in `code/` must execute using Python 3.11+ standard library where possible or minimal dependencies in `requirements.txt`. Scripts in `experiments/` must be executable (`chmod +x run_experiment.sh`) and self-verifying.

---

## Submitting Pull Requests

1. Fork the repository and create a descriptive branch: `git checkout -b lesson/XX-topic-name`.
2. Verify all lesson scripts run locally without errors: `make test`.
3. Ensure no temporary files (`*.rdb`, `*.aof`, `__pycache__`) are committed.
4. Submit your pull request with a summary of the systems concept demonstrated and test outputs.
